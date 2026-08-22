import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# TITLE
# ============================================================

st.title("💳 Credit Amount Analysis")


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()
df = clean_data(df)
df = create_features(df)
df = apply_sidebar_filters(df)


# ============================================================
# CHECK EMPTY DATA
# ============================================================

if len(df) == 0:

    st.warning(
        "No customers match the selected filters."
    )

    st.stop()


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Credit",
    f"{df['AMT_CREDIT'].sum():,.0f}"
)

c2.metric(
    "Average Credit",
    f"{df['AMT_CREDIT'].mean():,.0f}"
)

c3.metric(
    "Median Credit",
    f"{df['AMT_CREDIT'].median():,.0f}"
)

c4.metric(
    "Maximum Credit",
    f"{df['AMT_CREDIT'].max():,.0f}"
)

c5.metric(
    "Minimum Credit",
    f"{df['AMT_CREDIT'].min():,.0f}"
)


# ============================================================
# CREDIT AMOUNT DISTRIBUTION
# ============================================================

fig = px.histogram(
    df,
    x="AMT_CREDIT",
    nbins=50,
    title="Credit Amount Distribution"
)

fig.update_traces(
    texttemplate="%{y:,}",
    textposition="inside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# AVERAGE CREDIT BY TARGET
# ============================================================

data = (
    df.groupby("TARGET")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

data["Status"] = data["TARGET"].map({
    0: "No Payment Difficulty",
    1: "Payment Difficulty"
})

fig = px.bar(
    data,
    x="Status",
    y="AMT_CREDIT",
    title="Average Credit by TARGET",
    text="AMT_CREDIT"
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
# AVERAGE CREDIT BY GENDER
# ============================================================

data = (
    df.groupby("CODE_GENDER")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

fig = px.bar(
    data,
    x="CODE_GENDER",
    y="AMT_CREDIT",
    title="Average Credit by Gender",
    text="AMT_CREDIT"
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
# CREDIT BY INCOME / EDUCATION / CONTRACT
# ============================================================

for column, title in [
    ("NAME_INCOME_TYPE", "Credit by Income Type"),
    ("NAME_EDUCATION_TYPE", "Credit by Education"),
    ("NAME_CONTRACT_TYPE", "Credit by Contract Type")
]:

    data = (
        df.groupby(column)["AMT_CREDIT"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        data,
        x=column,
        y="AMT_CREDIT",
        title=title,
        text="AMT_CREDIT"
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
# DEFAULT RATE BY CREDIT RANGE
# ============================================================

data = (
    df.groupby(
        "CREDIT_GROUP",
        observed=True
    )["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

data.columns = [
    "Credit Group",
    "Default Rate"
]

fig = px.bar(
    data,
    x="Credit Group",
    y="Default Rate",
    title="Default Rate by Credit Range",
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
# 📌 KEY CREDIT AMOUNT INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("📌 Key Credit Amount Insights")


# ============================================================
# BASIC METRICS
# ============================================================

total_customers = len(df)

overall_default_rate = (
    df["TARGET"].mean() * 100
)

avg_credit = df["AMT_CREDIT"].mean()

median_credit = df["AMT_CREDIT"].median()

max_credit = df["AMT_CREDIT"].max()

min_credit = df["AMT_CREDIT"].min()


# ============================================================
# DEFAULT VS NON-DEFAULT
# ============================================================

target_credit = (
    df.groupby("TARGET")["AMT_CREDIT"]
    .mean()
)

default_avg_credit = target_credit.get(1, 0)

non_default_avg_credit = target_credit.get(0, 0)

credit_difference = (
    default_avg_credit -
    non_default_avg_credit
)


# ============================================================
# CREDIT GROUP RISK
# ============================================================

credit_risk = (
    df.groupby(
        "CREDIT_GROUP",
        observed=True
    )
    .agg(
        Customers=("SK_ID_CURR", "count"),
        Default_Rate=("TARGET", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean")
    )
    .reset_index()
)

credit_risk["Default_Rate"] *= 100


highest_risk_credit = (
    credit_risk
    .sort_values(
        "Default_Rate",
        ascending=False
    )
    .iloc[0]
)

highest_risk_credit_group = (
    highest_risk_credit["CREDIT_GROUP"]
)

highest_risk_credit_rate = (
    highest_risk_credit["Default_Rate"]
)


# ============================================================
# GENDER
# ============================================================

gender_credit = (
    df.groupby("CODE_GENDER")
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

gender_credit["Default_Rate"] *= 100


highest_gender_credit = (
    gender_credit
    .sort_values(
        "Avg_Credit",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# INCOME TYPE
# ============================================================

income_credit = (
    df.groupby("NAME_INCOME_TYPE")
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

income_credit["Default_Rate"] *= 100


highest_income_credit = (
    income_credit
    .sort_values(
        "Avg_Credit",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# EDUCATION
# ============================================================

education_credit = (
    df.groupby("NAME_EDUCATION_TYPE")
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

education_credit["Default_Rate"] *= 100


highest_education_credit = (
    education_credit
    .sort_values(
        "Avg_Credit",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# CONTRACT TYPE
# ============================================================

contract_credit = (
    df.groupby("NAME_CONTRACT_TYPE")
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

contract_credit["Default_Rate"] *= 100


highest_contract_credit = (
    contract_credit
    .sort_values(
        "Avg_Credit",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Credit",
    f"{avg_credit:,.0f}"
)

c2.metric(
    "Median Credit",
    f"{median_credit:,.0f}"
)

c3.metric(
    "Highest-Risk Credit Group",
    str(highest_risk_credit_group)
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

    st.error(
        f"🚨 **Highest-Risk Credit Range**\n\n"
        f"**{highest_risk_credit_group}** has the highest "
        f"observed default rate of "
        f"**{highest_risk_credit_rate:.2f}%**."
    )

    if default_avg_credit > non_default_avg_credit:

        st.warning(
            f"⚠️ **Higher Average Credit Among Defaulters**\n\n"
            f"Defaulters have an average credit amount of "
            f"**{default_avg_credit:,.0f}**, compared with "
            f"**{non_default_avg_credit:,.0f}** for "
            f"non-defaulters."
        )

    else:

        st.info(
            f"📊 **Credit Comparison**\n\n"
            f"Defaulters have an average credit amount of "
            f"**{default_avg_credit:,.0f}**, compared with "
            f"**{non_default_avg_credit:,.0f}** for "
            f"non-defaulters."
        )


with col2:

    st.info(
        f"👤 **Highest Average Credit by Gender**\n\n"
        f"**{highest_gender_credit['CODE_GENDER']}** has the "
        f"highest average credit of "
        f"**{highest_gender_credit['Avg_Credit']:,.0f}**."
    )

    st.info(
        f"💼 **Highest Average Credit by Income Type**\n\n"
        f"**{highest_income_credit['NAME_INCOME_TYPE']}** "
        f"has the highest average credit of "
        f"**{highest_income_credit['Avg_Credit']:,.0f}**."
    )


# ============================================================
# CREDIT GROUP SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📊 Credit Range Summary")

credit_display = credit_risk.copy()

credit_display.columns = [
    "Credit Group",
    "Customers",
    "Default Rate",
    "Average Credit",
    "Average Income"
]

st.dataframe(
    credit_display,
    use_container_width=True
)


# ============================================================
# INCOME TYPE SUMMARY
# ============================================================

st.subheader("💼 Credit by Income Type")

income_display = income_credit.copy()

income_display.columns = [
    "Income Type",
    "Applications",
    "Average Credit",
    "Average Income",
    "Default Rate"
]

income_display = income_display.sort_values(
    "Average Credit",
    ascending=False
)

st.dataframe(
    income_display,
    use_container_width=True
)


# ============================================================
# EDUCATION SUMMARY
# ============================================================

st.subheader("🎓 Credit by Education")

education_display = education_credit.copy()

education_display.columns = [
    "Education",
    "Applications",
    "Average Credit",
    "Default Rate"
]

education_display = education_display.sort_values(
    "Average Credit",
    ascending=False
)

st.dataframe(
    education_display,
    use_container_width=True
)


# ============================================================
# CONTRACT SUMMARY
# ============================================================

st.subheader("📑 Credit by Contract Type")

contract_display = contract_credit.copy()

contract_display.columns = [
    "Contract Type",
    "Applications",
    "Average Credit",
    "Default Rate"
]

st.dataframe(
    contract_display,
    use_container_width=True
)


# ============================================================
# BUSINESS SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📝 Credit Amount Summary")

st.write(
    f"• The filtered dataset contains "
    f"**{total_customers:,} customers** with an overall "
    f"default rate of **{overall_default_rate:.2f}%**."
)

st.write(
    f"• The average credit amount is "
    f"**{avg_credit:,.0f}**, while the median credit is "
    f"**{median_credit:,.0f}**."
)

st.write(
    f"• The maximum observed credit amount is "
    f"**{max_credit:,.0f}**."
)

st.write(
    f"• The **{highest_risk_credit_group}** credit range "
    f"has the highest observed default rate of "
    f"**{highest_risk_credit_rate:.2f}%**."
)

st.write(
    f"• **{highest_income_credit['NAME_INCOME_TYPE']}** "
    f"has the highest average credit among income types."
)

st.write(
    f"• **{highest_education_credit['NAME_EDUCATION_TYPE']}** "
    f"has the highest average credit among education groups."
)

st.write(
    f"• **{highest_contract_credit['NAME_CONTRACT_TYPE']}** "
    f"has the highest average credit among contract types."
)


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

st.markdown("### 💡 Business Recommendation")

if highest_risk_credit_rate > overall_default_rate:

    st.warning(
        f"⚠️ The **{highest_risk_credit_group}** credit range "
        f"has a default rate above the overall portfolio "
        f"average. Credit amount should be evaluated together "
        f"with income, credit-to-income ratio, annuity burden, "
        f"and external credit scores."
    )

else:

    st.info(
        "📊 Credit range alone does not show a default rate "
        "above the overall portfolio average. Credit amount "
        "should be combined with other risk indicators."
    )


st.caption(
    "Note: A higher credit amount does not necessarily "
    "cause default. The analysis shows observed relationships "
    "within the dataset."
)