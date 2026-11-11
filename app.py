
import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path

from analysis.text_to_sql import (
    get_database_schema,
    generate_sql,
    execute_sql,
    analyze_result
)


# =====================================
# 一、页面配置
# =====================================

BASE_DIR = Path(__file__).parent
REPORT_DIR = BASE_DIR / "reports"

st.set_page_config(
    page_title="FMCG AI Business Analyst",
    page_icon="📊",
    layout="wide"
)


# =====================================
# 二、左侧导航栏
# =====================================

st.sidebar.title("📊 FMCG AI")
st.sidebar.caption("Business Analyst")
st.sidebar.divider()

page = st.sidebar.radio(
    "功能导航",
    ["智能问数", "经营分析", "异常检测"]
)

st.sidebar.divider()
st.sidebar.caption("AI 驱动的快消品经营分析平台")


# =====================================
# 三、智能问数
# =====================================

if page == "智能问数":

    st.title("💬 智能问数")

    st.write(
        "通过自然语言提问，让 AI 自动生成 SQL、查询数据并输出经营分析。"
    )

    st.divider()

    question = st.text_area(
        "请输入你的经营分析问题",
        placeholder="例如：查询2026年9月华南大区的销售额、毛利额和毛利率",
        height=100
    )

    if st.button("🚀 开始分析", type="primary"):

        if not question.strip():

            st.warning("请先输入经营分析问题。")

        else:

            try:

                # 1. 读取数据库结构
                with st.spinner("正在读取数据库结构..."):
                    schema = get_database_schema()

                # 2. AI 生成 SQL
                with st.spinner("AI 正在生成 SQL..."):
                    sql = generate_sql(question, schema)

                st.subheader("① AI 生成的 SQL")
                st.code(sql, language="sql")

                # 3. 执行 SQL
                with st.spinner("正在查询数据库..."):
                    result = execute_sql(sql)

                st.subheader("② 数据查询结果")

                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )

                st.success(
                    f"查询成功，共返回 {len(result)} 行数据。"
                )

                # 4. AI 分析结果
                with st.spinner("AI 正在生成经营分析..."):
                    analysis = analyze_result(question, result)

                st.subheader("③ AI 经营分析报告")
                st.markdown(analysis)

            except Exception as e:

                st.error(f"分析过程中出现问题：{e}")


# =====================================
# 四、经营分析
# =====================================

elif page == "经营分析":

    st.title("📈 经营分析")

    st.write(
        "从整体经营、产品表现和客户贡献三个维度分析业务表现。"
    )

    st.divider()

    try:

        # ---------------------------------
        # 1. 读取分析结果
        # ---------------------------------

        region_df = pd.read_csv(
            REPORT_DIR / "region_performance.csv"
        )

        product_df = pd.read_csv(
            REPORT_DIR / "product_profitability.csv"
        )

        customer_df = pd.read_csv(
            REPORT_DIR / "customer_analysis.csv"
        )

        # ---------------------------------
        # 2. 整体经营概览
        # ---------------------------------

        # 处理百分比字段
        for col in ["gross_margin", "achievement_rate"]:

            region_df[col] = pd.to_numeric(
                region_df[col]
                .astype(str)
                .str.replace("%", "", regex=False),
                errors="coerce"
            )

        latest = region_df.iloc[-1]

        st.subheader("一、整体经营概览")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "最新月份销售额",
            f"¥{latest['sales_amount']:,.0f}"
        )

        col2.metric(
            "最新月份毛利额",
            f"¥{latest['gross_profit']:,.0f}"
        )

        col3.metric(
            "最新月份毛利率",
            f"{latest['gross_margin']:.0f}%"
        )

        col4.metric(
            "最新月份目标达成率",
            f"{latest['achievement_rate']:.0f}%"
        )

        st.caption(
            f"数据月份：{latest['month']}"
        )

        st.divider()

        # ---------------------------------
        # 3. 月度经营趋势
        # ---------------------------------

        st.subheader("二、月度经营趋势")

        fig_sales = px.line(
            region_df,
            x="month",
            y=["sales_amount", "target_amount"],
            markers=True,
            title="月度销售额与目标趋势",
            labels={
                "month": "月份",
                "value": "金额（元）",
                "variable": "指标"
            }
        )

        st.plotly_chart(
            fig_sales,
            use_container_width=True,
            key="monthly_sales_trend"
        )

        fig_achievement = px.bar(
            region_df,
            x="month",
            y="achievement_rate",
            title="月度目标达成率",
            labels={
                "month": "月份",
                "achievement_rate": "达成率（%）"
            }
        )

        st.plotly_chart(
            fig_achievement,
            use_container_width=True,
            key="monthly_achievement"
        )

        st.divider()

        # ---------------------------------
        # 4. 产品表现分析
        # ---------------------------------

        st.subheader("三、产品表现分析")

        # 按产品系列汇总
        product_group = (
            product_df.groupby("series", as_index=False)
            .agg(
                sales_aug_total=("sales_aug", "sum"),
                sales_sep_total=("sales_sep", "sum"),
                gross_profit_aug_total=("gross_profit_aug", "sum"),
                gross_profit_sep_total=("gross_profit_sep", "sum")
            )
        )

        # 计算销售额变化
        product_group["sales_change"] = (
            product_group["sales_sep_total"]
            - product_group["sales_aug_total"]
        )

        # 计算销售额环比变化率
        product_group["sales_change_rate"] = (
            product_group["sales_change"]
            / product_group["sales_aug_total"].replace(0, float("nan"))
            * 100
        )

        # 按9月销售额排序
        product_group = product_group.sort_values(
            "sales_sep_total",
            ascending=False
        )

        # 转换成长表，绘制8月和9月对比图
        product_chart_df = product_group.melt(
            id_vars=["series"],
            value_vars=[
                "sales_aug_total",
                "sales_sep_total"
            ],
            var_name="month",
            value_name="sales_amount"
        )

        product_chart_df["month"] = product_chart_df["month"].map({
            "sales_aug_total": "8月",
            "sales_sep_total": "9月"
        })

        fig_product = px.bar(
            product_chart_df,
            x="series",
            y="sales_amount",
            color="month",
            barmode="group",
            title="各产品系列销售额对比",
            labels={
                "series": "产品系列",
                "sales_amount": "销售额（元）",
                "month": "月份"
            }
        )

        st.plotly_chart(
            fig_product,
            use_container_width=True,
            key="product_sales_comparison"
        )

        # 产品分析数据表
        product_display = product_group.rename(
            columns={
                "series": "产品系列",
                "sales_aug_total": "8月销售额",
                "sales_sep_total": "9月销售额",
                "gross_profit_aug_total": "8月毛利额",
                "gross_profit_sep_total": "9月毛利额",
                "sales_change": "销售额变化",
                "sales_change_rate": "销售额环比变化率（%）"
            }
        )

        # 数值格式处理
        product_display["销售额环比变化率（%）"] = (
            product_display["销售额环比变化率（%）"].round(2)
        )

        st.dataframe(
            product_display,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ---------------------------------
        # 5. 客户贡献分析
        # ---------------------------------

        st.subheader("四、客户贡献分析")

        customer_top10 = customer_df.nlargest(
            10,
            "sales_amount"
        ).copy()

        fig_customer = px.bar(
            customer_top10,
            x="sales_amount",
            y="customer_name",
            orientation="h",
            title="销售额 TOP 10 客户",
            labels={
                "sales_amount": "销售额（元）",
                "customer_name": "客户"
            }
        )

        fig_customer.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )

        st.plotly_chart(
            fig_customer,
            use_container_width=True,
            key="customer_sales_top10"
        )

        # 客户数据展示
        customer_display = customer_top10[
            [
                "customer_name",
                "sales_amount",
                "gross_profit",
                "gross_margin",
                "achievement_rate",
                "sales_contribution"
            ]
        ].copy()

        customer_display = customer_display.rename(
            columns={
                "customer_name": "客户名称",
                "sales_amount": "销售额",
                "gross_profit": "毛利额",
                "gross_margin": "毛利率",
                "achievement_rate": "目标达成率",
                "sales_contribution": "销售贡献率"
            }
        )

        # 将小数形式的比例转换为百分比
        for col in ["毛利率", "目标达成率", "销售贡献率"]:

            customer_display[col] = (
                customer_display[col] * 100
            ).round(2)

        st.dataframe(
            customer_display,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.error(f"经营分析模块加载失败：{e}")


# =====================================
# 五、异常检测
# =====================================


# =====================================
# 五、异常检测
# =====================================

elif page == "异常检测":

    st.title("⚠️ 异常检测")

    st.write(
        "自动识别经营异常，并结合客户销售、库存和费用表现评估客户风险。"
    )

    st.divider()

    try:

        # ---------------------------------
        # 1. 读取异常检测和客户风险数据
        # ---------------------------------

        anomaly_df = pd.read_csv(
            REPORT_DIR / "anomaly_detection.csv"
        )

        risk_df = pd.read_csv(
            REPORT_DIR / "customer_risk_assessment.csv"
        )

        # ---------------------------------
        # 2. 经营异常预警
        # ---------------------------------

        st.subheader("一、经营异常预警")

        total_anomalies = len(anomaly_df)

        anomaly_types = anomaly_df["anomaly_type"].nunique()

        high_anomalies = (
            (anomaly_df["severity"] == "高").sum()
            if "severity" in anomaly_df.columns else 0
        )

        medium_anomalies = (
            (anomaly_df["severity"] == "中").sum()
            if "severity" in anomaly_df.columns else 0
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("异常总数", f"{total_anomalies}")

        col2.metric("异常类型数", f"{anomaly_types}")

        col3.metric("高严重程度异常", f"{high_anomalies}")

        col4.metric("中严重程度异常", f"{medium_anomalies}")

        st.caption("异常数据对比期间：2026年8月 vs 2026年9月")

        # 异常类型和严重程度分布
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            anomaly_type_count = (
                anomaly_df["anomaly_type"]
                .value_counts()
                .reset_index()
            )

            anomaly_type_count.columns = [
                "异常类型",
                "异常数量"
            ]

            fig_type = px.bar(
                anomaly_type_count,
                x="异常类型",
                y="异常数量",
                title="异常类型分布",
                text="异常数量"
            )

            st.plotly_chart(
                fig_type,
                use_container_width=True,
                key="anomaly_type_distribution"
            )

        with chart_col2:

            severity_count = (
                anomaly_df["severity"]
                .value_counts()
                .reset_index()
            )

            severity_count.columns = [
                "严重程度",
                "异常数量"
            ]

            fig_severity = px.pie(
                severity_count,
                names="严重程度",
                values="异常数量",
                title="异常严重程度分布",
                hole=0.4
            )

            st.plotly_chart(
                fig_severity,
                use_container_width=True,
                key="anomaly_severity_distribution"
            )

        # 异常明细筛选
        st.markdown("#### 异常明细")

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:

            anomaly_type_options = [
                "全部"
            ] + sorted(
                anomaly_df["anomaly_type"].dropna().unique().tolist()
            )

            selected_anomaly_type = st.selectbox(
                "筛选异常类型",
                anomaly_type_options,
                key="filter_anomaly_type"
            )

        with filter_col2:

            severity_options = [
                "全部"
            ] + sorted(
                anomaly_df["severity"].dropna().unique().tolist()
            )

            selected_severity = st.selectbox(
                "筛选严重程度",
                severity_options,
                key="filter_anomaly_severity"
            )

        anomaly_filtered = anomaly_df.copy()

        if selected_anomaly_type != "全部":

            anomaly_filtered = anomaly_filtered[
                anomaly_filtered["anomaly_type"]
                == selected_anomaly_type
            ]

        if selected_severity != "全部":

            anomaly_filtered = anomaly_filtered[
                anomaly_filtered["severity"]
                == selected_severity
            ]

        # 转换展示字段
        anomaly_display = anomaly_filtered.rename(
            columns={
                "anomaly_type": "异常类型",
                "entity_type": "对象类型",
                "entity_name": "对象名称",
                "previous_month": "上期月份",
                "current_month": "本期月份",
                "previous_value": "上期数值",
                "current_value": "本期数值",
                "change": "变化值",
                "change_rate": "变化率",
                "unit": "单位",
                "severity": "严重程度",
                "rule": "异常触发规则"
            }
        )

        anomaly_columns = [
            "异常类型",
            "对象类型",
            "对象名称",
            "上期数值",
            "本期数值",
            "变化值",
            "变化率",
            "单位",
            "严重程度",
            "异常触发规则"
        ]

        anomaly_columns = [
            col for col in anomaly_columns
            if col in anomaly_display.columns
        ]

        st.caption(
            f"当前筛选结果：{len(anomaly_filtered)} 条异常"
        )

        st.dataframe(
            anomaly_display[anomaly_columns],
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ---------------------------------
        # 3. 客户风险管理
        # ---------------------------------

        st.subheader("二、客户风险管理")

        high_risk_count = (
            (risk_df["risk_level"] == "高风险").sum()
        )

        medium_risk_count = (
            (risk_df["risk_level"] == "中风险").sum()
        )

        low_risk_count = (
            (risk_df["risk_level"] == "低风险").sum()
        )

        priority_count = (
            (risk_df["follow_up_priority"] == "优先跟进").sum()
        )

        risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)

        risk_col1.metric(
            "风险客户总数",
            f"{len(risk_df)}"
        )

        risk_col2.metric(
            "高风险客户",
            f"{high_risk_count}"
        )

        risk_col3.metric(
            "中风险客户",
            f"{medium_risk_count}"
        )

        risk_col4.metric(
            "优先跟进客户",
            f"{priority_count}"
        )

        # 客户风险等级分布
        risk_chart_col1, risk_chart_col2 = st.columns(2)

        with risk_chart_col1:

            risk_level_count = (
                risk_df["risk_level"]
                .value_counts()
                .reset_index()
            )

            risk_level_count.columns = [
                "风险等级",
                "客户数量"
            ]

            fig_risk = px.pie(
                risk_level_count,
                names="风险等级",
                values="客户数量",
                title="客户风险等级分布",
                hole=0.4
            )

            st.plotly_chart(
                fig_risk,
                use_container_width=True,
                key="customer_risk_distribution"
            )

        with risk_chart_col2:

            risk_reason_count = pd.DataFrame({
                "风险因素": [
                    "销售额下降",
                    "库存金额上升",
                    "费用率上升"
                ],
                "客户数量": [
                    (risk_df["sales_drop"] == "是").sum(),
                    (risk_df["inventory_rise"] == "是").sum(),
                    (risk_df["expense_rise"] == "是").sum()
                ]
            })

            fig_reason = px.bar(
                risk_reason_count,
                x="风险因素",
                y="客户数量",
                title="客户风险因素分布",
                text="客户数量"
            )

            st.plotly_chart(
                fig_reason,
                use_container_width=True,
                key="customer_risk_reason"
            )

        # ---------------------------------
        # 4. 优先跟进客户
        # ---------------------------------

        st.markdown("#### 优先跟进客户")

        risk_display = risk_df.copy()

        # 按风险数量、跟进优先级排序
        risk_display["_priority_sort"] = (
            risk_display["follow_up_priority"]
            .map({
                "优先跟进": 1,
                "重点关注": 2
            })
            .fillna(3)
        )

        risk_display = risk_display.sort_values(
            ["_priority_sort", "risk_signal_count"],
            ascending=[True, False]
        )

        # 只展示前20名
        risk_top20 = risk_display.head(20).copy()

        risk_top20 = risk_top20.rename(
            columns={
                "customer_name": "客户名称",
                "risk_level": "风险等级",
                "follow_up_priority": "跟进优先级",
                "risk_signal_count": "风险信号数",
                "risk_reasons": "主要风险原因",
                "sales_change_rate": "销售额变化率",
                "inventory_change_rate": "库存金额变化率",
                "expense_change_pp": "费用率变化（百分点）"
            }
        )

        # 将变化率转换为百分比展示
        for col in [
            "销售额变化率",
            "库存金额变化率"
        ]:

            if col in risk_top20.columns:

                risk_top20[col] = (
                    pd.to_numeric(
                        risk_top20[col],
                        errors="coerce"
                    ) * 100
                ).round(2).astype("string") + "%"

        if "费用率变化（百分点）" in risk_top20.columns:

            risk_top20["费用率变化（百分点）"] = (
                pd.to_numeric(
                    risk_top20["费用率变化（百分点）"],
                    errors="coerce"
                ).round(2)
            )

        risk_columns = [
            "客户名称",
            "风险等级",
            "跟进优先级",
            "风险信号数",
            "主要风险原因",
            "销售额变化率",
            "库存金额变化率",
            "费用率变化（百分点）"
        ]

        risk_columns = [
            col for col in risk_columns
            if col in risk_top20.columns
        ]

        st.dataframe(
            risk_top20[risk_columns],
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "说明：客户风险等级和跟进优先级来自已有客户风险评估结果；"
            "页面仅负责展示，不重新计算风险。"
        )

    except FileNotFoundError as e:

        st.error(
            f"找不到分析结果文件：{e.filename}。请确认 reports 文件夹中已有对应 CSV。"
        )

    except Exception as e:

        st.error(f"异常检测模块加载失败：{e}")
