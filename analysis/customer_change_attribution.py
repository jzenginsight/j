
from pathlib import Path
import pandas as pd

# 1. 路径配置
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

REPORT_DIR = PROJECT_DIR / "reports"

# 2. 读取客户环比分析数据
df = pd.read_csv(
    REPORT_DIR / "customer_growth_analysis.csv"
)

# 3. 分别计算增长和下降客户
growth_df = df[df["sales_change"] > 0].copy()
decline_df = df[df["sales_change"] < 0].copy()

# 4. 计算增长客户的增长贡献
total_growth = growth_df["sales_change"].sum()

growth_df["growth_contribution"] = (
    growth_df["sales_change"] / total_growth
)

# 5. 计算下降客户的下降贡献
total_decline = decline_df["sales_change"].abs().sum()

decline_df["decline_contribution"] = (
    decline_df["sales_change"].abs() / total_decline
)

# 6. 按销售变化金额排序
growth_df = growth_df.sort_values(
    "sales_change", ascending=False
)

decline_df = decline_df.sort_values(
    "sales_change", ascending=True
)

# 7. 输出前10名
print("\n========== 销售增长贡献 TOP10 ==========")
print(
    growth_df[
        ["customer_id", "customer_name",
         "sales_change", "growth_contribution"]
    ].head(10).to_string(index=False)
)

print("\n========== 销售下降贡献 TOP10 ==========")
print(
    decline_df[
        ["customer_id", "customer_name",
         "sales_change", "decline_contribution"]
    ].head(10).to_string(index=False)
)

# 8. 保存结果
growth_df.to_csv(
    REPORT_DIR / "customer_growth_contribution.csv",
    index=False,
    encoding="utf-8-sig"
)

decline_df.to_csv(
    REPORT_DIR / "customer_decline_contribution.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n客户变动归因分析完成！")
