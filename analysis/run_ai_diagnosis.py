
import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# ==================================
# 1. 获取项目路径
# ==================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "reports" / "ai_input.json"
PROMPT_FILE = BASE_DIR / "reports" / "ai_analysis_prompt.md"
OUTPUT_FILE = BASE_DIR / "reports" / "ai_business_report.md"

# ==================================
# 2. 读取环境变量
# ==================================

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("没有读取到 OPENROUTER_API_KEY")

# ==================================
# 3. 创建 OpenRouter 客户端
# ==================================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    timeout=120
)

# ==================================
# 4. 读取经营数据和 Prompt
# ==================================

print("正在读取经营数据...")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    business_data = json.load(f)

with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    system_prompt = f.read()

print("经营数据读取成功！")

# ==================================
# 5. 调用 AI 模型
# ==================================

print("正在调用 AI 进行经营诊断...")

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": (
                "请基于以下 JSON 经营数据完成经营诊断。"
                "严格遵守系统指令，不要编造数据。\n\n"
                + json.dumps(
                    business_data,
                    ensure_ascii=False,
                    indent=2
                )
            )
        }
    ]
)

# ==================================
# 6. 获取 AI 分析结果
# ==================================

result = response.choices[0].message.content

choice = response.choices[0]
message = choice.message

print("\n========== 模型响应诊断 ==========")

print("实际模型：", response.model)
print("结束原因：", choice.finish_reason)
print("原始结束原因：", getattr(choice, "native_finish_reason", None))
print("返回内容：", repr(message.content))

print(
    "是否包含 reasoning 字段：",
    bool(getattr(message, "reasoning", None))
)

print(
    "工具调用数量：",
    len(message.tool_calls or [])
)

print(
    "Token 使用情况：",
    response.usage.model_dump() if response.usage else None
)

print("==================================")

result = message.content

if not result:
    raise ValueError(
        "AI 返回内容为空，请根据上面的模型响应诊断信息排查。"
    )

# ==================================
# 7. 保存经营诊断报告
# ==================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(result)

print("\n========== AI 经营诊断完成 ==========")
print("实际使用模型：", response.model)
print("报告保存位置：", OUTPUT_FILE)
print("报告字符数：", len(result))
print("\n========== 分析结果预览 ==========\n")
print(result[:2000])
