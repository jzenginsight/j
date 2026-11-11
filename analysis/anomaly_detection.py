
from pathlib import Path

import duckdb
import pandas as pd


# ==================================================
# 1. 路径与参数配置
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DB_PATH = PROJECT_DIR / "database" / "fmcg_business.duckdb"
OUTPUT_PATH = PROJECT_DIR / "reports" / "anomaly_detection.csv"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

PREVIOUS_MONTH = "2026-08"
CURRENT_MONTH = "2026-09"

# 异常识别阈值
SALES_DROP_THRESHOLD = -0.15
CUSTOMER_DROP_THRESHOLD = -0.25

# 注意：毛利率、费用率的阈值单位是百分点
GROSS_MARGIN_DROP_THRESHOLD = -3.0
EXPENSE_RATE_RISE_THRESHOLD = 2.0

INVENTORY_RISE_THRESHOLD = 0.30


# ==================================================
# 2. 通用函数
# ==================================================

anomalies = []


def add_anomaly(
    anomaly_type,
    entity_type,
    entity_id,
    entity_name,
    previous_value,
    current_value,
    change,
    change_rate,
    unit,
    threshold_description,
):
    """将识别出的异常整理为统一记录。"""

    # 根据相对变化率判断异常等级
    if (
        change_rate is not None
        and (
            change_rate <= -0.40
            or change_rate >= 0.40
        )
    ):
        severity = "高"
    else:
        severity = "中"

    anomalies.append({
        "anomaly_type": anomaly_type,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "entity_name": entity_name,
        "previous_month": PREVIOUS_MONTH,
        "current_month": CURRENT_MONTH,
        "previous_value": previous_value,
        "current_value": current_value,
        "change": change,
        "change_rate": change_rate,
        "unit": unit,
        "severity": severity,
        "rule": threshold_description,
    })


def safe_rate_change(previous, current):
    """计算环比变化率，避免除以0。"""

    if pd.isna(previous) or previous == 0:
        return None

    return (current - previous) / abs(previous)


def get_month_values(df, key_columns, value_column):
    """将两个月的数据整理成可比较的宽表。"""

    result = df.pivot_table(
        index=key_columns,
        columns="month",
        values=value_column,
        aggfunc="sum",
        fill_value=0,
    ).reset_index()

    for month in [PREVIOUS_MONTH, CURRENT_MONTH]:
        if month not in result.columns:
            result[month] = 0

    return result


# ==================================================
# 3. 连接数据库
# ==================================================

if not DB_PATH.exists():
    raise FileNotFoundError(f"数据库不存在：{DB_PATH}")

con = duckdb.connect(str(DB_PATH), read_only=True)

try:

    # ==================================================
    # 4. 大区销售额与毛利率异常
    # ==================================================

    region_df = con.execute("""
        SELECT
            s.month,
            SUM(s.sales_amount) AS sales_amount,
            SUM(s.cost_amount) AS cost_amount
        FROM fact_sales s
        INNER JOIN dim_customer c
            ON s.customer_id = c.customer_id
        WHERE c.region = '华南'
          AND s.month IN ('2026-08', '2026-09')
        GROUP BY s.month
    """).df()

    if region_df.empty:
        raise ValueError("未查询到华南大区8月、9月销售数据。")

    region_df["gross_profit"] = (
        region_df["sales_amount"] - region_df["cost_amount"]
    )

    # 毛利率 = 毛利额 / 销售额
    region_df["gross_margin"] = (
        region_df["gross_profit"]
        / region_df["sales_amount"].replace(0, pd.NA)
    )

    region_sales = get_month_values(
        region_df, [], "sales_amount"
    )

    region_margin = get_month_values(
        region_df, [], "gross_margin"
    )

    # ---------- 4.1 大区销售额下降 ----------

    sales_aug = float(region_sales.iloc[0][PREVIOUS_MONTH])
    sales_sep = float(region_sales.iloc[0][CURRENT_MONTH])

    sales_change = sales_sep - sales_aug
    sales_change_rate = safe_rate_change(
        sales_aug, sales_sep
    )

    if (
        sales_change_rate is not None
        and sales_change_rate <= SALES_DROP_THRESHOLD
    ):
        add_anomaly(
            "大区销售额下降",
            "大区",
            "华南",
            "华南大区",
            sales_aug,
            sales_sep,
            sales_change,
            sales_change_rate,
            "元",
            "销售额环比下降15%及以上",
        )

    # ---------- 4.2 大区毛利率下降 ----------

    # 原始毛利率保留小数，不提前转换单位
    margin_aug_raw = float(
        region_margin.iloc[0][PREVIOUS_MONTH]
    )

    margin_sep_raw = float(
        region_margin.iloc[0][CURRENT_MONTH]
    )

    # 计算百分点变化
    margin_change_pp = (
        margin_sep_raw - margin_aug_raw
    ) * 100

    if margin_change_pp <= GROSS_MARGIN_DROP_THRESHOLD:

        add_anomaly(
            "大区毛利率下降",
            "大区",
            "华南",
            "华南大区",

            # 展示值转换为百分数
            margin_aug_raw * 100,
            margin_sep_raw * 100,

            # 变化值为百分点
            margin_change_pp,

            None,
            "百分点",
            "毛利率环比下降3个百分点及以上",
        )


    # ==================================================
    # 5. 客户销售额骤降
    # ==================================================

    customer_sales = con.execute("""
        SELECT
            s.month,
            c.customer_id,
            c.customer_name,
            SUM(s.sales_amount) AS sales_amount
        FROM fact_sales s
        INNER JOIN dim_customer c
            ON s.customer_id = c.customer_id
        WHERE c.region = '华南'
          AND s.month IN ('2026-08', '2026-09')
        GROUP BY
            s.month,
            c.customer_id,
            c.customer_name
    """).df()

    customer_wide = get_month_values(
        customer_sales,
        ["customer_id", "customer_name"],
        "sales_amount",
    )

    for _, row in customer_wide.iterrows():

        # 销售额保持原始金额，不乘100
        previous = float(row[PREVIOUS_MONTH])
        current = float(row[CURRENT_MONTH])

        # 绝对变化金额
        change = current - previous

        # 相对变化率
        change_rate = safe_rate_change(
            previous, current
        )

        if (
            change_rate is not None
            and change_rate <= CUSTOMER_DROP_THRESHOLD
        ):
            add_anomaly(
                "客户销售额骤降",
                "客户",
                row["customer_id"],
                row["customer_name"],
                previous,
                current,
                change,
                change_rate,
                "元",
                "客户销售额环比下降25%及以上",
            )


    # ==================================================
    # 6. 产品毛利率下降
    # ==================================================

    product_df = con.execute("""
        SELECT
            s.month,
            p.product_id,
            p.product_name,
            SUM(s.sales_amount) AS sales_amount,
            SUM(s.cost_amount) AS cost_amount
        FROM fact_sales s
        INNER JOIN dim_customer c
            ON s.customer_id = c.customer_id
        INNER JOIN dim_product p
            ON s.product_id = p.product_id
        WHERE c.region = '华南'
          AND s.month IN ('2026-08', '2026-09')
        GROUP BY
            s.month,
            p.product_id,
            p.product_name
    """).df()

    # 产品毛利率 = 产品毛利额 / 产品销售额
    product_df["gross_margin"] = (
        product_df["sales_amount"]
        - product_df["cost_amount"]
    ) / product_df["sales_amount"].replace(0, pd.NA)

    product_wide = get_month_values(
        product_df,
        ["product_id", "product_name"],
        "gross_margin",
    )

    for _, row in product_wide.iterrows():

        # 检查产品是否在两个月都有正销售额
        sales_check = product_df[
            product_df["product_id"] == row["product_id"]
        ]

        active_months = sales_check[
            sales_check["sales_amount"] > 0
        ]["month"].nunique()

        if active_months < 2:
            continue

        # 原始毛利率，小数形式
        previous_raw = float(row[PREVIOUS_MONTH])
        current_raw = float(row[CURRENT_MONTH])

        # 转换成百分点
        change_pp = (
            current_raw - previous_raw
        ) * 100

        # 判断条件：下降3个百分点及以上
        if change_pp <= GROSS_MARGIN_DROP_THRESHOLD:

            add_anomaly(
                "产品毛利率下降",
                "产品",
                row["product_id"],
                row["product_name"],

                # 展示值转换为百分数
                previous_raw * 100,
                current_raw * 100,

                # 变化值为百分点
                change_pp,

                None,
                "百分点",
                "产品毛利率环比下降3个百分点及以上",
            )


    # ==================================================
    # 7. 客户费用率上升
    # ==================================================

    # 分别聚合销售额与费用，避免多表JOIN导致金额重复
    expense_monthly = con.execute("""
        WITH sales_monthly AS (
            SELECT
                s.month,
                s.customer_id,
                SUM(s.sales_amount) AS sales_amount
            FROM fact_sales s
            INNER JOIN dim_customer c
                ON s.customer_id = c.customer_id
            WHERE c.region = '华南'
              AND s.month IN ('2026-08', '2026-09')
            GROUP BY s.month, s.customer_id
        ),

        expense_monthly AS (
            SELECT
                e.month,
                e.customer_id,
                SUM(e.expense_amount) AS expense_amount
            FROM fact_expense e
            INNER JOIN dim_customer c
                ON e.customer_id = c.customer_id
            WHERE c.region = '华南'
              AND e.month IN ('2026-08', '2026-09')
            GROUP BY e.month, e.customer_id
        )

        SELECT
            s.month,
            s.customer_id,
            c.customer_name,
            s.sales_amount,
            COALESCE(e.expense_amount, 0) AS expense_amount
        FROM sales_monthly s
        INNER JOIN dim_customer c
            ON s.customer_id = c.customer_id
        LEFT JOIN expense_monthly e
            ON s.month = e.month
            AND s.customer_id = e.customer_id
    """).df()

    # 费用率 = 费用金额 / 销售额
    expense_monthly["expense_rate"] = (
        expense_monthly["expense_amount"]
        / expense_monthly["sales_amount"]
    )

    expense_wide = get_month_values(
        expense_monthly,
        ["customer_id", "customer_name"],
        "expense_rate",
    )

    for _, row in expense_wide.iterrows():

        # 原始费用率，小数形式
        previous_raw = float(row[PREVIOUS_MONTH])
        current_raw = float(row[CURRENT_MONTH])

        # 转换为百分点
        change_pp = (
            current_raw - previous_raw
        ) * 100

        # 判断费用率是否上升2个百分点及以上
        if change_pp >= EXPENSE_RATE_RISE_THRESHOLD:

            add_anomaly(
                "客户费用率上升",
                "客户",
                row["customer_id"],
                row["customer_name"],

                # 展示值转换为百分数
                previous_raw * 100,
                current_raw * 100,

                # 变化值为百分点
                change_pp,

                None,
                "百分点",
                "客户费用率环比上升2个百分点及以上",
            )


    # ==================================================
    # 8. 客户库存金额上升
    # ==================================================

    inventory_df = con.execute("""
        WITH inventory_date AS (
            SELECT
                STRFTIME(
                    CAST(snapshot_date AS DATE), '%Y-%m'
                ) AS month,
                MAX(CAST(snapshot_date AS DATE)) AS latest_date
            FROM fact_inventory
            WHERE STRFTIME(
                CAST(snapshot_date AS DATE), '%Y-%m'
            ) IN ('2026-08', '2026-09')
            GROUP BY 1
        )

        SELECT
            STRFTIME(
                CAST(i.snapshot_date AS DATE), '%Y-%m'
            ) AS month,
            c.customer_id,
            c.customer_name,
            SUM(i.inventory_amount) AS inventory_amount

        FROM fact_inventory i

        INNER JOIN inventory_date d
            ON CAST(i.snapshot_date AS DATE) = d.latest_date

        INNER JOIN dim_customer c
            ON i.customer_id = c.customer_id

        WHERE c.region = '华南'

        GROUP BY
            1,
            c.customer_id,
            c.customer_name

    """).df()

    inventory_wide = get_month_values(
        inventory_df,
        ["customer_id", "customer_name"],
        "inventory_amount",
    )

    for _, row in inventory_wide.iterrows():

        previous = float(row[PREVIOUS_MONTH])
        current = float(row[CURRENT_MONTH])

        # 库存金额变化
        change = current - previous

        # 库存增长率
        change_rate = safe_rate_change(
            previous, current
        )

        if (
            change_rate is not None
            and change_rate >= INVENTORY_RISE_THRESHOLD
        ):
            add_anomaly(
                "客户库存金额上升",
                "客户",
                row["customer_id"],
                row["customer_name"],
                previous,
                current,
                change,
                change_rate,
                "元",
                "客户库存金额环比上升30%及以上",
            )

finally:
    con.close()


# ==================================================
# 9. 汇总异常结果
# ==================================================

columns = [
    "anomaly_type",
    "entity_type",
    "entity_id",
    "entity_name",
    "previous_month",
    "current_month",
    "previous_value",
    "current_value",
    "change",
    "change_rate",
    "unit",
    "severity",
    "rule",
]

result = pd.DataFrame(anomalies, columns=columns)

if not result.empty:

    result = result.sort_values(
        ["severity", "anomaly_type", "change"],
        ascending=[True, True, True],
    )


result.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig",
)


# ==================================================
# 10. 自动校验与运行摘要
# ==================================================

if not result.empty:

    if result["entity_id"].isna().any():
        raise ValueError("异常结果存在空实体ID。")

    if result["anomaly_type"].isna().any():
        raise ValueError("异常结果存在空异常类型。")

    if result["previous_value"].isna().any():
        raise ValueError("异常结果存在空的上期指标值。")

    if result["current_value"].isna().any():
        raise ValueError("异常结果存在空的本期指标值。")


print("=" * 55)
print("华南大区经营异常识别完成")
print("=" * 55)

print(f"对比期间：{PREVIOUS_MONTH} vs {CURRENT_MONTH}")
print(f"识别异常总数：{len(result)}")

if result.empty:

    print("当前阈值下未发现符合条件的异常。")

else:

    print("\n异常类型统计：")
    print(result["anomaly_type"].value_counts().to_string())

    print("\n异常等级统计：")
    print(result["severity"].value_counts().to_string())

print("\n数据校验：通过")
print(f"结果文件：{OUTPUT_PATH}")
