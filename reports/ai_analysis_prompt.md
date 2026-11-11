
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

{
  "analysis_period": {
    "previous_month": "Aug-26",
    "current_month": "Sep-26"
  },
  "overall_performance": {
    "previous_month": "Aug-26",
    "current_month": "Sep-26",
    "previous_sales": 538488.17,
    "current_sales": 519685.93,
    "sales_change": -18802.24000000005,
    "sales_growth_rate": -0.03491671878325581,
    "achievement_rate": 0.7084582995635277,
    "previous_gross_profit": 204235.66,
    "current_gross_profit": 193189.38,
    "gross_profit_change": -11046.279999999999,
    "previous_gross_margin": 0.3792760386918063,
    "current_gross_margin": 0.37174256382119103,
    "gross_margin_change_pp": -0.7533474870615287
  },
  "customer_performance": {
    "customer_count": 63,
    "weighted_gross_margin": 0.37174256382119114,
    "total_achievement_rate": 0.7084582995635277,
    "top_growth_customers": [
      {
        "customer_id": "C0274",
        "customer_name": "深圳经销商0274",
        "sales_aug": 11710.29,
        "sales_sep": 26985.850000000002,
        "sales_change": 15275.560000000001,
        "growth_rate": 1.3044561663289296,
        "growth_contribution": 0.1604627544672664
      },
      {
        "customer_id": "C0194",
        "customer_name": "广州经销商0194",
        "sales_aug": 7019.769999999999,
        "sales_sep": 15103.92,
        "sales_change": 8084.1500000000015,
        "growth_rate": 1.151626050426154,
        "growth_contribution": 0.08492028943793561
      },
      {
        "customer_id": "C0122",
        "customer_name": "广州经销商0122",
        "sales_aug": 3946.5499999999997,
        "sales_sep": 11842.579999999998,
        "sales_change": 7896.029999999999,
        "growth_rate": 2.0007424205952034,
        "growth_contribution": 0.08294417508465608
      },
      {
        "customer_id": "C0354",
        "customer_name": "厦门经销商0354",
        "sales_aug": 8387.31,
        "sales_sep": 14344.64,
        "sales_change": 5957.33,
        "growth_rate": 0.710278980984368,
        "growth_contribution": 0.06257902041368565
      },
      {
        "customer_id": "C0490",
        "customer_name": "广州经销商0490",
        "sales_aug": 3833.4199999999996,
        "sales_sep": 8842.070000000002,
        "sales_change": 5008.6500000000015,
        "growth_rate": 1.3065748078739094,
        "growth_contribution": 0.052613571951697614
      }
    ],
    "top_decline_customers": [
      {
        "customer_id": "C0338",
        "customer_name": "佛山经销商0338",
        "sales_aug": 23096.31,
        "sales_sep": 13720.99,
        "sales_change": -9375.320000000002,
        "growth_rate": -0.40592285087964275,
        "decline_contribution": 0.08224025510363411
      },
      {
        "customer_id": "C0378",
        "customer_name": "东莞经销商0378",
        "sales_aug": 13476.650000000001,
        "sales_sep": 4197.14,
        "sales_change": -9279.510000000002,
        "growth_rate": -0.6885620684665701,
        "decline_contribution": 0.08139981031439181
      },
      {
        "customer_id": "C0466",
        "customer_name": "厦门经销商0466",
        "sales_aug": 6755.110000000001,
        "sales_sep": 336.06,
        "sales_change": -6419.05,
        "growth_rate": -0.9502509951725434,
        "decline_contribution": 0.05630787104045328
      },
      {
        "customer_id": "C0402",
        "customer_name": "佛山经销商0402",
        "sales_aug": 15679.549999999997,
        "sales_sep": 9617.269999999999,
        "sales_change": -6062.279999999999,
        "growth_rate": -0.38663609606143035,
        "decline_contribution": 0.05317828657684845
      },
      {
        "customer_id": "C0242",
        "customer_name": "佛山经销商0242",
        "sales_aug": 8907.230000000001,
        "sales_sep": 3308.0600000000004,
        "sales_change": -5599.170000000001,
        "growth_rate": -0.6286095677331786,
        "decline_contribution": 0.04911588822233428
      }
    ],
    "customer_risk_list": [
      {
        "customer_id": "C0058",
        "customer_name": "佛山经销商0058",
        "risk_level": "高风险",
        "follow_up_priority": "优先跟进",
        "risk_signal_count": 2,
        "risk_reasons": "销售额下降、库存金额上升",
        "sales_change": -4523.900000000001,
        "sales_change_rate": -0.6512591432384304,
        "inventory_change": 25513.40999999999,
        "inventory_change_rate": 1.1618424695711724,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0234",
        "customer_name": "厦门经销商0234",
        "risk_level": "高风险",
        "follow_up_priority": "优先跟进",
        "risk_signal_count": 2,
        "risk_reasons": "销售额下降、库存金额上升",
        "sales_change": -5213.33,
        "sales_change_rate": -0.3697205747503853,
        "inventory_change": 10588.060000000001,
        "inventory_change_rate": 0.32778504258580937,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0242",
        "customer_name": "佛山经销商0242",
        "risk_level": "高风险",
        "follow_up_priority": "优先跟进",
        "risk_signal_count": 2,
        "risk_reasons": "销售额下降、库存金额上升",
        "sales_change": -5599.170000000001,
        "sales_change_rate": -0.6286095677331786,
        "inventory_change": 7392.010000000002,
        "inventory_change_rate": 0.3216734131539532,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0258",
        "customer_name": "东莞经销商0258",
        "risk_level": "高风险",
        "follow_up_priority": "优先跟进",
        "risk_signal_count": 2,
        "risk_reasons": "销售额下降、库存金额上升",
        "sales_change": -3858.6600000000017,
        "sales_change_rate": -0.2542270034082203,
        "inventory_change": 10269.070000000002,
        "inventory_change_rate": 0.7755128703749157,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0298",
        "customer_name": "深圳经销商0298",
        "risk_level": "高风险",
        "follow_up_priority": "优先跟进",
        "risk_signal_count": 2,
        "risk_reasons": "销售额下降、库存金额上升",
        "sales_change": -3627.5200000000013,
        "sales_change_rate": -0.38953318557462685,
        "inventory_change": 36934.810000000005,
        "inventory_change_rate": 2.0394749629485656,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0378",
        "customer_name": "东莞经销商0378",
        "risk_level": "高风险",
        "follow_up_priority": "优先跟进",
        "risk_signal_count": 2,
        "risk_reasons": "销售额下降、库存金额上升",
        "sales_change": -9279.510000000002,
        "sales_change_rate": -0.6885620684665701,
        "inventory_change": 6071.379999999999,
        "inventory_change_rate": 0.44173802958317254,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0442",
        "customer_name": "东莞经销商0442",
        "risk_level": "高风险",
        "follow_up_priority": "优先跟进",
        "risk_signal_count": 2,
        "risk_reasons": "销售额下降、库存金额上升",
        "sales_change": -2911.0999999999995,
        "sales_change_rate": -0.45054610007011,
        "inventory_change": 15125.410000000003,
        "inventory_change_rate": 0.38843309694128475,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0474",
        "customer_name": "佛山经销商0474",
        "risk_level": "高风险",
        "follow_up_priority": "优先跟进",
        "risk_signal_count": 2,
        "risk_reasons": "销售额下降、库存金额上升",
        "sales_change": -2751.91,
        "sales_change_rate": -0.4264523797347912,
        "inventory_change": 8055.109999999993,
        "inventory_change_rate": 0.31674896915445866,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0002",
        "customer_name": "深圳经销商0002",
        "risk_level": "高风险",
        "follow_up_priority": "重点关注",
        "risk_signal_count": 2,
        "risk_reasons": "库存金额上升、费用率上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 12172.970000000008,
        "inventory_change_rate": 0.44482175842607363,
        "expense_change_pp": 2.293923229021892
      },
      {
        "customer_id": "C0042",
        "customer_name": "厦门经销商0042",
        "risk_level": "高风险",
        "follow_up_priority": "重点关注",
        "risk_signal_count": 2,
        "risk_reasons": "销售额下降、费用率上升",
        "sales_change": -2207.45,
        "sales_change_rate": -0.38068080894132983,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": 2.0290057764690608
      },
      {
        "customer_id": "C0090",
        "customer_name": "广州经销商0090",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -1892.630000000001,
        "sales_change_rate": -0.30627509300899275,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0098",
        "customer_name": "东莞经销商0098",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 16143.680000000004,
        "inventory_change_rate": 0.9769311626280117,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0106",
        "customer_name": "佛山经销商0106",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -4449.25,
        "sales_change_rate": -0.609830479667977,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0122",
        "customer_name": "广州经销商0122",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 14208.449999999997,
        "inventory_change_rate": 0.8061234621134538,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0130",
        "customer_name": "深圳经销商0130",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 12539.699999999997,
        "inventory_change_rate": 0.520248048919422,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0138",
        "customer_name": "深圳经销商0138",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -4645.98,
        "sales_change_rate": -0.7120559593179191,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0154",
        "customer_name": "广州经销商0154",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 9941.489999999994,
        "inventory_change_rate": 0.3700728867314877,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0162",
        "customer_name": "厦门经销商0162",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -3406.4900000000002,
        "sales_change_rate": -0.5907440292450802,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0186",
        "customer_name": "深圳经销商0186",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 21920.19,
        "inventory_change_rate": 1.3254935183203143,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0202",
        "customer_name": "深圳经销商0202",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -5016.109999999999,
        "sales_change_rate": -0.37015464834234707,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0210",
        "customer_name": "佛山经销商0210",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 15019.269999999997,
        "inventory_change_rate": 0.46517131494093233,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0250",
        "customer_name": "深圳经销商0250",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -5495.399999999998,
        "sales_change_rate": -0.36599912486288505,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0282",
        "customer_name": "广州经销商0282",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 37837.759999999995,
        "inventory_change_rate": 1.7727469928514334,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0314",
        "customer_name": "东莞经销商0314",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -2295.1699999999996,
        "sales_change_rate": -0.5148348949208962,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0322",
        "customer_name": "厦门经销商0322",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 34676.49,
        "inventory_change_rate": 2.2234918896528546,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0338",
        "customer_name": "佛山经销商0338",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -9375.320000000002,
        "sales_change_rate": -0.40592285087964275,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0346",
        "customer_name": "厦门经销商0346",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 16793.070000000003,
        "inventory_change_rate": 1.930131441023944,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0354",
        "customer_name": "厦门经销商0354",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 43499.65,
        "inventory_change_rate": 8.128405549036168,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0394",
        "customer_name": "佛山经销商0394",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -1352.1299999999997,
        "sales_change_rate": -0.2830867728279575,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0402",
        "customer_name": "佛山经销商0402",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -6062.279999999999,
        "sales_change_rate": -0.38663609606143035,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0426",
        "customer_name": "东莞经销商0426",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 20416.370000000003,
        "inventory_change_rate": 0.5768374139640383,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0450",
        "customer_name": "深圳经销商0450",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 9565.57,
        "inventory_change_rate": 0.4545708137782111,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0458",
        "customer_name": "厦门经销商0458",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -3873.359999999999,
        "sales_change_rate": -0.4902354379561119,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0466",
        "customer_name": "厦门经销商0466",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -6419.05,
        "sales_change_rate": -0.9502509951725434,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0482",
        "customer_name": "广州经销商0482",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "销售额下降",
        "sales_change": -1643.0699999999997,
        "sales_change_rate": -0.3429678922254182,
        "inventory_change": null,
        "inventory_change_rate": null,
        "expense_change_pp": null
      },
      {
        "customer_id": "C0498",
        "customer_name": "东莞经销商0498",
        "risk_level": "中风险",
        "follow_up_priority": "常规关注",
        "risk_signal_count": 1,
        "risk_reasons": "库存金额上升",
        "sales_change": null,
        "sales_change_rate": null,
        "inventory_change": 22831.639999999996,
        "inventory_change_rate": 0.9839230845475267,
        "expense_change_pp": null
      }
    ]
  },
  "product_performance": {
    "top_growth_products": [
      {
        "product_id": "P054",
        "product_name": "休闲食品SKU054",
        "series": "膨化系列",
        "flavor": "原味",
        "spec": "120g",
        "sales_aug": 1753.13,
        "sales_sep": 12858.02,
        "sales_change": 11104.89,
        "growth_rate": 6.3343220411492585,
        "gross_margin_aug": 0.3713643597451415,
        "gross_margin_sep": 0.3781453131975219,
        "gross_margin_change": 0.006780953452380445,
        "sales_share_aug": 0.0032556518372539177,
        "sales_share_sep": 0.024741905173380395
      },
      {
        "product_id": "P034",
        "product_name": "休闲食品SKU034",
        "series": "膨化系列",
        "flavor": "番茄",
        "spec": "90g",
        "sales_aug": 3552.72,
        "sales_sep": 14511.140000000001,
        "sales_change": 10958.420000000002,
        "growth_rate": 3.084515526132091,
        "gross_margin_aug": 0.28202898061203807,
        "gross_margin_sep": 0.27505144323602426,
        "gross_margin_change": -0.006977537376013809,
        "sales_share_aug": 0.006597582264434889,
        "sales_share_sep": 0.027922903358187902
      },
      {
        "product_id": "P057",
        "product_name": "休闲食品SKU057",
        "series": "辣味系列",
        "flavor": "海苔",
        "spec": "90g",
        "sales_aug": 5011.389999999999,
        "sales_sep": 15145.34,
        "sales_change": 10133.95,
        "growth_rate": 2.022183466064306,
        "gross_margin_aug": 0.39944805732541255,
        "gross_margin_sep": 0.40310352887422807,
        "gross_margin_change": 0.0036554715488155143,
        "sales_share_aug": 0.00930640686126865,
        "sales_share_sep": 0.029143255812217203
      },
      {
        "product_id": "P061",
        "product_name": "休闲食品SKU061",
        "series": "经典系列",
        "flavor": "海苔",
        "spec": "120g",
        "sales_aug": 5896.8,
        "sales_sep": 15934.829999999996,
        "sales_change": 10038.029999999995,
        "growth_rate": 1.702284289784289,
        "gross_margin_aug": 0.3164835164835166,
        "gross_margin_sep": 0.29160461705584545,
        "gross_margin_change": -0.02487889942767113,
        "sales_share_aug": 0.010950658396079527,
        "sales_share_sep": 0.03066242336020142
      },
      {
        "product_id": "P004",
        "product_name": "休闲食品SKU004",
        "series": "膨化系列",
        "flavor": "原味",
        "spec": "40g",
        "sales_aug": 747.77,
        "sales_sep": 7987.66,
        "sales_change": 7239.889999999999,
        "growth_rate": 9.681974403894245,
        "gross_margin_aug": 0.2033379247629618,
        "gross_margin_sep": 0.25208884704656936,
        "gross_margin_change": 0.048750922283607556,
        "sales_share_aug": 0.0013886470337872046,
        "sales_share_sep": 0.0153701679012168
      }
    ],
    "top_decline_products": [
      {
        "product_id": "P087",
        "product_name": "休闲食品SKU087",
        "series": "辣味系列",
        "flavor": "原味",
        "spec": "90g",
        "sales_aug": 15475.259999999998,
        "sales_sep": 3639.7,
        "sales_change": -11835.559999999998,
        "growth_rate": -0.7648052439829767,
        "gross_margin_aug": 0.4256729773845479,
        "gross_margin_sep": 0.418718575706789,
        "gross_margin_change": -0.0069544016777589035,
        "sales_share_aug": 0.028738347213830152,
        "sales_share_sep": 0.007003653148739278
      },
      {
        "product_id": "P094",
        "product_name": "休闲食品SKU094",
        "series": "膨化系列",
        "flavor": "香辣",
        "spec": "70g",
        "sales_aug": 15625.42,
        "sales_sep": 4143.95,
        "sales_change": -11481.470000000001,
        "growth_rate": -0.7347943287284439,
        "gross_margin_aug": 0.38491253355109817,
        "gross_margin_sep": 0.375837063671135,
        "gross_margin_change": -0.00907546987996316,
        "sales_share_aug": 0.029017201993499688,
        "sales_share_sep": 0.00797395072827929
      },
      {
        "product_id": "P028",
        "product_name": "休闲食品SKU028",
        "series": "烘焙系列",
        "flavor": "香辣",
        "spec": "60g",
        "sales_aug": 16223.060000000001,
        "sales_sep": 7730.99,
        "sales_change": -8492.070000000002,
        "growth_rate": -0.5234567338097745,
        "gross_margin_aug": 0.35676006869234306,
        "gross_margin_sep": 0.3171430825806268,
        "gross_margin_change": -0.03961698611171627,
        "sales_share_aug": 0.030127049959147664,
        "sales_share_sep": 0.01487627344461683
      },
      {
        "product_id": "P066",
        "product_name": "休闲食品SKU066",
        "series": "经典系列",
        "flavor": "香辣",
        "spec": "90g",
        "sales_aug": 10422.16,
        "sales_sep": 2296.04,
        "sales_change": -8126.12,
        "growth_rate": -0.7796963393384865,
        "gross_margin_aug": 0.4004467404069789,
        "gross_margin_sep": 0.40837267643420844,
        "gross_margin_change": 0.007925936027229519,
        "sales_share_aug": 0.0193544827549322,
        "sales_share_sep": 0.004418130004019929
      },
      {
        "product_id": "P100",
        "product_name": "休闲食品SKU100",
        "series": "新品系列",
        "flavor": "原味",
        "spec": "60g",
        "sales_aug": 14519.310000000001,
        "sales_sep": 7506.01,
        "sales_change": -7013.300000000001,
        "growth_rate": -0.4830325959015959,
        "gross_margin_aug": 0.2996581793487432,
        "gross_margin_sep": 0.29914295344663805,
        "gross_margin_change": -0.0005152259021051764,
        "sales_share_aug": 0.026963099300770156,
        "sales_share_sep": 0.014443358125935796
      }
    ],
    "margin_attribution": {
      "mix_effect_pp": -0.6830520265945801,
      "margin_effect_pp": -0.07029546046694843,
      "total_margin_effect_pp": -0.7533474870615285,
      "negative_impact_top5": [
        {
          "product_id": "P087",
          "product_name": "休闲食品SKU087",
          "diagnosis_mix_effect_pp": -0.9176296038793573,
          "diagnosis_margin_effect_pp": -0.012428211364395609,
          "diagnosis_total_effect_pp": -0.930057815243753,
          "impact_type": "双重拖累",
          "product_priority": "高",
          "product_status": "正常销售"
        },
        {
          "product_id": "P094",
          "product_name": "休闲食品SKU094",
          "diagnosis_mix_effect_pp": -0.8004322462131332,
          "diagnosis_margin_effect_pp": -0.01678560461758112,
          "diagnosis_total_effect_pp": -0.8172178508307144,
          "impact_type": "双重拖累",
          "product_priority": "高",
          "product_status": "正常销售"
        },
        {
          "product_id": "P028",
          "product_name": "休闲食品SKU028",
          "diagnosis_mix_effect_pp": -0.5138773176251065,
          "diagnosis_margin_effect_pp": -0.08914480191340067,
          "diagnosis_total_effect_pp": -0.6030221195385072,
          "impact_type": "双重拖累",
          "product_priority": "高",
          "product_status": "正常销售"
        },
        {
          "product_id": "P066",
          "product_name": "休闲食品SKU066",
          "diagnosis_mix_effect_pp": -0.6040406060863563,
          "diagnosis_margin_effect_pp": 0.00942101039637774,
          "diagnosis_total_effect_pp": -0.5946195956899786,
          "impact_type": "结构负向、自身毛利率正向抵消",
          "product_priority": "高",
          "product_status": "正常销售"
        },
        {
          "product_id": "P016",
          "product_name": "休闲食品SKU016",
          "diagnosis_mix_effect_pp": -0.4213066438471779,
          "diagnosis_margin_effect_pp": -0.006821569191871603,
          "diagnosis_total_effect_pp": -0.4281282130390495,
          "impact_type": "双重拖累",
          "product_priority": "高",
          "product_status": "正常销售"
        }
      ],
      "mix_drag_top5": [
        {
          "product_id": "P087",
          "product_name": "休闲食品SKU087",
          "diagnosis_mix_effect_pp": -0.9176296038793573,
          "diagnosis_margin_effect_pp": -0.012428211364395609,
          "diagnosis_total_effect_pp": -0.930057815243753,
          "sales_share_aug": 0.028738347213830152,
          "sales_share_sep": 0.007003653148739278,
          "impact_type": "双重拖累",
          "product_priority": "高"
        },
        {
          "product_id": "P094",
          "product_name": "休闲食品SKU094",
          "diagnosis_mix_effect_pp": -0.8004322462131332,
          "diagnosis_margin_effect_pp": -0.01678560461758112,
          "diagnosis_total_effect_pp": -0.8172178508307144,
          "sales_share_aug": 0.029017201993499688,
          "sales_share_sep": 0.00797395072827929,
          "impact_type": "双重拖累",
          "product_priority": "高"
        },
        {
          "product_id": "P066",
          "product_name": "休闲食品SKU066",
          "diagnosis_mix_effect_pp": -0.6040406060863563,
          "diagnosis_margin_effect_pp": 0.00942101039637774,
          "diagnosis_total_effect_pp": -0.5946195956899786,
          "sales_share_aug": 0.0193544827549322,
          "sales_share_sep": 0.004418130004019929,
          "impact_type": "结构负向、自身毛利率正向抵消",
          "product_priority": "高"
        },
        {
          "product_id": "P028",
          "product_name": "休闲食品SKU028",
          "diagnosis_mix_effect_pp": -0.5138773176251065,
          "diagnosis_margin_effect_pp": -0.08914480191340067,
          "diagnosis_total_effect_pp": -0.6030221195385072,
          "sales_share_aug": 0.030127049959147664,
          "sales_share_sep": 0.01487627344461683,
          "impact_type": "双重拖累",
          "product_priority": "高"
        },
        {
          "product_id": "P098",
          "product_name": "休闲食品SKU098",
          "diagnosis_mix_effect_pp": -0.43982420079159606,
          "diagnosis_margin_effect_pp": 0.013733903009277109,
          "diagnosis_total_effect_pp": -0.42609029778231894,
          "sales_share_aug": 0.012499308944892883,
          "sales_share_sep": 0.0028942480701757696,
          "impact_type": "结构负向、自身毛利率正向抵消",
          "product_priority": "高"
        }
      ],
      "margin_drag_top5": [
        {
          "product_id": "P028",
          "product_name": "休闲食品SKU028",
          "diagnosis_mix_effect_pp": -0.5138773176251065,
          "diagnosis_margin_effect_pp": -0.08914480191340067,
          "diagnosis_total_effect_pp": -0.6030221195385072,
          "impact_type": "双重拖累",
          "product_priority": "高"
        },
        {
          "product_id": "P061",
          "product_name": "休闲食品SKU061",
          "diagnosis_mix_effect_pp": 0.5993245182899736,
          "diagnosis_margin_effect_pp": -0.051764383794498506,
          "diagnosis_total_effect_pp": 0.547560134495475,
          "impact_type": "结构正向、自身毛利率负向抵消",
          "product_priority": "高"
        },
        {
          "product_id": "P003",
          "product_name": "休闲食品SKU003",
          "diagnosis_mix_effect_pp": -0.18729110079419184,
          "diagnosis_margin_effect_pp": -0.02868917393777361,
          "diagnosis_total_effect_pp": -0.21598027473196546,
          "impact_type": "双重拖累",
          "product_priority": "关注"
        },
        {
          "product_id": "P038",
          "product_name": "休闲食品SKU038",
          "diagnosis_mix_effect_pp": 0.27753471735901253,
          "diagnosis_margin_effect_pp": -0.024078706308795803,
          "diagnosis_total_effect_pp": 0.2534560110502167,
          "impact_type": "结构正向、自身毛利率负向抵消",
          "product_priority": "关注"
        },
        {
          "product_id": "P082",
          "product_name": "休闲食品SKU082",
          "diagnosis_mix_effect_pp": -0.13722801295141956,
          "diagnosis_margin_effect_pp": -0.02029657866791177,
          "diagnosis_total_effect_pp": -0.15752459161933133,
          "impact_type": "双重拖累",
          "product_priority": "关注"
        }
      ],
      "positive_impact_top5": [
        {
          "product_id": "P054",
          "product_name": "休闲食品SKU054",
          "diagnosis_mix_effect_pp": 0.8052077355361682,
          "diagnosis_margin_effect_pp": 0.009492506543473955,
          "diagnosis_total_effect_pp": 0.8147002420796422,
          "impact_type": "双重正向",
          "product_priority": "高"
        },
        {
          "product_id": "P057",
          "product_name": "休闲食品SKU057",
          "diagnosis_mix_effect_pp": 0.796004729539322,
          "diagnosis_margin_effect_pp": 0.00702758239822407,
          "diagnosis_total_effect_pp": 0.8030323119375461,
          "impact_type": "双重正向",
          "product_priority": "高"
        },
        {
          "product_id": "P034",
          "product_name": "休闲食品SKU034",
          "diagnosis_mix_effect_pp": 0.5939959456801976,
          "diagnosis_margin_effect_pp": -0.012043398933499892,
          "diagnosis_total_effect_pp": 0.5819525467466977,
          "impact_type": "结构正向、自身毛利率负向抵消",
          "product_priority": "高"
        },
        {
          "product_id": "P061",
          "product_name": "休闲食品SKU061",
          "diagnosis_mix_effect_pp": 0.5993245182899736,
          "diagnosis_margin_effect_pp": -0.051764383794498506,
          "diagnosis_total_effect_pp": 0.547560134495475,
          "impact_type": "结构正向、自身毛利率负向抵消",
          "product_priority": "高"
        },
        {
          "product_id": "P088",
          "product_name": "休闲食品SKU088",
          "diagnosis_mix_effect_pp": 0.4731009630512475,
          "diagnosis_margin_effect_pp": 0.013923757004460127,
          "diagnosis_total_effect_pp": 0.4870247200557076,
          "impact_type": "双重正向",
          "product_priority": "高"
        }
      ]
    }
  },
  "data_checks": {
    "quality_check_table_count": 6,
    "customer_reconciliation_passed": true,
    "anomaly_count": 48
  },
  "entity_findings": [
    {
      "entity_id": "REGION",
      "entity": "大区",
      "categories": [
        "整体经营"
      ],
      "evidence": [
        {
          "finding": "大区销售额环比变化",
          "metric": "销售额环比增长率",
          "value": -3.49,
          "evidence": "上月销售额：538488.17；本月销售额：519685.93；变化额：-18802.24",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "C0274",
      "entity": "深圳经销商0274",
      "categories": [
        "客户销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长贡献客户",
          "metric": "销售额变化",
          "value": 15275.56,
          "evidence": "Aug-26销售额：11710.29；Sep-26销售额：26985.85；增长贡献：16.05%",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "C0194",
      "entity": "广州经销商0194",
      "categories": [
        "客户销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长贡献客户",
          "metric": "销售额变化",
          "value": 8084.15,
          "evidence": "Aug-26销售额：7019.77；Sep-26销售额：15103.92；增长贡献：8.49%",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "C0122",
      "entity": "广州经销商0122",
      "categories": [
        "客户销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长贡献客户",
          "metric": "销售额变化",
          "value": 7896.03,
          "evidence": "Aug-26销售额：3946.55；Sep-26销售额：11842.58；增长贡献：8.29%",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "C0354",
      "entity": "厦门经销商0354",
      "categories": [
        "客户销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长贡献客户",
          "metric": "销售额变化",
          "value": 5957.33,
          "evidence": "Aug-26销售额：8387.31；Sep-26销售额：14344.64；增长贡献：6.26%",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "C0490",
      "entity": "广州经销商0490",
      "categories": [
        "客户销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长贡献客户",
          "metric": "销售额变化",
          "value": 5008.65,
          "evidence": "Aug-26销售额：3833.42；Sep-26销售额：8842.07；增长贡献：5.26%",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "C0338",
      "entity": "佛山经销商0338",
      "categories": [
        "客户销售下降"
      ],
      "evidence": [
        {
          "finding": "主要销售下降拖累客户",
          "metric": "销售额变化",
          "value": -9375.32,
          "evidence": "Aug-26销售额：23096.31；Sep-26销售额：13720.99；下降贡献：8.22%",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0378",
      "entity": "东莞经销商0378",
      "categories": [
        "客户销售下降",
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "主要销售下降拖累客户",
          "metric": "销售额变化",
          "value": -9279.51,
          "evidence": "Aug-26销售额：13476.65；Sep-26销售额：4197.14；下降贡献：8.14%",
          "priority": "高"
        },
        {
          "finding": "销售下降且库存上升",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "销售额下降、库存金额上升",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0466",
      "entity": "厦门经销商0466",
      "categories": [
        "客户销售下降"
      ],
      "evidence": [
        {
          "finding": "主要销售下降拖累客户",
          "metric": "销售额变化",
          "value": -6419.05,
          "evidence": "Aug-26销售额：6755.11；Sep-26销售额：336.06；下降贡献：5.63%",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0402",
      "entity": "佛山经销商0402",
      "categories": [
        "客户销售下降"
      ],
      "evidence": [
        {
          "finding": "主要销售下降拖累客户",
          "metric": "销售额变化",
          "value": -6062.28,
          "evidence": "Aug-26销售额：15679.55；Sep-26销售额：9617.27；下降贡献：5.32%",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0242",
      "entity": "佛山经销商0242",
      "categories": [
        "客户销售下降",
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "主要销售下降拖累客户",
          "metric": "销售额变化",
          "value": -5599.17,
          "evidence": "Aug-26销售额：8907.23；Sep-26销售额：3308.06；下降贡献：4.91%",
          "priority": "高"
        },
        {
          "finding": "销售下降且库存上升",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "销售额下降、库存金额上升",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P054",
      "entity": "休闲食品SKU054",
      "categories": [
        "产品毛利率改善",
        "产品销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长产品",
          "metric": "销售额变化",
          "value": 11104.89,
          "evidence": "Aug-26销售额：1753.13；Sep-26销售额：12858.02",
          "priority": "关注"
        },
        {
          "finding": "产品对整体毛利率形成正向贡献",
          "metric": "毛利率影响（百分点）",
          "value": 0.8147,
          "evidence": "结构效应：0.8052个百分点；自身毛利率效应：0.0095个百分点；影响类型：双重正向",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P034",
      "entity": "休闲食品SKU034",
      "categories": [
        "产品毛利率改善",
        "产品销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长产品",
          "metric": "销售额变化",
          "value": 10958.42,
          "evidence": "Aug-26销售额：3552.72；Sep-26销售额：14511.14",
          "priority": "关注"
        },
        {
          "finding": "产品对整体毛利率形成正向贡献",
          "metric": "毛利率影响（百分点）",
          "value": 0.582,
          "evidence": "结构效应：0.5940个百分点；自身毛利率效应：-0.0120个百分点；影响类型：结构正向、自身毛利率负向抵消",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P057",
      "entity": "休闲食品SKU057",
      "categories": [
        "产品毛利率改善",
        "产品销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长产品",
          "metric": "销售额变化",
          "value": 10133.95,
          "evidence": "Aug-26销售额：5011.39；Sep-26销售额：15145.34",
          "priority": "关注"
        },
        {
          "finding": "产品对整体毛利率形成正向贡献",
          "metric": "毛利率影响（百分点）",
          "value": 0.803,
          "evidence": "结构效应：0.7960个百分点；自身毛利率效应：0.0070个百分点；影响类型：双重正向",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P061",
      "entity": "休闲食品SKU061",
      "categories": [
        "产品毛利率改善",
        "产品盈利分析",
        "产品销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长产品",
          "metric": "销售额变化",
          "value": 10038.03,
          "evidence": "Aug-26销售额：5896.80；Sep-26销售额：15934.83",
          "priority": "关注"
        },
        {
          "finding": "产品自身毛利率下降造成拖累",
          "metric": "自身毛利率效应（百分点）",
          "value": -0.0518,
          "evidence": "Aug-26产品毛利率：31.65%；Sep-26产品毛利率：29.16%；毛利率实际变化：-2.4879个百分点；结构效应：0.5993个百分点",
          "priority": "高"
        },
        {
          "finding": "产品对整体毛利率形成正向贡献",
          "metric": "毛利率影响（百分点）",
          "value": 0.5476,
          "evidence": "结构效应：0.5993个百分点；自身毛利率效应：-0.0518个百分点；影响类型：结构正向、自身毛利率负向抵消",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P004",
      "entity": "休闲食品SKU004",
      "categories": [
        "产品销售增长"
      ],
      "evidence": [
        {
          "finding": "主要销售增长产品",
          "metric": "销售额变化",
          "value": 7239.89,
          "evidence": "Aug-26销售额：747.77；Sep-26销售额：7987.66",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P087",
      "entity": "休闲食品SKU087",
      "categories": [
        "产品毛利率归因",
        "产品盈利风险",
        "产品结构分析",
        "产品销售下降"
      ],
      "evidence": [
        {
          "finding": "主要销售下降产品",
          "metric": "销售额变化",
          "value": -11835.56,
          "evidence": "Aug-26销售额：15475.26；Sep-26销售额：3639.70",
          "priority": "关注"
        },
        {
          "finding": "整体毛利率主要拖累产品",
          "metric": "毛利率影响（百分点）",
          "value": -0.9301,
          "evidence": "结构/销售组合效应：-0.9176个百分点；自身毛利率效应：-0.0124个百分点；影响类型：双重拖累",
          "priority": "高"
        },
        {
          "finding": "产品结构变化造成毛利率拖累",
          "metric": "产品结构/销售组合效应（百分点）",
          "value": -0.9176,
          "evidence": "Aug-26销售占比：2.87%；Sep-26销售占比：0.70%；自身毛利率效应：-0.0124个百分点；产品状态：正常销售",
          "priority": "高"
        },
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.9301,
          "evidence": "结构效应：-0.9176个百分点；自身毛利率效应：-0.0124个百分点；毛利率总影响：-0.9301个百分点",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P094",
      "entity": "休闲食品SKU094",
      "categories": [
        "产品毛利率归因",
        "产品盈利风险",
        "产品结构分析",
        "产品销售下降"
      ],
      "evidence": [
        {
          "finding": "主要销售下降产品",
          "metric": "销售额变化",
          "value": -11481.47,
          "evidence": "Aug-26销售额：15625.42；Sep-26销售额：4143.95",
          "priority": "关注"
        },
        {
          "finding": "整体毛利率主要拖累产品",
          "metric": "毛利率影响（百分点）",
          "value": -0.8172,
          "evidence": "结构/销售组合效应：-0.8004个百分点；自身毛利率效应：-0.0168个百分点；影响类型：双重拖累",
          "priority": "高"
        },
        {
          "finding": "产品结构变化造成毛利率拖累",
          "metric": "产品结构/销售组合效应（百分点）",
          "value": -0.8004,
          "evidence": "Aug-26销售占比：2.90%；Sep-26销售占比：0.80%；自身毛利率效应：-0.0168个百分点；产品状态：正常销售",
          "priority": "高"
        },
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.8172,
          "evidence": "结构效应：-0.8004个百分点；自身毛利率效应：-0.0168个百分点；毛利率总影响：-0.8172个百分点",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P028",
      "entity": "休闲食品SKU028",
      "categories": [
        "产品毛利率归因",
        "产品盈利分析",
        "产品盈利风险",
        "产品结构分析",
        "产品销售下降"
      ],
      "evidence": [
        {
          "finding": "主要销售下降产品",
          "metric": "销售额变化",
          "value": -8492.07,
          "evidence": "Aug-26销售额：16223.06；Sep-26销售额：7730.99",
          "priority": "关注"
        },
        {
          "finding": "整体毛利率主要拖累产品",
          "metric": "毛利率影响（百分点）",
          "value": -0.603,
          "evidence": "结构/销售组合效应：-0.5139个百分点；自身毛利率效应：-0.0891个百分点；影响类型：双重拖累",
          "priority": "高"
        },
        {
          "finding": "产品结构变化造成毛利率拖累",
          "metric": "产品结构/销售组合效应（百分点）",
          "value": -0.5139,
          "evidence": "Aug-26销售占比：3.01%；Sep-26销售占比：1.49%；自身毛利率效应：-0.0891个百分点；产品状态：正常销售",
          "priority": "高"
        },
        {
          "finding": "产品自身毛利率下降造成拖累",
          "metric": "自身毛利率效应（百分点）",
          "value": -0.0891,
          "evidence": "Aug-26产品毛利率：35.68%；Sep-26产品毛利率：31.71%；毛利率实际变化：-3.9617个百分点；结构效应：-0.5139个百分点",
          "priority": "高"
        },
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.603,
          "evidence": "结构效应：-0.5139个百分点；自身毛利率效应：-0.0891个百分点；毛利率总影响：-0.6030个百分点",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P066",
      "entity": "休闲食品SKU066",
      "categories": [
        "产品毛利率归因",
        "产品结构分析",
        "产品销售下降"
      ],
      "evidence": [
        {
          "finding": "主要销售下降产品",
          "metric": "销售额变化",
          "value": -8126.12,
          "evidence": "Aug-26销售额：10422.16；Sep-26销售额：2296.04",
          "priority": "关注"
        },
        {
          "finding": "整体毛利率主要拖累产品",
          "metric": "毛利率影响（百分点）",
          "value": -0.5946,
          "evidence": "结构/销售组合效应：-0.6040个百分点；自身毛利率效应：0.0094个百分点；影响类型：结构负向、自身毛利率正向抵消",
          "priority": "高"
        },
        {
          "finding": "产品结构变化造成毛利率拖累",
          "metric": "产品结构/销售组合效应（百分点）",
          "value": -0.604,
          "evidence": "Aug-26销售占比：1.94%；Sep-26销售占比：0.44%；自身毛利率效应：0.0094个百分点；产品状态：正常销售",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P100",
      "entity": "休闲食品SKU100",
      "categories": [
        "产品盈利风险",
        "产品销售下降"
      ],
      "evidence": [
        {
          "finding": "主要销售下降产品",
          "metric": "销售额变化",
          "value": -7013.3,
          "evidence": "Aug-26销售额：14519.31；Sep-26销售额：7506.01",
          "priority": "关注"
        },
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.3759,
          "evidence": "结构效应：-0.3748个百分点；自身毛利率效应：-0.0011个百分点；毛利率总影响：-0.3759个百分点",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "PRODUCT_PORTFOLIO",
      "entity": "整体产品组合",
      "categories": [
        "盈利分析"
      ],
      "evidence": [
        {
          "finding": "产品结构/销售组合效应",
          "metric": "毛利率影响（百分点）",
          "value": -0.6831,
          "evidence": "按业务诊断口径，将单月无销售产品的归因总影响归入结构/销售组合效应。",
          "priority": "高"
        },
        {
          "finding": "产品自身毛利率效应",
          "metric": "毛利率影响（百分点）",
          "value": -0.0703,
          "evidence": "仅对两个月均有销售的产品解释自身毛利率变化；无销售月份不视为真实毛利率0%。",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P016",
      "entity": "休闲食品SKU016",
      "categories": [
        "产品毛利率归因",
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "整体毛利率主要拖累产品",
          "metric": "毛利率影响（百分点）",
          "value": -0.4281,
          "evidence": "结构/销售组合效应：-0.4213个百分点；自身毛利率效应：-0.0068个百分点；影响类型：双重拖累",
          "priority": "高"
        },
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.4281,
          "evidence": "结构效应：-0.4213个百分点；自身毛利率效应：-0.0068个百分点；毛利率总影响：-0.4281个百分点",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P098",
      "entity": "休闲食品SKU098",
      "categories": [
        "产品结构分析"
      ],
      "evidence": [
        {
          "finding": "产品结构变化造成毛利率拖累",
          "metric": "产品结构/销售组合效应（百分点）",
          "value": -0.4398,
          "evidence": "Aug-26销售占比：1.25%；Sep-26销售占比：0.29%；自身毛利率效应：0.0137个百分点；产品状态：正常销售",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P003",
      "entity": "休闲食品SKU003",
      "categories": [
        "产品盈利分析",
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品自身毛利率下降造成拖累",
          "metric": "自身毛利率效应（百分点）",
          "value": -0.0287,
          "evidence": "Aug-26产品毛利率：43.35%；Sep-26产品毛利率：42.30%；毛利率实际变化：-1.0449个百分点；结构效应：-0.1873个百分点",
          "priority": "关注"
        },
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.216,
          "evidence": "结构效应：-0.1873个百分点；自身毛利率效应：-0.0287个百分点；毛利率总影响：-0.2160个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P038",
      "entity": "休闲食品SKU038",
      "categories": [
        "产品盈利分析"
      ],
      "evidence": [
        {
          "finding": "产品自身毛利率下降造成拖累",
          "metric": "自身毛利率效应（百分点）",
          "value": -0.0241,
          "evidence": "Aug-26产品毛利率：32.96%；Sep-26产品毛利率：31.65%；毛利率实际变化：-1.3135个百分点；结构效应：0.2775个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P082",
      "entity": "休闲食品SKU082",
      "categories": [
        "产品盈利分析",
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品自身毛利率下降造成拖累",
          "metric": "自身毛利率效应（百分点）",
          "value": -0.0203,
          "evidence": "Aug-26产品毛利率：47.77%；Sep-26产品毛利率：45.98%；毛利率实际变化：-1.7870个百分点；结构效应：-0.1372个百分点",
          "priority": "关注"
        },
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.1575,
          "evidence": "结构效应：-0.1372个百分点；自身毛利率效应：-0.0203个百分点；毛利率总影响：-0.1575个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P053",
      "entity": "休闲食品SKU053",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.4018,
          "evidence": "结构效应：-0.3993个百分点；自身毛利率效应：-0.0025个百分点；毛利率总影响：-0.4018个百分点",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P083",
      "entity": "休闲食品SKU083",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.3921,
          "evidence": "结构效应：-0.3845个百分点；自身毛利率效应：-0.0076个百分点；毛利率总影响：-0.3921个百分点",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P019",
      "entity": "休闲食品SKU019",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.3828,
          "evidence": "结构效应：-0.3716个百分点；自身毛利率效应：-0.0113个百分点；毛利率总影响：-0.3828个百分点",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P065",
      "entity": "休闲食品SKU065",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.335,
          "evidence": "结构效应：-0.3284个百分点；自身毛利率效应：-0.0066个百分点；毛利率总影响：-0.3350个百分点",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "P024",
      "entity": "休闲食品SKU024",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.2682,
          "evidence": "结构效应：-0.2582个百分点；自身毛利率效应：-0.0099个百分点；毛利率总影响：-0.2682个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P059",
      "entity": "休闲食品SKU059",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.2599,
          "evidence": "结构效应：-0.2565个百分点；自身毛利率效应：-0.0034个百分点；毛利率总影响：-0.2599个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P055",
      "entity": "休闲食品SKU055",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.2558,
          "evidence": "结构效应：-0.2496个百分点；自身毛利率效应：-0.0063个百分点；毛利率总影响：-0.2558个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P058",
      "entity": "休闲食品SKU058",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.2358,
          "evidence": "结构效应：-0.2178个百分点；自身毛利率效应：-0.0180个百分点；毛利率总影响：-0.2358个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P014",
      "entity": "休闲食品SKU014",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.2147,
          "evidence": "结构效应：-0.2016个百分点；自身毛利率效应：-0.0131个百分点；毛利率总影响：-0.2147个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P042",
      "entity": "休闲食品SKU042",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.1966,
          "evidence": "结构效应：-0.1942个百分点；自身毛利率效应：-0.0023个百分点；毛利率总影响：-0.1966个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P067",
      "entity": "休闲食品SKU067",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.1468,
          "evidence": "结构效应：-0.1408个百分点；自身毛利率效应：-0.0060个百分点；毛利率总影响：-0.1468个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P099",
      "entity": "休闲食品SKU099",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.1133,
          "evidence": "结构效应：-0.1085个百分点；自身毛利率效应：-0.0048个百分点；毛利率总影响：-0.1133个百分点",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P025",
      "entity": "休闲食品SKU025",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0965,
          "evidence": "结构效应：-0.0864个百分点；自身毛利率效应：-0.0100个百分点；毛利率总影响：-0.0965个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P020",
      "entity": "休闲食品SKU020",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0959,
          "evidence": "结构效应：-0.0856个百分点；自身毛利率效应：-0.0102个百分点；毛利率总影响：-0.0959个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P069",
      "entity": "休闲食品SKU069",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0845,
          "evidence": "结构效应：-0.0803个百分点；自身毛利率效应：-0.0042个百分点；毛利率总影响：-0.0845个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P052",
      "entity": "休闲食品SKU052",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.074,
          "evidence": "结构效应：-0.0722个百分点；自身毛利率效应：-0.0017个百分点；毛利率总影响：-0.0740个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P022",
      "entity": "休闲食品SKU022",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0708,
          "evidence": "结构效应：-0.0574个百分点；自身毛利率效应：-0.0135个百分点；毛利率总影响：-0.0708个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P018",
      "entity": "休闲食品SKU018",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0698,
          "evidence": "结构效应：-0.0667个百分点；自身毛利率效应：-0.0031个百分点；毛利率总影响：-0.0698个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P011",
      "entity": "休闲食品SKU011",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0687,
          "evidence": "结构效应：-0.0588个百分点；自身毛利率效应：-0.0099个百分点；毛利率总影响：-0.0687个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P049",
      "entity": "休闲食品SKU049",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0496,
          "evidence": "结构效应：-0.0455个百分点；自身毛利率效应：-0.0041个百分点；毛利率总影响：-0.0496个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P029",
      "entity": "休闲食品SKU029",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0462,
          "evidence": "结构效应：-0.0375个百分点；自身毛利率效应：-0.0087个百分点；毛利率总影响：-0.0462个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P021",
      "entity": "休闲食品SKU021",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0202,
          "evidence": "结构效应：-0.0086个百分点；自身毛利率效应：-0.0116个百分点；毛利率总影响：-0.0202个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P005",
      "entity": "休闲食品SKU005",
      "categories": [
        "产品盈利风险"
      ],
      "evidence": [
        {
          "finding": "产品结构与自身毛利率双重拖累",
          "metric": "毛利率总影响（百分点）",
          "value": -0.0187,
          "evidence": "结构效应：-0.0161个百分点；自身毛利率效应：-0.0027个百分点；毛利率总影响：-0.0187个百分点",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "P088",
      "entity": "休闲食品SKU088",
      "categories": [
        "产品毛利率改善"
      ],
      "evidence": [
        {
          "finding": "产品对整体毛利率形成正向贡献",
          "metric": "毛利率影响（百分点）",
          "value": 0.487,
          "evidence": "结构效应：0.4731个百分点；自身毛利率效应：0.0139个百分点；影响类型：双重正向",
          "priority": "关注"
        }
      ]
    },
    {
      "entity_id": "P095",
      "entity": "休闲食品SKU095",
      "categories": [
        "产品销售状态"
      ],
      "evidence": [
        {
          "finding": "当月无销售，需核查产品状态",
          "metric": "Sep-26销售占比",
          "value": 0,
          "evidence": "Aug-26销售占比：0.29%；Sep-26无销售；产品毛利率不可观察；归因总影响：-0.1342个百分点。不能将技术填充的0解释为真实毛利率下降。",
          "priority": "常规"
        }
      ]
    },
    {
      "entity_id": "C0058",
      "entity": "佛山经销商0058",
      "categories": [
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "销售下降且库存上升",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "销售额下降、库存金额上升",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0234",
      "entity": "厦门经销商0234",
      "categories": [
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "销售下降且库存上升",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "销售额下降、库存金额上升",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0258",
      "entity": "东莞经销商0258",
      "categories": [
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "销售下降且库存上升",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "销售额下降、库存金额上升",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0298",
      "entity": "深圳经销商0298",
      "categories": [
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "销售下降且库存上升",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "销售额下降、库存金额上升",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0442",
      "entity": "东莞经销商0442",
      "categories": [
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "销售下降且库存上升",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "销售额下降、库存金额上升",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0474",
      "entity": "佛山经销商0474",
      "categories": [
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "销售下降且库存上升",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "销售额下降、库存金额上升",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0002",
      "entity": "深圳经销商0002",
      "categories": [
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "存在多项经营风险信号",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "库存金额上升、费用率上升",
          "priority": "高"
        }
      ]
    },
    {
      "entity_id": "C0042",
      "entity": "厦门经销商0042",
      "categories": [
        "客户风险"
      ],
      "evidence": [
        {
          "finding": "存在多项经营风险信号",
          "metric": "风险等级",
          "value": "高风险",
          "evidence": "销售额下降、费用率上升",
          "priority": "高"
        }
      ]
    }
  ],
  "diagnosis_notes": {
    "finding_count": 84,
    "finding_count_is_unique_issue_count": false,
    "finding_explanation": "同一个客户或产品可能出现在多个分析类别中，不同发现代表不同分析角度，不能直接将发现条数视为独立经营问题数量。",
    "product_margin_method": "采用产品结构效应与产品自身毛利率效应进行对称分解。",
    "no_sales_product_warning": "当月无销售产品的毛利率不可观察。对于单月无销售产品，业务诊断口径将其归因总影响全部归入结构/销售组合效应，自身毛利率效应不作解释。不得将技术填充的0解释为真实毛利率。",
    "priority_method": "产品优先级根据毛利率总影响绝对值初步分级：大于等于0.30个百分点为高，大于等于0.10个百分点且小于0.30个百分点为关注，小于0.10个百分点为常规。该规则为项目初始规则，不代表企业官方标准。",
    "risk_interpretation": "销售下降与库存上升属于潜在库存压力信号，不能单独据此认定发生库存积压。实际经营原因仍需结合进货、出货、退货及终端动销核实。",
    "data_reconciliation": "通过"
  }
}
