
from pathlib import Path
import json
import math

import numpy as np
import pandas as pd


# ============================================================
# 1. 路径配置
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_DIR / "reports"

OUTPUT_SUMMARY = REPORT_DIR / "business_diagnosis_summary.csv"
OUTPUT_FINDINGS = REPORT_DIR / "business_diagnosis_findings.csv"
OUTPUT_JSON = REPORT_DIR / "business_diagnosis.json"


# ============================================================
# 2. 通用数据处理函数
# ============================================================

def read_report(file_name):
    """读取已有分析报告，并检查文件是否存在。"""

    file_path = REPORT_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"找不到报告文件：{file_path}")

    return pd.read_csv(file_path)


def clean_value(value):
    """
    将 Pandas / NumPy 数据类型转换为标准 Python 类型，
    同时处理 NaN、None 和无穷值。
    """

    if value is None:
        return None

    if isinstance(value, dict):
        return {
            key: clean_value(val)
            for key, val in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [clean_value(val) for val in value]

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.bool_,)):
        return bool(value)

    if isinstance(value, (np.floating, float)):
        value = float(value)

        if not math.isfinite(value):
            return None

        return value

    if pd.isna(value):
        return None

    return value


def clean_records(df):
    """将 DataFrame 转换为可以安全写入 JSON 的记录。"""

    records = df.to_dict(orient="records")

    return [
        {
            key: clean_value(value)
            for key, value in record.items()
        }
        for record in records
    ]


def add_finding(
    findings,
    category,
    finding,
    entity,
    metric,
    value,
    evidence,
    priority,
    entity_id=None
):
    """统一记录经营发现，并保留主体ID。"""

    findings.append({
        "category": category,
        "finding": finding,
        "entity": str(entity),
        "entity_id": (
            str(entity_id)
            if entity_id is not None
            else None
        ),
        "metric": metric,
        "value": clean_value(value),
        "evidence": evidence,
        "priority": priority
    })


def check_required_columns(df, required_columns, file_name):
    """检查报告是否包含必要字段。"""

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{file_name} 缺少必要字段：{missing_columns}"
        )


def convert_numeric(df, columns, file_name):
    """统一转换数值字段，并检查转换失败的数据。"""

    for col in columns:

        if col not in df.columns:
            raise ValueError(
                f"{file_name} 缺少数值字段：{col}"
            )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        if df[col].isna().any():
            raise ValueError(
                f"{file_name} 的字段 {col} 存在空值或非数值数据。"
            )

        if not np.isfinite(df[col]).all():
            raise ValueError(
                f"{file_name} 的字段 {col} 存在无穷值。"
            )


def get_product_priority(total_effect_pp):
    """
    根据产品毛利率总影响绝对值划分优先级。

    初始规则：
    >= 0.30个百分点：高
    >= 0.10个百分点：关注
    < 0.10个百分点：常规
    """

    impact = abs(float(total_effect_pp))

    if impact >= 0.30:
        return "高"

    elif impact >= 0.10:
        return "关注"

    else:
        return "常规"


# ============================================================
# 3. 读取已有分析结果
# ============================================================

print("开始读取已有分析报告...")

region_df = read_report("region_performance.csv")
customer_df = read_report("customer_analysis.csv")
growth_df = read_report("customer_growth_contribution.csv")
decline_df = read_report("customer_decline_contribution.csv")
product_df = read_report("product_profitability.csv")
bridge_df = read_report("gross_margin_bridge.csv")
anomaly_df = read_report("anomaly_detection.csv")
risk_df = read_report("customer_risk_assessment.csv")
quality_df = read_report("data_quality_check.csv")
reconciliation_df = read_report("customer_reconciliation.csv")

print("报告读取完成。")


# ============================================================
# 4. 基础字段检查
# ============================================================

check_required_columns(
    region_df,
    [
        "month",
        "sales_amount",
        "target_amount",
        "gross_profit"
    ],
    "region_performance.csv"
)

check_required_columns(
    customer_df,
    [
        "customer_id",
        "customer_name",
        "sales_amount",
        "target_amount",
        "gross_profit"
    ],
    "customer_analysis.csv"
)

check_required_columns(
    growth_df,
    [
        "customer_id",
        "customer_name",
        "sales_aug",
        "sales_sep",
        "sales_change",
        "growth_contribution"
    ],
    "customer_growth_contribution.csv"
)

check_required_columns(
    decline_df,
    [
        "customer_id",
        "customer_name",
        "sales_aug",
        "sales_sep",
        "sales_change",
        "decline_contribution"
    ],
    "customer_decline_contribution.csv"
)

check_required_columns(
    product_df,
    [
        "product_id",
        "product_name",
        "sales_aug",
        "sales_sep",
        "sales_change"
    ],
    "product_profitability.csv"
)

check_required_columns(
    bridge_df,
    [
        "product_id",
        "product_name",
        "sales_share_aug",
        "sales_share_sep",
        "gross_margin_aug",
        "gross_margin_sep",
        "mix_effect",
        "margin_effect",
        "total_effect"
    ],
    "gross_margin_bridge.csv"
)

check_required_columns(
    risk_df,
    [
        "customer_id",
        "customer_name",
        "risk_level",
        "follow_up_priority",
        "risk_reasons"
    ],
    "customer_risk_assessment.csv"
)

check_required_columns(
    reconciliation_df,
    ["差异"],
    "customer_reconciliation.csv"
)


# ============================================================
# 5. 大区整体经营表现
# ============================================================

region_df["month_date"] = pd.to_datetime(
    region_df["month"],
    format="%b-%y",
    errors="coerce"
)

if region_df["month_date"].isna().any():
    raise ValueError("大区经营数据存在无法识别的月份。")

region_df = region_df.sort_values(
    "month_date"
).reset_index(drop=True)

if len(region_df) < 2:
    raise ValueError(
        "大区经营数据不足两个月，无法进行环比分析。"
    )

convert_numeric(
    region_df,
    [
        "sales_amount",
        "target_amount",
        "gross_profit"
    ],
    "region_performance.csv"
)

previous_region = region_df.iloc[-2]
current_region = region_df.iloc[-1]

previous_month = str(previous_region["month"])
current_month = str(current_region["month"])

previous_sales = float(
    previous_region["sales_amount"]
)

current_sales = float(
    current_region["sales_amount"]
)

previous_profit = float(
    previous_region["gross_profit"]
)

current_profit = float(
    current_region["gross_profit"]
)

previous_target = float(
    previous_region["target_amount"]
)

current_target = float(
    current_region["target_amount"]
)

# 使用毛利额 / 销售额计算精确毛利率
previous_margin = (
    previous_profit / previous_sales
    if previous_sales != 0
    else None
)

current_margin = (
    current_profit / current_sales
    if current_sales != 0
    else None
)

sales_change = current_sales - previous_sales

sales_growth_rate = (
    sales_change / previous_sales
    if previous_sales != 0
    else None
)

profit_change = current_profit - previous_profit

achievement_rate = (
    current_sales / current_target
    if current_target != 0
    else None
)

margin_change_pp = (
    (current_margin - previous_margin) * 100
    if previous_margin is not None
    and current_margin is not None
    else None
)

print("大区经营表现提取完成。")


# ============================================================
# 6. 客户销售增长与下降贡献
# ============================================================

convert_numeric(
    growth_df,
    [
        "sales_aug",
        "sales_sep",
        "sales_change",
        "growth_contribution"
    ],
    "customer_growth_contribution.csv"
)

convert_numeric(
    decline_df,
    [
        "sales_aug",
        "sales_sep",
        "sales_change",
        "decline_contribution"
    ],
    "customer_decline_contribution.csv"
)

top_growth = (
    growth_df[
        growth_df["sales_change"] > 0
    ]
    .sort_values(
        "sales_change",
        ascending=False
    )
    .head(5)
)

top_decline = (
    decline_df[
        decline_df["sales_change"] < 0
    ]
    .sort_values(
        "decline_contribution",
        ascending=False
    )
    .head(5)
)


# ============================================================
# 7. 客户汇总与大区汇总核对
# ============================================================

reconciliation_df["差异"] = pd.to_numeric(
    reconciliation_df["差异"],
    errors="coerce"
)

if reconciliation_df["差异"].isna().any():
    raise ValueError(
        "客户汇总核对文件中的差异字段存在非数值。"
    )

reconciliation_passed = bool(
    (reconciliation_df["差异"].abs() < 0.01).all()
)

customer_df["sales_amount"] = pd.to_numeric(
    customer_df["sales_amount"],
    errors="coerce"
)

customer_df["gross_profit"] = pd.to_numeric(
    customer_df["gross_profit"],
    errors="coerce"
)

customer_df["target_amount"] = pd.to_numeric(
    customer_df["target_amount"],
    errors="coerce"
)

customer_sales_total = customer_df["sales_amount"].sum()
customer_profit_total = customer_df["gross_profit"].sum()
customer_target_total = customer_df["target_amount"].sum()

customer_weighted_margin = (
    customer_profit_total / customer_sales_total
    if customer_sales_total != 0
    else None
)

customer_total_achievement = (
    customer_sales_total / customer_target_total
    if customer_target_total != 0
    else None
)


# ============================================================
# 8. 产品销售变化与毛利率归因
# ============================================================

convert_numeric(
    product_df,
    [
        "sales_aug",
        "sales_sep",
        "sales_change"
    ],
    "product_profitability.csv"
)

product_df["product_id"] = (
    product_df["product_id"].astype(str)
)

bridge_df["product_id"] = (
    bridge_df["product_id"].astype(str)
)

# 8.1 产品销售增长与下降

top_product_growth = (
    product_df[
        product_df["sales_change"] > 0
    ]
    .sort_values(
        "sales_change",
        ascending=False
    )
    .head(5)
)

top_product_decline = (
    product_df[
        product_df["sales_change"] < 0
    ]
    .sort_values(
        "sales_change",
        ascending=True
    )
    .head(5)
)


# 8.2 读取产品级毛利率归因结果

bridge_numeric_columns = [
    "sales_share_aug",
    "sales_share_sep",
    "gross_margin_aug",
    "gross_margin_sep",
    "mix_effect",
    "margin_effect",
    "total_effect"
]

convert_numeric(
    bridge_df,
    bridge_numeric_columns,
    "gross_margin_bridge.csv"
)


# 8.3 将归因结果转换为百分点

bridge_df["mix_effect_pp"] = (
    bridge_df["mix_effect"] * 100
)

bridge_df["margin_effect_pp"] = (
    bridge_df["margin_effect"] * 100
)

bridge_df["total_effect_pp"] = (
    bridge_df["total_effect"] * 100
)

bridge_df["sales_share_change_pp"] = (
    bridge_df["sales_share_sep"]
    - bridge_df["sales_share_aug"]
) * 100


# 8.4 判断产品毛利率是否具备可比性

has_sales_both_months = (
    (bridge_df["sales_share_aug"] > 0)
    & (bridge_df["sales_share_sep"] > 0)
)

bridge_df["gross_margin_change_pp"] = (
    bridge_df["gross_margin_sep"]
    - bridge_df["gross_margin_aug"]
) * 100

bridge_df.loc[
    ~has_sales_both_months,
    "gross_margin_change_pp"
] = np.nan

bridge_df["margin_diagnosable"] = (
    has_sales_both_months
)


# 8.5 构建业务诊断口径

# 原始归因字段不修改，保留原始计算结果。
# 对单月无销售产品：
# 将其归因总影响全部归入结构/销售组合效应，
# 不将技术填充的0解释为真实自身毛利率变化。

bridge_df["diagnosis_mix_effect_pp"] = (
    bridge_df["mix_effect_pp"]
)

bridge_df["diagnosis_margin_effect_pp"] = (
    bridge_df["margin_effect_pp"]
)

not_comparable = ~bridge_df["margin_diagnosable"]

bridge_df.loc[
    not_comparable,
    "diagnosis_mix_effect_pp"
] = bridge_df.loc[
    not_comparable,
    "total_effect_pp"
]

bridge_df.loc[
    not_comparable,
    "diagnosis_margin_effect_pp"
] = 0

bridge_df["diagnosis_total_effect_pp"] = (
    bridge_df["diagnosis_mix_effect_pp"]
    + bridge_df["diagnosis_margin_effect_pp"]
)


# 校验：每个产品调整前后的总影响必须一致

if not np.allclose(
    bridge_df["diagnosis_total_effect_pp"],
    bridge_df["total_effect_pp"],
    atol=1e-8
):
    raise ValueError(
        "产品归因调整后总影响不一致，请检查。"
    )


# 8.6 产品影响类型判断

def classify_product_impact(row):

    mix = row["diagnosis_mix_effect_pp"]
    margin = row["diagnosis_margin_effect_pp"]

    epsilon = 1e-9

    mix_positive = mix > epsilon
    mix_negative = mix < -epsilon

    margin_positive = margin > epsilon
    margin_negative = margin < -epsilon

    if mix_negative and margin_negative:
        return "双重拖累"

    elif mix_positive and margin_positive:
        return "双重正向"

    elif mix_negative and margin_positive:
        return "结构负向、自身毛利率正向抵消"

    elif mix_positive and margin_negative:
        return "结构正向、自身毛利率负向抵消"

    elif mix_negative:
        if not row["margin_diagnosable"]:
            return "结构/销售组合负向，毛利率不可比"

        return "主要由产品结构拖累"

    elif margin_negative:
        return "主要由自身毛利率拖累"

    elif mix_positive:
        if not row["margin_diagnosable"]:
            return "结构/销售组合正向，毛利率不可比"

        return "主要由产品结构带来正向贡献"

    elif margin_positive:
        return "主要由自身毛利率带来正向贡献"

    else:
        return "影响不明显"


bridge_df["impact_type"] = bridge_df.apply(
    classify_product_impact,
    axis=1
)


# 8.7 产品销售状态

bridge_df["product_status"] = "正常销售"

bridge_df.loc[
    bridge_df["sales_share_sep"] == 0,
    "product_status"
] = "9月无销售，毛利率不可观察"

bridge_df.loc[
    bridge_df["sales_share_aug"] == 0,
    "product_status"
] = "8月无销售，毛利率不可观察"

bridge_df.loc[
    (bridge_df["sales_share_aug"] == 0)
    & (bridge_df["sales_share_sep"] == 0),
    "product_status"
] = "两个月均无销售，需检查数据"


# 8.8 产品优先级

bridge_df["product_priority"] = (
    bridge_df["diagnosis_total_effect_pp"]
    .apply(get_product_priority)
)


# 8.9 提取重点产品

# 整体毛利率负向影响 TOP5

top_product_margin_negative = (
    bridge_df[
        bridge_df["diagnosis_total_effect_pp"] < 0
    ]
    .sort_values(
        "diagnosis_total_effect_pp",
        ascending=True
    )
    .head(5)
)


# 产品结构效应拖累 TOP5

top_product_mix_drag = (
    bridge_df[
        bridge_df["diagnosis_mix_effect_pp"] < 0
    ]
    .sort_values(
        "diagnosis_mix_effect_pp",
        ascending=True
    )
    .head(5)
)


# 产品自身毛利率效应拖累 TOP5
# 只保留两个月均有销售的产品

top_product_margin_drag = (
    bridge_df[
        (bridge_df["diagnosis_margin_effect_pp"] < 0)
        & bridge_df["margin_diagnosable"]
    ]
    .sort_values(
        "diagnosis_margin_effect_pp",
        ascending=True
    )
    .head(5)
)


# 双重拖累产品
# 必须具备真实的毛利率可比性

double_negative_products = (
    bridge_df[
        (bridge_df["diagnosis_mix_effect_pp"] < 0)
        & (bridge_df["diagnosis_margin_effect_pp"] < 0)
        & bridge_df["margin_diagnosable"]
    ]
    .sort_values(
        "diagnosis_total_effect_pp",
        ascending=True
    )
)


# 整体毛利率正向贡献 TOP5

top_product_margin_positive = (
    bridge_df[
        bridge_df["diagnosis_total_effect_pp"] > 0
    ]
    .sort_values(
        "diagnosis_total_effect_pp",
        ascending=False
    )
    .head(5)
)


# 当月无销售产品

no_sales_products = bridge_df[
    bridge_df["sales_share_sep"] == 0
].copy()


# 8.10 汇总整体产品结构效应和自身毛利率效应

mix_effect_pp = float(
    bridge_df["diagnosis_mix_effect_pp"].sum()
)

margin_effect_pp = float(
    bridge_df["diagnosis_margin_effect_pp"].sum()
)

total_margin_effect_pp = (
    mix_effect_pp + margin_effect_pp
)

# 转回小数形式，方便保留原始变量结构

mix_effect = mix_effect_pp / 100
margin_effect = margin_effect_pp / 100
total_margin_effect = total_margin_effect_pp / 100


print("客户和产品分析结果提取完成。")


# ============================================================
# 9. 客户风险汇总
# ============================================================

high_risk_count = int(
    (risk_df["risk_level"] == "高风险").sum()
)

medium_risk_count = int(
    (risk_df["risk_level"] == "中风险").sum()
)

priority_customer_df = risk_df[
    risk_df["follow_up_priority"] == "优先跟进"
].copy()

focus_customer_df = risk_df[
    risk_df["follow_up_priority"] == "重点关注"
].copy()

routine_customer_df = risk_df[
    risk_df["follow_up_priority"] == "常规关注"
].copy()

other_high_risk = risk_df[
    (risk_df["risk_level"] == "高风险")
    & (risk_df["follow_up_priority"] != "优先跟进")
].copy()

print("客户风险汇总完成。")


# ============================================================
# 10. 构建经营摘要
# ============================================================

summary = [

    {
        "metric": "分析期间",
        "value": f"{previous_month} vs {current_month}",
        "description": "本次经营诊断的环比分析期间"
    },

    {
        "metric": "本月销售额",
        "value": current_sales,
        "description": "最近月份的大区销售额"
    },

    {
        "metric": "销售额环比变化",
        "value": sales_change,
        "description": "本月销售额减去上月销售额"
    },

    {
        "metric": "销售额环比增长率",
        "value": sales_growth_rate,
        "description": "销售额环比变化额除以上月销售额"
    },

    {
        "metric": "本月目标达成率",
        "value": achievement_rate,
        "description": "本月销售额除以本月目标额"
    },

    {
        "metric": "本月毛利额",
        "value": current_profit,
        "description": "最近月份的大区毛利额"
    },

    {
        "metric": "毛利额环比变化",
        "value": profit_change,
        "description": "本月毛利额减去上月毛利额"
    },

    {
        "metric": "本月毛利率",
        "value": current_margin,
        "description": "最近月份的大区整体毛利率"
    },

    {
        "metric": "毛利率环比变化（百分点）",
        "value": margin_change_pp,
        "description": "本月毛利率减去上月毛利率"
    },

    {
        "metric": "客户加权毛利率",
        "value": customer_weighted_margin,
        "description": "客户汇总毛利额除以客户汇总销售额"
    },

    {
        "metric": "客户汇总目标达成率",
        "value": customer_total_achievement,
        "description": "客户汇总销售额除以客户汇总目标额"
    },

    {
        "metric": "产品结构效应（百分点）",
        "value": mix_effect_pp,
        "description": "按业务诊断口径计算的产品结构/销售组合效应"
    },

    {
        "metric": "产品自身毛利率效应（百分点）",
        "value": margin_effect_pp,
        "description": "仅对两个月均有销售的产品解释真实毛利率变化"
    },

    {
        "metric": "毛利率归因合计（百分点）",
        "value": total_margin_effect_pp,
        "description": "产品结构效应与自身毛利率效应之和"
    },

    {
        "metric": "高风险客户数",
        "value": high_risk_count,
        "description": "风险评估结果中的高风险客户数量"
    },

    {
        "metric": "中风险客户数",
        "value": medium_risk_count,
        "description": "风险评估结果中的中风险客户数量"
    },

    {
        "metric": "优先跟进客户数",
        "value": int(len(priority_customer_df)),
        "description": "销售下降且库存上升的优先跟进客户数量"
    },

    {
        "metric": "重点关注客户数",
        "value": int(len(focus_customer_df)),
        "description": "其他需要重点关注的客户数量"
    },

    {
        "metric": "数据质量检查表数量",
        "value": int(len(quality_df)),
        "description": "本次数据质量检查覆盖的表数量"
    },

    {
        "metric": "客户与大区汇总核对",
        "value": "通过" if reconciliation_passed else "未通过",
        "description": "客户汇总与大区汇总差异是否小于0.01"
    }

]

summary_df = pd.DataFrame(summary)


# ============================================================
# 11. 提炼经营发现
# ============================================================

findings = []


# ------------------------------------------------------------
# 11.1 大区销售表现
# ------------------------------------------------------------

if sales_growth_rate is not None:

    add_finding(
        findings,
        "整体经营",
        "大区销售额环比变化",
        "大区",
        "销售额环比增长率",
        round(sales_growth_rate * 100, 2),

        (
            f"上月销售额：{previous_sales:.2f}；"
            f"本月销售额：{current_sales:.2f}；"
            f"变化额：{sales_change:.2f}"
        ),

        "高" if sales_growth_rate < -0.10 else "常规",
        entity_id="REGION"
    )


# ------------------------------------------------------------
# 11.2 销售增长贡献客户
# ------------------------------------------------------------

for _, row in top_growth.iterrows():

    add_finding(
        findings,
        "客户销售增长",
        "主要销售增长贡献客户",
        row["customer_name"],
        "销售额变化",
        round(float(row["sales_change"]), 2),

        (
            f"{previous_month}销售额：{row['sales_aug']:.2f}；"
            f"{current_month}销售额：{row['sales_sep']:.2f}；"
            f"增长贡献：{row['growth_contribution']:.2%}"
        ),

        "关注",
        entity_id=row["customer_id"]
    )


# ------------------------------------------------------------
# 11.3 销售下降贡献客户
# ------------------------------------------------------------

for _, row in top_decline.iterrows():

    add_finding(
        findings,
        "客户销售下降",
        "主要销售下降拖累客户",
        row["customer_name"],
        "销售额变化",
        round(float(row["sales_change"]), 2),

        (
            f"{previous_month}销售额：{row['sales_aug']:.2f}；"
            f"{current_month}销售额：{row['sales_sep']:.2f}；"
            f"下降贡献：{row['decline_contribution']:.2%}"
        ),

        "高",
        entity_id=row["customer_id"]
    )


# ------------------------------------------------------------
# 11.4 产品销售增长
# ------------------------------------------------------------

for _, row in top_product_growth.iterrows():

    add_finding(
        findings,
        "产品销售增长",
        "主要销售增长产品",
        row["product_name"],
        "销售额变化",
        round(float(row["sales_change"]), 2),

        (
            f"{previous_month}销售额：{row['sales_aug']:.2f}；"
            f"{current_month}销售额：{row['sales_sep']:.2f}"
        ),

        "关注",
        entity_id=row["product_id"]
    )


# ------------------------------------------------------------
# 11.5 产品销售下降
# ------------------------------------------------------------

for _, row in top_product_decline.iterrows():

    add_finding(
        findings,
        "产品销售下降",
        "主要销售下降产品",
        row["product_name"],
        "销售额变化",
        round(float(row["sales_change"]), 2),

        (
            f"{previous_month}销售额：{row['sales_aug']:.2f}；"
            f"{current_month}销售额：{row['sales_sep']:.2f}"
        ),

        "关注",
        entity_id=row["product_id"]
    )


# ------------------------------------------------------------
# 11.6 整体毛利率归因
# ------------------------------------------------------------

add_finding(
    findings,
    "盈利分析",
    "产品结构/销售组合效应",
    "整体产品组合",
    "毛利率影响（百分点）",
    round(mix_effect_pp, 4),

    (
        "按业务诊断口径，将单月无销售产品的归因总影响"
        "归入结构/销售组合效应。"
    ),

    "高" if mix_effect_pp < -0.10 else "关注",
    entity_id="PRODUCT_PORTFOLIO"
)

add_finding(
    findings,
    "盈利分析",
    "产品自身毛利率效应",
    "整体产品组合",
    "毛利率影响（百分点）",
    round(margin_effect_pp, 4),

    (
        "仅对两个月均有销售的产品解释自身毛利率变化；"
        "无销售月份不视为真实毛利率0%。"
    ),

    "高" if margin_effect_pp < -0.10 else "关注",
    entity_id="PRODUCT_PORTFOLIO"
)


# ------------------------------------------------------------
# 11.7 产品整体毛利率影响 TOP5
# ------------------------------------------------------------

for _, row in top_product_margin_negative.iterrows():

    add_finding(
        findings,
        "产品毛利率归因",
        "整体毛利率主要拖累产品",
        row["product_name"],
        "毛利率影响（百分点）",
        round(float(row["diagnosis_total_effect_pp"]), 4),

        (
            f"结构/销售组合效应："
            f"{row['diagnosis_mix_effect_pp']:.4f}个百分点；"
            f"自身毛利率效应："
            f"{row['diagnosis_margin_effect_pp']:.4f}个百分点；"
            f"影响类型：{row['impact_type']}"
        ),

        row["product_priority"],
        entity_id=row["product_id"]
    )


# ------------------------------------------------------------
# 11.8 产品结构效应拖累 TOP5
# ------------------------------------------------------------

for _, row in top_product_mix_drag.iterrows():

    add_finding(
        findings,
        "产品结构分析",
        "产品结构变化造成毛利率拖累",
        row["product_name"],
        "产品结构/销售组合效应（百分点）",
        round(float(row["diagnosis_mix_effect_pp"]), 4),

        (
            f"{previous_month}销售占比："
            f"{row['sales_share_aug']:.2%}；"
            f"{current_month}销售占比："
            f"{row['sales_share_sep']:.2%}；"
            f"自身毛利率效应："
            f"{row['diagnosis_margin_effect_pp']:.4f}个百分点；"
            f"产品状态：{row['product_status']}"
        ),

        row["product_priority"],
        entity_id=row["product_id"]
    )


# ------------------------------------------------------------
# 11.9 产品自身毛利率效应拖累 TOP5
# ------------------------------------------------------------

for _, row in top_product_margin_drag.iterrows():

    add_finding(
        findings,
        "产品盈利分析",
        "产品自身毛利率下降造成拖累",
        row["product_name"],
        "自身毛利率效应（百分点）",
        round(float(row["diagnosis_margin_effect_pp"]), 4),

        (
            f"{previous_month}产品毛利率："
            f"{row['gross_margin_aug']:.2%}；"
            f"{current_month}产品毛利率："
            f"{row['gross_margin_sep']:.2%}；"
            f"毛利率实际变化："
            f"{row['gross_margin_change_pp']:.4f}个百分点；"
            f"结构效应："
            f"{row['diagnosis_mix_effect_pp']:.4f}个百分点"
        ),

        row["product_priority"],
        entity_id=row["product_id"]
    )


# ------------------------------------------------------------
# 11.10 产品结构与自身毛利率双重拖累
# ------------------------------------------------------------

for _, row in double_negative_products.iterrows():

    add_finding(
        findings,
        "产品盈利风险",
        "产品结构与自身毛利率双重拖累",
        row["product_name"],
        "毛利率总影响（百分点）",
        round(float(row["diagnosis_total_effect_pp"]), 4),

        (
            f"结构效应："
            f"{row['diagnosis_mix_effect_pp']:.4f}个百分点；"
            f"自身毛利率效应："
            f"{row['diagnosis_margin_effect_pp']:.4f}个百分点；"
            f"毛利率总影响："
            f"{row['diagnosis_total_effect_pp']:.4f}个百分点"
        ),

        row["product_priority"],
        entity_id=row["product_id"]
    )


# ------------------------------------------------------------
# 11.11 产品正向贡献 TOP5
# ------------------------------------------------------------

for _, row in top_product_margin_positive.iterrows():

    add_finding(
        findings,
        "产品毛利率改善",
        "产品对整体毛利率形成正向贡献",
        row["product_name"],
        "毛利率影响（百分点）",
        round(float(row["diagnosis_total_effect_pp"]), 4),

        (
            f"结构效应："
            f"{row['diagnosis_mix_effect_pp']:.4f}个百分点；"
            f"自身毛利率效应："
            f"{row['diagnosis_margin_effect_pp']:.4f}个百分点；"
            f"影响类型：{row['impact_type']}"
        ),

        "关注",
        entity_id=row["product_id"]
    )


# ------------------------------------------------------------
# 11.12 当月无销售产品
# ------------------------------------------------------------

for _, row in no_sales_products.iterrows():

    add_finding(
        findings,
        "产品销售状态",
        "当月无销售，需核查产品状态",
        row["product_name"],
        f"{current_month}销售占比",
        0,

        (
            f"{previous_month}销售占比："
            f"{row['sales_share_aug']:.2%}；"
            f"{current_month}无销售；"
            f"产品毛利率不可观察；"
            f"归因总影响："
            f"{row['diagnosis_total_effect_pp']:.4f}个百分点。"
            f"不能将技术填充的0解释为真实毛利率下降。"
        ),

        "常规",
        entity_id=row["product_id"]
    )


# ------------------------------------------------------------
# 11.13 优先跟进客户
# ------------------------------------------------------------

for _, row in priority_customer_df.iterrows():

    add_finding(
        findings,
        "客户风险",
        "销售下降且库存上升",
        row["customer_name"],
        "风险等级",
        row["risk_level"],
        row["risk_reasons"],
        "高",
        entity_id=row["customer_id"]
    )


# ------------------------------------------------------------
# 11.14 其他高风险客户
# ------------------------------------------------------------

for _, row in other_high_risk.iterrows():

    add_finding(
        findings,
        "客户风险",
        "存在多项经营风险信号",
        row["customer_name"],
        "风险等级",
        row["risk_level"],
        row["risk_reasons"],
        "高",
        entity_id=row["customer_id"]
    )


findings_df = pd.DataFrame(findings)


# ============================================================
# 12. 构建产品主体级诊断
# ============================================================

# 同一个产品的销售表现、结构效应、自身毛利率效应
# 整合到同一条产品记录中，方便 AI 综合分析。

product_sales_map = (
    product_df
    .drop_duplicates(subset=["product_id"])
    .set_index("product_id")["sales_change"]
    .to_dict()
)

product_entity_diagnosis = []

for _, row in bridge_df.iterrows():

    product_id = str(row["product_id"])

    sales_change_value = product_sales_map.get(
        product_id,
        None
    )

    if not row["margin_diagnosable"]:
        margin_change_value = None
    else:
        margin_change_value = clean_value(
            row["gross_margin_change_pp"]
        )

    product_entity_diagnosis.append({

        "product_id": product_id,

        "product_name": row["product_name"],

        "sales_change": clean_value(
            sales_change_value
        ),

        "sales_share_aug": clean_value(
            row["sales_share_aug"]
        ),

        "sales_share_sep": clean_value(
            row["sales_share_sep"]
        ),

        "sales_share_change_pp": clean_value(
            row["sales_share_change_pp"]
        ),

        "mix_effect_pp": clean_value(
            row["diagnosis_mix_effect_pp"]
        ),

        "margin_effect_pp": clean_value(
            row["diagnosis_margin_effect_pp"]
        ),

        "total_effect_pp": clean_value(
            row["diagnosis_total_effect_pp"]
        ),

        "gross_margin_change_pp": margin_change_value,

        "margin_diagnosable": bool(
            row["margin_diagnosable"]
        ),

        "impact_type": row["impact_type"],

        "product_status": row["product_status"],

        "product_priority": row["product_priority"]

    })


# ============================================================
# 13. 构建客户主体级诊断
# ============================================================

customer_entity_diagnosis = []

for _, row in risk_df.iterrows():

    customer_entity_diagnosis.append({

        "customer_id": str(row["customer_id"]),

        "customer_name": row["customer_name"],

        "risk_level": row["risk_level"],

        "follow_up_priority": row["follow_up_priority"],

        "risk_signal_count": clean_value(
            row.get("risk_signal_count")
        ),

        "risk_reasons": row["risk_reasons"],

        "sales_change": clean_value(
            row.get("sales_change")
        ),

        "sales_change_rate": clean_value(
            row.get("sales_change_rate")
        ),

        "inventory_change": clean_value(
            row.get("inventory_change")
        ),

        "inventory_change_rate": clean_value(
            row.get("inventory_change_rate")
        ),

        "expense_change_pp": clean_value(
            row.get("expense_change_pp")
        )

    })


# ============================================================
# 14. 综合诊断结果校验
# ============================================================

print("\n开始进行综合诊断结果校验...")


# 14.1 产品归因总影响校验

assert np.allclose(
    bridge_df["diagnosis_total_effect_pp"].sum(),
    total_margin_effect_pp,
    atol=1e-8
), "产品归因汇总与整体归因不一致！"


# 14.2 原始归因总影响与诊断归因总影响校验

assert np.allclose(
    bridge_df["total_effect_pp"],
    bridge_df["diagnosis_total_effect_pp"],
    atol=1e-8
), "产品级归因调整前后总影响不一致！"


# 14.3 整体毛利率变化与归因合计校验

if margin_change_pp is not None:

    if abs(
        margin_change_pp - total_margin_effect_pp
    ) >= 0.01:

        raise ValueError(
            "整体毛利率变化与归因结果不一致！"
            f"毛利率变化：{margin_change_pp:.4f}；"
            f"归因合计：{total_margin_effect_pp:.4f}"
        )


# 14.4 无销售产品不得进入自身毛利率拖累榜单

assert bridge_df.loc[
    top_product_margin_drag.index,
    "margin_diagnosable"
].all(), "无销售产品进入自身毛利率拖累榜单！"


# 14.5 无销售产品不得进入双重拖累榜单

assert bridge_df.loc[
    double_negative_products.index,
    "margin_diagnosable"
].all(), "无销售产品进入双重拖累榜单！"


# 14.6 客户与大区汇总核对

if not reconciliation_passed:

    raise ValueError(
        "客户汇总与大区汇总核对未通过，请先检查数据。"
    )


print("综合诊断结果校验通过！")


# ============================================================
# 15. 生成JSON，供下一阶段AI模块使用
# ============================================================

diagnosis_result = {

    # --------------------------------------------------------
    # 分析期间
    # --------------------------------------------------------

    "analysis_period": {

        "previous_month": previous_month,

        "current_month": current_month

    },


    # --------------------------------------------------------
    # 整体经营表现
    # --------------------------------------------------------

    "overall_performance": {

        "previous_sales": previous_sales,

        "current_sales": current_sales,

        "sales_change": sales_change,

        "sales_growth_rate": sales_growth_rate,

        "achievement_rate": achievement_rate,

        "previous_gross_profit": previous_profit,

        "current_gross_profit": current_profit,

        "gross_profit_change": profit_change,

        "previous_gross_margin": previous_margin,

        "current_gross_margin": current_margin,

        "gross_margin_change_pp": margin_change_pp

    },


    # --------------------------------------------------------
    # 客户经营表现
    # --------------------------------------------------------

    "customer_performance": {

        "customer_count": int(len(customer_df)),

        "weighted_gross_margin": customer_weighted_margin,

        "total_achievement_rate": customer_total_achievement,

        "top_growth_customers": clean_records(
            top_growth
        ),

        "top_decline_customers": clean_records(
            top_decline
        ),

        "customer_entity_diagnosis": (
            customer_entity_diagnosis
        )

    },


    # --------------------------------------------------------
    # 产品经营表现
    # --------------------------------------------------------

    "product_performance": {

        "top_growth_products": clean_records(
            top_product_growth
        ),

        "top_decline_products": clean_records(
            top_product_decline
        ),

        "mix_effect_pp": mix_effect_pp,

        "margin_effect_pp": margin_effect_pp,

        "total_margin_effect_pp": total_margin_effect_pp,


        # 产品级毛利率归因

        "product_margin_diagnosis": {

            "negative_impact_top5": clean_records(
                top_product_margin_negative[
                    [
                        "product_id",
                        "product_name",
                        "diagnosis_mix_effect_pp",
                        "diagnosis_margin_effect_pp",
                        "diagnosis_total_effect_pp",
                        "impact_type",
                        "product_priority",
                        "product_status"
                    ]
                ]
            ),


            "mix_drag_top5": clean_records(
                top_product_mix_drag[
                    [
                        "product_id",
                        "product_name",
                        "diagnosis_mix_effect_pp",
                        "diagnosis_margin_effect_pp",
                        "diagnosis_total_effect_pp",
                        "sales_share_aug",
                        "sales_share_sep",
                        "impact_type",
                        "product_priority"
                    ]
                ]
            ),


            "margin_drag_top5": clean_records(
                top_product_margin_drag[
                    [
                        "product_id",
                        "product_name",
                        "diagnosis_mix_effect_pp",
                        "diagnosis_margin_effect_pp",
                        "diagnosis_total_effect_pp",
                        "gross_margin_aug",
                        "gross_margin_sep",
                        "gross_margin_change_pp",
                        "product_status",
                        "impact_type",
                        "product_priority"
                    ]
                ]
            ),


            "double_negative_products": clean_records(
                double_negative_products[
                    [
                        "product_id",
                        "product_name",
                        "diagnosis_mix_effect_pp",
                        "diagnosis_margin_effect_pp",
                        "diagnosis_total_effect_pp",
                        "impact_type",
                        "product_priority"
                    ]
                ]
            ),


            "positive_impact_top5": clean_records(
                top_product_margin_positive[
                    [
                        "product_id",
                        "product_name",
                        "diagnosis_mix_effect_pp",
                        "diagnosis_margin_effect_pp",
                        "diagnosis_total_effect_pp",
                        "impact_type",
                        "product_priority"
                    ]
                ]
            ),


            "no_sales_products": clean_records(
                no_sales_products[
                    [
                        "product_id",
                        "product_name",
                        "sales_share_aug",
                        "sales_share_sep",
                        "diagnosis_total_effect_pp",
                        "product_status"
                    ]
                ]
            ),


            # 所有产品主体级诊断
            "product_entity_diagnosis": (
                product_entity_diagnosis
            ),


            "product_count": int(len(bridge_df)),

            "negative_impact_count": int(
                (
                    bridge_df["diagnosis_total_effect_pp"] < 0
                ).sum()
            ),

            "positive_impact_count": int(
                (
                    bridge_df["diagnosis_total_effect_pp"] > 0
                ).sum()
            ),

            "double_negative_count": int(
                len(double_negative_products)
            ),

            "no_sales_count": int(
                len(no_sales_products)
            )

        }

    },


    # --------------------------------------------------------
    # 客户风险
    # --------------------------------------------------------

    "customer_risk": {

        "high_risk_count": high_risk_count,

        "medium_risk_count": medium_risk_count,

        "priority_follow_up_count": int(
            len(priority_customer_df)
        ),

        "focus_customer_count": int(
            len(focus_customer_df)
        ),

        "routine_customer_count": int(
            len(routine_customer_df)
        ),

        "priority_customers": clean_records(
            priority_customer_df
        ),

        "other_high_risk_customers": clean_records(
            other_high_risk
        )

    },


    # --------------------------------------------------------
    # 数据质量与核对
    # --------------------------------------------------------

    "data_checks": {

        "quality_check_table_count": int(
            len(quality_df)
        ),

        "customer_reconciliation_passed": bool(
            reconciliation_passed
        ),

        "anomaly_count": int(
            len(anomaly_df)
        )

    },


    # --------------------------------------------------------
    # 经营发现
    # --------------------------------------------------------

    "findings": clean_records(
        findings_df
    ),


    # --------------------------------------------------------
    # AI解读时需要遵守的诊断口径
    # --------------------------------------------------------

    "diagnosis_notes": {

        "finding_count": int(
            len(findings_df)
        ),

        "finding_count_is_unique_issue_count": False,

        "finding_explanation": (
            "同一个客户或产品可能出现在多个分析类别中，"
            "不同发现代表不同分析角度，"
            "不能直接将发现条数视为独立经营问题数量。"
        ),

        "product_margin_method": (
            "采用产品结构效应与产品自身毛利率效应"
            "进行对称分解。"
        ),

        "no_sales_product_warning": (
            "当月无销售产品的毛利率不可观察。"
            "对于单月无销售产品，业务诊断口径将其归因总影响"
            "全部归入结构/销售组合效应，自身毛利率效应不作解释。"
            "不得将技术填充的0解释为真实毛利率。"
        ),

        "priority_method": (
            "产品优先级根据毛利率总影响绝对值初步分级："
            "大于等于0.30个百分点为高，"
            "大于等于0.10个百分点且小于0.30个百分点为关注，"
            "小于0.10个百分点为常规。"
            "该规则为项目初始规则，不代表企业官方标准。"
        ),

        "risk_interpretation": (
            "销售下降与库存上升属于潜在库存压力信号，"
            "不能单独据此认定发生库存积压。"
            "实际经营原因仍需结合进货、出货、退货及终端动销核实。"
        ),

        "data_reconciliation": (
            "通过" if reconciliation_passed else "未通过"
        )

    }

}


# ============================================================
# 16. JSON序列化校验
# ============================================================

# 先进行一次内存序列化，确保不存在 NaN、Infinity 等非法值

json_output = json.dumps(
    clean_value(diagnosis_result),
    ensure_ascii=False,
    indent=4,
    allow_nan=False
)


# ============================================================
# 17. 输出文件
# ============================================================

summary_df.to_csv(
    OUTPUT_SUMMARY,
    index=False,
    encoding="utf-8-sig"
)

findings_df.to_csv(
    OUTPUT_FINDINGS,
    index=False,
    encoding="utf-8-sig"
)

with open(
    OUTPUT_JSON,
    "w",
    encoding="utf-8"
) as f:

    f.write(json_output)


# ============================================================
# 18. 输出运行结果
# ============================================================

print("\n" + "=" * 60)
print("综合经营诊断完成！")
print("=" * 60)

print(
    f"分析期间：{previous_month} 至 {current_month}"
)

print(
    f"销售额环比变化：{sales_growth_rate:.2%}"
    if sales_growth_rate is not None
    else "销售额环比变化：无法计算"
)

print(
    f"毛利率变化：{margin_change_pp:.2f} 个百分点"
    if margin_change_pp is not None
    else "毛利率变化：无法计算"
)

print(
    f"产品结构/销售组合效应："
    f"{mix_effect_pp:.4f} 个百分点"
)

print(
    f"产品自身毛利率效应："
    f"{margin_effect_pp:.4f} 个百分点"
)

print(
    f"毛利率归因合计："
    f"{total_margin_effect_pp:.4f} 个百分点"
)

print(f"高风险客户：{high_risk_count} 个")

print(
    f"优先跟进客户：{len(priority_customer_df)} 个"
)

print(
    f"重点关注客户：{len(focus_customer_df)} 个"
)

print(
    f"产品级诊断数量：{len(product_entity_diagnosis)} 个"
)

print(
    f"当月无销售产品：{len(no_sales_products)} 个"
)

print(
    f"经营发现：{len(findings_df)} 条"
)

print(
    f"客户与大区汇总核对："
    f"{'通过' if reconciliation_passed else '未通过'}"
)

print("\n输出文件：")

print(OUTPUT_SUMMARY)
print(OUTPUT_FINDINGS)
print(OUTPUT_JSON)

print("\n全部校验通过，JSON已成功生成。")
