import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# TITLE
# ============================================================

st.title("⚠️ Annuity Burden Analysis")


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

    st.warning("No customers match the selected filters.")
    st.stop()


# ============================================================
# BASIC METRICS
# ============================================================

avg_ratio = df["ANNUITY_INCOME_RATIO"].mean()
max_ratio = df["ANNUITY_INCOME_RATIO"].max()


c1, c2 = st.columns(2)

c1.metric(
    "Average Annuity/Income Ratio",
    f"{avg_ratio:.3f}"
)

c2.metric(
    "Highest Ratio",
    f"{max_ratio:.3f}"
)


# ============================================================
# 1. ANNUITY-TO-INCOME DISTRIBUTION
# ============================================================

fig = px.histogram(
    df,
    x="ANNUITY_INCOME_RATIO",
    nbins=50,
    title="Annuity-to-Income Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 2. DEFAULT RATE BY ANNUITY BURDEN
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
    "Burden Group",
    "Default Rate"
]

fig = px.bar(
    data,
    x="Burden Group",
    y="Default Rate",
    title="Default Rate by Annuity Burden",
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
# 3. ANNUITY/INCOME RATIO BY GENDER
# ============================================================

data = (
    df.groupby("CODE_GENDER")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
    .reset_index()
)

fig = px.bar(
    data,
    x="CODE_GENDER",
    y="ANNUITY_INCOME_RATIO",
    title="Annuity/Income Ratio by Gender",
    text="ANNUITY_INCOME_RATIO"
)

# VALUES INSIDE BAR
fig.update_traces(
    texttemplate="%{text:.3f}",
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
# 4. ANNUITY/INCOME RATIO BY INCOME TYPE
# ============================================================

data = (
    df.groupby("NAME_INCOME_TYPE")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    data,
    x="NAME_INCOME_TYPE",
    y="ANNUITY_INCOME_RATIO",
    title="Annuity/Income Ratio by Income Type",
    text="ANNUITY_INCOME_RATIO"
)

# VALUES INSIDE BAR
fig.update_traces(
    texttemplate="%{text:.3f}",
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
# 5. ANNUITY/INCOME RATIO BY EDUCATION
# ============================================================

data = (
    df.groupby("NAME_EDUCATION_TYPE")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    data,
    x="NAME_EDUCATION_TYPE",
    y="ANNUITY_INCOME_RATIO",
    title="Annuity/Income Ratio by Education",
    text="ANNUITY_INCOME_RATIO"
)

# VALUES INSIDE BAR
fig.update_traces(
    texttemplate="%{text:.3f}",
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
# 6. ANNUITY/INCOME RATIO VS TARGET
# ============================================================

fig = px.box(
    df,
    x="TARGET",
    y="ANNUITY_INCOME_RATIO",
    title="Annuity/Income Ratio vs TARGET"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 📌 KEY ANNUITY BURDEN INSIGHTS
# ============================================================

st.markdown("---")
st.subheader("📌 Key Annuity Burden Insights")


# ============================================================
# BASIC METRICS
# ============================================================

total_customers = len(df)

overall_default_rate = (
    df["TARGET"].mean() * 100
)


# ============================================================
# BURDEN GROUP RISK
# ============================================================

burden_risk = (
    df.groupby(
        "ANNUITY_BURDEN_GROUP",
        observed=True
    )["TARGET"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

highest_risk_burden = burden_risk.index[0]
highest_burden_default = burden_risk.iloc[0]

lowest_risk_burden = burden_risk.index[-1]
lowest_burden_default = burden_risk.iloc[-1]


# ============================================================
# GENDER BURDEN
# ============================================================

gender_burden = (
    df.groupby("CODE_GENDER")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
    .sort_values(ascending=False)
)

highest_gender_burden = gender_burden.index[0]
highest_gender_ratio = gender_burden.iloc[0]


# ============================================================
# INCOME TYPE BURDEN
# ============================================================

income_burden = (
    df.groupby("NAME_INCOME_TYPE")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
    .sort_values(ascending=False)
)

highest_income_burden_type = income_burden.index[0]
highest_income_burden_ratio = income_burden.iloc[0]


# ============================================================
# EDUCATION BURDEN
# ============================================================

education_burden = (
    df.groupby("NAME_EDUCATION_TYPE")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
    .sort_values(ascending=False)
)

highest_education_burden = education_burden.index[0]
highest_education_ratio = education_burden.iloc[0]


# ============================================================
# DEFAULT VS NON-DEFAULT
# ============================================================

target_burden = (
    df.groupby("TARGET")[
        "ANNUITY_INCOME_RATIO"
    ]
    .mean()
)

default_ratio = target_burden.get(1, 0)
non_default_ratio = target_burden.get(0, 0)

ratio_difference = (
    default_ratio - non_default_ratio
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Burden Ratio",
    f"{avg_ratio:.3f}"
)

c2.metric(
    "Highest Burden Ratio",
    f"{max_ratio:.3f}"
)

c3.metric(
    "Highest-Risk Burden Group",
    str(highest_risk_burden)
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
        f"🚨 **Highest-Risk Burden Group**\n\n"
        f"**{highest_risk_burden}** has the highest "
        f"observed default rate of "
        f"**{highest_burden_default:.2f}%**."
    )

    st.info(
        f"👤 **Gender with Highest Average Burden**\n\n"
        f"**{highest_gender_burden}** has the highest "
        f"average annuity-to-income ratio of "
        f"**{highest_gender_ratio:.3f}**."
    )

    st.warning(
        f"💼 **Highest-Burden Income Type**\n\n"
        f"**{highest_income_burden_type}** has the highest "
        f"average annuity-to-income ratio of "
        f"**{highest_income_burden_ratio:.3f}**."
    )


with col2:

    st.warning(
        f"🎓 **Highest-Burden Education Group**\n\n"
        f"**{highest_education_burden}** has the highest "
        f"average annuity-to-income ratio of "
        f"**{highest_education_ratio:.3f}**."
    )

    if default_ratio > non_default_ratio:

        st.error(
            f"⚠️ **Default Customers Show Higher Burden**\n\n"
            f"Defaulted customers have an average "
            f"annuity-to-income ratio of "
            f"**{default_ratio:.3f}**, compared with "
            f"**{non_default_ratio:.3f}** for non-defaulted "
            f"customers."
        )

    else:

        st.success(
            f"🟢 **Default Customers Do Not Show Higher Burden**\n\n"
            f"Defaulted customers have an average ratio "
            f"of **{default_ratio:.3f}**, compared with "
            f"**{non_default_ratio:.3f}** for non-defaulted "
            f"customers."
        )

    st.info(
        f"📊 **Burden Difference**\n\n"
        f"The difference between defaulted and non-defaulted "
        f"customers is **{ratio_difference:.3f}**."
    )


# ============================================================
# BURDEN GROUP SUMMARY
# ============================================================

st.markdown("---")
st.subheader("📊 Annuity Burden Group Summary")

burden_summary = (
    df.groupby(
        "ANNUITY_BURDEN_GROUP",
        observed=True
    )
    .agg(
        Customers=("SK_ID_CURR", "count"),
        Default_Rate=("TARGET", "mean"),
        Avg_Annuity_Ratio=(
            "ANNUITY_INCOME_RATIO",
            "mean"
        ),
        Avg_Income=(
            "AMT_INCOME_TOTAL",
            "mean"
        ),
        Avg_Credit=(
            "AMT_CREDIT",
            "mean"
        )
    )
    .reset_index()
)

burden_summary["Default_Rate"] *= 100

burden_summary.columns = [
    "Burden Group",
    "Customers",
    "Default Rate",
    "Average Annuity/Income Ratio",
    "Average Income",
    "Average Credit"
]

st.dataframe(
    burden_summary,
    use_container_width=True
)


# ============================================================
# BUSINESS SUMMARY
# ============================================================

st.markdown("---")
st.subheader("📝 Annuity Burden Summary")

st.write(
    f"• The filtered dataset contains "
    f"**{total_customers:,} customers** with an overall "
    f"default rate of **{overall_default_rate:.2f}%**."
)

st.write(
    f"• The average annuity-to-income ratio is "
    f"**{avg_ratio:.3f}**, while the maximum observed "
    f"ratio is **{max_ratio:.3f}**."
)

st.write(
    f"• **{highest_risk_burden}** has the highest observed "
    f"default rate among annuity burden groups at "
    f"**{highest_burden_default:.2f}%**."
)

st.write(
    f"• **{highest_income_burden_type}** has the highest "
    f"average annuity-to-income ratio among income types."
)

st.write(
    f"• **{highest_education_burden}** has the highest "
    f"average annuity-to-income ratio among education groups."
)


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

st.markdown("### 💡 Business Recommendation")

if default_ratio > non_default_ratio:

    st.warning(
        "🔴 Defaulted customers show a higher average "
        "annuity-to-income ratio than non-defaulted "
        "customers. Annuity burden can therefore be "
        "considered as one of the risk-screening indicators."
    )

else:

    st.info(
        "📊 The filtered data does not show a higher "
        "average annuity burden among defaulted customers. "
        "Annuity burden should therefore be evaluated "
        "alongside other risk factors."
    )


st.caption(
    "Note: Annuity-to-income ratio represents repayment "
    "burden relative to income. Observed relationships "
    "with TARGET are associations and should not be "
    "interpreted as causal relationships."
)