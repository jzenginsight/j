# FMCG AI Business Analyst

**AI 驱动的快消品经营分析与业务决策辅助平台**

[在线体验](https://ucxfafjxereeyg2ayaua2o.streamlit.app/) ｜ [GitHub Repository](https://github.com/jzenginsight/j)

---

## 1. 项目简介

FMCG AI Business Analyst 是一个面向快速消费品（FMCG）行业的 AI 经营分析项目。

项目模拟休闲食品企业的经营管理场景，整合销售、客户、产品、库存、目标及费用等业务数据，利用 Python、SQL、DuckDB 和大语言模型，构建从数据查询、经营分析到异常识别的辅助分析系统。

项目希望解决传统经营分析中常见的几个问题：

- **数据查询门槛高：** 业务人员需要掌握 SQL 或依赖数据分析人员获取数据。
- **经营分析效率低：** 多维度数据分散，人工整理和分析耗时。
- **异常发现不及时：** 销售、毛利、库存及客户表现需要人工逐项排查。
- **数据与业务决策脱节：** 分析结果需要进一步转化为可理解的业务信息。

通过自然语言交互和自动化分析，让业务人员能够更便捷地获取经营数据、识别经营问题。

## 2. 核心功能

### 2.1 AI 智能问数

通过自然语言描述业务问题，系统自动完成：

1. 读取数据库结构及字段信息。
2. 调用大语言模型生成 SQL。
3. 执行 SQL 并查询 DuckDB 数据库。
4. 展示 SQL 语句和查询结果。
5. 调用 AI 对查询结果进行经营分析。

**示例问题：**

- 查询 2026 年 9 月各大区销售额和毛利率。
- 分析华南大区的销售表现。
- 查询销售额排名靠前的客户。

### 2.2 经营分析

从区域、产品和客户三个维度展示经营表现。

- **区域经营：** 销售额、毛利额、毛利率、目标达成率等指标。
- **产品表现：** 产品销售及盈利能力分析。
- **客户贡献：** 客户销售贡献、毛利表现及目标达成情况。

通过指标卡片、图表和数据明细，辅助用户了解整体经营情况。

### 2.3 异常检测

基于预设的业务规则识别经营异常，并结合客户销售、库存和费用表现评估客户风险。

主要覆盖：

- 区域销售及毛利表现异常。
- 客户销售变化异常。
- 产品毛利率变化异常。
- 客户费用率异常。
- 客户库存变化异常。
- 客户风险评估及异常严重程度展示。

## 3. 系统技术架构

| 技术 | 应用场景 |
|---|---|
| Python | 数据处理与业务分析 |
| Pandas / NumPy | 数据清洗及计算 |
| DuckDB | 本地分析型数据库 |
| SQL | 业务数据查询 |
| OpenRouter API | 接入大语言模型 |
| OpenAI Python SDK | 模型接口调用 |
| Streamlit | Web 应用与交互界面 |
| Plotly | 数据可视化 |
| GitHub | 代码版本管理 |
| Streamlit Community Cloud | 在线部署 |

## 4. 项目数据

本项目当前使用模拟业务数据，不包含真实企业经营数据。

**数据周期：** 2025-10 至 2026-09

主要数据表：

| 数据表 | 业务含义 |
|---|---|
| dim_customer | 客户基础信息 |
| dim_product | 产品基础信息 |
| fact_sales | 销售明细 |
| fact_inventory | 客户库存快照 |
| fact_target | 销售目标 |
| fact_expense | 客户费用 |

数据库使用 DuckDB 存储，支持通过 SQL 进行多维度经营分析。

## 5. 项目目录结构

```text
FMCG_AI_Business_Analyst/
│
├── analysis/                 # 业务分析及 AI 查询模块
│   └── text_to_sql.py        # 自然语言转 SQL
│
├── data/
│   └── raw/                  # 原始模拟数据
│
├── database/
│   └── fmcg_business.duckdb  # DuckDB 业务数据库
│
├── docs/                     # 项目文档
│
├── reports/                  # 分析结果及报告
│   ├── region_performance.csv
│   ├── product_profitability.csv
│   ├── customer_analysis.csv
│   ├── anomaly_detection.csv
│   └── customer_risk_assessment.csv
│
├── sql/                      # SQL 分析脚本
│
├── app.py                    # Streamlit Web 应用入口
├── main.py                   # 项目主程序
├── run_sql.py                # SQL 执行入口
├── check_database.py         # 数据库检查
├── requirements.txt          # 项目依赖
├── .gitignore                # Git 忽略配置
└── README.md                 # 项目说明文档
```

## 6. 在线体验

项目已部署至 Streamlit Community Cloud。

访问地址：**请替换为你的 Streamlit 公网网址**

在线体验可以使用自然语言输入经营问题，查看 AI 生成的 SQL、数据查询结果及分析内容。

## 7. 本地运行

### 环境要求

- Python 3.10+
- Git
- OpenRouter API Key

### 安装步骤

**1. 克隆项目**

```bash
git clone https://github.com/jzenginsight/j.git
cd j
```

**2. 创建虚拟环境**

```bash
python -m venv .venv
```

Windows PowerShell 激活环境：

```powershell
.venv\Scripts\Activate.ps1
```

**3. 安装依赖**

```bash
pip install -r requirements.txt
```

**4. 配置 API Key**

在项目根目录创建 `.env` 文件：

```env
OPENROUTER_API_KEY=your_api_key
```

将 `your_api_key` 替换为自己的 OpenRouter API Key。

**5. 启动应用**

```bash
streamlit run app.py
```

浏览器访问：

```text
http://localhost:8501
```

## 8. 安全说明

- `.env` 文件及 API Key 不应上传至 GitHub。
- 云端部署通过 Streamlit Secrets 管理 API Key。
- 项目当前使用模拟数据进行功能演示。
- AI 生成的分析内容应结合实际业务口径进行复核。

## 9. 后续优化方向

当前版本已完成核心 MVP 和公网部署。后续计划包括：

- 使用真实业务数据完善数据模型和分析逻辑。
- 优化 AI 生成 SQL 的准确性及复杂业务问题理解能力。
- 深化产品结构、毛利变化及客户经营诊断。
- 完善经营策略建议与分析报告生成。
- 持续优化系统稳定性和用户体验。

---

**Project:** FMCG AI Business Analyst  
**Version:** MVP v1.0  
**Data:** Synthetic FMCG Business Data  
**Deployment:** Streamlit Community Cloud