import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📑 Contract Type Analysis")


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()
df = clean_data(df)
df = create_features(df)
df = apply_sidebar_filters(df)


# ============================================================
# CONTRACT TYPE SUMMARY
# ============================================================

summary = (
    df.groupby("NAME_CONTRACT_TYPE")
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Default_Rate=("TARGET", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Avg_Annuity=("AMT_ANNUITY", "mean"),
        Avg_Ratio=("CREDIT_INCOME_RATIO", "mean")
    )
    .reset_index()
)

summary["Default_Rate"] *= 100


# ============================================================
# CONTRACT APPLICATION METRICS
# ============================================================

for contract in summary["NAME_CONTRACT_TYPE"]:

    row = summary[
        summary["NAME_CONTRACT_TYPE"] == contract
    ].iloc[0]

    st.metric(
        f"{contract} Applications",
        f"{row['Applications']:,}"
    )


# ============================================================
# SEPARATOR
# ============================================================

st.markdown("---")


# ============================================================
# 1. APPLICATIONS BY CONTRACT TYPE
# ============================================================

fig = px.bar(
    summary,
    x="NAME_CONTRACT_TYPE",
    y="Applications",
    title="Applications by Contract Type",
    text="Applications"
)

fig.update_traces(
    texttemplate="%{text:,}",
    textposition="inside"
)

fig.update_layout(
    yaxis_title="Applications"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 2. DEFAULT RATE BY CONTRACT TYPE
# ============================================================

fig = px.bar(
    summary,
    x="NAME_CONTRACT_TYPE",
    y="Default_Rate",
    title="Default Rate by Contract Type",
    text="Default_Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="inside"
)

fig.update_layout(
    yaxis_title="Default Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 3. AVERAGE CREDIT BY CONTRACT TYPE
# ============================================================

fig = px.bar(
    summary,
    x="NAME_CONTRACT_TYPE",
    y="Avg_Credit",
    title="Average Credit by Contract Type",
    text="Avg_Credit"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside"
)

fig.update_layout(
    yaxis_title="Average Credit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 4. AVERAGE INCOME BY CONTRACT TYPE
# ============================================================

fig = px.bar(
    summary,
    x="NAME_CONTRACT_TYPE",
    y="Avg_Income",
    title="Average Income by Contract Type",
    text="Avg_Income"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside"
)

fig.update_layout(
    yaxis_title="Average Income"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 5. AVERAGE ANNUITY BY CONTRACT TYPE
# ============================================================

fig = px.bar(
    summary,
    x="NAME_CONTRACT_TYPE",
    y="Avg_Annuity",
    title="Average Annuity by Contract Type",
    text="Avg_Annuity"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside"
)

fig.update_layout(
    yaxis_title="Average Annuity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 6. CREDIT-TO-INCOME RATIO
# ============================================================

fig = px.bar(
    summary,
    x="NAME_CONTRACT_TYPE",
    y="Avg_Ratio",
    title="Credit-to-Income Ratio by Contract Type",
    text="Avg_Ratio"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="inside"
)

fig.update_layout(
    yaxis_title="Credit / Income Ratio"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# DATA TABLE
# ============================================================

st.dataframe(
    summary,
    use_container_width=True
)


# ============================================================
# 📌 CONTRACT TYPE INSIGHTS
# ============================================================

st.markdown("---")

st.subheader(
    "📌 Contract Type Insights"
)


# ============================================================
# CHECK DATA
# ============================================================

if len(summary) == 0:

    st.warning(
        "No contract type data available for the selected filters."
    )

else:

    # ========================================================
    # BASIC METRICS
    # ========================================================

    total_applications = int(
        summary["Applications"].sum()
    )

    overall_default_rate = (
        df["TARGET"].mean() * 100
        if len(df)
        else 0
    )


    # ========================================================
    # HIGHEST APPLICATION CONTRACT
    # ========================================================

    highest_applications = (
        summary
        .sort_values(
            "Applications",
            ascending=False
        )
        .iloc[0]
    )


    # ========================================================
    # HIGHEST DEFAULT RATE
    # ========================================================

    highest_default = (
        summary
        .sort_values(
            "Default_Rate",
            ascending=False
        )
        .iloc[0]
    )


    # ========================================================
    # LOWEST DEFAULT RATE
    # ========================================================

    lowest_default = (
        summary
        .sort_values(
            "Default_Rate"
        )
        .iloc[0]
    )


    # ========================================================
    # HIGHEST CREDIT
    # ========================================================

    highest_credit = (
        summary
        .sort_values(
            "Avg_Credit",
            ascending=False
        )
        .iloc[0]
    )


    # ========================================================
    # HIGHEST INCOME
    # ========================================================

    highest_income = (
        summary
        .sort_values(
            "Avg_Income",
            ascending=False
        )
        .iloc[0]
    )


    # ========================================================
    # HIGHEST ANNUITY
    # ========================================================

    highest_annuity = (
        summary
        .sort_values(
            "Avg_Annuity",
            ascending=False
        )
        .iloc[0]
    )


    # ========================================================
    # HIGHEST CREDIT-INCOME RATIO
    # ========================================================

    highest_ratio = (
        summary
        .sort_values(
            "Avg_Ratio",
            ascending=False
        )
        .iloc[0]
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Applications",
        f"{total_applications:,}"
    )

    c2.metric(
        "Overall Default Rate",
        f"{overall_default_rate:.2f}%"
    )

    c3.metric(
        "Highest Risk Contract",
        str(
            highest_default["NAME_CONTRACT_TYPE"]
        )
    )

    c4.metric(
        "Highest Default Rate",
        f"{highest_default['Default_Rate']:.2f}%"
    )


    # ========================================================
    # INSIGHT CARDS
    # ========================================================

    col1, col2 = st.columns(2)


    # ========================================================
    # LEFT INSIGHTS
    # ========================================================

    with col1:

        st.info(
            f"📊 **Most Common Contract Type**\n\n"
            f"**{highest_applications['NAME_CONTRACT_TYPE']}** "
            f"has the highest number of applications with "
            f"**{int(highest_applications['Applications']):,}** "
            f"applications."
        )

        st.error(
            f"🚨 **Highest Default Risk**\n\n"
            f"**{highest_default['NAME_CONTRACT_TYPE']}** "
            f"has the highest default rate at "
            f"**{highest_default['Default_Rate']:.2f}%**."
        )

        st.success(
            f"🟢 **Lowest Default Risk**\n\n"
            f"**{lowest_default['NAME_CONTRACT_TYPE']}** "
            f"has the lowest default rate at "
            f"**{lowest_default['Default_Rate']:.2f}%**."
        )


    # ========================================================
    # RIGHT INSIGHTS
    # ========================================================

    with col2:

        st.info(
            f"💳 **Highest Average Credit**\n\n"
            f"**{highest_credit['NAME_CONTRACT_TYPE']}** "
            f"has the highest average credit amount of "
            f"**{highest_credit['Avg_Credit']:,.0f}**."
        )

        st.info(
            f"💰 **Highest Average Income**\n\n"
            f"**{highest_income['NAME_CONTRACT_TYPE']}** "
            f"has the highest average income of "
            f"**{highest_income['Avg_Income']:,.0f}**."
        )

        st.warning(
            f"📈 **Highest Credit-to-Income Ratio**\n\n"
            f"**{highest_ratio['NAME_CONTRACT_TYPE']}** "
            f"has the highest average credit-to-income "
            f"ratio of **{highest_ratio['Avg_Ratio']:.2f}**."
        )


    # ========================================================
    # CONTRACT RISK COMPARISON
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🔍 Contract Risk Comparison"
    )


    risk_comparison = summary[
        [
            "NAME_CONTRACT_TYPE",
            "Applications",
            "Default_Rate",
            "Avg_Credit",
            "Avg_Income",
            "Avg_Annuity",
            "Avg_Ratio"
        ]
    ].copy()


    risk_comparison.columns = [
        "Contract Type",
        "Applications",
        "Default Rate",
        "Average Credit",
        "Average Income",
        "Average Annuity",
        "Credit / Income Ratio"
    ]


    st.dataframe(
        risk_comparison,
        use_container_width=True
    )


    # ========================================================
    # RISK DIFFERENCE
    # ========================================================

    if len(summary) > 1:

        default_rate_difference = (
            highest_default["Default_Rate"]
            - lowest_default["Default_Rate"]
        )

        st.warning(
            f"⚠️ **Default Rate Gap:** "
            f"There is a **{default_rate_difference:.2f} percentage-point** "
            f"difference between the highest-risk and "
            f"lowest-risk contract types."
        )


    # ========================================================
    # BUSINESS SUMMARY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📝 Contract Type Summary"
    )


    st.write(
        f"• The filtered dataset contains "
        f"**{total_applications:,} applications**."
    )


    st.write(
        f"• **{highest_applications['NAME_CONTRACT_TYPE']}** "
        f"is the most common contract type with "
        f"**{int(highest_applications['Applications']):,} "
        f"applications**."
    )


    st.write(
        f"• **{highest_default['NAME_CONTRACT_TYPE']}** "
        f"has the highest default rate at "
        f"**{highest_default['Default_Rate']:.2f}%**."
    )


    st.write(
        f"• **{lowest_default['NAME_CONTRACT_TYPE']}** "
        f"has the lowest default rate at "
        f"**{lowest_default['Default_Rate']:.2f}%**."
    )


    st.write(
        f"• **{highest_credit['NAME_CONTRACT_TYPE']}** "
        f"has the highest average credit amount of "
        f"**{highest_credit['Avg_Credit']:,.0f}**."
    )


    st.write(
        f"• **{highest_ratio['NAME_CONTRACT_TYPE']}** "
        f"has the highest credit-to-income ratio of "
        f"**{highest_ratio['Avg_Ratio']:.2f}**."
    )


    # ========================================================
    # BUSINESS RECOMMENDATION
    # ========================================================

    st.markdown(
        "### 💡 Business Recommendation"
    )


    if (
        highest_default["Default_Rate"]
        > overall_default_rate
    ):

        st.warning(
            f"🔴 The **{highest_default['NAME_CONTRACT_TYPE']}** "
            f"contract type has a default rate above the "
            f"overall portfolio average. Applications under "
            f"this contract type may require additional "
            f"credit-risk assessment."
        )

    else:

        st.success(
            "🟢 Contract-level default rates are relatively "
            "close to the overall portfolio default rate."
        )


    # ========================================================
    # CREDIT-INCOME RATIO RECOMMENDATION
    # ========================================================

    if (
        highest_ratio["Avg_Ratio"]
        > summary["Avg_Ratio"].mean()
    ):

        st.info(
            f"📌 The **{highest_ratio['NAME_CONTRACT_TYPE']}** "
            f"contract type has a relatively high "
            f"credit-to-income burden and should be monitored "
            f"alongside other risk indicators."
        )


    # ========================================================
    # NOTE
    # ========================================================

    st.caption(
        "Note: Differences between contract types represent "
        "observed patterns in the dataset and should not be "
        "interpreted as causal relationships."
    )