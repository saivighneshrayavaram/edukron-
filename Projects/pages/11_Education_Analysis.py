import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# TITLE
# ============================================================

st.title("🎓 Education Analysis")


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()
df = clean_data(df)
df = create_features(df)
df = apply_sidebar_filters(df)


# ============================================================
# EDUCATION SUMMARY
# ============================================================

summary = (
    df.groupby("NAME_EDUCATION_TYPE")
    .agg(
        Customers=("SK_ID_CURR", "count"),
        Default_Rate=("TARGET", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Avg_Annuity=("AMT_ANNUITY", "mean"),
        Avg_Ratio=("CREDIT_INCOME_RATIO", "mean")
    )
    .reset_index()
)

summary["Default_Rate"] *= 100


# ============================================================
# KEY VALUES
# ============================================================

most_common = df["NAME_EDUCATION_TYPE"].mode().iloc[0]

highest_income = summary.loc[
    summary["Avg_Income"].idxmax(),
    "NAME_EDUCATION_TYPE"
]

lowest_default = summary.loc[
    summary["Default_Rate"].idxmin(),
    "NAME_EDUCATION_TYPE"
]

highest_default = summary.loc[
    summary["Default_Rate"].idxmax(),
    "NAME_EDUCATION_TYPE"
]


# ============================================================
# KPI CARDS
# ============================================================

c1, c2 = st.columns(2)

c1.metric(
    "Most Common Education",
    most_common
)

c2.metric(
    "Highest Income Education",
    highest_income
)

c1.metric(
    "Lowest Default Education",
    lowest_default
)

c2.metric(
    "Highest Default Education",
    highest_default
)


# ============================================================
# 1. CUSTOMERS BY EDUCATION
# ============================================================

fig = px.bar(
    summary,
    x="NAME_EDUCATION_TYPE",
    y="Customers",
    title="Customers by Education",
    text="Customers"
)

fig.update_traces(
    texttemplate="%{text:,}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 2. DEFAULT RATE BY EDUCATION
# ============================================================

fig = px.bar(
    summary,
    x="NAME_EDUCATION_TYPE",
    y="Default_Rate",
    title="Default Rate by Education",
    text="Default_Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 3. INCOME BY EDUCATION
# ============================================================

fig = px.bar(
    summary,
    x="NAME_EDUCATION_TYPE",
    y="Avg_Income",
    title="Income by Education",
    text="Avg_Income"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 4. CREDIT BY EDUCATION
# ============================================================

fig = px.bar(
    summary,
    x="NAME_EDUCATION_TYPE",
    y="Avg_Credit",
    title="Credit by Education",
    text="Avg_Credit"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 5. ANNUITY BY EDUCATION
# ============================================================

fig = px.bar(
    summary,
    x="NAME_EDUCATION_TYPE",
    y="Avg_Annuity",
    title="Annuity by Education",
    text="Avg_Annuity"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 6. CREDIT-TO-INCOME RATIO BY EDUCATION
# ============================================================

fig = px.bar(
    summary,
    x="NAME_EDUCATION_TYPE",
    y="Avg_Ratio",
    title="Credit-to-Income Ratio by Education",
    text="Avg_Ratio"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# EDUCATION SUMMARY TABLE
# ============================================================

st.dataframe(
    summary,
    use_container_width=True
)