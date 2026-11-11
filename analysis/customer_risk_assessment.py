
from pathlib import Path

import pandas as pd


# ==================================================
# 1. 路径配置
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

INPUT_PATH = PROJECT_DIR / "reports" / "anomaly_detection.csv"
OUTPUT_PATH = PROJECT_DIR / "reports" / "customer_risk_assessment.csv"


# ==================================================
# 2. 读取异常识别结果
# ==================================================

if not INPUT_PATH.exists():
    raise FileNotFoundError(f"找不到异常识别文件：{INPUT_PATH}")

anomaly_df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

required_columns = [
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
]

missing_columns = [
    col for col in required_columns
    if col not in anomaly_df.columns
]

if missing_columns:
    raise ValueError(f"异常结果缺少必要字段：{missing_columns}")


# ==================================================
# 3. 筛选客户异常
# ==================================================

customer_df = anomaly_df[
    anomaly_df["entity_type"] == "客户"
].copy()

customer_df["change"] = pd.to_numeric(
    customer_df["change"], errors="coerce"
)

customer_df["change_rate"] = pd.to_numeric(
    customer_df["change_rate"], errors="coerce"
)

# 只保留本阶段关注的三类客户异常
risk_types = [
    "客户销售额骤降",
    "客户库存金额上升",
    "客户费用率上升",
]

customer_df = customer_df[
    customer_df["anomaly_type"].isin(risk_types)
].copy()


# ==================================================
# 4. 定义单个客户的指标提取函数
# ==================================================

def get_metric(customer_group, anomaly_type, column):
    """
    根据客户和异常类型，提取对应指标。
    如果客户没有触发该异常，则返回 None。
    """

    matched = customer_group[
        customer_group["anomaly_type"] == anomaly_type
    ]

    if matched.empty:
        return None

    return matched.iloc[0][column]


# ==================================================
# 5. 按客户整合多指标异常
# ==================================================

risk_records = []

for (customer_id, customer_name), group in customer_df.groupby(
    ["entity_id", "entity_name"]
):

    # 三类风险信号
    sales_drop = (
        "客户销售额骤降" in group["anomaly_type"].values
    )

    inventory_rise = (
        "客户库存金额上升" in group["anomaly_type"].values
    )

    expense_rise = (
        "客户费用率上升" in group["anomaly_type"].values
    )

    # 统计触发的风险信号数量
    risk_signal_count = sum([
        sales_drop,
        inventory_rise,
        expense_rise,
    ])

    # 风险等级
    if risk_signal_count >= 2:
        risk_level = "高风险"
    else:
        risk_level = "中风险"

    # 跟进优先级
    if sales_drop and inventory_rise:
        follow_up_priority = "优先跟进"
    elif risk_signal_count >= 2:
        follow_up_priority = "重点关注"
    else:
        follow_up_priority = "常规关注"

    # 风险原因
    risk_reasons = []

    if sales_drop:
        risk_reasons.append("销售额下降")

    if inventory_rise:
        risk_reasons.append("库存金额上升")

    if expense_rise:
        risk_reasons.append("费用率上升")

    # 提取各指标具体变化
    sales_change_rate = get_metric(
        group, "客户销售额骤降", "change_rate"
    )

    sales_change = get_metric(
        group, "客户销售额骤降", "change"
    )

    inventory_change_rate = get_metric(
        group, "客户库存金额上升", "change_rate"
    )

    inventory_change = get_metric(
        group, "客户库存金额上升", "change"
    )

    expense_change = get_metric(
        group, "客户费用率上升", "change"
    )

    risk_records.append({
        "customer_id": customer_id,
        "customer_name": customer_name,

        "sales_drop": "是" if sales_drop else "否",
        "inventory_rise": "是" if inventory_rise else "否",
        "expense_rise": "是" if expense_rise else "否",

        "risk_signal_count": risk_signal_count,
        "risk_level": risk_level,
        "follow_up_priority": follow_up_priority,
        "risk_reasons": "、".join(risk_reasons),

        "sales_change": sales_change,
        "sales_change_rate": sales_change_rate,

        "inventory_change": inventory_change,
        "inventory_change_rate": inventory_change_rate,

        "expense_change_pp": expense_change,
    })


# ==================================================
# 6. 生成客户风险清单
# ==================================================

risk_df = pd.DataFrame(risk_records)

if not risk_df.empty:

    # 优先跟进的客户排在前面
    priority_order = {
        "优先跟进": 1,
        "重点关注": 2,
        "常规关注": 3,
    }

    risk_df["_priority_sort"] = (
        risk_df["follow_up_priority"].map(priority_order)
    )

    risk_df = risk_df.sort_values(
        by=["_priority_sort", "risk_signal_count"],
        ascending=[True, False],
    )

    risk_df = risk_df.drop(columns=["_priority_sort"])

# 输出结果
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

risk_df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig",
)


# ==================================================
# 7. 输出运行摘要
# ==================================================

print("=" * 55)
print("客户多指标交叉风险识别完成")
print("=" * 55)

print(f"参与分析的客户数：{risk_df['customer_id'].nunique()}")

print("\n风险等级统计：")

if not risk_df.empty:
    print(risk_df["risk_level"].value_counts())

    print("\n跟进优先级统计：")
    print(risk_df["follow_up_priority"].value_counts())

    print("\n同时出现销售下降和库存上升的客户数：")

    double_risk_count = (
        (risk_df["sales_drop"] == "是")
        & (risk_df["inventory_rise"] == "是")
    ).sum()

    print(double_risk_count)

    print("\n优先跟进客户：")

    print(
        risk_df[
            risk_df["follow_up_priority"] == "优先跟进"
        ][[
            "customer_id",
            "customer_name",
            "risk_signal_count",
            "risk_reasons",
        ]].to_string(index=False)
    )

else:
    print("当前没有识别到客户异常。")

print(f"\n结果文件：{OUTPUT_PATH}")
print("=" * 55)
