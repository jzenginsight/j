
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv


# 1. 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. 读取项目根目录中的 .env
load_dotenv(BASE_DIR / ".env")

# 3. 获取 API Key
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("没有读取到 OPENROUTER_API_KEY，请检查 .env 文件")


# 4. 创建 OpenRouter 客户端
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    timeout=120
)


# 5. 向 AI 发送测试请求
print("正在连接 OpenRouter...")

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "system",
            "content": "你是一名专业的快消品行业经营分析师。"
        },
        {
            "role": "user",
            "content": """
            请解释以下三个经营指标：

            1. 销售额同比增长率
            2. 毛利率
            3. 产品结构效应

            请使用中文回答，并结合快消品行业举例。
            """
        }
    ]
)


# 6. 输出 AI 回答
result = response.choices[0].message.content

print("\n========== AI 回答 ==========\n")
print(result)

print("\n========== 调用成功 ==========")
print("模型：", response.model)


