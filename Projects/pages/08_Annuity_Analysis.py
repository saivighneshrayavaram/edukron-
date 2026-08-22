import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# TITLE
# ============================================================

st.title("💵 Annuity Analysis")


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()
df = clean_data(df)
df = create_features(df)
df = apply_sidebar_filters(df)


# ============================================================
# CHECK DATA
# ============================================================

if len(df) == 0:

    st.warning(
        "⚠️ No customers match the selected filters."
    )

    st.stop()


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Annuity",
    f"{df['AMT_ANNUITY'].mean():,.0f}"
)

c2.metric(
    "Median Annuity",
    f"{df['AMT_ANNUITY'].median():,.0f}"
)

c3.metric(
    "Maximum Annuity",
    f"{df['AMT_ANNUITY'].max():,.0f}"
)

default_annuity = df.loc[
    df["TARGET"] == 1,
    "AMT_ANNUITY"
].mean()

c4.metric(
    "Avg Annuity of Defaulters",
    f"{default_annuity:,.0f}"
)


# ============================================================
# ANNUITY DISTRIBUTION
# ============================================================

fig = px.histogram(
    df,
    x="AMT_ANNUITY",
    nbins=50,
    title="Annuity Distribution",
    text_auto=True
)

fig.update_traces(
    textposition="inside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# AVERAGE ANNUITY BY TARGET
# ============================================================

data = (
    df.groupby("TARGET")["AMT_ANNUITY"]
    .mean()
    .reset_index()
)

fig = px.bar(
    data,
    x="TARGET",
    y="AMT_ANNUITY",
    title="Average Annuity by TARGET",
    text="AMT_ANNUITY"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# ANNUITY VS INCOME
# ============================================================

sample = df.sample(
    min(10000, len(df)),
    random_state=42
)

fig = px.scatter(
    sample,
    x="AMT_INCOME_TOTAL",
    y="AMT_ANNUITY",
    color="TARGET",
    title="Annuity vs Income"
)

fig.update_traces(
    texttemplate="%{y:,.0f}",
    textposition="top center"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# ANNUITY VS CREDIT
# ============================================================

sample = df.sample(
    min(10000, len(df)),
    random_state=42
)

fig = px.scatter(
    sample,
    x="AMT_CREDIT",
    y="AMT_ANNUITY",
    color="TARGET",
    title="Annuity vs Credit"
)

fig.update_traces(
    texttemplate="%{y:,.0f}",
    textposition="top center"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# AVERAGE ANNUITY BY INCOME TYPE
# ============================================================

data = (
    df.groupby("NAME_INCOME_TYPE")["AMT_ANNUITY"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    data,
    x="NAME_INCOME_TYPE",
    y="AMT_ANNUITY",
    title="Average Annuity by Income Type",
    text="AMT_ANNUITY"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    xaxis_tickangle=-45,
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# DEFAULT RATE BY ANNUITY BURDEN
# ============================================================

data = (
    df.groupby(
        "ANNUITY_BURDEN_GROUP",
        observed=True
    )["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

data.columns = [
    "Annuity Burden",
    "Default Rate"
]

fig = px.bar(
    data,
    x="Annuity Burden",
    y="Default Rate",
    title="Default Rate by Annuity Burden",
    text="Default Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 📌 KEY ANNUITY INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("📌 Key Annuity Insights")


# ============================================================
# BASIC METRICS
# ============================================================

total_customers = len(df)

overall_default_rate = (
    df["TARGET"].mean() * 100
)

avg_annuity = df["AMT_ANNUITY"].mean()

median_annuity = df["AMT_ANNUITY"].median()

max_annuity = df["AMT_ANNUITY"].max()


# ============================================================
# DEFAULT VS NON-DEFAULT ANNUITY
# ============================================================

target_annuity = (
    df.groupby("TARGET")["AMT_ANNUITY"]
    .mean()
)

default_avg_annuity = target_annuity.get(1, 0)

non_default_avg_annuity = target_annuity.get(0, 0)

annuity_difference = (
    default_avg_annuity -
    non_default_avg_annuity
)


# ============================================================
# ANNUITY BURDEN RISK
# ============================================================

burden_risk = (
    df.groupby(
        "ANNUITY_BURDEN_GROUP",
        observed=True
    )
    .agg(
        Customers=("SK_ID_CURR", "count"),
        Default_Rate=("TARGET", "mean"),
        Avg_Annuity=("AMT_ANNUITY", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean")
    )
    .reset_index()
)

burden_risk["Default_Rate"] *= 100


highest_risk_burden = (
    burden_risk
    .sort_values(
        "Default_Rate",
        ascending=False
    )
    .iloc[0]
)

highest_risk_burden_name = (
    highest_risk_burden["ANNUITY_BURDEN_GROUP"]
)

highest_risk_burden_rate = (
    highest_risk_burden["Default_Rate"]
)


# ============================================================
# INCOME TYPE ANALYSIS
# ============================================================

income_annuity = (
    df.groupby("NAME_INCOME_TYPE")
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Avg_Annuity=("AMT_ANNUITY", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

income_annuity["Default_Rate"] *= 100


highest_income_annuity = (
    income_annuity
    .sort_values(
        "Avg_Annuity",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# ANNUITY / INCOME RATIO
# ============================================================

avg_burden_ratio = (
    df["ANNUITY_INCOME_RATIO"].mean()
)

max_burden_ratio = (
    df["ANNUITY_INCOME_RATIO"].max()
)


# ============================================================
# CREDIT VS ANNUITY
# ============================================================

avg_credit = df["AMT_CREDIT"].mean()


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Annuity",
    f"{avg_annuity:,.0f}"
)

c2.metric(
    "Median Annuity",
    f"{median_annuity:,.0f}"
)

c3.metric(
    "Average Annuity/Income",
    f"{avg_burden_ratio:.3f}"
)

c4.metric(
    "Overall Default Rate",
    f"{overall_default_rate:.2f}%"
)


# ============================================================
# INSIGHT CARDS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    if default_avg_annuity > non_default_avg_annuity:

        st.warning(
            f"""
            ⚠️ **Higher Annuity Among Defaulters**

            Defaulters have an average annuity of
            **{default_avg_annuity:,.0f}**, compared with
            **{non_default_avg_annuity:,.0f}** for
            non-defaulters.
            """
        )

    else:

        st.info(
            f"""
            📊 **Annuity Comparison**

            Defaulters have an average annuity of
            **{default_avg_annuity:,.0f}**, compared with
            **{non_default_avg_annuity:,.0f}** for
            non-defaulters.
            """
        )


    st.error(
        f"""
        🚨 **Highest-Risk Annuity Burden**

        **{highest_risk_burden_name}** has the highest
        observed default rate of
        **{highest_risk_burden_rate:.2f}%**.
        """
    )


with col2:

    st.info(
        f"""
        💼 **Highest Average Annuity by Income Type**

        **{highest_income_annuity['NAME_INCOME_TYPE']}**
        has the highest average annuity of
        **{highest_income_annuity['Avg_Annuity']:,.0f}**.
        """
    )


    st.warning(
        f"""
        💰 **Repayment Burden**

        The average annuity represents
        **{avg_burden_ratio * 100:.2f}%** of average
        income based on the annuity-to-income ratio.
        """
    )


# ============================================================
# ANNUITY BURDEN SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📊 Annuity Burden Summary")

burden_display = burden_risk.copy()

burden_display.columns = [
    "Annuity Burden",
    "Customers",
    "Default Rate",
    "Average Annuity",
    "Average Income"
]

st.dataframe(
    burden_display,
    use_container_width=True
)


# ============================================================
# INCOME TYPE SUMMARY
# ============================================================

st.subheader("💼 Annuity by Income Type")

income_display = income_annuity.copy()

income_display.columns = [
    "Income Type",
    "Applications",
    "Average Annuity",
    "Average Income",
    "Default Rate"
]

income_display = income_display.sort_values(
    "Average Annuity",
    ascending=False
)

st.dataframe(
    income_display,
    use_container_width=True
)


# ============================================================
# BUSINESS SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📝 Annuity Analysis Summary")

st.write(
    f"• The filtered dataset contains "
    f"**{total_customers:,} customers** with an overall "
    f"default rate of **{overall_default_rate:.2f}%**."
)

st.write(
    f"• The average annuity is "
    f"**{avg_annuity:,.0f}**, while the median annuity is "
    f"**{median_annuity:,.0f}**."
)

st.write(
    f"• The maximum observed annuity is "
    f"**{max_annuity:,.0f}**."
)

st.write(
    f"• The average annuity-to-income ratio is "
    f"**{avg_burden_ratio:.3f}**, indicating the relative "
    f"repayment burden compared with income."
)

st.write(
    f"• The **{highest_risk_burden_name}** burden group has "
    f"the highest observed default rate of "
    f"**{highest_risk_burden_rate:.2f}%**."
)

st.write(
    f"• **{highest_income_annuity['NAME_INCOME_TYPE']}** "
    f"has the highest average annuity among income types."
)


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

st.markdown("### 💡 Business Recommendation")

if default_avg_annuity > non_default_avg_annuity:

    st.warning(
        "⚠️ Defaulters have a higher average annuity than "
        "non-defaulters. Loan payment burden can therefore "
        "be considered as one of the risk indicators."
    )

else:

    st.info(
        "📊 Defaulters do not have a higher average annuity "
        "than non-defaulters in the filtered dataset. "
        "Annuity should therefore be evaluated together "
        "with income, credit amount, external scores, and "
        "other risk indicators."
    )


# ============================================================
# FOOTER NOTE
# ============================================================

st.caption(
    "Note: Higher annuity does not necessarily cause default. "
    "These are observed relationships in the dataset."
)