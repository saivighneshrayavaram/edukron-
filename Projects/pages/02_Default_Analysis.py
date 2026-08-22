import streamlit as st
import pandas as pd

# ============================================================
# IMPORT UTILS
# ============================================================

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters
from utils.kpis import total_applications

from utils.charts import (
    bar_chart,
    pie_chart,
    donut_chart,
    histogram
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()


# ============================================================
# CLEAN DATA
# ============================================================

df = clean_data(df)


# ============================================================
# CREATE FEATURES
# ============================================================

df = create_features(df)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

filtered_df = apply_sidebar_filters(df)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📊 Executive Overview")

st.write(
    """
    Provide management with an overall picture of
    loan applicants and credit risk.
    """
)

st.markdown("---")


# ============================================================
# KPI CALCULATIONS
# ============================================================

kpis = total_applications(filtered_df)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Applications",
        f"{kpis['total_applications']:,}"
    )

with col2:
    st.metric(
        "Total Default Customers",
        f"{kpis['default_customers']:,}"
    )

with col3:
    st.metric(
        "Total Non-Default Customers",
        f"{kpis['non_default_customers']:,}"
    )

with col4:
    st.metric(
        "Default Rate %",
        f"{kpis['default_rate']:.2f}%"
    )


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Total Credit Amount",
        f"{filtered_df['AMT_CREDIT'].sum():,.0f}"
    )

with col6:
    st.metric(
        "Average Credit Amount",
        f"{kpis['avg_credit']:,.0f}"
    )

with col7:
    st.metric(
        "Average Income",
        f"{kpis['avg_income']:,.0f}"
    )

with col8:
    st.metric(
        "Average Annuity",
        f"{kpis['avg_annuity']:,.0f}"
    )


# ============================================================
# CHART 1
# DEFAULT VS NON-DEFAULT CUSTOMERS
# ============================================================

st.markdown("---")

st.subheader("🎯 Default vs Non-Default Customers")

target_data = pd.DataFrame({
    "Customer Status": [
        "Non-Default",
        "Default"
    ],
    "Customers": [
        kpis["non_default_customers"],
        kpis["default_customers"]
    ]
})

fig = donut_chart(
    target_data,
    names="Customer Status",
    values="Customers",
    title="Default vs Non-Default Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CHART 2
# TOTAL APPLICATIONS BY GENDER
# ============================================================

st.markdown("---")

st.subheader("👥 Total Applications by Gender")

gender_data = (
    filtered_df["CODE_GENDER"]
    .value_counts()
    .reset_index()
)

gender_data.columns = [
    "Gender",
    "Applications"
]

fig = bar_chart(
    gender_data,
    x="Gender",
    y="Applications",
    title="Total Applications by Gender"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CHART 3
# APPLICATIONS BY CONTRACT TYPE
# ============================================================

st.markdown("---")

st.subheader("💳 Applications by Contract Type")

contract_data = (
    filtered_df["NAME_CONTRACT_TYPE"]
    .value_counts()
    .reset_index()
)

contract_data.columns = [
    "Contract Type",
    "Applications"
]

fig = bar_chart(
    contract_data,
    x="Contract Type",
    y="Applications",
    title="Applications by Contract Type"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CHART 4
# APPLICATIONS BY INCOME TYPE
# ============================================================

st.markdown("---")

st.subheader("💰 Applications by Income Type")

income_data = (
    filtered_df["NAME_INCOME_TYPE"]
    .value_counts()
    .reset_index()
)

income_data.columns = [
    "Income Type",
    "Applications"
]

fig = bar_chart(
    income_data,
    x="Income Type",
    y="Applications",
    title="Applications by Income Type"
)

fig.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CHART 5
# CREDIT AMOUNT DISTRIBUTION
# ============================================================

st.markdown("---")

st.subheader("💵 Credit Amount Distribution")

fig = histogram(
    filtered_df,
    x="AMT_CREDIT",
    title="Credit Amount Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CHART 6
# OVERALL APPLICANT SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📈 Overall Applicant Summary")

summary_data = pd.DataFrame({
    "Status": [
        "Non-Default",
        "Default"
    ],
    "Applications": [
        kpis["non_default_customers"],
        kpis["default_customers"]
    ]
})

fig = bar_chart(
    summary_data,
    x="Status",
    y="Applications",
    title="Overall Applicant Summary"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# IMPORTANT INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("💡 Important Insights")


# ============================================================
# 1. OVERALL DEFAULT RATE
# ============================================================

st.write(
    f"🔴 **Overall Default Rate:** "
    f"{kpis['default_rate']:.2f}%"
)


# ============================================================
# 2. AVERAGE CUSTOMER INCOME
# ============================================================

st.write(
    f"💰 **Average Customer Income:** "
    f"{kpis['avg_income']:,.2f}"
)


# ============================================================
# 3. AVERAGE LOAN AMOUNT
# ============================================================

st.write(
    f"💳 **Average Loan Amount:** "
    f"{kpis['avg_credit']:,.2f}"
)


# ============================================================
# 4. MOST COMMON INCOME TYPE
# ============================================================

most_common_income = (
    filtered_df["NAME_INCOME_TYPE"]
    .dropna()
    .mode()
)

if len(most_common_income) > 0:

    st.write(
        f"👔 **Most Common Income Type:** "
        f"{most_common_income.iloc[0]}"
    )


# ============================================================
# 5. MOST COMMON EDUCATION LEVEL
# ============================================================

most_common_education = (
    filtered_df["NAME_EDUCATION_TYPE"]
    .dropna()
    .mode()
)

if len(most_common_education) > 0:

    st.write(
        f"🎓 **Most Common Education Level:** "
        f"{most_common_education.iloc[0]}"
    )


# ============================================================
# 6. HIGHEST RISK CUSTOMER SEGMENT
# ============================================================

st.write("⚠️ **Highest Risk Customer Segment**")

risk_data = (
    filtered_df
    .groupby("NAME_INCOME_TYPE")["TARGET"]
    .agg(
        Customers="count",
        Default_Rate="mean"
    )
    .reset_index()
)

risk_data["Default_Rate"] = (
    risk_data["Default_Rate"] * 100
)

# Remove very small groups
risk_data = risk_data[
    risk_data["Customers"] >= 100
]

if len(risk_data) > 0:

    highest_risk = risk_data.loc[
        risk_data["Default_Rate"].idxmax()
    ]

    st.write(
        f"The highest-risk customer segment is "
        f"**{highest_risk['NAME_INCOME_TYPE']}**, "
        f"with a default rate of "
        f"**{highest_risk['Default_Rate']:.2f}%**."
    )


# ============================================================
# RISK SEGMENT TABLE
# ============================================================

st.markdown("---")

st.subheader("📋 Customer Risk Segment Summary")

risk_table = (
    filtered_df
    .groupby("NAME_INCOME_TYPE")
    .agg(
        Customers=("TARGET", "count"),
        Defaults=("TARGET", "sum"),
        Average_Income=("AMT_INCOME_TOTAL", "mean"),
        Average_Credit=("AMT_CREDIT", "mean")
    )
    .reset_index()
)

risk_table["Default Rate %"] = (
    risk_table["Defaults"] /
    risk_table["Customers"] *
    100
)

risk_table = risk_table.sort_values(
    "Default Rate %",
    ascending=False
)

st.dataframe(
    risk_table,
    use_container_width=True
)


# ============================================================
# FILTERED DATA PREVIEW
# ============================================================

st.markdown("---")

st.subheader("🔍 Filtered Applicant Data")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Page 1 – Executive Overview | "
    "Home Credit Default Risk Dashboard"
)


# ============================================================
# KEY INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("💡 Key Insights & Risk Analysis")


# ============================================================
# 1. OVERALL DEFAULT RATE
# ============================================================

st.write(
    f"🔴 **Overall Default Rate:** "
    f"{kpis['default_rate']:.2f}%"
)


# ============================================================
# 2. DEFAULT CUSTOMER COUNT
# ============================================================

st.write(
    f"⚠️ **Default Customers:** "
    f"{kpis['default_customers']:,} out of "
    f"{kpis['total_applications']:,} applications"
)


# ============================================================
# 3. AVERAGE CUSTOMER INCOME
# ============================================================

st.write(
    f"💰 **Average Customer Income:** "
    f"{kpis['avg_income']:,.2f}"
)


# ============================================================
# 4. AVERAGE LOAN AMOUNT
# ============================================================

st.write(
    f"💳 **Average Loan Amount:** "
    f"{kpis['avg_credit']:,.2f}"
)


# ============================================================
# 5. MOST COMMON INCOME TYPE
# ============================================================

most_common_income = (
    filtered_df["NAME_INCOME_TYPE"]
    .dropna()
    .mode()
)

if len(most_common_income) > 0:

    st.write(
        f"👔 **Most Common Income Type:** "
        f"{most_common_income.iloc[0]}"
    )


# ============================================================
# 6. MOST COMMON EDUCATION LEVEL
# ============================================================

most_common_education = (
    filtered_df["NAME_EDUCATION_TYPE"]
    .dropna()
    .mode()
)

if len(most_common_education) > 0:

    st.write(
        f"🎓 **Most Common Education Level:** "
        f"{most_common_education.iloc[0]}"
    )


# ============================================================
# 7. HIGHEST-RISK INCOME SEGMENT
# ============================================================

risk_data = (
    filtered_df
    .groupby("NAME_INCOME_TYPE")["TARGET"]
    .agg(
        Customers="count",
        Default_Rate="mean"
    )
    .reset_index()
)

risk_data["Default_Rate"] = (
    risk_data["Default_Rate"] * 100
)

# Remove very small groups
risk_data = risk_data[
    risk_data["Customers"] >= 100
]

if len(risk_data) > 0:

    highest_risk = risk_data.loc[
        risk_data["Default_Rate"].idxmax()
    ]

    st.write(
        f"🚨 **Highest-Risk Income Segment:** "
        f"{highest_risk['NAME_INCOME_TYPE']} "
        f"with a default rate of "
        f"**{highest_risk['Default_Rate']:.2f}%**."
    )


# ============================================================
# 8. HIGHEST-RISK GENDER
# ============================================================

gender_risk = (
    filtered_df
    .groupby("CODE_GENDER")["TARGET"]
    .agg(
        Customers="count",
        Default_Rate="mean"
    )
    .reset_index()
)

gender_risk["Default_Rate"] = (
    gender_risk["Default_Rate"] * 100
)

gender_risk = gender_risk[
    gender_risk["Customers"] >= 100
]

if len(gender_risk) > 0:

    highest_gender_risk = gender_risk.loc[
        gender_risk["Default_Rate"].idxmax()
    ]

    st.write(
        f"👤 **Highest-Risk Gender:** "
        f"{highest_gender_risk['CODE_GENDER']} "
        f"with a default rate of "
        f"**{highest_gender_risk['Default_Rate']:.2f}%**."
    )


# ============================================================
# 9. HIGHEST-RISK CONTRACT TYPE
# ============================================================

contract_risk = (
    filtered_df
    .groupby("NAME_CONTRACT_TYPE")["TARGET"]
    .agg(
        Customers="count",
        Default_Rate="mean"
    )
    .reset_index()
)

contract_risk["Default_Rate"] = (
    contract_risk["Default_Rate"] * 100
)

contract_risk = contract_risk[
    contract_risk["Customers"] >= 100
]

if len(contract_risk) > 0:

    highest_contract_risk = contract_risk.loc[
        contract_risk["Default_Rate"].idxmax()
    ]

    st.write(
        f"💳 **Highest-Risk Contract Type:** "
        f"{highest_contract_risk['NAME_CONTRACT_TYPE']} "
        f"with a default rate of "
        f"**{highest_contract_risk['Default_Rate']:.2f}%**."
    )


# ============================================================
# 10. CREDIT AMOUNT INSIGHT
# ============================================================

median_credit = filtered_df["AMT_CREDIT"].median()

high_credit_customers = filtered_df[
    filtered_df["AMT_CREDIT"] > median_credit
]

if len(high_credit_customers) > 0:

    high_credit_default_rate = (
        high_credit_customers["TARGET"].mean() * 100
    )

    st.write(
        f"💵 **High-Credit Customer Default Rate:** "
        f"Customers with credit above the median have a "
        f"default rate of "
        f"**{high_credit_default_rate:.2f}%**."
    )


# ============================================================
# 11. MANAGEMENT SUMMARY
# ============================================================

st.markdown("### 📌 Management Summary")

if kpis["default_rate"] >= 10:

    st.warning(
        f"⚠️ The portfolio shows a relatively high default rate "
        f"of **{kpis['default_rate']:.2f}%**. "
        f"Management should closely monitor high-risk customer "
        f"segments and strengthen credit-risk assessment."
    )

else:

    st.success(
        f"✅ The portfolio has a default rate of "
        f"**{kpis['default_rate']:.2f}%**. "
        f"Overall credit risk appears relatively controlled, "
        f"but high-risk segments should still be monitored."
    )