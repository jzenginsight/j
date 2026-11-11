
import pandas as pd
from pathlib import Path

# 1. 定位项目路径
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
REPORT_DIR = PROJECT_DIR / "reports"

# 2. 读取数据
customer = pd.read_csv(
    REPORT_DIR / "customer_growth_analysis.csv"
)

region = pd.read_csv(
    REPORT_DIR / "region_performance.csv"
)

# 3. 正确解析月份
# %b：英文月份缩写，例如 Aug
# %y：两位年份，例如 26
region["month"] = pd.to_datetime(
    region["month"],
    format="%b-%y"
)

# 4. 获取大区8月和9月销售额
region_aug = region.loc[
    region["month"].dt.strftime("%Y-%m") == "2026-08",
    "sales_amount"
].iloc[0]

region_sep = region.loc[
    region["month"].dt.strftime("%Y-%m") == "2026-09",
    "sales_amount"
].iloc[0]

# 5. 汇总客户销售额
customer_aug = customer["sales_aug"].sum()
customer_sep = customer["sales_sep"].sum()

# 6. 计算客户和大区销售变化
customer_change = customer_sep - customer_aug
region_change = region_sep - region_aug

# 7. 输出核对结果
result = pd.DataFrame({
    "指标": [
        "8月销售额",
        "9月销售额",
        "8月至9月销售变化"
    ],
    "客户汇总": [
        customer_aug,
        customer_sep,
        customer_change
    ],
    "大区汇总": [
        region_aug,
        region_sep,
        region_change
    ]
})

result["差异"] = result["客户汇总"] - result["大区汇总"]

print("===== 客户与大区销售额核对 =====")
print(result.round(2).to_string(index=False))

print("\n客户数量：", customer["customer_id"].nunique())

# 8. 判断是否核对一致
tolerance = 0.01

if result["差异"].abs().max() <= tolerance:
    print("\n核对通过：客户销售额与大区销售额一致！")
else:
    print("\n核对未通过：请检查客户范围和数据口径。")

# 9. 保存结果
result.to_csv(
    REPORT_DIR / "customer_reconciliation.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n核对结果已保存：customer_reconciliation.csv")
