import json
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 读取 AI 输入文件
INPUT_FILE = BASE_DIR / "reports" / "ai_input.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print("========== AI 输入数据检查 ==========")

print("数据类型：", type(data).__name__)

if isinstance(data, dict):
    print("\n一级字段：")
    for key, value in data.items():
        print(f"\n字段名称：{key}")
        print("数据类型：", type(value).__name__)

        if isinstance(value, list):
            print("数据条数：", len(value))
            if value:
                print("第一条数据：", str(value[0])[:300])

        elif isinstance(value, dict):
            print("子字段：", list(value.keys()))

        else:
            print("数据内容：", str(value)[:300])

elif isinstance(data, list):
    print("数据条数：", len(data))
    if data:
        print("第一条数据：", str(data[0])[:500])

print("\n========== 检查完成 ==========")