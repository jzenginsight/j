
from pathlib import Path
import duckdb
import pandas as pd

# ==========================================
# 1. 配置项目路径
# ==========================================

# 当前 Python 文件所在目录：analysis
BASE_DIR = Path(__file__).resolve().parent

# 项目根目录：FMCG_AI_Business_Analyst
PROJECT_DIR = BASE_DIR.parent

# 数据库路径
DB_PATH = PROJECT_DIR / "database" / "fmcg_business.duckdb"

# 报告输出目录
REPORT_DIR = PROJECT_DIR / "reports"

# 如果 reports 文件夹不存在，自动创建
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("项目根目录：", PROJECT_DIR)
print("数据库路径：", DB_PATH)
print("报告输出目录：", REPORT_DIR)

# ==========================================
# 2. 连接数据库
# ==========================================

if not DB_PATH.exists():
    raise FileNotFoundError(f"找不到数据库文件：{DB_PATH}")

con = duckdb.connect(str(DB_PATH), read_only=True)

# ==========================================
# 3. 查询华南大区月度经营数据
# ==========================================

sql = """
WITH sales_monthly AS (
    -- 第一步：先计算华南每个月的实际销售和成本
    SELECT
        s.month,
        SUM(s.sales_amount) AS sales_amount,
        SUM(s.cost_amount) AS cost_amount
    FROM fact_sales s
    INNER JOIN dim_customer c
        ON s.customer_id = c.customer_id
    WHERE c.region = '华南'
    GROUP BY s.month
),

target_monthly AS (
    -- 第二步：独立计算华南每个月的销售目标
    SELECT
        t.month,
        SUM(t.target_amount) AS target_amount
    FROM fact_target t
    INNER JOIN dim_customer c
        ON t.customer_id = c.customer_id
    WHERE c.region = '华南'
    GROUP BY t.month
)

-- 第三步：将两个已经汇总的数据集按月份关联
SELECT
    COALESCE(s.month, t.month) AS month,
    COALESCE(s.sales_amount, 0) AS sales_amount,
    COALESCE(t.target_amount, 0) AS target_amount,
    COALESCE(s.sales_amount, 0)
        - COALESCE(s.cost_amount, 0) AS gross_profit,

    (
        COALESCE(s.sales_amount, 0)
        - COALESCE(s.cost_amount, 0)
    ) / NULLIF(s.sales_amount, 0) AS gross_margin

FROM sales_monthly s
FULL OUTER JOIN target_monthly t
    ON s.month = t.month

ORDER BY month
"""

df = con.execute(sql).df()

con.close()

# ==========================================
# 4. 计算经营指标
# ==========================================

# 目标达成率
df["achievement_rate"] = (
    df["sales_amount"]
    / df["target_amount"].replace(0, pd.NA)
)

# ==========================================
# 5. 输出分析结果
# ==========================================

print("\n========== 华南大区月度经营分析 ==========")
print(df.to_string(index=False))

# ==========================================
# 6. 保存分析结果
# ==========================================

output_path = REPORT_DIR / "region_performance.csv"

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\n========== 运行完成 ==========")
print("数据记录数：", len(df))
print("文件保存位置：", output_path)
