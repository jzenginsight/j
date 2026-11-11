
import duckdb

# 连接数据库
con = duckdb.connect(
    "database/fmcg_business.duckdb",
    read_only=True
)

# 1. 检查销售数据规模
print("\n========== 销售数据规模 ==========")

result = con.execute("""
    SELECT
        COUNT(*) AS sales_rows,
        COUNT(DISTINCT order_id) AS unique_orders,
        COUNT(DISTINCT customer_id) AS customers,
        COUNT(DISTINCT product_id) AS products
    FROM fact_sales
""").df()

print(result.to_string(index=False))


# 2. 检查销售数据日期范围
print("\n========== 销售日期范围 ==========")

result = con.execute("""
    SELECT
        MIN(order_date) AS start_date,
        MAX(order_date) AS end_date
    FROM fact_sales
""").df()

print(result.to_string(index=False))


# 3. 检查是否存在无效客户ID
print("\n========== 无效客户ID检查 ==========")

result = con.execute("""
    SELECT COUNT(*) AS invalid_customer_count
    FROM fact_sales s
    LEFT JOIN dim_customer c
        ON s.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
""").df()

print(result.to_string(index=False))


# 4. 检查是否存在无效产品ID
print("\n========== 无效产品ID检查 ==========")

result = con.execute("""
    SELECT COUNT(*) AS invalid_product_count
    FROM fact_sales s
    LEFT JOIN dim_product p
        ON s.product_id = p.product_id
    WHERE p.product_id IS NULL
""").df()

print(result.to_string(index=False))


con.close()

print("\n数据库检查完成！")
