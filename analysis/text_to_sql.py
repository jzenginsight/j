
import os
import re
from pathlib import Path

import duckdb
from dotenv import load_dotenv
from openai import OpenAI

import streamlit as st
# ==========================================
# 1. 项目路径与 API 配置
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_FILE = BASE_DIR / "database" / "fmcg_business.duckdb"

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("OPENROUTER_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    raise ValueError("没有读取到 OPENROUTER_API_KEY，请检查本地 .env 或 Streamlit Cloud Secrets")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    timeout=120
)


# ==========================================
# 2. 自动读取数据库表结构
# ==========================================

def get_database_schema():

    con = duckdb.connect(
        str(DB_FILE),
        read_only=True
    )

    try:
        tables = con.execute("SHOW TABLES").fetchall()

        schema_text = ""

        for table in tables:
            table_name = table[0]

            columns = con.execute(
                f'DESCRIBE "{table_name}"'
            ).fetchall()

            schema_text += f"\n数据表：{table_name}\n"

            for column in columns:
                column_name = column[0]
                column_type = column[1]

                schema_text += (
                    f"- {column_name}: {column_type}\n"
                )

        return schema_text

    finally:
        con.close()


# ==========================================
# 3. 构建 AI Prompt
# ==========================================

def build_sql_prompt(question, schema):

    system_prompt = f"""
你是一名专业的快消品行业数据分析师，
擅长使用 DuckDB SQL 进行经营数据分析。

你的任务是根据用户的问题生成 SQL 查询语句。

数据库结构如下：

{schema}

请遵守以下规则：

1. 只能使用数据库中真实存在的表和字段。
2. 必须生成 DuckDB 兼容的 SQL。
3. 只允许生成一条 SELECT 查询语句。
4. 不允许 INSERT、UPDATE、DELETE、DROP、ALTER 等操作。
5. 涉及月份时优先使用 month 字段。
5.1 区域筛选必须使用数据库中的实际取值：
    东北、华中南、华东、西南、西北、华北、华南、华中。
    用户说"华南大区"时，使用 region = '华南'。
6. 销售额使用 sales_amount。
7. 毛利额使用 gross_profit。
8. 毛利率必须严格按照以下公式计算：

   SUM(gross_profit) / NULLIF(SUM(sales_amount), 0)

   注意：
   - 分子必须是毛利额 gross_profit
   - 分母必须是销售额 sales_amount
   - 绝对不能反过来计算
   - 不允许使用销售额 / 毛利额
   - 毛利率通常以小数形式返回，例如 0.3717 表示 37.17%
9. 需要客户或产品名称时，使用对应维度表关联。
10. 不要编造数据库中不存在的字段。
11. 严格区分金额变化和百分比变化：
   - 字段名包含 change 的金额字段，不能直接乘以100%作为变化率。
   - 字段名包含 change_rate 的字段才是变化率。
   - 变化率字段以小数形式存储，例如 -0.020944 应展示为 -2.09%。
   - 不允许自行推算或替换数据库已经提供的变化率。
   - 展示百分比时，必须使用对应的 change_rate 字段。
12. 所有分析结论必须与查询结果一致，
   不得编造行业标准或未经验证的业务原因。
只返回 SQL 语句，不要返回解释、Markdown 或其他内容。
"""

    user_prompt = f"""
请根据以下问题生成 SQL：

{question}
"""

    return system_prompt, user_prompt


# ==========================================
# 4. 调用大模型生成 SQL
# ==========================================

def generate_sql(question, schema):

    system_prompt, user_prompt = build_sql_prompt(
        question,
        schema
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    sql = response.choices[0].message.content

    if not sql or not sql.strip():
        raise ValueError("AI 没有返回 SQL")

    # 去除模型可能返回的 Markdown 代码块
    sql = re.sub(
        r"^```(?:sql)?\s*|\s*```$",
        "",
        sql.strip(),
        flags=re.IGNORECASE
    )

    return sql.strip()


# ==========================================
# 5. 主程序
# ==========================================

if __name__ == "__main__":

    print("正在读取数据库结构...")

    schema = get_database_schema()

    print("数据库结构读取成功！")

    question = input(
        "\n请输入你的经营分析问题：\n"
    ).strip()

    if not question:
        raise ValueError("问题不能为空")

    print("\nAI 正在生成 SQL，请稍候...")

    sql = generate_sql(
        question,
        schema
    )


    # ==========================================
    # 5. 执行 AI 生成的 SQL
    # ==========================================

def execute_sql(sql):

    # 基础安全检查：只允许单条 SELECT 查询
    clean_sql = sql.strip().rstrip(";").strip()

    if not re.match(r"^(SELECT|WITH)\b", clean_sql, re.IGNORECASE):
        raise ValueError("只允许执行 SELECT 或 WITH 查询")

    if ";" in clean_sql:
        raise ValueError("不允许执行多条 SQL 语句")

    forbidden = (
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|"
        r"COPY|ATTACH|DETACH|INSTALL|LOAD|CALL|PRAGMA)\b"
    )

    if re.search(forbidden, clean_sql, re.IGNORECASE):
        raise ValueError("SQL 包含不允许执行的操作")

    # 以只读模式连接数据库
    con = duckdb.connect(
        str(DB_FILE),
        read_only=True
    )

    try:
        result = con.execute(clean_sql).df()
        return result

    finally:
        con.close()


    # ==========================================
    # 6. AI 自动分析查询结果
    # ==========================================

def analyze_result(question, result):

    # 将查询结果转换为 JSON
    result_json = result.to_json(
        orient="records",
        force_ascii=False
    )

    system_prompt = """
你是一名资深快消品行业经营分析师。

请根据用户的问题和数据库实际查询结果，
输出简洁、专业的经营分析。

要求：

1. 首先概括核心数据。
2. 解释关键指标的业务含义。
3. 提出有数据依据的经营观察。
4. 如果数据不足以判断原因，明确说明需要进一步分析。
5. 不允许编造数据或推测未经验证的原因。
6. 使用中文回答，结构清晰。
7. 金额单位为元，毛利率转换为百分比展示。
"""

    user_prompt = f"""
用户问题：
{question}

数据库查询结果：
{result_json}

请根据以上信息进行经营分析。
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    message = response.choices[0].message
    analysis = message.content

    if not analysis or not analysis.strip():
        print("AI 本次没有返回文本。")
        print("Finish reason:", response.choices[0].finish_reason)
        print("Response:", response.model_dump_json(indent=2))
        raise ValueError("AI 没有返回经营分析结果，请检查模型响应")

    return analysis.strip()

    return analysis.strip()


    print("\n========== AI 生成的 SQL ==========\n")
    print(sql)

    print("\n正在执行 SQL...")

    result = execute_sql(sql)

    print("\n========== 查询结果 ==========\n")
    print(result.to_string(index=False))

    print("\nSQL 查询执行成功！")
    print("\nAI 正在分析经营数据...")



    print("\n========== AI 经营分析 ==========\n")
    print(analysis)
