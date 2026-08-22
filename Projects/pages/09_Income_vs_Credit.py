import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# TITLE
# ============================================================

st.title("📈 Income vs Credit Analysis")


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

    st.warning("No customers match the selected filters.")
    st.stop()


# ============================================================
# BASIC CALCULATIONS
# ============================================================

avg_ratio = df["CREDIT_INCOME_RATIO"].mean()
max_ratio = df["CREDIT_INCOME_RATIO"].max()

high_ratio = df[
    df["CREDIT_INCOME_RATIO"] > 6
]

if len(high_ratio) > 0:
    high_risk_rate = (
        high_ratio["TARGET"].mean() * 100
    )
else:
    high_risk_rate = 0


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Average Credit/Income",
    f"{avg_ratio:.2f}"
)

c2.metric(
    "Highest Ratio",
    f"{max_ratio:.2f}"
)

c3.metric(
    "Default Rate Ratio > 6",
    f"{high_risk_rate:.2f}%"
)


# ============================================================
# 1. INCOME VS CREDIT
# ============================================================

sample = df.sample(
    min(10000, len(df)),
    random_state=42
)

fig = px.scatter(
    sample,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    color="TARGET",
    title="Income vs Credit",
    labels={
        "AMT_INCOME_TOTAL": "Income",
        "AMT_CREDIT": "Credit",
        "TARGET": "Default"
    }
)

# SHOW CREDIT VALUE ON POINTS
fig.update_traces(
    text=sample["AMT_CREDIT"],
    texttemplate="%{text:,.0f}",
    textposition="top center"
)

fig.update_layout(
    legend_title_text="Default"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 2. CREDIT-TO-INCOME RATIO DISTRIBUTION
# ============================================================

fig = px.histogram(
    df,
    x="CREDIT_INCOME_RATIO",
    nbins=50,
    title="Credit-to-Income Ratio Distribution"
)

# SHOW VALUES ON HISTOGRAM
fig.update_traces(
    texttemplate="%{y:,}",
    textposition="inside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CREATE CREDIT-INCOME RISK GROUP
# ============================================================

df["CREDIT_INCOME_RISK"] = pd.cut(
    df["CREDIT_INCOME_RATIO"],
    bins=[
        0,
        2,
        4,
        6,
        float("inf")
    ],
    labels=[
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]
)


# ============================================================
# 3. DEFAULT RATE VS CREDIT/INCOME RATIO
# ============================================================

data = (
    df.groupby(
        "CREDIT_INCOME_RISK",
        observed=True
    )["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

data.columns = [
    "Risk Group",
    "Default Rate"
]

fig = px.bar(
    data,
    x="Risk Group",
    y="Default Rate",
    title="Default Rate vs Credit/Income Ratio",
    text="Default Rate"
)

# VALUES INSIDE BAR
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
# 4. CREDIT/INCOME RATIO BY GENDER
# ============================================================

data = (
    df.groupby("CODE_GENDER")[
        "CREDIT_INCOME_RATIO"
    ]
    .mean()
    .reset_index()
)

fig = px.bar(
    data,
    x="CODE_GENDER",
    y="CREDIT_INCOME_RATIO",
    title="Credit/Income Ratio by Gender",
    text="CREDIT_INCOME_RATIO"
)

# VALUES INSIDE BAR
fig.update_traces(
    texttemplate="%{text:.2f}",
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
# 5. CREDIT/INCOME RATIO BY EDUCATION
# ============================================================

data = (
    df.groupby("NAME_EDUCATION_TYPE")[
        "CREDIT_INCOME_RATIO"
    ]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    data,
    x="NAME_EDUCATION_TYPE",
    y="CREDIT_INCOME_RATIO",
    title="Credit/Income Ratio by Education",
    text="CREDIT_INCOME_RATIO"
)

# VALUES INSIDE BAR
fig.update_traces(
    texttemplate="%{text:.2f}",
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
# KEY INCOME VS CREDIT INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("📌 Key Income vs Credit Insights")


# ============================================================
# OVERALL DEFAULT RATE
# ============================================================

overall_default_rate = (
    df["TARGET"].mean() * 100
)

total_customers = len(df)


# ============================================================
# RISK GROUP ANALYSIS
# ============================================================

risk_summary = (
    df.groupby(
        "CREDIT_INCOME_RISK",
        observed=True
    )
    .agg(
        Customers=("SK_ID_CURR", "count"),
        Default_Rate=("TARGET", "mean"),
        Avg_Ratio=("CREDIT_INCOME_RATIO", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean")
    )
    .reset_index()
)

risk_summary["Default_Rate"] *= 100


highest_risk_group = (
    risk_summary
    .sort_values(
        "Default_Rate",
        ascending=False
    )
    .iloc[0]
)

highest_risk_group_name = (
    highest_risk_group["CREDIT_INCOME_RISK"]
)

highest_risk_group_rate = (
    highest_risk_group["Default_Rate"]
)


# ============================================================
# GENDER ANALYSIS
# ============================================================

gender_ratio = (
    df.groupby("CODE_GENDER")
    .agg(
        Avg_Ratio=("CREDIT_INCOME_RATIO", "mean"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

gender_ratio["Default_Rate"] *= 100


highest_gender_ratio = (
    gender_ratio
    .sort_values(
        "Avg_Ratio",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# EDUCATION ANALYSIS
# ============================================================

education_ratio = (
    df.groupby("NAME_EDUCATION_TYPE")
    .agg(
        Avg_Ratio=("CREDIT_INCOME_RATIO", "mean"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

education_ratio["Default_Rate"] *= 100


highest_education_ratio = (
    education_ratio
    .sort_values(
        "Avg_Ratio",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# HIGH RATIO ANALYSIS
# ============================================================

high_ratio_customers = df[
    df["CREDIT_INCOME_RATIO"] > 6
]

high_ratio_count = len(
    high_ratio_customers
)

high_ratio_percentage = (
    high_ratio_count / total_customers * 100
    if total_customers > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Credit/Income",
    f"{avg_ratio:.2f}"
)

c2.metric(
    "Highest Credit/Income",
    f"{max_ratio:.2f}"
)

c3.metric(
    "Customers Ratio > 6",
    f"{high_ratio_count:,}"
)

c4.metric(
    "Ratio > 6 Share",
    f"{high_ratio_percentage:.2f}%"
)


# ============================================================
# INSIGHT CARDS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.error(
        f"🚨 **Highest-Risk Credit Burden Group**\n\n"
        f"**{highest_risk_group_name}** has the highest "
        f"observed default rate of "
        f"**{highest_risk_group_rate:.2f}%**."
    )

    st.warning(
        f"💳 **High Credit Burden Customers**\n\n"
        f"**{high_ratio_count:,} customers** have a "
        f"credit-to-income ratio above **6**, representing "
        f"**{high_ratio_percentage:.2f}%** of the filtered "
        f"customers."
    )


with col2:

    st.info(
        f"👤 **Highest Gender Credit Burden**\n\n"
        f"**{highest_gender_ratio['CODE_GENDER']}** has the "
        f"highest average credit-to-income ratio of "
        f"**{highest_gender_ratio['Avg_Ratio']:.2f}**."
    )

    st.info(
        f"🎓 **Highest Education Credit Burden**\n\n"
        f"**{highest_education_ratio['NAME_EDUCATION_TYPE']}** "
        f"has the highest average credit-to-income ratio "
        f"of **{highest_education_ratio['Avg_Ratio']:.2f}**."
    )


# ============================================================
# HIGH RATIO DEFAULT COMPARISON
# ============================================================

if len(high_ratio_customers) > 0:

    high_ratio_default = (
        high_ratio_customers["TARGET"]
        .mean() * 100
    )

    if high_ratio_default > overall_default_rate:

        st.warning(
            f"⚠️ **High Credit Burden and Default Risk**\n\n"
            f"Customers with a credit-to-income ratio "
            f"above **6** have an observed default rate of "
            f"**{high_ratio_default:.2f}%**, compared with "
            f"the overall rate of "
            f"**{overall_default_rate:.2f}%**."
        )

    else:

        st.info(
            f"📊 Customers with a credit-to-income ratio "
            f"above **6** have an observed default rate of "
            f"**{high_ratio_default:.2f}%**, which is not "
            f"higher than the overall rate of "
            f"**{overall_default_rate:.2f}%**."
        )


# ============================================================
# RISK GROUP SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📊 Credit-to-Income Risk Summary")

risk_summary_display = risk_summary.copy()

risk_summary_display.columns = [
    "Risk Group",
    "Customers",
    "Default Rate",
    "Average Ratio",
    "Average Income",
    "Average Credit"
]

st.dataframe(
    risk_summary_display,
    use_container_width=True
)


# ============================================================
# GENDER SUMMARY
# ============================================================

st.subheader("👤 Credit Burden by Gender")

gender_display = gender_ratio.copy()

gender_display.columns = [
    "Gender",
    "Average Credit/Income Ratio",
    "Default Rate"
]

st.dataframe(
    gender_display,
    use_container_width=True
)


# ============================================================
# EDUCATION SUMMARY
# ============================================================

st.subheader("🎓 Credit Burden by Education")

education_display = education_ratio.copy()

education_display.columns = [
    "Education",
    "Average Credit/Income Ratio",
    "Default Rate"
]

education_display = education_display.sort_values(
    "Average Credit/Income Ratio",
    ascending=False
)

st.dataframe(
    education_display,
    use_container_width=True
)


# ============================================================
# BUSINESS SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📝 Income vs Credit Summary")

st.write(
    f"• The filtered dataset contains "
    f"**{total_customers:,} customers** with an overall "
    f"default rate of **{overall_default_rate:.2f}%**."
)

st.write(
    f"• The average credit-to-income ratio is "
    f"**{avg_ratio:.2f}**, with a maximum observed ratio "
    f"of **{max_ratio:.2f}**."
)

st.write(
    f"• **{high_ratio_count:,} customers** have a "
    f"credit-to-income ratio above **6**."
)

st.write(
    f"• The highest observed default rate occurs in the "
    f"**{highest_risk_group_name}** credit-burden group."
)

st.write(
    f"• **{highest_gender_ratio['CODE_GENDER']}** has the "
    f"highest average credit-to-income ratio among gender "
    f"groups."
)

st.write(
    f"• **{highest_education_ratio['NAME_EDUCATION_TYPE']}** "
    f"has the highest average credit-to-income ratio among "
    f"education groups."
)


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

st.markdown("### 💡 Business Recommendation")

if high_ratio_count > 0:

    st.warning(
        "⚠️ Customers with a high credit-to-income ratio "
        "may have greater borrowing exposure relative to "
        "their income. Consider this ratio together with "
        "external credit scores, annuity burden, income "
        "stability, and employment history during risk "
        "assessment."
    )

else:

    st.success(
        "🟢 No customers in the filtered dataset have a "
        "credit-to-income ratio above the selected threshold."
    )


st.caption(
    "Note: Credit-to-income ratio is an observed risk "
    "indicator. A high ratio does not by itself mean that "
    "a customer will default."
)