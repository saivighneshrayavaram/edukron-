import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# PAGE TITLE
# ============================================================

st.title("💼 Employment Analysis")


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
# BASIC CALCULATIONS
# ============================================================

avg_employment = df["EMPLOYMENT_YEARS"].mean()

occupation = (
    df["OCCUPATION_TYPE"]
    .mode(dropna=True)
)

income_type = (
    df["NAME_INCOME_TYPE"]
    .mode(dropna=True)
)

if len(income_type) > 0:
    income_type = income_type.iloc[0]
else:
    income_type = "N/A"


# ============================================================
# OCCUPATION RISK
# ============================================================

occupation_risk = (
    df.dropna(subset=["OCCUPATION_TYPE"])
    .groupby("OCCUPATION_TYPE")["TARGET"]
    .mean()
    .sort_values(ascending=False)
)

if len(occupation_risk) > 0:

    highest_risk_occupation = (
        occupation_risk.index[0]
    )

else:

    highest_risk_occupation = "N/A"


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Average Employment Years",
    f"{avg_employment:.1f}"
)


c2.metric(
    "Most Common Occupation",
    occupation.iloc[0]
    if len(occupation)
    else "N/A"
)


c3.metric(
    "Most Common Income Type",
    income_type
)


c4.metric(
    "Highest Risk Occupation",
    highest_risk_occupation
)


# ============================================================
# 1. EMPLOYMENT YEARS DISTRIBUTION
# ============================================================

fig = px.histogram(
    df,
    x="EMPLOYMENT_YEARS",
    nbins=40,
    title="Employment Years Distribution"
)

fig.update_traces(
    texttemplate="%{y:,.0f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Employment Years",
    yaxis_title="Number of Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 2. DEFAULT RATE BY EMPLOYMENT YEARS
# ============================================================
# IMPORTANT:
# We group employment years into ranges.
# This avoids the huge number of labels shown in your screenshot.
# ============================================================

df["EMPLOYMENT_GROUP"] = pd.cut(
    df["EMPLOYMENT_YEARS"],
    bins=[
        0,
        5,
        10,
        15,
        20,
        25,
        30,
        float("inf")
    ],
    labels=[
        "0-5 Years",
        "5-10 Years",
        "10-15 Years",
        "15-20 Years",
        "20-25 Years",
        "25-30 Years",
        "30+ Years"
    ],
    include_lowest=True
)


employment_default = (
    df.groupby(
        "EMPLOYMENT_GROUP",
        observed=True
    )["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

employment_default.columns = [
    "Employment Group",
    "Default Rate"
]


fig = px.bar(
    employment_default,
    x="Employment Group",
    y="Default Rate",
    text="Default Rate",
    title="Default Rate by Employment Years"
)


fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="inside"
)


fig.update_layout(
    xaxis_title="Employment Duration",
    yaxis_title="Default Rate (%)"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 3. APPLICATIONS BY INCOME TYPE
# ============================================================

data = (
    df["NAME_INCOME_TYPE"]
    .value_counts()
    .reset_index()
)

data.columns = [
    "Income Type",
    "Applications"
]


fig = px.bar(
    data,
    x="Income Type",
    y="Applications",
    text="Applications",
    title="Applications by Income Type"
)


fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside"
)


fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Income Type",
    yaxis_title="Applications"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 4. DEFAULT RATE BY INCOME TYPE
# ============================================================

data = (
    df.dropna(subset=["NAME_INCOME_TYPE"])
    .groupby("NAME_INCOME_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
    .reset_index()
)

data.columns = [
    "Income Type",
    "Default Rate"
]


fig = px.bar(
    data,
    x="Income Type",
    y="Default Rate",
    text="Default Rate",
    title="Default Rate by Income Type"
)


fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="inside"
)


fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Income Type",
    yaxis_title="Default Rate (%)"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 5. APPLICATIONS BY OCCUPATION
# ============================================================

data = (
    df["OCCUPATION_TYPE"]
    .dropna()
    .value_counts()
    .reset_index()
)

data.columns = [
    "Occupation",
    "Applications"
]


fig = px.bar(
    data,
    x="Occupation",
    y="Applications",
    text="Applications",
    title="Applications by Occupation"
)


fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside"
)


fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Occupation",
    yaxis_title="Applications"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 6. DEFAULT RATE BY OCCUPATION
# ============================================================

data = (
    df.dropna(subset=["OCCUPATION_TYPE"])
    .groupby("OCCUPATION_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
    .reset_index()
)

data.columns = [
    "Occupation",
    "Default Rate"
]


fig = px.bar(
    data,
    x="Occupation",
    y="Default Rate",
    text="Default Rate",
    title="Default Rate by Occupation"
)


fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="inside"
)


fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Occupation",
    yaxis_title="Default Rate (%)"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 7. TOP 20 ORGANIZATION TYPES BY DEFAULT RATE
# ============================================================

data = (
    df.dropna(subset=["ORGANIZATION_TYPE"])
    .groupby("ORGANIZATION_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)

data.columns = [
    "Organization",
    "Default Rate"
]


fig = px.bar(
    data,
    x="Organization",
    y="Default Rate",
    text="Default Rate",
    title="Top 20 Organization Types by Default Rate"
)


fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="inside"
)


fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Organization",
    yaxis_title="Default Rate (%)"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 📌 EMPLOYMENT KEY INSIGHTS
# ============================================================

st.markdown("---")

st.subheader(
    "📌 Employment Key Insights"
)


# ============================================================
# OVERALL METRICS
# ============================================================

total_customers = len(df)

overall_default_rate = (
    df["TARGET"].mean() * 100
)


# ============================================================
# EMPLOYMENT YEARS RISK
# ============================================================

employment_risk = (
    df.groupby(
        "EMPLOYMENT_GROUP",
        observed=True
    )["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)


if len(employment_risk) > 0:

    highest_risk_employment_years = (
        employment_risk.index[0]
    )

    highest_employment_default = (
        employment_risk.iloc[0]
    )

else:

    highest_risk_employment_years = "N/A"
    highest_employment_default = 0


# ============================================================
# INCOME TYPE RISK
# ============================================================

income_risk = (
    df.dropna(subset=["NAME_INCOME_TYPE"])
    .groupby("NAME_INCOME_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)


if len(income_risk) > 0:

    highest_risk_income_type = (
        income_risk.index[0]
    )

    highest_income_default = (
        income_risk.iloc[0]
    )

    lowest_risk_income_type = (
        income_risk.index[-1]
    )

    lowest_income_default = (
        income_risk.iloc[-1]
    )

else:

    highest_risk_income_type = "N/A"
    highest_income_default = 0

    lowest_risk_income_type = "N/A"
    lowest_income_default = 0


# ============================================================
# OCCUPATION RISK
# ============================================================

occupation_risk = (
    df.dropna(subset=["OCCUPATION_TYPE"])
    .groupby("OCCUPATION_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)


if len(occupation_risk) > 0:

    highest_risk_occupation = (
        occupation_risk.index[0]
    )

    highest_occupation_default = (
        occupation_risk.iloc[0]
    )

    lowest_risk_occupation = (
        occupation_risk.index[-1]
    )

    lowest_occupation_default = (
        occupation_risk.iloc[-1]
    )

else:

    highest_risk_occupation = "N/A"
    highest_occupation_default = 0

    lowest_risk_occupation = "N/A"
    lowest_occupation_default = 0


# ============================================================
# ORGANIZATION RISK
# ============================================================

organization_risk = (
    df.dropna(subset=["ORGANIZATION_TYPE"])
    .groupby("ORGANIZATION_TYPE")["TARGET"]
    .agg(["mean", "count"])
    .reset_index()
)


organization_risk["Default Rate"] = (
    organization_risk["mean"] * 100
)


reliable_organizations = organization_risk[
    organization_risk["count"] >= 50
]


if len(reliable_organizations) > 0:

    reliable_organizations = (
        reliable_organizations
        .sort_values(
            "Default Rate",
            ascending=False
        )
    )

    highest_risk_organization = (
        reliable_organizations.iloc[0][
            "ORGANIZATION_TYPE"
        ]
    )

    highest_organization_default = (
        reliable_organizations.iloc[0][
            "Default Rate"
        ]
    )

else:

    highest_risk_organization = "N/A"
    highest_organization_default = 0


# ============================================================
# INCOME TYPE WITH HIGHEST AVERAGE INCOME
# ============================================================

income_by_type = (
    df.dropna(subset=["NAME_INCOME_TYPE"])
    .groupby("NAME_INCOME_TYPE")[
        "AMT_INCOME_TOTAL"
    ]
    .mean()
    .sort_values(ascending=False)
)


if len(income_by_type) > 0:

    highest_income_group = (
        income_by_type.index[0]
    )

    highest_average_income = (
        income_by_type.iloc[0]
    )

else:

    highest_income_group = "N/A"
    highest_average_income = 0


# ============================================================
# OCCUPATION WITH HIGHEST AVERAGE INCOME
# ============================================================

occupation_income = (
    df.dropna(subset=["OCCUPATION_TYPE"])
    .groupby("OCCUPATION_TYPE")[
        "AMT_INCOME_TOTAL"
    ]
    .mean()
    .sort_values(ascending=False)
)


if len(occupation_income) > 0:

    highest_income_occupation = (
        occupation_income.index[0]
    )

    highest_occupation_income = (
        occupation_income.iloc[0]
    )

else:

    highest_income_occupation = "N/A"
    highest_occupation_income = 0


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Overall Default Rate",
    f"{overall_default_rate:.2f}%"
)


c2.metric(
    "Average Employment",
    f"{avg_employment:.1f} Years"
)


c3.metric(
    "Highest-Risk Income Type",
    str(highest_risk_income_type)
)


c4.metric(
    "Highest-Risk Occupation",
    str(highest_risk_occupation)
)


# ============================================================
# INSIGHT CARDS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.error(
        f"🚨 **Highest-Risk Occupation**\n\n"
        f"**{highest_risk_occupation}** has the highest "
        f"observed default rate of "
        f"**{highest_occupation_default:.2f}%**."
    )


    st.warning(
        f"💼 **Highest-Risk Income Type**\n\n"
        f"**{highest_risk_income_type}** has an observed "
        f"default rate of "
        f"**{highest_income_default:.2f}%**."
    )


    st.success(
        f"🟢 **Lowest-Risk Occupation**\n\n"
        f"**{lowest_risk_occupation}** has the lowest "
        f"observed default rate of "
        f"**{lowest_occupation_default:.2f}%**."
    )


with col2:

    st.info(
        f"⏳ **Employment Duration Risk**\n\n"
        f"Customers in the **{highest_risk_employment_years}** "
        f"employment group show the highest observed "
        f"default rate of "
        f"**{highest_employment_default:.2f}%**."
    )


    st.warning(
        f"🏢 **Highest-Risk Organization Type**\n\n"
        f"**{highest_risk_organization}** has an observed "
        f"default rate of "
        f"**{highest_organization_default:.2f}%** "
        f"among organizations with sufficient records."
    )


    st.info(
        f"💰 **Highest-Income Employment Group**\n\n"
        f"**{highest_income_group}** has the highest "
        f"average income of "
        f"**{highest_average_income:,.0f}**."
    )


# ============================================================
# INCOME TYPE SUMMARY
# ============================================================

st.markdown("---")

st.subheader(
    "💰 Employment Income Summary"
)


income_summary = (
    df.dropna(subset=["NAME_INCOME_TYPE"])
    .groupby("NAME_INCOME_TYPE")
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Default_Rate=("TARGET", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Avg_Annuity=("AMT_ANNUITY", "mean")
    )
    .reset_index()
)


income_summary["Default_Rate"] *= 100


income_summary.columns = [
    "Income Type",
    "Applications",
    "Default Rate",
    "Average Income",
    "Average Credit",
    "Average Annuity"
]


income_summary = (
    income_summary
    .sort_values(
        "Default Rate",
        ascending=False
    )
)


st.dataframe(
    income_summary,
    use_container_width=True
)


# ============================================================
# OCCUPATION RISK SUMMARY
# ============================================================

st.markdown("---")

st.subheader(
    "💼 Occupation Risk Summary"
)


occupation_summary = (
    df.dropna(subset=["OCCUPATION_TYPE"])
    .groupby("OCCUPATION_TYPE")
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Default_Rate=("TARGET", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean")
    )
    .reset_index()
)


occupation_summary["Default_Rate"] *= 100


occupation_summary.columns = [
    "Occupation",
    "Applications",
    "Default Rate",
    "Average Income",
    "Average Credit"
]


occupation_summary = (
    occupation_summary
    .sort_values(
        "Default Rate",
        ascending=False
    )
)


st.dataframe(
    occupation_summary,
    use_container_width=True
)


# ============================================================
# ORGANIZATION RISK SUMMARY
# ============================================================

st.markdown("---")

st.subheader(
    "🏢 Organization Risk Summary"
)


organization_summary = (
    df.dropna(subset=["ORGANIZATION_TYPE"])
    .groupby("ORGANIZATION_TYPE")
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Default_Rate=("TARGET", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean")
    )
    .reset_index()
)


organization_summary["Default_Rate"] *= 100


organization_summary.columns = [
    "Organization",
    "Applications",
    "Default Rate",
    "Average Income",
    "Average Credit"
]


organization_summary = (
    organization_summary
    .sort_values(
        "Default Rate",
        ascending=False
    )
    .head(20)
)


st.dataframe(
    organization_summary,
    use_container_width=True
)


# ============================================================
# BUSINESS SUMMARY
# ============================================================

st.markdown("---")

st.subheader(
    "📝 Employment Analysis Summary"
)


st.write(
    f"• The filtered dataset contains "
    f"**{total_customers:,} customers** with an overall "
    f"default rate of **{overall_default_rate:.2f}%**."
)


st.write(
    f"• The average employment duration is "
    f"**{avg_employment:.1f} years**."
)


st.write(
    f"• **{income_type}** is the most common income type "
    f"among the filtered customers."
)


st.write(
    f"• **{highest_risk_income_type}** has the highest "
    f"observed default rate among income types at "
    f"**{highest_income_default:.2f}%**."
)


st.write(
    f"• **{highest_risk_occupation}** has the highest "
    f"observed occupation-level default rate at "
    f"**{highest_occupation_default:.2f}%**."
)


st.write(
    f"• **{highest_risk_organization}** has the highest "
    f"observed organization-level default rate among "
    f"organizations with at least 50 customers."
)


st.write(
    f"• **{highest_income_occupation}** has the highest "
    f"average income among occupation groups at "
    f"**{highest_occupation_income:,.0f}**."
)


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

st.markdown(
    "### 💡 Business Recommendation"
)


if highest_income_default > overall_default_rate:

    st.warning(
        f"🔴 **{highest_risk_income_type}** shows a default "
        f"rate above the overall portfolio average. "
        f"This employment/income segment may require "
        f"additional risk assessment."
    )

else:

    st.success(
        "🟢 Income-type default rates are generally "
        "within the overall portfolio range."
    )


if highest_occupation_default > overall_default_rate:

    st.warning(
        f"⚠️ **{highest_risk_occupation}** has an observed "
        f"default rate above the portfolio average and "
        f"could be monitored as a higher-risk occupation "
        f"segment."
    )

else:

    st.info(
        "📊 Occupation-level default rates are generally "
        "within the overall portfolio range."
    )


# ============================================================
# NOTE
# ============================================================

st.caption(
    "Note: Employment type, occupation, and organization "
    "are observed associations with default behavior and "
    "should not be interpreted as causal relationships."
)