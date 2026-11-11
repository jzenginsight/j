
from pathlib import Path
import duckdb
import pandas as pd

# 1. 获取项目路径
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DB_PATH = PROJECT_DIR / "database" / "fmcg_business.duckdb"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# 2. 连接数据库
con = duckdb.connect(str(DB_PATH), read_only=True)

# 3. 查询华南大区2026年9月客户经营数据
sql = """
WITH customer_base AS (
    SELECT
        customer_id,
        customer_name,
        region
    FROM dim_customer
    WHERE region = '华南'
),

sales_customer AS (
    SELECT
        customer_id,
        SUM(sales_amount) AS sales_amount,
        SUM(cost_amount) AS cost_amount
    FROM fact_sales
    WHERE month = '2026-09'
    GROUP BY customer_id
),

target_customer AS (
    SELECT
        customer_id,
        SUM(target_amount) AS target_amount
    FROM fact_target
    WHERE month = '2026-09'
    GROUP BY customer_id
)

SELECT
    c.customer_id,
    c.customer_name,

    COALESCE(s.sales_amount, 0) AS sales_amount,
    COALESCE(t.target_amount, 0) AS target_amount,

    COALESCE(s.sales_amount, 0)
        - COALESCE(s.cost_amount, 0) AS gross_profit,

    (
        COALESCE(s.sales_amount, 0)
        - COALESCE(s.cost_amount, 0)
    ) / NULLIF(s.sales_amount, 0) AS gross_margin

FROM customer_base c

LEFT JOIN sales_customer s
    ON c.customer_id = s.customer_id

LEFT JOIN target_customer t
    ON c.customer_id = t.customer_id

ORDER BY sales_amount DESC
"""

df = con.execute(sql).df()
con.close()

# 4. 计算客户目标达成率
df["achievement_rate"] = (
    df["sales_amount"]
    / df["target_amount"].replace(0, pd.NA)
)

# 5. 计算客户销售贡献率
total_sales = df["sales_amount"].sum()

df["sales_contribution"] = (
    df["sales_amount"] / total_sales
    if total_sales != 0 else 0
)

# 6. 输出结果
print("\n========== 华南客户经营分析 ==========")
print(df.to_string(index=False))

# 7. 保存文件
output_path = REPORT_DIR / "customer_analysis.csv"

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\n分析完成！")
print("客户数量：", len(df))
print("文件保存位置：", output_path)
