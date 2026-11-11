# FMCG AI Business Analyst - 数据字典

## 数据范围

- 模拟企业：Demo FMCG
- 数据周期：2025-10 至 2026-09
- 数据类型：模拟数据，不代表真实企业经营情况

## 表结构

### dim_customer
客户主数据：customer_id, customer_name, region, city,
channel, customer_level, build_date, status

### dim_product
产品主数据：product_id, product_name, series, flavor,
spec, unit_price, unit_cost, launch_date, product_status

### fact_sales
销售明细：order_id, order_date, customer_id, product_id,
quantity, discount_rate, unit_price, unit_cost,
sales_amount, cost_amount, gross_profit, month

### fact_inventory
库存快照：snapshot_date, customer_id, product_id,
inventory_qty, unit_cost, inventory_amount, month

### fact_target
客户月度目标：month, customer_id, target_amount

### fact_expense
客户月度费用：month, customer_id, expense_type,
expense_amount

## 核心指标口径

- 销售额 = SUM(sales_amount)
- 销售成本 = SUM(cost_amount)
- 毛利额 = 销售额 - 销售成本
- 毛利率 = 毛利额 / 销售额
- 目标达成率 = 实际销售额 / 销售目标
- 费用率 = 费用金额 / 销售额
- 扣除已记录费用后的贡献额 = 毛利额 - 费用金额

注意：费用数据只覆盖本项目模拟的三类费用，
不等于企业完整损益表。
