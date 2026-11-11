
import pandas as pd
from pathlib import Path

# =====================================
# 1. 路径配置
# =====================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
REPORT_DIR = PROJECT_DIR / "reports"

INPUT_PATH = REPORT_DIR / "product_profitability.csv"
OUTPUT_PATH = REPORT_DIR / "gross_margin_bridge.csv"

# =====================================
# 2. 读取产品分析数据
# =====================================

if not INPUT_PATH.exists():
    raise FileNotFoundError(
        f"找不到文件：{INPUT_PATH}，请先运行 product_profitability.py"
    )

df = pd.read_csv(INPUT_PATH)

required_columns = [
    "product_id",
    "product_name",
    "sales_aug",
    "sales_sep",
    "gross_margin_aug",
    "gross_margin_sep",
    "sales_share_aug",
    "sales_share_sep"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"缺少必要字段：{missing_columns}")

# =====================================
# 3. 数据预处理
# =====================================

numeric_columns = [
    "sales_aug",
    "sales_sep",
    "gross_margin_aug",
    "gross_margin_sep",
    "sales_share_aug",
    "sales_share_sep"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 没有销售额的月份，销售占比为0
df[["sales_share_aug", "sales_share_sep"]] = (
    df[["sales_share_aug", "sales_share_sep"]].fillna(0)
)

# 某产品当月没有销售时，其毛利率在数学上没有定义。
# 为分解计算，将该月份的毛利率暂设为0。
df[["gross_margin_aug", "gross_margin_sep"]] = (
    df[["gross_margin_aug", "gross_margin_sep"]].fillna(0)
)

# =====================================
# 4. Shapley两因素分解
# =====================================

# 产品结构效应
# 销售占比变化 × 两期平均产品毛利率
df["mix_effect"] = (
    (df["sales_share_sep"] - df["sales_share_aug"])
    * (df["gross_margin_aug"] + df["gross_margin_sep"]) / 2
)

# 产品自身毛利率效应
# 产品毛利率变化 × 两期平均销售占比
df["margin_effect"] = (
    (df["gross_margin_sep"] - df["gross_margin_aug"])
    * (df["sales_share_aug"] + df["sales_share_sep"]) / 2
)

# 产品对整体毛利率变化的总影响
df["total_effect"] = (
    df["mix_effect"] + df["margin_effect"]
)

# =====================================
# 5. 计算大区整体毛利率变化
# =====================================

total_sales_aug = df["sales_aug"].sum()
total_sales_sep = df["sales_sep"].sum()

if total_sales_aug <= 0 or total_sales_sep <= 0:
    raise ValueError("8月或9月销售额合计小于等于0，无法计算毛利率。")

# 用产品销售额和产品毛利率还原大区毛利率
gm_aug = (
    df["sales_aug"] * df["gross_margin_aug"]
).sum() / total_sales_aug

gm_sep = (
    df["sales_sep"] * df["gross_margin_sep"]
).sum() / total_sales_sep

actual_gm_change = gm_sep - gm_aug

# 两项归因结果
total_mix_effect = df["mix_effect"].sum()
total_margin_effect = df["margin_effect"].sum()

explained_change = total_mix_effect + total_margin_effect

# =====================================
# 6. 数据校验
# =====================================

difference = actual_gm_change - explained_change

print("===== 毛利率归因校验 =====")
print(f"8月整体毛利率：{gm_aug:.2%}")
print(f"9月整体毛利率：{gm_sep:.2%}")
print(f"整体毛利率变化：{actual_gm_change * 100:.4f} 个百分点")

print(f"\n产品结构效应：{total_mix_effect * 100:.4f} 个百分点")
print(f"产品自身毛利率效应：{total_margin_effect * 100:.4f} 个百分点")
print(f"归因合计：{explained_change * 100:.4f} 个百分点")

print(f"\n归因校验差异：{difference * 100:.8f} 个百分点")

if abs(difference) <= 1e-8:
    print("校验通过：两项归因之和与整体毛利率变化一致。")
else:
    print("校验未通过：请检查产品销售占比和毛利率计算口径。")

# =====================================
# 7. 输出产品级归因明细
# =====================================

output_columns = [
    "product_id",
    "product_name",
    "sales_share_aug",
    "sales_share_sep",
    "gross_margin_aug",
    "gross_margin_sep",
    "mix_effect",
    "margin_effect",
    "total_effect"
]

result = df[output_columns].copy()

# 按对整体毛利率影响的绝对值排序
result["abs_total_effect"] = result["total_effect"].abs()

result = result.sort_values(
    by="abs_total_effect",
    ascending=False
)

result = result.drop(columns=["abs_total_effect"])

result.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print(f"\n归因明细已保存：{OUTPUT_PATH}")
