
import duckdb
import pandas as pd
from pathlib import Path

# =====================================
# 1. 定位项目路径
# =====================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DB_PATH = PROJECT_DIR / "database" / "fmcg_business.duckdb"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================
# 2. 连接 DuckDB
# =====================================

con = duckdb.connect(str(DB_PATH), read_only=True)


# =====================================
# 3. SQL：查询华南大区8月、9月产品销售
# =====================================

sql = """
WITH product_monthly AS (

    SELECT
        s.product_id,

        SUM(
            CASE
                WHEN s.month = '2026-08'
                THEN s.sales_amount ELSE 0
            END
        ) AS sales_aug,

        SUM(
            CASE
                WHEN s.month = '2026-09'
                THEN s.sales_amount ELSE 0
            END
        ) AS sales_sep,

        SUM(
            CASE
                WHEN s.month = '2026-08'
                THEN s.cost_amount ELSE 0
            END
        ) AS cost_aug,

        SUM(
            CASE
                WHEN s.month = '2026-09'
                THEN s.cost_amount ELSE 0
            END
        ) AS cost_sep

    FROM fact_sales s

    INNER JOIN dim_customer c
        ON s.customer_id = c.customer_id

    WHERE c.region = '华南'
      AND s.month IN ('2026-08', '2026-09')

    GROUP BY s.product_id
)

SELECT
    p.product_id,
    p.product_name,
    p.series,
    p.flavor,
    p.spec,

    COALESCE(m.sales_aug, 0) AS sales_aug,
    COALESCE(m.sales_sep, 0) AS sales_sep,

    COALESCE(m.cost_aug, 0) AS cost_aug,
    COALESCE(m.cost_sep, 0) AS cost_sep

FROM dim_product p

LEFT JOIN product_monthly m
    ON p.product_id = m.product_id

ORDER BY p.product_id
"""

df = con.execute(sql).df()
con.close()


# =====================================
# 4. Pandas：计算产品盈利指标
# =====================================

# 销售额变化
df["sales_change"] = df["sales_sep"] - df["sales_aug"]

# 销售增长率
df["growth_rate"] = (
    df["sales_change"] / df["sales_aug"].replace(0, pd.NA)
)

# 毛利额
df["gross_profit_aug"] = df["sales_aug"] - df["cost_aug"]
df["gross_profit_sep"] = df["sales_sep"] - df["cost_sep"]

# 毛利率
df["gross_margin_aug"] = (
    df["gross_profit_aug"] / df["sales_aug"].replace(0, pd.NA)
)

df["gross_margin_sep"] = (
    df["gross_profit_sep"] / df["sales_sep"].replace(0, pd.NA)
)

# 华南大区各月销售额
total_sales_aug = df["sales_aug"].sum()
total_sales_sep = df["sales_sep"].sum()

# 产品销售占比
df["sales_share_aug"] = df["sales_aug"] / total_sales_aug
df["sales_share_sep"] = df["sales_sep"] / total_sales_sep

# 毛利率变化（百分点）
df["gross_margin_change"] = (
    df["gross_margin_sep"] - df["gross_margin_aug"]
)


# =====================================
# 5. 输出产品盈利能力分析结果
# =====================================

output_columns = [
    "product_id",
    "product_name",
    "series",
    "flavor",
    "spec",
    "sales_aug",
    "sales_sep",
    "sales_change",
    "growth_rate",
    "gross_profit_aug",
    "gross_profit_sep",
    "gross_margin_aug",
    "gross_margin_sep",
    "gross_margin_change",
    "sales_share_aug",
    "sales_share_sep"
]

result = df[output_columns].copy()

# 排序：按9月销售额从高到低
result = result.sort_values(
    by="sales_sep",
    ascending=False
)

# 保存CSV
output_path = REPORT_DIR / "product_profitability.csv"

result.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)


# =====================================
# 6. 输出数据核对及摘要
# =====================================

print("===== 产品盈利能力分析完成 =====")

print("产品数量：", result["product_id"].nunique())

print(f"8月产品销售额合计：{total_sales_aug:,.2f}")
print(f"9月产品销售额合计：{total_sales_sep:,.2f}")

print("\n===== TOP10销售产品 =====")

print(
    result[
        ["product_id", "product_name", "sales_sep",
         "gross_margin_sep", "sales_share_sep"]
    ].head(10).to_string(index=False)
)

print("\n结果保存位置：", output_path)
