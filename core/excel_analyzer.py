"""
Excel 结构化数据分析模块
支持 Excel/CSV 文件的结构化查询、聚合、筛选、排序
"""
import os
import re
import json
from typing import List, Dict, Any, Optional, Tuple

import pandas as pd


class ExcelAnalyzer:
    """Excel/CSV 结构化数据分析器"""

    # 支持的安全操作
    SAFE_AGGREGATIONS = {
        'sum': lambda s: s.sum(),
        'avg': lambda s: s.mean(),
        'mean': lambda s: s.mean(),
        'max': lambda s: s.max(),
        'min': lambda s: s.min(),
        'count': lambda s: s.count(),
        'unique_count': lambda s: s.nunique(),
    }

    def __init__(self, llm_base_url: str = "http://127.0.0.1:1234", llm_model: str = "qwen/qwen3.5-9b", api_key: Optional[str] = None):
        self.llm_base_url = llm_base_url
        self.llm_model = llm_model
        self.api_key = api_key

    def load(self, filepath: str) -> Dict[str, pd.DataFrame]:
        """加载 Excel 或 CSV 文件，返回 {sheet_name: DataFrame}"""
        ext = os.path.splitext(filepath)[1].lower()

        if ext == '.csv':
            # 尝试多种编码
            for encoding in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
                try:
                    df = pd.read_csv(filepath, encoding=encoding)
                    return {'Sheet1': df}
                except Exception:
                    continue
            raise ValueError(f"无法读取 CSV 文件：{filepath}")

        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(filepath, sheet_name=None)

        else:
            raise ValueError(f"不支持的文件格式：{ext}")

    def get_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """获取 DataFrame 的 schema 信息"""
        schema = {
            'columns': [],
            'row_count': len(df),
            'sample': df.head(3).to_dict(orient='records')
        }

        for col in df.columns:
            dtype = str(df[col].dtype)
            sample_values = df[col].dropna().head(3).tolist()
            # 转换为字符串便于 JSON 序列化
            sample_values = [str(v) for v in sample_values]

            schema['columns'].append({
                'name': str(col),
                'dtype': dtype,
                'sample_values': sample_values
            })

        return schema

    def save_schema(self, filepath: str, sheets: Dict[str, pd.DataFrame]) -> str:
        """保存 schema 到 .schema.json 文件，返回 schema 文件路径"""
        schema_path = filepath + '.schema.json'
        schemas = {}
        for sheet_name, df in sheets.items():
            schemas[str(sheet_name)] = self.get_schema(df)

        with open(schema_path, 'w', encoding='utf-8') as f:
            json.dump(schemas, f, ensure_ascii=False, indent=2)

        return schema_path

    def load_schema(self, filepath: str) -> Optional[Dict[str, Any]]:
        """加载 schema 文件"""
        schema_path = filepath + '.schema.json'
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def _call_llm(self, prompt: str, max_tokens: int = 500) -> str:
        """调用 LM Studio 生成分析计划"""
        try:
            import requests
            payload = {
                "model": self.llm_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": max_tokens,
                "stream": False
            }
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            response = requests.post(
                f"{self.llm_base_url}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                print(f"[Warning] LLM 调用失败：{response.status_code}")
                return ""
        except Exception as e:
            print(f"[Warning] LLM 调用错误：{e}")
            return ""

    def _parse_analysis_plan(self, llm_output: str) -> Optional[Dict[str, Any]]:
        """从 LLM 输出中解析 JSON 分析计划"""
        # 尝试提取 JSON 块
        json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
        if not json_match:
            return None

        try:
            plan = json.loads(json_match.group())
            return plan
        except json.JSONDecodeError:
            return None

    def build_analysis_prompt(self, question: str, schema: Dict[str, Any]) -> str:
        """构建让 LLM 生成分析计划的 prompt"""
        schema_text = json.dumps(schema, ensure_ascii=False, indent=2)

        return f"""你是一个数据分析助手。请根据用户问题和以下 Excel/CSV 表格结构，生成一个 JSON 格式的分析计划。

表格结构：
{schema_text}

用户问题：{question}

请按以下 JSON 格式返回分析计划（不要返回其他内容）：
{{
  "operation": "sum|avg|count|max|min|filter|sort|top_n|group_by",
  "target_column": "要进行计算的列名",
  "filter_conditions": [
    {{"column": "列名", "operator": "==|>|>=|<|<=|contains", "value": "值"}}
  ],
  "group_by_column": "如需分组统计，填写分组列名",
  "sort_column": "排序列名",
  "sort_ascending": false,
  "top_n": 10,
  "sheet_name": "工作表名称"
}}

注意：
- 列名必须严格使用表格结构中存在的列名
- operation 只能是以下之一：sum、avg、count、max、min、filter、sort、top_n、group_by
- 如果问题只需要筛选数据，operation 用 filter
- 如果问题需要统计总和/平均值等，operation 用 sum/avg 等
- 返回必须是合法 JSON，不要添加注释
"""

    def apply_plan(self, sheets: Dict[str, pd.DataFrame], plan: Dict[str, Any]) -> Dict[str, Any]:
        """根据分析计划执行安全的 pandas 操作"""
        operation = plan.get('operation', 'filter')
        sheet_name = plan.get('sheet_name')

        # 如果没有指定 sheet，使用第一个
        if sheet_name is None or sheet_name not in sheets:
            sheet_name = list(sheets.keys())[0]

        df = sheets[sheet_name].copy()

        # 1. 应用过滤条件
        filter_conditions = plan.get('filter_conditions', [])
        for condition in filter_conditions:
            col = condition.get('column')
            op = condition.get('operator', '==')
            value = condition.get('value')

            if col not in df.columns:
                continue

            try:
                # 对数值列统一使用 pd.to_numeric 转换（可处理千分位、小数等）
                if pd.api.types.is_numeric_dtype(df[col]) and op != 'contains':
                    value = pd.to_numeric(str(value).replace(',', ''), errors='coerce')
                    if pd.isna(value):
                        print(f"[Warning] 无法将 '{condition.get('value')}' 转换为数值")
                        continue

                if op == '==':
                    df = df[df[col] == value]
                elif op == '!=':
                    df = df[df[col] != value]
                elif op == '>':
                    df = df[df[col] > value]
                elif op == '>=':
                    df = df[df[col] >= value]
                elif op == '<':
                    df = df[df[col] < value]
                elif op == '<=':
                    df = df[df[col] <= value]
                elif op == 'contains':
                    df = df[df[col].astype(str).str.contains(str(value), na=False)]
            except Exception as e:
                print(f"[Warning] 过滤条件执行失败：{condition}，错误：{e}")
                continue

        # 2. 执行操作
        result = {
            'sheet_name': sheet_name,
            'operation': operation,
            'row_count': len(df),
            'plan': plan
        }

        target_column = plan.get('target_column')
        group_by_column = plan.get('group_by_column')

        if operation in self.SAFE_AGGREGATIONS:
            if target_column and target_column in df.columns:
                try:
                    series = pd.to_numeric(df[target_column], errors='coerce').dropna()
                    if len(series) > 0:
                        result['value'] = float(self.SAFE_AGGREGATIONS[operation](series))
                        result['unit'] = target_column
                    else:
                        result['value'] = None
                        result['warning'] = f"列 '{target_column}' 中没有可计算的数值"
                except Exception as e:
                    result['error'] = f"聚合计算失败：{e}"
            else:
                result['error'] = f"未找到目标列 '{target_column}'"

        elif operation == 'group_by':
            if group_by_column and target_column and group_by_column in df.columns and target_column in df.columns:
                try:
                    agg_df = df.groupby(group_by_column)[target_column].apply(lambda s: pd.to_numeric(s, errors='coerce').sum()).reset_index()
                    result['data'] = agg_df.to_dict(orient='records')
                except Exception as e:
                    result['error'] = f"分组统计失败：{e}"
            else:
                result['error'] = f"分组列或目标列不存在"

        elif operation == 'sort':
            sort_column = plan.get('sort_column')
            ascending = plan.get('sort_ascending', True)
            if sort_column and sort_column in df.columns:
                df = df.sort_values(by=sort_column, ascending=ascending)
            result['data'] = df.head(50).to_dict(orient='records')

        elif operation == 'top_n':
            sort_column = plan.get('sort_column')
            ascending = plan.get('sort_ascending', False)
            top_n = plan.get('top_n', 10)
            if sort_column and sort_column in df.columns:
                df = df.sort_values(by=sort_column, ascending=ascending)
            result['data'] = df.head(top_n).to_dict(orient='records')

        else:  # filter 或其他
            result['data'] = df.head(50).to_dict(orient='records')

        return result

    def analyze(self, question: str, filepath: str) -> Dict[str, Any]:
        """分析单个 Excel/CSV 文件"""
        # 加载数据
        sheets = self.load(filepath)

        # 加载或生成 schema
        schema = self.load_schema(filepath)
        if schema is None:
            schema = {}
            for sheet_name, df in sheets.items():
                schema[str(sheet_name)] = self.get_schema(df)
            self.save_schema(filepath, sheets)

        # 让 LLM 生成分析计划
        prompt = self.build_analysis_prompt(question, schema)
        llm_output = self._call_llm(prompt)

        if not llm_output:
            return {
                'error': '无法生成分析计划（LLM 调用失败）',
                'data': []
            }

        plan = self._parse_analysis_plan(llm_output)
        if plan is None:
            return {
                'error': '无法解析 LLM 返回的分析计划',
                'raw_output': llm_output,
                'data': []
            }

        # 执行分析计划
        return self.apply_plan(sheets, plan)


def format_excel_result(result: Dict[str, Any]) -> str:
    """将分析结果格式化为易读字符串"""
    if 'error' in result:
        return f"❌ 分析失败：{result['error']}"

    operation = result.get('operation', '')
    sheet_name = result.get('sheet_name', '')

    if 'value' in result:
        value = result['value']
        unit = result.get('unit', '')
        if value is not None:
            # 格式化数值
            if isinstance(value, float):
                value_str = f"{value:.2f}"
            else:
                value_str = str(value)
            return f"📊 {sheet_name} 的 {unit} {operation} 结果为：**{value_str}**"
        else:
            return f"⚠️ {result.get('warning', '无法计算')}"

    data = result.get('data', [])
    if data:
        df = pd.DataFrame(data)
        return f"📋 {sheet_name} 查询结果（共 {len(data)} 条）：\n\n{df.to_string(index=False)}"

    return "未找到相关数据"
