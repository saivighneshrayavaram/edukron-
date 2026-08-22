import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


st.title("👨‍👩‍👧 Family & Children Analysis")


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()
df = clean_data(df)
df = create_features(df)
df = apply_sidebar_filters(df)


# ============================================================
# BASIC METRICS
# ============================================================

avg_children = df["CNT_CHILDREN"].mean()
avg_family = df["CNT_FAM_MEMBERS"].mean()

with_children = (
    df["CNT_CHILDREN"] > 0
).sum()

without_children = (
    df["CNT_CHILDREN"] == 0
).sum()

family_risk = (
    df.groupby("NAME_FAMILY_STATUS")["TARGET"]
    .mean()
    .sort_values(ascending=False)
)

highest_risk = family_risk.index[0]


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Average Children",
    f"{avg_children:.2f}"
)

c2.metric(
    "Average Family Members",
    f"{avg_family:.2f}"
)

c3.metric(
    "Customers with Children",
    f"{with_children:,}"
)

c4.metric(
    "Without Children",
    f"{without_children:,}"
)

c5.metric(
    "Highest Risk Family Type",
    highest_risk
)


# ============================================================
# 1. CUSTOMERS BY NUMBER OF CHILDREN
# ============================================================

data = (
    df["CNT_CHILDREN"]
    .value_counts()
    .sort_index()
    .reset_index()
)

data.columns = [
    "Children",
    "Customers"
]

fig = px.bar(
    data,
    x="Children",
    y="Customers",
    text="Customers",
    title="Customers by Number of Children"
)

fig.update_traces(
    texttemplate="%{text:,}",
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
# 2. DEFAULT RATE BY NUMBER OF CHILDREN
# ============================================================

data = (
    df.groupby("CNT_CHILDREN")["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

data.columns = [
    "Children",
    "Default Rate"
]

fig = px.line(
    data,
    x="Children",
    y="Default Rate",
    markers=True,
    text="Default Rate",
    title="Default Rate by Number of Children"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="top center"
)

fig.update_layout(
    yaxis_title="Default Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 3. CUSTOMERS BY FAMILY SIZE
# ============================================================

data = (
    df["CNT_FAM_MEMBERS"]
    .value_counts()
    .sort_index()
    .reset_index()
)

data.columns = [
    "Family Size",
    "Customers"
]

fig = px.bar(
    data,
    x="Family Size",
    y="Customers",
    text="Customers",
    title="Customers by Family Size"
)

fig.update_traces(
    texttemplate="%{text:,}",
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
# 4. DEFAULT RATE BY FAMILY SIZE
# ============================================================

data = (
    df.groupby("CNT_FAM_MEMBERS")["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

data.columns = [
    "Family Size",
    "Default Rate"
]

fig = px.line(
    data,
    x="Family Size",
    y="Default Rate",
    markers=True,
    text="Default Rate",
    title="Default Rate by Family Size"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="top center"
)

fig.update_layout(
    yaxis_title="Default Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 5. APPLICATIONS BY FAMILY STATUS
# ============================================================

data = (
    df["NAME_FAMILY_STATUS"]
    .value_counts()
    .reset_index()
)

data.columns = [
    "Family Status",
    "Applications"
]

fig = px.bar(
    data,
    x="Family Status",
    y="Applications",
    text="Applications",
    title="Applications by Family Status"
)

fig.update_traces(
    texttemplate="%{text:,}",
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
# 6. DEFAULT RATE BY FAMILY STATUS
# ============================================================

data = (
    df.groupby("NAME_FAMILY_STATUS")["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

data.columns = [
    "Family Status",
    "Default Rate"
]

fig = px.bar(
    data,
    x="Family Status",
    y="Default Rate",
    text="Default Rate",
    title="Default Rate by Family Status"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="inside"
)

fig.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode="hide",
    yaxis_title="Default Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 7. INCOME VS FAMILY SIZE
# ============================================================

sample = df.sample(
    min(10000, len(df))
)

fig = px.scatter(
    sample,
    x="CNT_FAM_MEMBERS",
    y="AMT_INCOME_TOTAL",
    color="TARGET",
    title="Income vs Family Size"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 📌 KEY FAMILY & CHILDREN INSIGHTS
# ============================================================

st.markdown("---")

st.subheader(
    "📌 Key Family & Children Insights"
)


if len(df) == 0:

    st.warning(
        "No customers match the selected filters."
    )

else:

    # ========================================================
    # BASIC METRICS
    # ========================================================

    total_customers = len(df)

    overall_default_rate = (
        df["TARGET"].mean() * 100
    )

    children_percentage = (
        with_children / total_customers * 100
        if total_customers
        else 0
    )

    no_children_percentage = (
        without_children / total_customers * 100
        if total_customers
        else 0
    )


    # ========================================================
    # FAMILY STATUS RISK
    # ========================================================

    family_risk = (
        df.groupby("NAME_FAMILY_STATUS")["TARGET"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    highest_risk_family = (
        family_risk.index[0]
    )

    highest_family_default = (
        family_risk.iloc[0]
    )

    lowest_risk_family = (
        family_risk.index[-1]
    )

    lowest_family_default = (
        family_risk.iloc[-1]
    )


    # ========================================================
    # CHILDREN RISK
    # ========================================================

    children_risk = (
        df.groupby("CNT_CHILDREN")["TARGET"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    highest_risk_children = (
        children_risk.index[0]
    )

    highest_children_default = (
        children_risk.iloc[0]
    )


    # ========================================================
    # FAMILY SIZE RISK
    # ========================================================

    family_size_risk = (
        df.groupby("CNT_FAM_MEMBERS")["TARGET"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    highest_risk_family_size = (
        family_size_risk.index[0]
    )

    highest_family_size_default = (
        family_size_risk.iloc[0]
    )


    # ========================================================
    # MOST COMMON FAMILY STATUS
    # ========================================================

    family_status_count = (
        df["NAME_FAMILY_STATUS"]
        .value_counts()
    )

    most_common_family_status = (
        family_status_count.index[0]
    )

    most_common_family_count = (
        family_status_count.iloc[0]
    )


    # ========================================================
    # INCOME BY FAMILY STATUS
    # ========================================================

    income_by_family = (
        df.groupby("NAME_FAMILY_STATUS")[
            "AMT_INCOME_TOTAL"
        ]
        .mean()
        .sort_values(ascending=False)
    )

    highest_income_family = (
        income_by_family.index[0]
    )

    highest_family_income = (
        income_by_family.iloc[0]
    )


    # ========================================================
    # CREDIT BY FAMILY STATUS
    # ========================================================

    credit_by_family = (
        df.groupby("NAME_FAMILY_STATUS")[
            "AMT_CREDIT"
        ]
        .mean()
        .sort_values(ascending=False)
    )

    highest_credit_family = (
        credit_by_family.index[0]
    )

    highest_family_credit = (
        credit_by_family.iloc[0]
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Overall Default Rate",
        f"{overall_default_rate:.2f}%"
    )

    c2.metric(
        "Customers with Children",
        f"{children_percentage:.2f}%"
    )

    c3.metric(
        "Highest-Risk Family Status",
        str(highest_risk_family)
    )

    c4.metric(
        "Highest Family Default Rate",
        f"{highest_family_default:.2f}%"
    )


    # ========================================================
    # INSIGHT CARDS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"👪 **Most Common Family Status**\n\n"
            f"**{most_common_family_status}** is the most "
            f"common family status with "
            f"**{most_common_family_count:,} customers**."
        )

        st.error(
            f"🚨 **Highest-Risk Family Status**\n\n"
            f"**{highest_risk_family}** has the highest "
            f"observed default rate of "
            f"**{highest_family_default:.2f}%**."
        )

        st.success(
            f"🟢 **Lowest-Risk Family Status**\n\n"
            f"**{lowest_risk_family}** has the lowest "
            f"observed default rate of "
            f"**{lowest_family_default:.2f}%**."
        )

    with col2:

        st.warning(
            f"👶 **Highest-Risk Children Group**\n\n"
            f"Customers with **{highest_risk_children} children** "
            f"have the highest observed default rate of "
            f"**{highest_children_default:.2f}%**."
        )

        st.warning(
            f"👨‍👩‍👧‍👦 **Highest-Risk Family Size**\n\n"
            f"Customers with **{highest_risk_family_size} family "
            f"members** have a default rate of "
            f"**{highest_family_size_default:.2f}%**."
        )

        st.info(
            f"💰 **Highest-Income Family Group**\n\n"
            f"**{highest_income_family}** has the highest "
            f"average income of "
            f"**{highest_family_income:,.0f}**."
        )


    # ========================================================
    # CHILDREN RISK SUMMARY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "👶 Children & Default Risk"
    )

    children_summary = (
        df.groupby("CNT_CHILDREN")
        .agg(
            Customers=("SK_ID_CURR", "count"),
            Default_Rate=("TARGET", "mean"),
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

    children_summary["Default_Rate"] *= 100

    children_summary.columns = [
        "Children",
        "Customers",
        "Default Rate",
        "Average Income",
        "Average Credit"
    ]

    st.dataframe(
        children_summary,
        use_container_width=True
    )


    # ========================================================
    # FAMILY SIZE RISK SUMMARY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "👨‍👩‍👧‍👦 Family Size Risk"
    )

    family_size_summary = (
        df.groupby("CNT_FAM_MEMBERS")
        .agg(
            Customers=("SK_ID_CURR", "count"),
            Default_Rate=("TARGET", "mean"),
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

    family_size_summary["Default_Rate"] *= 100

    family_size_summary.columns = [
        "Family Size",
        "Customers",
        "Default Rate",
        "Average Income",
        "Average Credit"
    ]

    st.dataframe(
        family_size_summary,
        use_container_width=True
    )


    # ========================================================
    # FAMILY STATUS RISK SUMMARY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "👪 Family Status Risk Summary"
    )

    family_summary = (
        df.groupby("NAME_FAMILY_STATUS")
        .agg(
            Customers=("SK_ID_CURR", "count"),
            Default_Rate=("TARGET", "mean"),
            Avg_Income=(
                "AMT_INCOME_TOTAL",
                "mean"
            ),
            Avg_Credit=(
                "AMT_CREDIT",
                "mean"
            ),
            Avg_Annuity=(
                "AMT_ANNUITY",
                "mean"
            )
        )
        .reset_index()
    )

    family_summary["Default_Rate"] *= 100

    family_summary = family_summary.sort_values(
        "Default_Rate",
        ascending=False
    )

    family_summary.columns = [
        "Family Status",
        "Customers",
        "Default Rate",
        "Average Income",
        "Average Credit",
        "Average Annuity"
    ]

    st.dataframe(
        family_summary,
        use_container_width=True
    )


    # ========================================================
    # BUSINESS SUMMARY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📝 Family Analysis Summary"
    )

    st.write(
        f"• The filtered dataset contains "
        f"**{total_customers:,} customers**, with an overall "
        f"default rate of **{overall_default_rate:.2f}%**."
    )

    st.write(
        f"• **{children_percentage:.2f}%** of customers have "
        f"at least one child, while "
        f"**{no_children_percentage:.2f}%** have no children."
    )

    st.write(
        f"• **{most_common_family_status}** is the most common "
        f"family status."
    )

    st.write(
        f"• **{highest_risk_family}** has the highest observed "
        f"family-status default rate of "
        f"**{highest_family_default:.2f}%**."
    )

    st.write(
        f"• The group with **{highest_risk_children} children** "
        f"has the highest observed children-related default rate "
        f"of **{highest_children_default:.2f}%**."
    )

    st.write(
        f"• The **{highest_risk_family_size}-member** family group "
        f"has the highest observed default rate of "
        f"**{highest_family_size_default:.2f}%**."
    )

    st.write(
        f"• **{highest_income_family}** has the highest average "
        f"income among family-status groups."
    )

    st.write(
        f"• **{highest_credit_family}** has the highest average "
        f"credit amount of **{highest_family_credit:,.0f}**."
    )


    # ========================================================
    # BUSINESS RECOMMENDATION
    # ========================================================

    st.markdown(
        "### 💡 Business Recommendation"
    )

    if highest_family_default > overall_default_rate:

        st.warning(
            f"🔴 **{highest_risk_family}** has a default rate "
            f"above the overall portfolio average. This family "
            f"segment may require additional risk assessment."
        )

    else:

        st.success(
            "🟢 Family-status default rates are generally "
            "within the overall portfolio range."
        )


    if highest_children_default > overall_default_rate:

        st.info(
            f"👶 The group with **{highest_risk_children} children** "
            f"shows an above-average default rate. Number of "
            f"children can be considered as an additional "
            f"segmentation variable."
        )


    if highest_family_size_default > overall_default_rate:

        st.info(
            f"👨‍👩‍👧‍👦 The **{highest_risk_family_size}-member** "
            f"family group shows an above-average default rate "
            f"and may warrant additional financial assessment."
        )


    st.caption(
        "Note: Family structure and default rates represent "
        "observed associations in the dataset and should not "
        "be interpreted as causal relationships."
    )