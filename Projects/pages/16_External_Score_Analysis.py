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

st.title("📊 External Credit Score Analysis")


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()
df = clean_data(df)
df = create_features(df)
df = apply_sidebar_filters(df)


# ============================================================
# TOP KPI CARDS
# ============================================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Average EXT_SOURCE_1",
    f"{df['EXT_SOURCE_1'].mean():.3f}"
)

c2.metric(
    "Average EXT_SOURCE_2",
    f"{df['EXT_SOURCE_2'].mean():.3f}"
)

c3.metric(
    "Average EXT_SOURCE_3",
    f"{df['EXT_SOURCE_3'].mean():.3f}"
)


# ============================================================
# MISSING EXTERNAL SCORES
# ============================================================

missing_scores = df[
    [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]
].isna().any(axis=1).sum()


st.metric(
    "Records with Missing External Scores",
    f"{missing_scores:,}"
)


# ============================================================
# EXTERNAL SCORE DISTRIBUTIONS
# ============================================================

for column in [
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3"
]:

    fig = px.histogram(
        df,
        x=column,
        nbins=40,
        title=f"{column} Distribution"
    )

    # --------------------------------------------------------
    # SHOW COUNT INSIDE EACH HISTOGRAM BAR
    # --------------------------------------------------------

    fig.update_traces(
        texttemplate="%{y:,}",
        textposition="inside"
    )

    fig.update_layout(
        xaxis_title=column,
        yaxis_title="Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SCORES BY TARGET
# ============================================================

score_data = (
    df.groupby("TARGET")[
        [
            "EXT_SOURCE_1",
            "EXT_SOURCE_2",
            "EXT_SOURCE_3"
        ]
    ]
    .mean()
    .reset_index()
)


score_long = score_data.melt(
    id_vars="TARGET",
    var_name="Score",
    value_name="Average"
)


# ============================================================
# EXTERNAL SCORES BY TARGET
# ============================================================

fig = px.bar(
    score_long,
    x="Score",
    y="Average",
    color="TARGET",
    barmode="group",
    title="External Scores by TARGET"
)

# ------------------------------------------------------------
# SHOW AVERAGE SCORE INSIDE BARS
# ------------------------------------------------------------

fig.update_traces(
    texttemplate="%{y:.3f}",
    textposition="inside"
)

fig.update_layout(
    xaxis_title="External Score",
    yaxis_title="Average Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# EXT_SOURCE_1 VS EXT_SOURCE_2
# ============================================================

scatter_sample = df.sample(
    min(10000, len(df)),
    random_state=42
)


fig = px.scatter(
    scatter_sample,
    x="EXT_SOURCE_1",
    y="EXT_SOURCE_2",
    color="TARGET",
    title="EXT_SOURCE_1 vs EXT_SOURCE_2",
    hover_data=[
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "TARGET"
    ]
)

fig.update_layout(
    xaxis_title="EXT_SOURCE_1",
    yaxis_title="EXT_SOURCE_2"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# EXT_SOURCE_2 VS EXT_SOURCE_3
# ============================================================

scatter_sample = df.sample(
    min(10000, len(df)),
    random_state=42
)


fig = px.scatter(
    scatter_sample,
    x="EXT_SOURCE_2",
    y="EXT_SOURCE_3",
    color="TARGET",
    title="EXT_SOURCE_2 vs EXT_SOURCE_3",
    hover_data=[
        "EXT_SOURCE_2",
        "EXT_SOURCE_3",
        "TARGET"
    ]
)

fig.update_layout(
    xaxis_title="EXT_SOURCE_2",
    yaxis_title="EXT_SOURCE_3"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# AVERAGE SCORE GROUP
# ============================================================

df["EXTERNAL_SCORE_GROUP"] = pd.cut(
    df["AVERAGE_EXTERNAL_SCORE"],
    bins=[
        0,
        0.3,
        0.5,
        0.7,
        1
    ],
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
)


data = (
    df.groupby(
        "EXTERNAL_SCORE_GROUP",
        observed=True
    )["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)


data.columns = [
    "External Score Group",
    "Default Rate"
]


# ============================================================
# EXTERNAL SCORE VS DEFAULT RATE
# ============================================================

fig = px.bar(
    data,
    x="External Score Group",
    y="Default Rate",
    title="External Score vs Default Rate"
)

# ------------------------------------------------------------
# SHOW DEFAULT RATE INSIDE BARS
# ------------------------------------------------------------

fig.update_traces(
    texttemplate="%{y:.2f}%",
    textposition="inside"
)

fig.update_layout(
    xaxis_title="External Score Group",
    yaxis_title="Default Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 📌 KEY EXTERNAL SCORE INSIGHTS
# ============================================================

st.markdown("---")

st.subheader(
    "📌 Key External Credit Score Insights"
)


# ============================================================
# CHECK EMPTY DATA
# ============================================================

if len(df) == 0:

    st.warning(
        "No customers match the selected filters."
    )

else:

    # ========================================================
    # BASIC STATISTICS
    # ========================================================

    total_customers = len(df)

    default_count = int(
        (df["TARGET"] == 1).sum()
    )

    default_rate = (
        df["TARGET"].mean() * 100
    )


    score_columns = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]


    # ========================================================
    # AVERAGE SCORES
    # ========================================================

    average_scores = (
        df[score_columns]
        .mean()
        .sort_values()
    )


    lowest_score_name = (
        average_scores.index[0]
    )

    lowest_score_value = (
        average_scores.iloc[0]
    )


    highest_score_name = (
        average_scores.index[-1]
    )

    highest_score_value = (
        average_scores.iloc[-1]
    )


    # ========================================================
    # SCORE VS TARGET
    # ========================================================

    target_correlations = (
        df[
            score_columns + ["TARGET"]
        ]
        .corr()["TARGET"]
        .drop("TARGET")
        .sort_values()
    )


    strongest_negative_score = (
        target_correlations.index[0]
    )

    strongest_negative_corr = (
        target_correlations.iloc[0]
    )


    strongest_positive_score = (
        target_correlations.index[-1]
    )

    strongest_positive_corr = (
        target_correlations.iloc[-1]
    )


    # ========================================================
    # DEFAULT VS NON-DEFAULT SCORES
    # ========================================================

    score_comparison = (
        df.groupby("TARGET")[score_columns]
        .mean()
    )


    # ========================================================
    # MISSING SCORE PERCENTAGE
    # ========================================================

    missing_percentage = (
        missing_scores / total_customers * 100
        if total_customers
        else 0
    )


    # ========================================================
    # SCORE GROUP ANALYSIS
    # ========================================================

    group_data = (
        df.groupby(
            "EXTERNAL_SCORE_GROUP",
            observed=True
        )["TARGET"]
        .agg(
            Default_Rate="mean",
            Customers="count"
        )
        .reset_index()
    )


    group_data["Default_Rate"] = (
        group_data["Default_Rate"] * 100
    )


    if len(group_data) > 0:

        highest_risk_group = (
            group_data
            .sort_values(
                "Default_Rate",
                ascending=False
            )
            .iloc[0]
        )


        lowest_risk_group = (
            group_data
            .sort_values(
                "Default_Rate"
            )
            .iloc[0]
        )


    # ========================================================
    # KPI CARDS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Average External Score",
        f"{df['AVERAGE_EXTERNAL_SCORE'].mean():.3f}"
    )


    c2.metric(
        "Lowest Average Score",
        f"{lowest_score_value:.3f}"
    )


    c3.metric(
        "Missing Score %",
        f"{missing_percentage:.2f}%"
    )


    c4.metric(
        "Overall Default Rate",
        f"{default_rate:.2f}%"
    )


    # ========================================================
    # INSIGHT CARDS
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.warning(
            f"📉 **Lowest External Score**\n\n"
            f"**{lowest_score_name}** has the lowest "
            f"average score at **{lowest_score_value:.3f}**."
        )


        st.error(
            f"🚨 **Strongest Risk Indicator**\n\n"
            f"**{strongest_negative_score}** has the strongest "
            f"negative correlation with TARGET "
            f"(**{strongest_negative_corr:.3f}**). "
            f"Lower scores are associated with higher default risk."
        )


        st.info(
            f"📊 **Highest Average Score**\n\n"
            f"**{highest_score_name}** has the highest "
            f"average external score at "
            f"**{highest_score_value:.3f}**."
        )


    with col2:

        st.warning(
            f"⚠️ **Missing External Scores**\n\n"
            f"**{missing_scores:,}** customers "
            f"(**{missing_percentage:.2f}%**) have at least "
            f"one missing external credit score."
        )


        if len(group_data) > 0:

            st.error(
                f"🔴 **Highest-Risk Score Group**\n\n"
                f"Customers in the **{highest_risk_group['EXTERNAL_SCORE_GROUP']}** "
                f"score group have the highest default rate "
                f"of **{highest_risk_group['Default_Rate']:.2f}%**."
            )


            st.success(
                f"🟢 **Lowest-Risk Score Group**\n\n"
                f"Customers in the **{lowest_risk_group['EXTERNAL_SCORE_GROUP']}** "
                f"score group have the lowest default rate "
                f"of **{lowest_risk_group['Default_Rate']:.2f}%**."
            )


    # ========================================================
    # DEFAULT VS NON-DEFAULT COMPARISON
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🔍 Default vs Non-Default Score Comparison"
    )


    comparison_data = (
        score_comparison
        .T
        .reset_index()
    )


    comparison_data.columns = [
        "External Score",
        "Non-Default",
        "Default"
    ]


    st.dataframe(
        comparison_data,
        use_container_width=True
    )


    # ========================================================
    # SCORE DIFFERENCE INSIGHTS
    # ========================================================

    st.markdown(
        "### 📊 Score Difference"
    )


    difference_rows = []


    for score in score_columns:

        if (
            0 in score_comparison.index
            and 1 in score_comparison.index
        ):

            non_default_score = (
                score_comparison.loc[
                    0,
                    score
                ]
            )


            default_score = (
                score_comparison.loc[
                    1,
                    score
                ]
            )


            difference = (
                non_default_score
                - default_score
            )


            difference_rows.append({
                "Score": score,
                "Non-Default Average": non_default_score,
                "Default Average": default_score,
                "Difference": difference
            })


    difference_df = pd.DataFrame(
        difference_rows
    )


    if len(difference_df) > 0:

        difference_df = (
            difference_df
            .sort_values(
                "Difference",
                ascending=False
            )
        )


        st.dataframe(
            difference_df,
            use_container_width=True
        )


        largest_gap = (
            difference_df.iloc[0]
        )


        st.info(
            f"💡 **Largest Score Gap:** "
            f"{largest_gap['Score']} shows the largest "
            f"difference between non-default and default "
            f"customers (**{largest_gap['Difference']:.3f}**)."
        )


    # ========================================================
    # BUSINESS SUMMARY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📝 External Credit Score Summary"
    )


    st.write(
        f"• The filtered dataset contains "
        f"**{total_customers:,} customers**, with an overall "
        f"default rate of **{default_rate:.2f}%**."
    )


    st.write(
        f"• **{missing_scores:,} customers** have at least "
        f"one missing external credit score, representing "
        f"**{missing_percentage:.2f}%** of the filtered population."
    )


    st.write(
        f"• **{strongest_negative_score}** has the strongest "
        f"negative relationship with TARGET, with a correlation "
        f"of **{strongest_negative_corr:.3f}**."
    )


    if len(group_data) > 0:

        st.write(
            f"• The **{highest_risk_group['EXTERNAL_SCORE_GROUP']}** "
            f"score group has the highest default rate "
            f"(**{highest_risk_group['Default_Rate']:.2f}%**)."
        )


        st.write(
            f"• The **{lowest_risk_group['EXTERNAL_SCORE_GROUP']}** "
            f"score group has the lowest default rate "
            f"(**{lowest_risk_group['Default_Rate']:.2f}%**)."
        )


    # ========================================================
    # BUSINESS RECOMMENDATION
    # ========================================================

    st.markdown(
        "### 💡 Business Recommendation"
    )


    if (
        strongest_negative_corr < -0.10
    ):

        st.warning(
            f"🔴 External credit scores appear to be useful "
            f"risk indicators in the current dataset. "
            f"Lower **{strongest_negative_score}** values "
            f"are associated with higher default risk. "
            f"Consider giving this feature greater attention "
            f"during credit-risk assessment."
        )

    else:

        st.info(
            "📊 The external scores show relatively weak "
            "linear relationships with TARGET in the current "
            "filtered population."
        )


    if missing_percentage > 20:

        st.warning(
            f"⚠️ Missing external scores are relatively high "
            f"(**{missing_percentage:.2f}%**). "
            f"Missing-value handling should be carefully "
            f"considered before using these features in a model."
        )

    else:

        st.success(
            f"✅ Missing external scores are relatively "
            f"manageable at **{missing_percentage:.2f}%**."
        )


    # ========================================================
    # NOTE
    # ========================================================

    st.caption(
        "Note: Correlation indicates association, not causation. "
        "External credit scores should be evaluated together "
        "with other financial and demographic features."
    )