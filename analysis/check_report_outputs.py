from pathlib import Path
import pandas as pd

REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"

for file_path in sorted(REPORT_DIR.glob("*.csv")):
    df = pd.read_csv(file_path)
    if not list(REPORT_DIR.glob("*.csv")):
        print(f"没有找到CSV文件，请检查目录：{REPORT_DIR}")
    print("\n" + "=" * 60)
    print(f"文件名称：{file_path.name}")
    print(f"数据行数：{len(df)}")
    print(f"字段名称：{df.columns.tolist()}")
    print("\n前2行数据：")
    print(df.head(2).to_string(index=False))