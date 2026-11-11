
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "database" / "fmcg_business.duckdb"
SQL_PATH = BASE_DIR / "sql" / "day1_analysis.sql"
OUTPUT_DIR = BASE_DIR / "reports" / "sql_results"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 连接数据库
con = duckdb.connect(str(DB_PATH), read_only=True)

# 读取 SQL 文件
sql_text = SQL_PATH.read_text(encoding="utf-8")

# 按分号拆分 SQL 语句
statements = [
    statement.strip()
    for statement in sql_text.split(";")
    if statement.strip()
]

print(f"共发现 {len(statements)} 条 SQL 查询")

for i, statement in enumerate(statements, start=1):

    print(f"\n========== SQL 查询 {i} ==========")

    result = con.execute(statement).df()

    print(result.head(10).to_string(index=False))
    print(f"\n结果行数：{len(result)}")

    output_path = OUTPUT_DIR / f"query_{i}_result.csv"

    result.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"结果已保存：{output_path}")

con.close()

print("\n全部 SQL 查询执行完成！")
