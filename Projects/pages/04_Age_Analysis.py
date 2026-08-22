import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Age Analysis",
    page_icon="🎂",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎂 Age Analysis")

st.markdown("""
This page analyzes customer age distribution and examines
how age groups are associated with credit default risk.
""")


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

if df.empty:

    st.warning("⚠️ No customers match the selected filters.")

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

average_age = df["AGE"].mean()

minimum_age = df["AGE"].min()

maximum_age = df["AGE"].max()

median_age = df["AGE"].median()

total_customers = len(df)

age_group_counts = (
    df["AGE_GROUP"]
    .value_counts()
    .sort_index()
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📌 Age KPIs")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Customers",
    f"{total_customers:,}"
)

c2.metric(
    "Average Age",
    f"{average_age:.1f} Years"
)

c3.metric(
    "Median Age",
    f"{median_age:.1f} Years"
)

c4.metric(
    "Minimum Age",
    f"{minimum_age:.1f} Years"
)

c5.metric(
    "Maximum Age",
    f"{maximum_age:.1f} Years"
)


st.markdown("---")


# ============================================================
# AGE DISTRIBUTION
# ============================================================

st.subheader("📊 Age Distribution")


col1, col2 = st.columns(2)


# ============================================================
# 1. AGE GROUP DISTRIBUTION
# ============================================================

with col1:

    age_data = (
        df["AGE_GROUP"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_data.columns = [
        "Age Group",
        "Customers"
    ]

    fig = px.bar(
        age_data,
        x="Age Group",
        y="Customers",
        title="Customers by Age Group",
        text="Customers"
    )

    # VALUES INSIDE BAR
    fig.update_traces(
        texttemplate="%{text:,}",
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
# 2. AGE HISTOGRAM
# ============================================================

with col2:

    fig = px.histogram(
        df,
        x="AGE",
        nbins=30,
        title="Age Distribution",
        text_auto=True
    )

    # VALUES INSIDE HISTOGRAM
    fig.update_traces(
        textposition="inside"
    )

    fig.update_layout(
        uniformtext_minsize=9,
        uniformtext_mode="hide"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DEFAULT RISK BY AGE
# ============================================================

st.subheader("⚠️ Default Risk by Age")


col1, col2 = st.columns(2)


# ============================================================
# 3. DEFAULT RATE BY AGE GROUP
# ============================================================

with col1:

    age_default = (
        df.groupby(
            "AGE_GROUP",
            observed=True
        )["TARGET"]
        .mean()
        .mul(100)
        .reset_index()
    )

    age_default.columns = [
        "Age Group",
        "Default Rate"
    ]

    fig = px.bar(
        age_default,
        x="Age Group",
        y="Default Rate",
        title="Default Rate by Age Group",
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
# 4. CUSTOMERS BY AGE GROUP - DONUT
# ============================================================

with col2:

    fig = px.pie(
        age_data,
        names="Age Group",
        values="Customers",
        hole=0.5,
        title="Customer Distribution by Age Group"
    )

    # VALUES INSIDE DONUT
    fig.update_traces(
        textposition="inside",
        textinfo="label+value",
        texttemplate="%{label}<br>%{value:,}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# AVERAGE CREDIT BY AGE GROUP
# ============================================================

st.subheader("💰 Financial Analysis by Age")


credit_age = (
    df.groupby(
        "AGE_GROUP",
        observed=True
    )["AMT_CREDIT"]
    .mean()
    .reset_index()
)

credit_age.columns = [
    "Age Group",
    "Average Credit"
]


fig = px.bar(
    credit_age,
    x="Age Group",
    y="Average Credit",
    title="Average Credit Amount by Age Group",
    text="Average Credit"
)

# VALUES INSIDE BAR
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
# AVERAGE INCOME BY AGE GROUP
# ============================================================

income_age = (
    df.groupby(
        "AGE_GROUP",
        observed=True
    )["AMT_INCOME_TOTAL"]
    .mean()
    .reset_index()
)

income_age.columns = [
    "Age Group",
    "Average Income"
]


fig = px.bar(
    income_age,
    x="Age Group",
    y="Average Income",
    title="Average Income by Age Group",
    text="Average Income"
)

# VALUES INSIDE BAR
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
# AVERAGE ANNUITY BY AGE GROUP
# ============================================================

annuity_age = (
    df.groupby(
        "AGE_GROUP",
        observed=True
    )["AMT_ANNUITY"]
    .mean()
    .reset_index()
)

annuity_age.columns = [
    "Age Group",
    "Average Annuity"
]


fig = px.bar(
    annuity_age,
    x="Age Group",
    y="Average Annuity",
    title="Average Annuity by Age Group",
    text="Average Annuity"
)

# VALUES INSIDE BAR
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
# KEY INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("💡 Key Insights")


# ============================================================
# HIGHEST CUSTOMER AGE GROUP
# ============================================================

if len(age_group_counts) > 0:

    most_common_age_group = (
        age_group_counts.idxmax()
    )

    most_common_age_count = (
        age_group_counts.max()
    )

    st.write(
        f"👥 **Most Common Age Group:** "
        f"**{most_common_age_group}** has the highest number "
        f"of customers with **{most_common_age_count:,} customers**."
    )


# ============================================================
# HIGHEST DEFAULT AGE GROUP
# ============================================================

if len(age_default) > 0:

    highest_risk_age = (
        age_default.loc[
            age_default["Default Rate"].idxmax(),
            "Age Group"
        ]
    )

    highest_risk_rate = (
        age_default["Default Rate"].max()
    )

    st.write(
        f"🔴 **Highest Age Risk:** "
        f"Age group **{highest_risk_age}** has the highest "
        f"default rate of **{highest_risk_rate:.2f}%**."
    )


# ============================================================
# LOWEST DEFAULT AGE GROUP
# ============================================================

if len(age_default) > 0:

    lowest_risk_age = (
        age_default.loc[
            age_default["Default Rate"].idxmin(),
            "Age Group"
        ]
    )

    lowest_risk_rate = (
        age_default["Default Rate"].min()
    )

    st.write(
        f"🟢 **Lowest Age Risk:** "
        f"Age group **{lowest_risk_age}** has the lowest "
        f"default rate of **{lowest_risk_rate:.2f}%**."
    )


# ============================================================
# AGE SUMMARY
# ============================================================

st.write(
    f"🎂 **Age Summary:** "
    f"The average customer age is **{average_age:.1f} years**, "
    f"with ages ranging from **{minimum_age:.1f} to "
    f"{maximum_age:.1f} years**."
)


# ============================================================
# EXECUTIVE AGE SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📝 Age Analysis Summary")

st.info(
    f"""
The filtered portfolio contains **{total_customers:,} customers**.

The average customer age is **{average_age:.1f} years**,
while the median age is **{median_age:.1f} years**.

The most common age group is **{most_common_age_group}**.

The highest observed default rate is in the
**{highest_risk_age}** age group at **{highest_risk_rate:.2f}%**.
"""
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Home Credit Default Risk Dashboard • Age Analysis"
)