
-- =====================================================
-- 1. 各大区销售额、目标达成率、毛利率
-- =====================================================

WITH sales_by_customer AS (
    SELECT
        customer_id,
        SUM(sales_amount) AS sales_amount,
        SUM(cost_amount) AS cost_amount,
        SUM(gross_profit) AS gross_profit
    FROM fact_sales
    WHERE month = '2026-09'
    GROUP BY customer_id
),
customer_result AS (
    SELECT
        c.region,
        c.customer_id,
        COALESCE(s.sales_amount, 0) AS sales_amount,
        COALESCE(s.cost_amount, 0) AS cost_amount,
        COALESCE(s.gross_profit, 0) AS gross_profit,
        t.target_amount
    FROM dim_customer c
    LEFT JOIN sales_by_customer s
        ON c.customer_id = s.customer_id
    LEFT JOIN fact_target t
        ON c.customer_id = t.customer_id
        AND t.month = '2026-09'
)
SELECT
    region,
    SUM(sales_amount) AS sales_amount,
    SUM(target_amount) AS target_amount,
    ROUND(
        SUM(sales_amount) / NULLIF(SUM(target_amount), 0),
        4
    ) AS attainment_rate,
    ROUND(
        SUM(gross_profit) / NULLIF(SUM(sales_amount), 0),
        4
    ) AS gross_margin_rate
FROM customer_result
GROUP BY region
ORDER BY attainment_rate;


-- =====================================================

-- 2. 对比 2026-08 与 2026-09 各产品系列销售变化

WITH product_sales AS (
    SELECT
        p.series,
        SUM(
            CASE WHEN s.month = '2026-08'
                 THEN s.sales_amount ELSE 0 END
        ) AS sales_last_month,
        SUM(
            CASE WHEN s.month = '2026-09'
                 THEN s.sales_amount ELSE 0 END
        ) AS sales_current_month
    FROM fact_sales s
    JOIN dim_product p
        ON s.product_id = p.product_id
    WHERE s.month IN ('2026-08', '2026-09')
    GROUP BY p.series
)
SELECT
    series,
    sales_last_month,
    sales_current_month,
    sales_current_month - sales_last_month AS sales_change,
    ROUND(
        (sales_current_month - sales_last_month)
        / NULLIF(sales_last_month, 0),
        4
    ) AS mom_growth_rate
FROM product_sales
ORDER BY sales_change;


-- =====================================================
-- 3. 识别销售规模较高但毛利率较低的客户
-- =====================================================

WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales_amount) AS sales_amount,
        SUM(gross_profit) AS gross_profit
    FROM fact_sales
    WHERE month BETWEEN '2026-07' AND '2026-09'
    GROUP BY customer_id
),
customer_expense AS (
    SELECT
        customer_id,
        SUM(expense_amount) AS expense_amount
    FROM fact_expense
    WHERE month BETWEEN '2026-07' AND '2026-09'
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.customer_name,
    c.region,
    COALESCE(s.sales_amount, 0) AS sales_amount,
    COALESCE(s.gross_profit, 0) AS gross_profit,
    ROUND(
        s.gross_profit / NULLIF(s.sales_amount, 0),
        4
    ) AS gross_margin_rate,
    COALESCE(e.expense_amount, 0) AS expense_amount,
    ROUND(
        (s.gross_profit - COALESCE(e.expense_amount, 0))
        / NULLIF(s.sales_amount, 0),
        4
    ) AS contribution_rate
FROM dim_customer c
JOIN customer_sales s
    ON c.customer_id = s.customer_id
LEFT JOIN customer_expense e
    ON c.customer_id = e.customer_id
WHERE s.sales_amount > 50000
ORDER BY contribution_rate ASC
LIMIT 20;


-- =====================================================
-- 4. 识别最近三个月没有交易的客户
-- =====================================================

WITH recent_sales AS (
    SELECT
        customer_id,
        COUNT(DISTINCT month) AS active_months,
        SUM(sales_amount) AS recent_sales
    FROM fact_sales
    WHERE month BETWEEN '2026-07' AND '2026-09'
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.customer_name,
    c.region,
    COALESCE(s.active_months, 0) AS active_months,
    COALESCE(s.recent_sales, 0) AS recent_sales
FROM dim_customer c
LEFT JOIN recent_sales s
    ON c.customer_id = s.customer_id
WHERE COALESCE(s.active_months, 0) = 0
ORDER BY c.region, c.customer_id;


-- =====================================================
-- 5. 识别高库存、低动销 SKU
-- =====================================================

WITH latest_inventory AS (
    SELECT
        customer_id,
        product_id,
        inventory_qty,
        inventory_amount
    FROM fact_inventory
    WHERE snapshot_date = (
        SELECT MAX(snapshot_date)
        FROM fact_inventory
    )
),
recent_sales AS (
    SELECT
        customer_id,
        product_id,
        SUM(quantity) AS sales_qty
    FROM fact_sales
    WHERE month BETWEEN '2026-07' AND '2026-09'
    GROUP BY customer_id, product_id
)
SELECT
    c.region,
    c.customer_name,
    p.product_name,
    p.series,
    i.inventory_qty,
    i.inventory_amount,
    COALESCE(s.sales_qty, 0) AS recent_sales_qty,
    ROUND(
        i.inventory_qty
        / NULLIF(COALESCE(s.sales_qty, 0) / 3.0, 0),
        2
    ) AS estimated_stock_months
FROM latest_inventory i
JOIN dim_customer c
    ON i.customer_id = c.customer_id
JOIN dim_product p
    ON i.product_id = p.product_id
LEFT JOIN recent_sales s
    ON i.customer_id = s.customer_id
    AND i.product_id = s.product_id
WHERE i.inventory_qty >= 500
    AND COALESCE(s.sales_qty, 0) < 300
ORDER BY i.inventory_qty DESC
LIMIT 30;
