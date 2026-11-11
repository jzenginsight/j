
import json
from pathlib import Path


# =========================
# 1. 路径配置
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
import pandas as pd

CUSTOMER_FILE = BASE_DIR / "reports" / "customer_decline_contribution.csv"
INPUT_FILE = BASE_DIR / "reports" / "ai_input.json"
OUTPUT_FILE = BASE_DIR / "reports" / "report_validation.json"


# =========================
# 2. 通用校验函数
# =========================

validation_results = []


def add_check(name, passed, expected, actual, message=""):
    """
    记录一项校验结果
    """
    validation_results.append({
        "check_name": name,
        "passed": bool(passed),
        "expected": expected,
        "actual": actual,
        "message": message
    })


def is_close(a, b, tolerance=0.000001):
    """
    判断两个数字是否足够接近
    避免浮点数精度误差
    """
    return abs(a - b) <= tolerance


# =========================
# 3. 读取 AI 输入数据
# =========================

def load_data():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"找不到文件：{INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# 4. 校验整体经营指标
# =========================

def validate_overall(data):

    overall = data["overall_performance"]

    # 销售额变化
    expected_sales_change = (
        overall["current_sales"] -
        overall["previous_sales"]
    )

    add_check(
        "销售额变化校验",
        is_close(expected_sales_change, overall["sales_change"]),
        round(expected_sales_change, 2),
        round(overall["sales_change"], 2),
        "本月销售额减去上月销售额"
    )

    # 销售增长率
    expected_growth_rate = (
        overall["current_sales"] /
        overall["previous_sales"] - 1
    )

    add_check(
        "销售增长率校验",
        is_close(expected_growth_rate, overall["sales_growth_rate"]),
        round(expected_growth_rate, 6),
        round(overall["sales_growth_rate"], 6),
        "销售额环比增长率"
    )

    # 毛利额变化
    expected_gp_change = (
        overall["current_gross_profit"] -
        overall["previous_gross_profit"]
    )

    add_check(
        "毛利额变化校验",
        is_close(expected_gp_change, overall["gross_profit_change"]),
        round(expected_gp_change, 2),
        round(overall["gross_profit_change"], 2),
        "本月毛利额减去上月毛利额"
    )

    # 毛利率变化
    expected_margin_change = (
        overall["current_gross_margin"] -
        overall["previous_gross_margin"]
    ) * 100

    add_check(
        "毛利率变化校验",
        is_close(
            expected_margin_change,
            overall["gross_margin_change_pp"]
        ),
        round(expected_margin_change, 4),
        round(overall["gross_margin_change_pp"], 4),
        "毛利率变化，单位为百分点"
    )


# =========================
# 5. 校验客户下降贡献
# =========================


def validate_customers(data):

    customers = data["customer_performance"]

    # 1. 读取独立客户下降明细
    if not CUSTOMER_FILE.exists():
        raise FileNotFoundError(
            f"找不到客户下降明细：{CUSTOMER_FILE}"
        )

    df = pd.read_csv(CUSTOMER_FILE)

    # 2. 从独立明细中重新计算销售额变化
    df["calculated_change"] = (
        df["sales_sep"] - df["sales_aug"]
    )

    # 检查明细中的销售变化计算是否正确
    detail_errors = (
        df["calculated_change"] - df["sales_change"]
    ).abs()

    add_check(
        "客户明细销售变化校验",
        bool((detail_errors <= 0.01).all()),
        "所有客户计算一致",
        int((detail_errors > 0.01).sum()),
        "本月销售额减去上月销售额"
    )

    # 3. 根据独立明细重新排序，获取Top 5
    independent_top5 = (
        df.sort_values("calculated_change")
        .head(5)
        .reset_index(drop=True)
    )

    # 4. 获取AI输入文件中的Top 5
    ai_top5 = customers.get(
        "top_decline_customers", []
    )[:5]

    # 5. 比较客户编号
    independent_ids = (
        independent_top5["customer_id"].tolist()
    )

    ai_ids = [
        item["customer_id"]
        for item in ai_top5
    ]

    add_check(
        "Top 5下降客户名单校验",
        independent_ids == ai_ids,
        independent_ids,
        ai_ids,
        "比较独立明细与AI输入中的客户名单"
    )

    # 6. 比较下降金额
    independent_sum = independent_top5[
        "calculated_change"
    ].sum()

    ai_sum = sum(
        item["sales_change"]
        for item in ai_top5
    )

    add_check(
        "Top 5下降客户金额校验",
        is_close(independent_sum, ai_sum, 0.01),
        round(independent_sum, 2),
        round(ai_sum, 2),
        "分别从独立明细和AI输入中计算Top 5下降金额"
    )

    # 7. 比较每个客户的销售变化
    amount_errors = []

    for independent, ai in zip(
        independent_top5.to_dict("records"),
        ai_top5
    ):
        difference = abs(
            independent["calculated_change"]
            - ai["sales_change"]
        )

        if difference > 0.01:
            amount_errors.append({
                "customer_id": independent["customer_id"],
                "difference": round(difference, 2)
            })

    add_check(
        "Top 5逐客户金额校验",
        len(amount_errors) == 0,
        "每个客户金额一致",
        amount_errors if amount_errors else "全部一致",
        "检查每个客户的销售额变化"
    )



# =========================
# 6. 校验产品毛利率归因
# =========================

def validate_products(data):

    attribution = data["product_performance"][
        "margin_attribution"
    ]

    mix_effect = attribution["mix_effect_pp"]
    margin_effect = attribution["margin_effect_pp"]
    total_effect = attribution["total_margin_effect_pp"]

    # 两项归因是否等于总影响
    expected_total = mix_effect + margin_effect

    add_check(
        "产品毛利率归因加总",
        is_close(expected_total, total_effect),
        round(expected_total, 4),
        round(total_effect, 4),
        "产品结构效应 + 产品自身毛利率效应"
    )

    # 归因总影响是否与整体毛利率变化一致
    overall = data["overall_performance"]

    add_check(
        "产品归因与整体毛利率变化",
        is_close(
            total_effect,
            overall["gross_margin_change_pp"]
        ),
        round(overall["gross_margin_change_pp"], 4),
        round(total_effect, 4),
        "检查产品归因结果与整体毛利率变化是否一致"
    )


# =========================
# 7. 校验数据质量信息
# =========================

def validate_data_quality(data):

    checks = data["data_checks"]

    add_check(
        "客户数据勾稽",
        checks["customer_reconciliation_passed"] is True,
        True,
        checks["customer_reconciliation_passed"],
        "客户数据勾稽是否通过"
    )

    add_check(
        "异常数量非负",
        checks["anomaly_count"] >= 0,
        "大于等于0",
        checks["anomaly_count"],
        "异常记录数量不能为负数"
    )

    notes = data["diagnosis_notes"]

    add_check(
        "诊断发现数量口径",
        notes["finding_count_is_unique_issue_count"] is False,
        False,
        notes["finding_count_is_unique_issue_count"],
        "不能将诊断发现条数直接当作独立经营问题数量"
    )


# =========================
# 8. 输出校验报告
# =========================

def save_report():

    total = len(validation_results)

    passed = sum(
        1 for item in validation_results
        if item["passed"]
    )

    failed = total - passed

    report = {
        "validation_summary": {
            "total_checks": total,
            "passed_checks": passed,
            "failed_checks": failed,
            "pass_rate": round(passed / total, 4)
            if total else 0
        },
        "validation_details": validation_results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\n========== AI报告数据校验结果 ==========")

    for item in validation_results:
        status = "通过" if item["passed"] else "失败"

        print(f"[{status}] {item['check_name']}")
        print(f"  预期值：{item['expected']}")
        print(f"  实际值：{item['actual']}")

        if item["message"]:
            print(f"  说明：{item['message']}")

    print("\n========== 校验汇总 ==========")
    print(f"校验项目：{total}")
    print(f"通过数量：{passed}")
    print(f"失败数量：{failed}")
    print(f"通过率：{report['validation_summary']['pass_rate']:.2%}")
    print(f"\n校验报告已保存：{OUTPUT_FILE}")


# =========================
# 9. 主程序
# =========================

if __name__ == "__main__":

    print("开始执行 AI 报告数据校验...")

    data = load_data()

    validate_overall(data)
    validate_customers(data)
    validate_products(data)
    validate_data_quality(data)

    save_report()
