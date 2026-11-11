import json
from pathlib import Path
from collections import defaultdict


# ============================================================
# 1. 路径配置
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "reports" / "business_diagnosis.json"
OUTPUT_JSON = BASE_DIR / "reports" / "ai_input.json"
OUTPUT_PROMPT = BASE_DIR / "reports" / "ai_analysis_prompt.md"


# ============================================================
# 2. 通用函数
# =========
# ===================================================

def load_json(file_path):
    """读取 JSON 文件。"""
    if not file_path.exists():
        raise FileNotFoundError(f"找不到文件：{file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def safe_list(data, key):
    """安全获取列表字段。"""
    value = data.get(key, [])
    return value if isinstance(value, list) else []


def select_fields(records, fields):
    """只保留指定字段，减少传给 AI 的数据量。"""
    result = []

    for record in records:
        item = {
            field: record.get(field)
            for field in fields
            if field in record
        }
        result.append(item)

    return result


def merge_findings_by_entity(findings):
    """
    按客户/产品 ID 合并经营发现。
    同一个实体可能有多个分析角度，但不重复计算为多个问题。
    """
    grouped = defaultdict(lambda: {
        "entity_id": None,
        "entity": None,
        "categories": set(),
        "evidence": []
    })

    for item in findings:
        entity_id = item.get("entity_id")

        if not entity_id:
            continue

        entity = grouped[entity_id]

        entity["entity_id"] = entity_id
        entity["entity"] = item.get("entity")
        entity["categories"].add(item.get("category", "未分类"))

        evidence = {
            "finding": item.get("finding"),
            "metric": item.get("metric"),
            "value": item.get("value"),
            "evidence": item.get("evidence"),
            "priority": item.get("priority")
        }

        if evidence not in entity["evidence"]:
            entity["evidence"].append(evidence)

    result = []

    for entity in grouped.values():
        entity["categories"] = sorted(entity["categories"])

        # 每个实体最多保留 5 条证据，避免输入过长
        entity["evidence"] = entity["evidence"][:5]

        result.append(entity)

    return result


# ============================================================
# 3. 构建精简 AI 输入
# ============================================================

def build_ai_input(data):

    analysis_period = data.get("analysis_period", {})
    overall = data.get("overall_performance", {})
    customer = data.get("customer_performance", {})
    product = data.get("product_performance", {})
    data_checks = data.get("data_checks", {})
    notes = data.get("diagnosis_notes", {})

    # -------------------------
    # 整体经营表现
    # -------------------------

    overall_input = {
        "previous_month": analysis_period.get("previous_month"),
        "current_month": analysis_period.get("current_month"),
        "previous_sales": overall.get("previous_sales"),
        "current_sales": overall.get("current_sales"),
        "sales_change": overall.get("sales_change"),
        "sales_growth_rate": overall.get("sales_growth_rate"),
        "achievement_rate": overall.get("achievement_rate"),
        "previous_gross_profit": overall.get("previous_gross_profit"),
        "current_gross_profit": overall.get("current_gross_profit"),
        "gross_profit_change": overall.get("gross_profit_change"),
        "previous_gross_margin": overall.get("previous_gross_margin"),
        "current_gross_margin": overall.get("current_gross_margin"),
        "gross_margin_change_pp": overall.get("gross_margin_change_pp")
    }

    # -------------------------
    # 客户表现
    # -------------------------

    customer_input = {
        "customer_count": customer.get("customer_count"),
        "weighted_gross_margin": customer.get("weighted_gross_margin"),
        "total_achievement_rate": customer.get("total_achievement_rate"),

        "top_growth_customers": select_fields(
            safe_list(customer, "top_growth_customers"),
            [
                "customer_id",
                "customer_name",
                "sales_aug",
                "sales_sep",
                "sales_change",
                "growth_rate",
                "growth_contribution"
            ]
        ),

        "top_decline_customers": select_fields(
            safe_list(customer, "top_decline_customers"),
            [
                "customer_id",
                "customer_name",
                "sales_aug",
                "sales_sep",
                "sales_change",
                "growth_rate",
                "decline_contribution"
            ]
        ),

        "customer_risk_list": select_fields(
            safe_list(customer, "customer_entity_diagnosis"),
            [
                "customer_id",
                "customer_name",
                "risk_level",
                "follow_up_priority",
                "risk_signal_count",
                "risk_reasons",
                "sales_change",
                "sales_change_rate",
                "inventory_change",
                "inventory_change_rate",
                "expense_change_pp"
            ]
        )
    }

    # -------------------------
    # 产品销售表现
    # -------------------------

    product_input = {
        "top_growth_products": select_fields(
            safe_list(product, "top_growth_products"),
            [
                "product_id",
                "product_name",
                "series",
                "flavor",
                "spec",
                "sales_aug",
                "sales_sep",
                "sales_change",
                "growth_rate",
                "gross_margin_aug",
                "gross_margin_sep",
                "gross_margin_change",
                "sales_share_aug",
                "sales_share_sep"
            ]
        ),

        "top_decline_products": select_fields(
            safe_list(product, "top_decline_products"),
            [
                "product_id",
                "product_name",
                "series",
                "flavor",
                "spec",
                "sales_aug",
                "sales_sep",
                "sales_change",
                "growth_rate",
                "gross_margin_aug",
                "gross_margin_sep",
                "gross_margin_change",
                "sales_share_aug",
                "sales_share_sep"
            ]
        )
    }

    # -------------------------
    # 产品毛利率归因
    # -------------------------

    margin_diagnosis = product.get("product_margin_diagnosis", {})

    product_input["margin_attribution"] = {
        "mix_effect_pp": product.get("mix_effect_pp"),
        "margin_effect_pp": product.get("margin_effect_pp"),
        "total_margin_effect_pp": product.get("total_margin_effect_pp"),

        "negative_impact_top5": select_fields(
            safe_list(margin_diagnosis, "negative_impact_top5"),
            [
                "product_id",
                "product_name",
                "diagnosis_mix_effect_pp",
                "diagnosis_margin_effect_pp",
                "diagnosis_total_effect_pp",
                "impact_type",
                "product_priority",
                "product_status"
            ]
        ),

        "mix_drag_top5": select_fields(
            safe_list(margin_diagnosis, "mix_drag_top5"),
            [
                "product_id",
                "product_name",
                "diagnosis_mix_effect_pp",
                "diagnosis_margin_effect_pp",
                "diagnosis_total_effect_pp",
                "sales_share_aug",
                "sales_share_sep",
                "impact_type",
                "product_priority"
            ]
        ),

        "margin_drag_top5": select_fields(
            safe_list(margin_diagnosis, "margin_drag_top5"),
            [
                "product_id",
                "product_name",
                "diagnosis_mix_effect_pp",
                "diagnosis_margin_effect_pp",
                "diagnosis_total_effect_pp",
                "impact_type",
                "product_priority"
            ]
        ),

        "positive_impact_top5": select_fields(
            safe_list(margin_diagnosis, "positive_impact_top5"),
            [
                "product_id",
                "product_name",
                "diagnosis_mix_effect_pp",
                "diagnosis_margin_effect_pp",
                "diagnosis_total_effect_pp",
                "impact_type",
                "product_priority"
            ]
        )
    }

    # -------------------------
    # 数据质量与诊断口径
    # -------------------------

    grouped_findings = merge_findings_by_entity(
        safe_list(data, "findings")
    )

    result = {
        "analysis_period": analysis_period,
        "overall_performance": overall_input,
        "customer_performance": customer_input,
        "product_performance": product_input,
        "data_checks": data_checks,

        "entity_findings": grouped_findings,

        "diagnosis_notes": notes
    }

    return result


# ============================================================
# 4. 生成 AI 分析指令
# ============================================================

def build_prompt(ai_input):

    data_json = json.dumps(
        ai_input,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
# 角色

你是一名具有快消品行业经验的资深经营分析师。
请基于提供的经营数据，撰写一份管理层可以阅读的经营诊断报告。

# 分析任务

1. 分析整体销售额、毛利额和毛利率变化。
2. 分析客户增长来源、下降客户及风险客户。
3. 分析产品销售增长和下降来源。
4. 判断毛利率下降主要来自产品结构变化，还是产品自身毛利率变化。
5. 找出需要优先跟进的客户和产品。
6. 提出具体、可执行的经营建议。

# 必须遵守的规则

1. 所有数字必须来自输入数据，不得编造。
2. Python 已完成指标计算，不得擅自修改指标。
3. 区分已确认事实、原因假设、经营建议和待验证事项。
4. 不得把相关性直接表述为因果关系。
5. 客户风险中的空值代表没有对应记录或未触发，不代表数值为0。
6. 销售下降且库存上升属于潜在库存压力信号，不能直接断言库存积压。
7. 单月无销售的产品，其毛利率不可观察，不得解释为毛利率下降。
8. findings 是不同维度的诊断证据，同一客户或产品可能重复出现，不能将发现条数视为独立问题数。
9. 毛利率归因优先使用整体归因结果，产品级证据用于解释贡献来源。
10. 建议必须尽量对应具体客户、产品或指标。

# 报告结构

## 一、经营总览
概括销售额、毛利额、毛利率和达成情况。

## 二、核心经营问题
提炼3—5个最重要的问题，按影响程度排序。
每个问题包含：
- 已确认事实
- 数据证据
- 可能原因
- 需要进一步核实的事项

## 三、客户经营分析
分析增长客户、下降客户和高风险客户。
区分销售下降、库存上升、费用率上升等不同风险组合。

## 四、产品经营分析
分析产品销售增长和下降来源。
重点解释产品结构效应与产品自身毛利率效应。

## 五、重点跟进清单
分别列出需要跟进的客户和产品，并说明原因。

## 六、行动建议
给出短期（1周内）和中期（1个月内）的行动建议。
建议具体、可执行、可验证。

## 七、待补充数据
列出当前数据不足以判断、需要业务部门补充的信息。

# 输出要求

- 使用中文。
- 先给结论，再给证据。
- 重要数字保留合理精度。
- 使用 Markdown 标题和表格。
- 不要重复罗列所有数据。
- 不得把推测写成事实。

# 本次经营分析数据

以下是经过 Python 整理的结构化数据，请严格依据这些数据分析：

{data_json}
"""

    return prompt

# ============================================================
# 5. 主程序：执行数据读取、整理和文件生成
# ============================================================

if __name__ == "__main__":

    print("开始生成 AI 分析输入文件...")

    # 1. 检查输入文件
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"找不到经营诊断文件：{INPUT_FILE}"
        )

    # 2. 确保 reports 文件夹存在
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    # 3. 读取经营诊断数据
    data = load_json(INPUT_FILE)
    print("已读取 business_diagnosis.json")

    # 4. 构建 AI 输入数据
    ai_input = build_ai_input(data)

    # 5. 保存 AI 输入 JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as file:
        json.dump(
            ai_input,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(f"已生成：{OUTPUT_JSON}")

    # 6. 构建 AI 分析 Prompt
    prompt = build_prompt(ai_input)

    # 7. 保存 AI 分析指令
    OUTPUT_PROMPT.write_text(
        prompt,
        encoding="utf-8"
    )

    print(f"已生成：{OUTPUT_PROMPT}")

    print("\nAI 输入文件生成完成！")
    print(f"客户风险数量：{len(ai_input['customer_performance']['customer_risk_list'])}")
    print(f"实体诊断数量：{len(ai_input['entity_findings'])}")
    print(f"AI 输入文件大小：{OUTPUT_JSON.stat().st_size} bytes")

    {json.dumps(ai_input, ensure_ascii=False, indent=2)}