
from pathlib import Path
import duckdb
import pandas as pd

# 1. 路径配置
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DB_PATH = PROJECT_DIR / "database" / "fmcg_business.duckdb"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# 2. 连接数据库
con = duckdb.connect(str(DB_PATH), read_only=True)

# 3. 查询华南客户8月和9月销售额
sql = """
WITH customer_base AS (
    SELECT
        customer_id,
        customer_name
    FROM dim_customer
    WHERE region = '华南'
),

monthly_sales AS (
    SELECT
        customer_id,
        month,
        SUM(sales_amount) AS sales_amount
    FROM fact_sales
    WHERE month IN ('2026-08', '2026-09')
    GROUP BY customer_id, month
)

SELECT
    c.customer_id,
    c.customer_name,

    COALESCE(
        SUM(CASE WHEN s.month = '2026-08'
            THEN s.sales_amount ELSE 0 END), 0
    ) AS sales_aug,

    COALESCE(
        SUM(CASE WHEN s.month = '2026-09'
            THEN s.sales_amount ELSE 0 END), 0
    ) AS sales_sep

FROM customer_base c
LEFT JOIN monthly_sales s
    ON c.customer_id = s.customer_id

GROUP BY
    c.customer_id,
    c.customer_name

ORDER BY sales_sep DESC
"""

df = con.execute(sql).df()
con.close()

# 4. 计算销售额变化
df["sales_change"] = df["sales_sep"] - df["sales_aug"]

# 5. 计算环比增长率
df["growth_rate"] = (
    df["sales_change"]
    / df["sales_aug"].replace(0, pd.NA)
)

# 6. 判断客户交易状态
def classify_customer(row):
    if row["sales_aug"] == 0 and row["sales_sep"] > 0:
        return "新增交易"

    elif row["sales_aug"] > 0 and row["sales_sep"] == 0:
        return "停止交易"

    elif row["sales_change"] > 0:
        return "销售增长"

    elif row["sales_change"] < 0:
        return "销售下降"

    else:
        return "销售持平"

df["customer_status"] = df.apply(
    classify_customer, axis=1
)

# 7. 输出结果
print("\n========== 华南客户环比分析 ==========")
print(df.to_string(index=False))

# 8. 保存结果
output_path = REPORT_DIR / "customer_growth_analysis.csv"

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\n分析完成！")
print("客户数量：", len(df))
print("文件保存位置：", output_path)
