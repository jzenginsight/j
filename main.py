
from pathlib import Path
import numpy as np
import pandas as pd
import duckdb

# =========================================================
# 1. 项目基础配置
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
DB_DIR = BASE_DIR / "database"
SQL_DIR = BASE_DIR / "sql"
DOCS_DIR = BASE_DIR / "docs"
REPORTS_DIR = BASE_DIR / "reports"

for folder in [RAW_DIR, DB_DIR, SQL_DIR, DOCS_DIR, REPORTS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "fmcg_business.duckdb"

# 固定随机种子，保证每次生成结果一致
rng = np.random.default_rng(20261031)

MONTHS = pd.date_range("2025-10-01", "2026-09-01", freq="MS")

REGIONS = [
    "华东", "华南", "华北", "华中",
    "西南", "西北", "东北", "华中南"
]

CHANNELS = ["传统流通", "现代渠道", "电商", "特通渠道"]

# =========================================================
# 2. 生成客户主数据
# =========================================================

def generate_customers(n=500):

    cities = {
        "华东": ["上海", "杭州", "南京", "苏州", "合肥"],
        "华南": ["广州", "深圳", "佛山", "东莞", "厦门"],
        "华北": ["北京", "天津", "石家庄", "济南"],
        "华中": ["郑州", "武汉", "长沙", "南昌"],
        "西南": ["成都", "重庆", "昆明", "贵阳"],
        "西北": ["西安", "兰州", "银川", "乌鲁木齐"],
        "东北": ["沈阳", "大连", "长春", "哈尔滨"],
        "华中南": ["南宁", "海口", "柳州", "桂林"]
    }

    rows = []

    for i in range(1, n + 1):
        region = REGIONS[(i - 1) % len(REGIONS)]
        city = rng.choice(cities[region])

        rows.append({
            "customer_id": f"C{i:04d}",
            "customer_name": f"{city}经销商{i:04d}",
            "region": region,
            "city": city,
            "channel": rng.choice(CHANNELS, p=[0.55, 0.20, 0.15, 0.10]),
            "customer_level": rng.choice(
                ["A", "B", "C"], p=[0.15, 0.35, 0.50]
            ),
            "build_date": pd.Timestamp("2022-01-01")
                          + pd.Timedelta(days=int(rng.integers(0, 1600))),
            "status": rng.choice(["正常", "观察"], p=[0.90, 0.10])
        })

    return pd.DataFrame(rows)


# =========================================================
# 3. 生成产品主数据
# =========================================================

def generate_products(n=100):

    series_list = ["经典系列", "辣味系列", "烘焙系列", "膨化系列", "新品系列"]
    flavors = ["原味", "香辣", "番茄", "烧烤", "海苔"]
    specs = ["40g", "60g", "70g", "90g", "120g"]

    rows = []

    for i in range(1, n + 1):
        price = float(rng.choice([3.0, 4.0, 5.0, 6.0, 8.0, 10.0]))
        cost_rate = float(rng.uniform(0.45, 0.72))

        rows.append({
            "product_id": f"P{i:03d}",
            "product_name": f"休闲食品SKU{i:03d}",
            "series": series_list[(i - 1) % len(series_list)],
            "flavor": rng.choice(flavors),
            "spec": rng.choice(specs),
            "unit_price": round(price, 2),
            "unit_cost": round(price * cost_rate, 2),
            "launch_date": pd.Timestamp("2024-01-01")
                           + pd.Timedelta(days=int(rng.integers(0, 900))),
            "product_status": rng.choice(
                ["正常销售", "新品"], p=[0.85, 0.15]
            )
        })

    return pd.DataFrame(rows)


# =========================================================
# 4. 生成销售明细
# =========================================================

def generate_sales(customers, products, n=60000):

    customer_ids = customers["customer_id"].to_numpy()
    product_ids = products["product_id"].to_numpy()

    customer_weights = np.array([
        1.5 if level == "A" else 1.0 if level == "B" else 0.5
        for level in customers["customer_level"]
    ])
    customer_weights = customer_weights / customer_weights.sum()

    product_weights = rng.uniform(0.5, 1.5, len(products))
    product_weights = product_weights / product_weights.sum()

    selected_customers = rng.choice(
        customer_ids, size=n, p=customer_weights
    )
    selected_products = rng.choice(
        product_ids, size=n, p=product_weights
    )

    month_indices = rng.integers(0, len(MONTHS), size=n)
    dates = []

    for idx in month_indices:
        month = MONTHS[idx]
        day = int(rng.integers(
            0, (month + pd.offsets.MonthEnd(0)).day
        ))
        dates.append(month + pd.Timedelta(days=day))

    sales = pd.DataFrame({
        "order_id": [f"O{i:07d}" for i in range(1, n + 1)],
        "order_date": pd.to_datetime(dates),
        "customer_id": selected_customers,
        "product_id": selected_products,
        "quantity": rng.integers(10, 301, size=n),
        "discount_rate": rng.uniform(0, 0.12, size=n).round(4)
    })

    product_info = products.set_index("product_id")

    sales["unit_price"] = sales["product_id"].map(
        product_info["unit_price"]
    )
    sales["unit_cost"] = sales["product_id"].map(
        product_info["unit_cost"]
    )

    sales["sales_amount"] = (
        sales["quantity"]
        * sales["unit_price"]
        * (1 - sales["discount_rate"])
    ).round(2)

    sales["cost_amount"] = (
        sales["quantity"] * sales["unit_cost"]
    ).round(2)

    sales["gross_profit"] = (
        sales["sales_amount"] - sales["cost_amount"]
    ).round(2)

    sales["month"] = sales["order_date"].dt.strftime("%Y-%m")

    return sales


# =========================================================
# 5. 生成客户月度销售目标
# =========================================================

def generate_targets(customers, sales):

    actual = (
        sales.groupby(["customer_id", "month"])["sales_amount"]
        .sum()
        .reset_index()
        .rename(columns={"sales_amount": "actual_amount"})
    )

    # 生成全部客户 × 全部月份的目标骨架
    customer_month = pd.MultiIndex.from_product(
        [
            customers["customer_id"],
            MONTHS.strftime("%Y-%m")
        ],
        names=["customer_id", "month"]
    ).to_frame(index=False)

    result = customer_month.merge(
        actual,
        on=["customer_id", "month"],
        how="left"
    )

    result["actual_amount"] = result["actual_amount"].fillna(0)

    # 补充客户所属大区及客户级别
    result = result.merge(
        customers[["customer_id", "region", "customer_level"]],
        on="customer_id",
        how="left"
    )

    region_attainment = {
        "华东": 0.95,
        "华南": 0.74,
        "华北": 0.92,
        "华中": 0.88,
        "西南": 0.90,
        "西北": 0.86,
        "东北": 0.89,
        "华中南": 0.91
    }

    base_target_map = {
        "A": 18000,
        "B": 10000,
        "C": 5000
    }

    result["attainment_factor"] = result["region"].map(
        region_attainment
    )

    result["base_target"] = result["customer_level"].map(
        base_target_map
    )

    random_factor = rng.uniform(0.85, 1.15, len(result))

    result["target_amount"] = np.maximum(
        result["actual_amount"] / result["attainment_factor"],
        result["base_target"] * random_factor
    ).round(2)

    return result[
        ["month", "customer_id", "target_amount"]
    ]

    region_attainment = {
        "华东": 0.95,
        "华南": 0.74,
        "华北": 0.92,
        "华中": 0.88,
        "西南": 0.90,
        "西北": 0.86,
        "东北": 0.89,
        "华中南": 0.91
    }

    rows = []

    for customer in customers.itertuples():
        for month in MONTHS:
            month_str = month.strftime("%Y-%m")

            actual_row = actual[
                (actual["customer_id"] == customer.customer_id)
                & (actual["month"] == month_str)
            ]

            actual_amount = (
                float(actual_row["actual_amount"].iloc[0])
                if not actual_row.empty else 0.0
            )

            factor = region_attainment[customer.region]

            # 不同客户级别有不同目标基数
            base_target = (
                18000 if customer.customer_level == "A"
                else 10000 if customer.customer_level == "B"
                else 5000
            )

            # 目标与实际销售关联，但保留合理的最低目标
            target_amount = max(
                actual_amount / factor,
                base_target * rng.uniform(0.85, 1.15)
            )

            rows.append({
                "month": month_str,
                "customer_id": customer.customer_id,
                "target_amount": round(target_amount, 2)
            })

    return pd.DataFrame(rows)


# =========================================================
# 6. 生成客户库存快照
# =========================================================

def generate_inventory(customers, products, n=50000):

    customer_ids = customers["customer_id"].to_numpy()
    product_ids = products["product_id"].to_numpy()

    customer_choices = rng.choice(customer_ids, size=n)
    product_choices = rng.choice(product_ids, size=n)
    month_choices = rng.integers(0, len(MONTHS), size=n)

    inventory = pd.DataFrame({
        "snapshot_date": [
            MONTHS[i] + pd.offsets.MonthEnd(0)
            for i in month_choices
        ],
        "customer_id": customer_choices,
        "product_id": product_choices,
        "inventory_qty": rng.integers(0, 2001, size=n)
    })

    product_info = products.set_index("product_id")

    inventory["unit_cost"] = inventory["product_id"].map(
        product_info["unit_cost"]
    )

    inventory["inventory_amount"] = (
        inventory["inventory_qty"] * inventory["unit_cost"]
    ).round(2)

    inventory["month"] = (
        pd.to_datetime(inventory["snapshot_date"]).dt.strftime("%Y-%m")
    )

    # 同一个客户、SKU、月份只保留一条快照
    inventory = inventory.drop_duplicates(
        ["month", "customer_id", "product_id"]
    ).reset_index(drop=True)

    return inventory


# =========================================================
# 7. 生成客户费用数据
# =========================================================

def generate_expenses(customers, sales):

    actual = (
        sales.groupby(["customer_id", "month"])["sales_amount"]
        .sum()
        .reset_index()
    )

    expense_types = ["市场推广费", "物流费用", "陈列费用"]

    rows = []

    for record in actual.itertuples():
        for expense_type in expense_types:

            rate = {
                "市场推广费": 0.025,
                "物流费用": 0.035,
                "陈列费用": 0.015
            }[expense_type]

            expense_amount = (
                record.sales_amount
                * rate
                * rng.uniform(0.7, 1.3)
            )

            rows.append({
                "month": record.month,
                "customer_id": record.customer_id,
                "expense_type": expense_type,
                "expense_amount": round(expense_amount, 2)
            })

    return pd.DataFrame(rows)


# =========================================================
# 8. 数据质量检查
# =========================================================

def validate_data(tables):

    checks = []

    for table_name, df in tables.items():
        checks.append({
            "table_name": table_name,
            "row_count": len(df),
            "null_count": int(df.isnull().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum())
        })

    result = pd.DataFrame(checks)

    print("\n========== 数据质量检查 ==========")
    print(result.to_string(index=False))

    return result


# =========================================================
# 9. 导出 CSV 并创建 DuckDB
# =========================================================

def save_tables(tables):

    for table_name, df in tables.items():
        csv_path = RAW_DIR / f"{table_name}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    if DB_PATH.exists():
        DB_PATH.unlink()

    con = duckdb.connect(str(DB_PATH))

    for table_name, df in tables.items():
        con.register("temp_df", df)
        con.execute(
            f"CREATE TABLE {table_name} AS SELECT * FROM temp_df"
        )
        con.unregister("temp_df")

    print("\n========== 数据库创建成功 ==========")
    print(f"数据库路径：{DB_PATH}")

    print("\n========== 数据表记录数 ==========")

    for table_name in tables:
        count = con.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        print(f"{table_name}: {count:,}")

    con.close()


# =========================================================
# 10. 生成数据字典
# =========================================================

def generate_data_dictionary():

    content = """# FMCG AI Business Analyst - 数据字典

## 数据范围

- 模拟企业：Demo FMCG
- 数据周期：2025-10 至 2026-09
- 数据类型：模拟数据，不代表真实企业经营情况

## 表结构

### dim_customer
客户主数据：customer_id, customer_name, region, city,
channel, customer_level, build_date, status

### dim_product
产品主数据：product_id, product_name, series, flavor,
spec, unit_price, unit_cost, launch_date, product_status

### fact_sales
销售明细：order_id, order_date, customer_id, product_id,
quantity, discount_rate, unit_price, unit_cost,
sales_amount, cost_amount, gross_profit, month

### fact_inventory
库存快照：snapshot_date, customer_id, product_id,
inventory_qty, unit_cost, inventory_amount, month

### fact_target
客户月度目标：month, customer_id, target_amount

### fact_expense
客户月度费用：month, customer_id, expense_type,
expense_amount

## 核心指标口径

- 销售额 = SUM(sales_amount)
- 销售成本 = SUM(cost_amount)
- 毛利额 = 销售额 - 销售成本
- 毛利率 = 毛利额 / 销售额
- 目标达成率 = 实际销售额 / 销售目标
- 费用率 = 费用金额 / 销售额
- 扣除已记录费用后的贡献额 = 毛利额 - 费用金额

注意：费用数据只覆盖本项目模拟的三类费用，
不等于企业完整损益表。
"""

    (DOCS_DIR / "data_dictionary.md").write_text(
        content, encoding="utf-8"
    )


# =========================================================
# 11. 主程序
# =========================================================

def main():

    print("开始生成 FMCG 模拟业务数据...")

    customers = generate_customers()
    products = generate_products()
    sales = generate_sales(customers, products)
    targets = generate_targets(customers, sales)
    inventory = generate_inventory(customers, products)
    expenses = generate_expenses(customers, sales)

    tables = {
        "dim_customer": customers,
        "dim_product": products,
        "fact_sales": sales,
        "fact_inventory": inventory,
        "fact_target": targets,
        "fact_expense": expenses
    }

    quality_result = validate_data(tables)

    quality_result.to_csv(
        REPORTS_DIR / "data_quality_check.csv",
        index=False,
        encoding="utf-8-sig"
    )

    save_tables(tables)
    generate_data_dictionary()

    print("\n===================================")
    print("Day 1 数据生成任务完成！")
    print("请检查 data/raw、database、docs 和 reports 文件夹。")
    print("===================================")


if __name__ == "__main__":
    main()
