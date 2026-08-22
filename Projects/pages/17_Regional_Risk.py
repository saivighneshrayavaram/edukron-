import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


st.title("🌍 Regional Risk Analysis")


df = load_data()
df = clean_data(df)
df = create_features(df)
df = apply_sidebar_filters(df)


# ============================================================
# CHECK EMPTY DATA
# ============================================================

if len(df) == 0:

    st.warning("No customers match the selected filters.")
    st.stop()


# ============================================================
# COMMON RATING
# ============================================================

common_rating = (
    df["REGION_RATING_CLIENT"]
    .mode()
    .iloc[0]
)


rating_risk = (
    df.groupby("REGION_RATING_CLIENT")["TARGET"]
    .mean()
    .sort_values(ascending=False)
)


highest_risk_rating = rating_risk.index[0]


avg_population = (
    df["REGION_POPULATION_RELATIVE"].mean()
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3 = st.columns(3)


c1.metric(
    "Most Common Region Rating",
    str(common_rating)
)


c2.metric(
    "Highest Risk Rating",
    str(highest_risk_rating)
)


c3.metric(
    "Average Population Indicator",
    f"{avg_population:.4f}"
)


# ============================================================
# 1. CUSTOMERS BY REGION RATING
# ============================================================

data = (
    df["REGION_RATING_CLIENT"]
    .value_counts()
    .reset_index()
)

data.columns = [
    "Region Rating",
    "Customers"
]


fig = px.bar(
    data,
    x="Region Rating",
    y="Customers",
    title="Customers by Region Rating",
    text="Customers"
)

fig.update_traces(
    textposition="inside",
    texttemplate="%{text:,}"
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
# 2. DEFAULT RATE BY REGION RATING
# ============================================================

data = (
    df.groupby("REGION_RATING_CLIENT")["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

data.columns = [
    "Region Rating",
    "Default Rate"
]


fig = px.bar(
    data,
    x="Region Rating",
    y="Default Rate",
    title="Default Rate by Region Rating",
    text="Default Rate"
)

fig.update_traces(
    textposition="inside",
    texttemplate="%{text:.2f}%"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide",
    yaxis_title="Default Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 3. AVERAGE CREDIT BY REGION RATING
# ============================================================

data = (
    df.groupby("REGION_RATING_CLIENT")["AMT_CREDIT"]
    .mean()
    .reset_index()
)


fig = px.bar(
    data,
    x="REGION_RATING_CLIENT",
    y="AMT_CREDIT",
    title="Average Credit by Region Rating",
    text="AMT_CREDIT"
)

fig.update_traces(
    textposition="inside",
    texttemplate="%{text:,.0f}"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide",
    yaxis_title="Average Credit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 4. AVERAGE INCOME BY REGION RATING
# ============================================================

data = (
    df.groupby("REGION_RATING_CLIENT")[
        "AMT_INCOME_TOTAL"
    ]
    .mean()
    .reset_index()
)


fig = px.bar(
    data,
    x="REGION_RATING_CLIENT",
    y="AMT_INCOME_TOTAL",
    title="Average Income by Region Rating",
    text="AMT_INCOME_TOTAL"
)

fig.update_traces(
    textposition="inside",
    texttemplate="%{text:,.0f}"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide",
    yaxis_title="Average Income"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 5. REGIONAL MISMATCH
# ============================================================

for column, title in [

    (
        "REG_REGION_NOT_LIVE_REGION",
        "Region Mismatch vs Default"
    ),

    (
        "REG_REGION_NOT_WORK_REGION",
        "Work Region Mismatch vs Default"
    ),

    (
        "REG_CITY_NOT_LIVE_CITY",
        "City Mismatch vs Default"
    ),

    (
        "REG_CITY_NOT_WORK_CITY",
        "Work City Mismatch vs Default"
    )

]:

    data = (
        df.groupby(column)["TARGET"]
        .mean()
        .mul(100)
        .reset_index()
    )

    data.columns = [
        column,
        "Default Rate"
    ]


    fig = px.bar(
        data,
        x=column,
        y="Default Rate",
        title=title,
        text="Default Rate"
    )

    fig.update_traces(
        textposition="inside",
        texttemplate="%{text:.2f}%"
    )

    fig.update_layout(
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        yaxis_title="Default Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 📌 REGIONAL RISK INSIGHTS
# ============================================================

st.markdown("---")
st.subheader("📌 Regional Risk Insights")


# ============================================================
# BASIC REGIONAL STATISTICS
# ============================================================

total_customers = len(df)


total_defaults = int(
    (df["TARGET"] == 1).sum()
)


overall_default_rate = (
    df["TARGET"].mean() * 100
)


# ============================================================
# HIGHEST / LOWEST RISK REGION
# ============================================================

rating_risk = (
    df.groupby("REGION_RATING_CLIENT")["TARGET"]
    .mean()
    .sort_values(ascending=False)
)


highest_risk_rating = rating_risk.index[0]


highest_risk_rate = (
    rating_risk.iloc[0] * 100
)


lowest_risk_rating = rating_risk.index[-1]


lowest_risk_rate = (
    rating_risk.iloc[-1] * 100
)


# ============================================================
# REGION CUSTOMER DISTRIBUTION
# ============================================================

region_counts = (
    df["REGION_RATING_CLIENT"]
    .value_counts()
)


most_populated_rating = (
    region_counts.index[0]
)


most_populated_count = (
    region_counts.iloc[0]
)


# ============================================================
# CREDIT BY REGION
# ============================================================

avg_credit_by_region = (
    df.groupby("REGION_RATING_CLIENT")[
        "AMT_CREDIT"
    ]
    .mean()
    .sort_values(ascending=False)
)


highest_credit_rating = (
    avg_credit_by_region.index[0]
)


highest_avg_credit = (
    avg_credit_by_region.iloc[0]
)


lowest_credit_rating = (
    avg_credit_by_region.index[-1]
)


lowest_avg_credit = (
    avg_credit_by_region.iloc[-1]
)


# ============================================================
# INCOME BY REGION
# ============================================================

avg_income_by_region = (
    df.groupby("REGION_RATING_CLIENT")[
        "AMT_INCOME_TOTAL"
    ]
    .mean()
    .sort_values(ascending=False)
)


highest_income_rating = (
    avg_income_by_region.index[0]
)


highest_avg_income = (
    avg_income_by_region.iloc[0]
)


# ============================================================
# POPULATION INDICATOR
# ============================================================

avg_population = (
    df["REGION_POPULATION_RELATIVE"].mean()
)


# ============================================================
# REGIONAL MISMATCH INSIGHTS
# ============================================================

mismatch_results = []


mismatch_columns = [

    (
        "REG_REGION_NOT_LIVE_REGION",
        "Region Live Mismatch"
    ),

    (
        "REG_REGION_NOT_WORK_REGION",
        "Region Work Mismatch"
    ),

    (
        "REG_CITY_NOT_LIVE_CITY",
        "City Live Mismatch"
    ),

    (
        "REG_CITY_NOT_WORK_CITY",
        "City Work Mismatch"
    )

]


for column, label in mismatch_columns:

    if column in df.columns:

        mismatch_data = (
            df.groupby(column)["TARGET"]
            .mean()
            * 100
        )

        if len(mismatch_data) > 0:

            highest_group = (
                mismatch_data.idxmax()
            )

            highest_rate = (
                mismatch_data.max()
            )

            mismatch_results.append({
                "Factor": label,
                "Group": highest_group,
                "Default Rate": highest_rate
            })


# ============================================================
# KPI SUMMARY
# ============================================================

c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Overall Default Rate",
    f"{overall_default_rate:.2f}%"
)


c2.metric(
    "Highest Risk Rating",
    str(highest_risk_rating)
)


c3.metric(
    "Highest Risk Default Rate",
    f"{highest_risk_rate:.2f}%"
)


c4.metric(
    "Most Common Rating",
    str(common_rating)
)


# ============================================================
# INSIGHT CARDS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.error(
        f"🚨 **Highest Regional Risk**\n\n"
        f"Region rating **{highest_risk_rating}** "
        f"has the highest default rate of "
        f"**{highest_risk_rate:.2f}%**."
    )


    st.success(
        f"🟢 **Lowest Regional Risk**\n\n"
        f"Region rating **{lowest_risk_rating}** "
        f"has the lowest default rate of "
        f"**{lowest_risk_rate:.2f}%**."
    )


    st.info(
        f"👥 **Largest Customer Group**\n\n"
        f"Region rating **{most_populated_rating}** "
        f"contains the highest number of customers "
        f"(**{most_populated_count:,}**)."
    )


with col2:

    st.info(
        f"💳 **Highest Average Credit**\n\n"
        f"Region rating **{highest_credit_rating}** "
        f"has the highest average credit of "
        f"**{highest_avg_credit:,.0f}**."
    )


    st.info(
        f"💰 **Highest Average Income**\n\n"
        f"Region rating **{highest_income_rating}** "
        f"has the highest average income of "
        f"**{highest_avg_income:,.0f}**."
    )


    st.info(
        f"🌍 **Population Indicator**\n\n"
        f"The average regional population indicator "
        f"is **{avg_population:.4f}**."
    )


# ============================================================
# REGIONAL MISMATCH INSIGHTS
# ============================================================

if len(mismatch_results) > 0:

    st.markdown(
        "### 🚨 Regional Mismatch Insights"
    )


    mismatch_df = pd.DataFrame(
        mismatch_results
    )


    mismatch_df["Default Rate"] = (
        mismatch_df["Default Rate"]
        .round(2)
    )


    st.dataframe(
        mismatch_df,
        use_container_width=True
    )


    highest_mismatch = (
        mismatch_df
        .sort_values(
            "Default Rate",
            ascending=False
        )
        .iloc[0]
    )


    st.warning(
        f"⚠️ **Highest Mismatch Risk:** "
        f"{highest_mismatch['Factor']} "
        f"shows the highest observed default rate "
        f"for group **{highest_mismatch['Group']}**, "
        f"at **{highest_mismatch['Default Rate']:.2f}%**."
    )


# ============================================================
# REGIONAL RISK SUMMARY
# ============================================================

st.markdown("---")
st.subheader("📝 Regional Risk Summary")


summary_points = []


summary_points.append(
    f"The filtered dataset contains **{total_customers:,} "
    f"customers**, with an overall default rate of "
    f"**{overall_default_rate:.2f}%**."
)


summary_points.append(
    f"Region rating **{highest_risk_rating}** has the "
    f"highest default rate at **{highest_risk_rate:.2f}%**, "
    f"while rating **{lowest_risk_rating}** has the lowest "
    f"default rate at **{lowest_risk_rate:.2f}%**."
)


summary_points.append(
    f"Region rating **{highest_credit_rating}** has the "
    f"highest average credit amount "
    f"(**{highest_avg_credit:,.0f}**)."
)


summary_points.append(
    f"Region rating **{highest_income_rating}** has the "
    f"highest average customer income "
    f"(**{highest_avg_income:,.0f}**)."
)


if len(mismatch_results) > 0:

    summary_points.append(
        f"Regional and city mismatch indicators should "
        f"be monitored because some mismatch groups show "
        f"different default rates."
    )


for point in summary_points:

    st.write(
        f"• {point}"
    )


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

st.markdown("### 💡 Business Recommendation")


if highest_risk_rate > overall_default_rate:

    st.warning(
        f"🔴 Region rating **{highest_risk_rating}** "
        f"has a default rate above the overall dataset "
        f"average. Applications from this region could "
        f"receive additional risk assessment."
    )

else:

    st.success(
        "🟢 Regional default rates are relatively "
        "consistent with the overall dataset."
    )


st.info(
    "📌 **Note:** Regional correlation and default-rate "
    "differences indicate associations in the dataset. "
    "They should not be treated as proof that geography "
    "causes loan default."
)