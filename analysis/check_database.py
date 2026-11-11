
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "database" / "fmcg_business.duckdb"

con = duckdb.connect(str(DB_FILE), read_only=True)

print("========== 区域分布 ==========")

print(
    con.execute("""
        SELECT region, COUNT(*) AS customer_count
        FROM dim_customer
        GROUP BY region
    """).df().to_string(index=False)
)

print("\n========== 销售月份分布 ==========")

print(
    con.execute("""
        SELECT month, COUNT(*) AS sales_count
        FROM fact_sales
        GROUP BY month
        ORDER BY month
    """).df().to_string(index=False)
)

print("\n========== 筛选条件匹配数量 ==========")

print(
    con.execute("""
        SELECT COUNT(*)
        FROM fact_sales f
        JOIN dim_customer c
            ON f.customer_id = c.customer_id
        WHERE c.region = '华南大区'
          AND f.month = '2026-09'
    """).fetchone()
)

con.close()
