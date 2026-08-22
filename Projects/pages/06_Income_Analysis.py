import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# TITLE
# ============================================================

st.title("💰 Income Analysis")


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

    st.warning(
        "⚠️ No customers match the selected filters."
    )

    st.stop()


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)


c1.metric(
    "Total Income",
    f"{df['AMT_INCOME_TOTAL'].sum():,.0f}"
)


c2.metric(
    "Average Income",
    f"{df['AMT_INCOME_TOTAL'].mean():,.0f}"
)


c3.metric(
    "Median Income",
    f"{df['AMT_INCOME_TOTAL'].median():,.0f}"
)


c4.metric(
    "Maximum Income",
    f"{df['AMT_INCOME_TOTAL'].max():,.0f}"
)


default_income = df.loc[
    df["TARGET"] == 1,
    "AMT_INCOME_TOTAL"
].mean()


c5.metric(
    "Avg Income of Defaulters",
    f"{default_income:,.0f}"
)


# ============================================================
# 1. INCOME DISTRIBUTION
# ============================================================

fig = px.histogram(
    df,
    x="AMT_INCOME_TOTAL",
    nbins=50,
    title="Income Distribution",
    text_auto=True
)

fig.update_traces(
    textposition="inside"
)

fig.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 2. CUSTOMERS BY INCOME GROUP
# ============================================================

data = (
    df["INCOME_GROUP"]
    .value_counts()
    .reset_index()
)

data.columns = [
    "Income Group",
    "Customers"
]


fig = px.bar(
    data,
    x="Income Group",
    y="Customers",
    title="Customers by Income Group",
    text="Customers"
)

fig.update_traces(
    texttemplate="%{y:,}",
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
# 3. DEFAULT RATE BY INCOME GROUP
# ============================================================

data = (
    df.groupby(
        "INCOME_GROUP",
        observed=True
    )["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

data.columns = [
    "Income Group",
    "Default Rate"
]


fig = px.bar(
    data,
    x="Income Group",
    y="Default Rate",
    title="Default Rate by Income Group",
    text="Default Rate"
)

fig.update_traces(
    texttemplate="%{y:.2f}%",
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
# 4. INCOME VS CREDIT
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
        "AMT_CREDIT": "Credit Amount",
        "TARGET": "Default"
    },
    hover_data=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "TARGET"
    ]
)


# Show credit value near points
# Only useful when the number of points is manageable

if len(sample) <= 100:

    fig.update_traces(
        texttemplate="%{y:,.0f}",
        textposition="top center"
    )


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 5. AVERAGE INCOME BY EDUCATION
# ============================================================

data = (
    df.groupby(
        "NAME_EDUCATION_TYPE"
    )["AMT_INCOME_TOTAL"]
    .mean()
    .sort_values(
        ascending=False
    )
    .reset_index()
)


fig = px.bar(
    data,
    x="NAME_EDUCATION_TYPE",
    y="AMT_INCOME_TOTAL",
    title="Average Income by Education",
    text="AMT_INCOME_TOTAL"
)


fig.update_traces(
    texttemplate="%{y:,.0f}",
    textposition="inside",
    insidetextanchor="middle"
)


fig.update_layout(
    xaxis_tickangle=-45,
    uniformtext_minsize=8,
    uniformtext_mode="hide"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 📌 KEY INCOME INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("📌 Key Income Insights")


# ============================================================
# BASIC METRICS
# ============================================================

total_customers = len(df)

overall_default_rate = (
    df["TARGET"].mean() * 100
)

avg_income = (
    df["AMT_INCOME_TOTAL"].mean()
)

median_income = (
    df["AMT_INCOME_TOTAL"].median()
)

max_income = (
    df["AMT_INCOME_TOTAL"].max()
)

min_income = (
    df["AMT_INCOME_TOTAL"].min()
)


# ============================================================
# DEFAULT VS NON-DEFAULT INCOME
# ============================================================

target_income = (
    df.groupby("TARGET")[
        "AMT_INCOME_TOTAL"
    ].mean()
)


default_avg_income = target_income.get(
    1,
    0
)

non_default_avg_income = target_income.get(
    0,
    0
)


# ============================================================
# INCOME GROUP RISK
# ============================================================

income_risk = (
    df.groupby(
        "INCOME_GROUP",
        observed=True
    )
    .agg(
        Customers=(
            "SK_ID_CURR",
            "count"
        ),
        Avg_Income=(
            "AMT_INCOME_TOTAL",
            "mean"
        ),
        Default_Rate=(
            "TARGET",
            "mean"
        ),
        Avg_Credit=(
            "AMT_CREDIT",
            "mean"
        )
    )
    .reset_index()
)


income_risk["Default_Rate"] *= 100


# ============================================================
# HIGHEST RISK INCOME GROUP
# ============================================================

highest_risk_income = (
    income_risk
    .sort_values(
        "Default_Rate",
        ascending=False
    )
    .iloc[0]
)


highest_risk_group = (
    highest_risk_income[
        "INCOME_GROUP"
    ]
)


highest_risk_rate = (
    highest_risk_income[
        "Default_Rate"
    ]
)


# ============================================================
# HIGHEST INCOME GROUP
# ============================================================

highest_income_group = (
    income_risk
    .sort_values(
        "Avg_Income",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# EDUCATION ANALYSIS
# ============================================================

education_income = (
    df.groupby(
        "NAME_EDUCATION_TYPE"
    )
    .agg(
        Customers=(
            "SK_ID_CURR",
            "count"
        ),
        Avg_Income=(
            "AMT_INCOME_TOTAL",
            "mean"
        ),
        Default_Rate=(
            "TARGET",
            "mean"
        )
    )
    .reset_index()
)


education_income[
    "Default_Rate"
] *= 100


highest_education_income = (
    education_income
    .sort_values(
        "Avg_Income",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# INCOME VS CREDIT
# ============================================================

avg_credit = (
    df["AMT_CREDIT"].mean()
)


avg_credit_income_ratio = (
    df["CREDIT_INCOME_RATIO"].mean()
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Average Income",
    f"{avg_income:,.0f}"
)


c2.metric(
    "Median Income",
    f"{median_income:,.0f}"
)


c3.metric(
    "Highest-Risk Income Group",
    str(highest_risk_group)
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
        f"""
        🚨 **Highest-Risk Income Group**

        **{highest_risk_group}** has the highest observed
        default rate of **{highest_risk_rate:.2f}%**.
        """
    )


    if default_avg_income < non_default_avg_income:

        st.warning(
            f"""
            ⚠️ **Lower Income Among Defaulters**

            Defaulters have an average income of
            **{default_avg_income:,.0f}**, compared with
            **{non_default_avg_income:,.0f}** for
            non-defaulters.
            """
        )

    else:

        st.info(
            f"""
            📊 **Income Comparison**

            Defaulters have an average income of
            **{default_avg_income:,.0f}**, compared with
            **{non_default_avg_income:,.0f}** for
            non-defaulters.
            """
        )


with col2:

    st.info(
        f"""
        💰 **Highest-Income Group**

        **{highest_income_group['INCOME_GROUP']}**
        has the highest average income of
        **{highest_income_group['Avg_Income']:,.0f}**.
        """
    )


    st.info(
        f"""
        🎓 **Highest Income by Education**

        **{highest_education_income['NAME_EDUCATION_TYPE']}**
        has the highest average income of
        **{highest_education_income['Avg_Income']:,.0f}**.
        """
    )


# ============================================================
# INCOME GROUP SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📊 Income Group Summary")


income_display = income_risk.copy()


income_display.columns = [
    "Income Group",
    "Customers",
    "Average Income",
    "Default Rate",
    "Average Credit"
]


st.dataframe(
    income_display,
    use_container_width=True
)


# ============================================================
# EDUCATION SUMMARY
# ============================================================

st.subheader("🎓 Income by Education")


education_display = (
    education_income.copy()
)


education_display.columns = [
    "Education",
    "Customers",
    "Average Income",
    "Default Rate"
]


education_display = (
    education_display
    .sort_values(
        "Average Income",
        ascending=False
    )
)


st.dataframe(
    education_display,
    use_container_width=True
)


# ============================================================
# BUSINESS SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📝 Income Analysis Summary")


st.write(
    f"• The filtered dataset contains "
    f"**{total_customers:,} customers** with an overall "
    f"default rate of **{overall_default_rate:.2f}%**."
)


st.write(
    f"• The average customer income is "
    f"**{avg_income:,.0f}**, while the median income is "
    f"**{median_income:,.0f}**."
)


st.write(
    f"• The maximum observed income is "
    f"**{max_income:,.0f}**."
)


st.write(
    f"• The **{highest_risk_group}** income group has the "
    f"highest observed default rate of "
    f"**{highest_risk_rate:.2f}%**."
)


st.write(
    f"• **{highest_income_group['INCOME_GROUP']}** has "
    f"the highest average income."
)


st.write(
    f"• **{highest_education_income['NAME_EDUCATION_TYPE']}** "
    f"has the highest average income among education groups."
)


st.write(
    f"• The average credit-to-income ratio is "
    f"**{avg_credit_income_ratio:.2f}**, showing the "
    f"relationship between borrowing and earning capacity."
)


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

st.markdown("### 💡 Business Recommendation")


if highest_risk_rate > overall_default_rate:

    st.warning(
        f"""
        ⚠️ The **{highest_risk_group}** income group has
        a default rate above the overall portfolio average.
        Income should be evaluated together with credit
        amount, annuity burden, employment stability, and
        external credit scores.
        """
    )

else:

    st.info(
        """
        📊 Income group alone does not show a substantially
        higher default rate than the overall portfolio.
        Income should therefore be combined with other
        financial risk indicators.
        """
    )


st.caption(
    "Note: Income level does not directly cause or prevent "
    "default. These insights represent observed patterns "
    "within the dataset."
)