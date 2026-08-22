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
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📊 Executive Overview")

st.markdown("""
### Home Credit Default Risk

This page provides a high-level view of the loan portfolio,
customer characteristics, financial behavior, and default risk.
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

    st.warning(
        "⚠️ No customers match the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_customers = len(df)

total_defaults = (
    df["TARGET"] == 1
).sum()

default_rate = (
    df["TARGET"].mean() * 100
)

avg_income = (
    df["AMT_INCOME_TOTAL"].mean()
)

avg_credit = (
    df["AMT_CREDIT"].mean()
)

avg_annuity = (
    df["AMT_ANNUITY"].mean()
)

avg_external_score = (
    df["AVERAGE_EXTERNAL_SCORE"].mean()
    if "AVERAGE_EXTERNAL_SCORE" in df.columns
    else 0
)


# ============================================================
# KPI ROW
# ============================================================

st.subheader("📌 Portfolio KPIs")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Customers",
    f"{total_customers:,}"
)

c2.metric(
    "Defaults",
    f"{total_defaults:,}"
)

c3.metric(
    "Default Rate",
    f"{default_rate:.2f}%"
)

c4.metric(
    "Avg Income",
    f"{avg_income:,.0f}"
)

c5.metric(
    "Avg Credit",
    f"{avg_credit:,.0f}"
)

c6.metric(
    "Avg Annuity",
    f"{avg_annuity:,.0f}"
)


st.markdown("---")


# ============================================================
# DEFAULT DISTRIBUTION
# ============================================================

st.subheader("⚠️ Default Risk Overview")

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Default Distribution
# ------------------------------------------------------------

with col1:

    default_data = (
        df["TARGET"]
        .value_counts()
        .reset_index()
    )

    default_data.columns = [
        "TARGET",
        "Customers"
    ]

    default_data["Status"] = (
        default_data["TARGET"]
        .map({
            0: "No Payment Difficulty",
            1: "Payment Difficulty"
        })
    )

    fig = px.pie(
        default_data,
        names="Status",
        values="Customers",
        hole=0.45,
        title="Customer Default Distribution"
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


# ------------------------------------------------------------
# Default Rate by Gender
# ------------------------------------------------------------

with col2:

    if "CODE_GENDER" in df.columns:

        gender_data = (
            df.groupby("CODE_GENDER")["TARGET"]
            .mean()
            .mul(100)
            .reset_index()
        )

        gender_data.columns = [
            "Gender",
            "Default Rate"
        ]

        fig = px.bar(
            gender_data,
            x="Gender",
            y="Default Rate",
            title="Default Rate by Gender",
            text="Default Rate"
        )

        # VALUES INSIDE BAR
        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="inside",
            insidetextanchor="middle"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# FINANCIAL OVERVIEW
# ============================================================

st.subheader("💰 Financial Overview")

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Income vs Credit
# ------------------------------------------------------------

with col1:

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
        }
    )

    # SHOW CREDIT VALUE ON EACH POINT
    fig.update_traces(
        texttemplate="%{y:,.0f}",
        textposition="top center"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Credit-to-Income Risk
# ------------------------------------------------------------

with col2:

    if "CREDIT_INCOME_RATIO" in df.columns:

        risk_data = df.copy()

        risk_data["Credit Risk Group"] = pd.cut(
            risk_data["CREDIT_INCOME_RATIO"],
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

        ratio_data = (
            risk_data
            .groupby(
                "Credit Risk Group",
                observed=True
            )["TARGET"]
            .mean()
            .mul(100)
            .reset_index()
        )

        ratio_data.columns = [
            "Risk Group",
            "Default Rate"
        ]

        fig = px.bar(
            ratio_data,
            x="Risk Group",
            y="Default Rate",
            title="Default Rate by Credit-to-Income Risk",
            text="Default Rate"
        )

        # VALUES INSIDE BAR
        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="inside",
            insidetextanchor="middle"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# CUSTOMER PROFILE
# ============================================================

st.subheader("👥 Customer Profile")

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Age Groups
# ------------------------------------------------------------

with col1:

    if "AGE_GROUP" in df.columns:

        age_data = (
            df.groupby(
                "AGE_GROUP",
                observed=True
            )["TARGET"]
            .mean()
            .mul(100)
            .reset_index()
        )

        age_data.columns = [
            "Age Group",
            "Default Rate"
        ]

        fig = px.bar(
            age_data,
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

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ------------------------------------------------------------
# Income Type
# ------------------------------------------------------------

with col2:

    if "NAME_INCOME_TYPE" in df.columns:

        income_data = (
            df.groupby(
                "NAME_INCOME_TYPE"
            )["TARGET"]
            .mean()
            .mul(100)
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        income_data.columns = [
            "Income Type",
            "Default Rate"
        ]

        fig = px.bar(
            income_data,
            x="Income Type",
            y="Default Rate",
            title="Top Income Types by Default Rate",
            text="Default Rate"
        )

        # VALUES INSIDE BAR
        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="inside",
            insidetextanchor="middle"
        )

        fig.update_layout(
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# EXTERNAL CREDIT SCORE
# ============================================================

st.subheader("📊 External Credit Score")

if "AVERAGE_EXTERNAL_SCORE" in df.columns:

    score_data = (
        df.groupby("TARGET")[
            "AVERAGE_EXTERNAL_SCORE"
        ]
        .mean()
        .reset_index()
    )

    score_data["Status"] = (
        score_data["TARGET"]
        .map({
            0: "No Payment Difficulty",
            1: "Payment Difficulty"
        })
    )

    fig = px.bar(
        score_data,
        x="Status",
        y="AVERAGE_EXTERNAL_SCORE",
        title="Average External Score by Customer Status",
        text="AVERAGE_EXTERNAL_SCORE"
    )

    # VALUES INSIDE BAR
    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="inside",
        insidetextanchor="middle"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# KEY INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("💡 Key Business Insights")


# ------------------------------------------------------------
# Calculate dynamic insights
# ------------------------------------------------------------

insights = []


# Default insight

if default_rate > 10:

    insights.append(
        f"🔴 The current portfolio has a relatively high "
        f"default rate of **{default_rate:.2f}%**."
    )

else:

    insights.append(
        f"🟢 The current portfolio default rate is "
        f"**{default_rate:.2f}%**."
    )


# Credit-income insight

if "CREDIT_INCOME_RATIO" in df.columns:

    high_ratio = df[
        df["CREDIT_INCOME_RATIO"] > 6
    ]

    if len(high_ratio) > 0:

        high_ratio_default = (
            high_ratio["TARGET"].mean() * 100
        )

        insights.append(
            f"⚠️ Customers with a credit-to-income "
            f"ratio above 6 have a default rate of "
            f"**{high_ratio_default:.2f}%**."
        )


# External score insight

if "AVERAGE_EXTERNAL_SCORE" in df.columns:

    default_score = df.loc[
        df["TARGET"] == 1,
        "AVERAGE_EXTERNAL_SCORE"
    ].mean()

    non_default_score = df.loc[
        df["TARGET"] == 0,
        "AVERAGE_EXTERNAL_SCORE"
    ].mean()

    if (
        pd.notna(default_score)
        and pd.notna(non_default_score)
    ):

        if default_score < non_default_score:

            insights.append(
                f"📉 Customers with payment difficulties "
                f"have a lower average external credit "
                f"score (**{default_score:.3f}**) compared "
                f"with other customers (**{non_default_score:.3f}**)."
            )


# Age insight

if "AGE_GROUP" in df.columns:

    age_risk = (
        df.groupby(
            "AGE_GROUP",
            observed=True
        )["TARGET"]
        .mean()
    )

    if len(age_risk) > 0:

        highest_age = age_risk.idxmax()

        highest_age_rate = (
            age_risk.max() * 100
        )

        insights.append(
            f"👤 The **{highest_age}** age group "
            f"has the highest observed default rate "
            f"at **{highest_age_rate:.2f}%**."
        )


# Housing insight

if "NAME_HOUSING_TYPE" in df.columns:

    housing_risk = (
        df.groupby(
            "NAME_HOUSING_TYPE"
        )["TARGET"]
        .mean()
    )

    if len(housing_risk) > 0:

        highest_housing = (
            housing_risk.idxmax()
        )

        highest_housing_rate = (
            housing_risk.max() * 100
        )

        insights.append(
            f"🏠 **{highest_housing}** has the highest "
            f"observed default rate among housing categories "
            f"at **{highest_housing_rate:.2f}%**."
        )


# Display insights

for insight in insights:

    st.write(insight)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📝 Executive Summary")

st.info(f"""
The current filtered portfolio contains **{total_customers:,} customers**,
with **{total_defaults:,} customers** experiencing payment difficulties.

The overall default rate is **{default_rate:.2f}%**.

The analysis indicates that financial burden, credit-to-income
relationships, external credit scores, customer demographics,
and other applicant characteristics can be useful indicators
when assessing default risk.

Use the detailed analysis pages in the sidebar to investigate
specific risk factors and customer segments.
""")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Home Credit Default Risk Dashboard • Executive Overview"
)