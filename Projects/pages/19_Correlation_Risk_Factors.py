import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📊 Correlation & Risk Factor Analysis")


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()
df = clean_data(df)
df = create_features(df)
df = apply_sidebar_filters(df)


# ============================================================
# NUMERICAL COLUMNS
# ============================================================

numeric_columns = [
    "TARGET",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",
    "CNT_CHILDREN",
    "CNT_FAM_MEMBERS",
    "AGE",
    "EMPLOYMENT_YEARS",
    "CREDIT_INCOME_RATIO",
    "ANNUITY_INCOME_RATIO",
    "CREDIT_GOODS_RATIO"
]

numeric_columns = [
    col
    for col in numeric_columns
    if col in df.columns
]


# ============================================================
# CORRELATION MATRIX
# ============================================================

if len(numeric_columns) >= 2:

    corr = df[numeric_columns].corr()

else:

    corr = pd.DataFrame()


# ============================================================
# CORRELATION HEATMAP
# ============================================================

if not corr.empty:

    st.subheader("🔥 Correlation Heatmap")

    fig = px.imshow(
        corr,
        text_auto=".2f",
        title="Correlation Heatmap",
        aspect="auto"
    )

    fig.update_layout(
        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "Not enough numerical columns available "
        "for correlation analysis."
    )


# ============================================================
# CORRELATION WITH TARGET
# ============================================================

if "TARGET" in corr.columns:

    target_corr = (
        corr["TARGET"]
        .drop("TARGET")
        .sort_values()
    )

    correlation_df = target_corr.reset_index()

    correlation_df.columns = [
        "Feature",
        "Correlation"
    ]

else:

    correlation_df = pd.DataFrame(
        columns=[
            "Feature",
            "Correlation"
        ]
    )


# ============================================================
# CORRELATION BAR CHART
# ============================================================

st.subheader("Correlation with TARGET")


if len(correlation_df) > 0:

    fig = px.bar(
        correlation_df,
        x="Correlation",
        y="Feature",
        orientation="h",
        title="Correlation with TARGET",
        text="Correlation"
    )

    # --------------------------------------------------------
    # SHOW VALUES INSIDE BARS
    # --------------------------------------------------------

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="inside"
    )

    fig.update_layout(
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "Correlation with TARGET cannot be calculated."
    )


# ============================================================
# POSITIVE CORRELATIONS
# ============================================================

st.subheader("⬆️ Positive Correlations")


if len(correlation_df) > 0:

    positive = (
        correlation_df
        .sort_values(
            "Correlation",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        positive,
        use_container_width=True
    )

else:

    st.info(
        "No correlation data available."
    )


# ============================================================
# NEGATIVE CORRELATIONS
# ============================================================

st.subheader("⬇️ Negative Correlations")


if len(correlation_df) > 0:

    negative = (
        correlation_df
        .sort_values(
            "Correlation"
        )
        .head(10)
    )

    st.dataframe(
        negative,
        use_container_width=True
    )

else:

    st.info(
        "No correlation data available."
    )


# ============================================================
# CREDIT VS INCOME
# ============================================================

st.subheader("💰 Credit vs Income")


if (
    "AMT_INCOME_TOTAL" in df.columns
    and "AMT_CREDIT" in df.columns
    and "TARGET" in df.columns
    and len(df) > 0
):

    sample = df.sample(
        min(10000, len(df)),
        random_state=42
    )

    fig = px.scatter(
        sample,
        x="AMT_INCOME_TOTAL",
        y="AMT_CREDIT",
        color="TARGET",
        title="Credit vs Income",
        hover_data=[
            "AMT_INCOME_TOTAL",
            "AMT_CREDIT",
            "TARGET"
        ]
    )

    fig.update_traces(
        marker=dict(
            size=7
        )
    )

    fig.update_layout(
        xaxis_title="Income",
        yaxis_title="Credit Amount"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "Required columns are not available "
        "for Credit vs Income analysis."
    )


# ============================================================
# EXTERNAL SCORE VS TARGET
# ============================================================

st.subheader("📊 External Score vs TARGET")


if (
    "AVERAGE_EXTERNAL_SCORE" in df.columns
    and "TARGET" in df.columns
):

    # --------------------------------------------------------
    # SELECT REQUIRED COLUMNS
    # --------------------------------------------------------

    score_df = df[
        [
            "TARGET",
            "AVERAGE_EXTERNAL_SCORE"
        ]
    ].dropna()


    if len(score_df) > 0:

        # ----------------------------------------------------
        # CREATE BOX PLOT
        # ----------------------------------------------------

        fig = px.box(
            score_df,
            x="TARGET",
            y="AVERAGE_EXTERNAL_SCORE",
            color="TARGET",
            title="External Score vs TARGET",
            points=False
        )


        # ----------------------------------------------------
        # CALCULATE STATISTICS
        # ----------------------------------------------------

        grouped_stats = (
            score_df
            .groupby("TARGET")[
                "AVERAGE_EXTERNAL_SCORE"
            ]
            .agg(
                Mean="mean",
                Median="median",
                Minimum="min",
                Maximum="max"
            )
            .reset_index()
        )


        # ----------------------------------------------------
        # REMOVE LEGEND
        # ----------------------------------------------------

        fig.update_layout(
            showlegend=False
        )


        # ----------------------------------------------------
        # BOX PLOT HOVER
        # ----------------------------------------------------

        fig.update_traces(
            hovertemplate=
            "<b>TARGET:</b> %{x}<br>"
            "<b>External Score:</b> %{y:.3f}"
            "<extra></extra>"
        )


        # ----------------------------------------------------
        # ADD MEAN + MEDIAN VALUES
        # ----------------------------------------------------

        for _, row in grouped_stats.iterrows():

            target_value = row["TARGET"]

            mean_value = row["Mean"]

            median_value = row["Median"]


            # ----------------------------------------------
            # Mean marker
            # ----------------------------------------------

            fig.add_trace(
                go.Scatter(
                    x=[target_value],
                    y=[mean_value],
                    mode="markers",
                    marker=dict(
                        symbol="diamond",
                        size=12
                    ),
                    name="Mean",
                    hovertemplate=(
                        f"<b>TARGET:</b> {target_value}<br>"
                        f"<b>Mean:</b> {mean_value:.3f}"
                        "<extra></extra>"
                    ),
                    showlegend=False
                )
            )


            # ----------------------------------------------
            # Mean + Median label
            # ----------------------------------------------

            fig.add_annotation(
                x=target_value,
                y=mean_value + 0.08,
                text=(
                    f"<b>Mean:</b> {mean_value:.3f}<br>"
                    f"<b>Median:</b> {median_value:.3f}"
                ),
                showarrow=False,
                font=dict(
                    size=12
                ),
                align="center"
            )


        # ----------------------------------------------------
        # X-AXIS LABELS
        # ----------------------------------------------------

        fig.update_layout(
            xaxis=dict(
                title="TARGET",
                tickmode="array",
                tickvals=[0, 1],
                ticktext=[
                    "Non-Default (0)",
                    "Default (1)"
                ]
            ),

            yaxis=dict(
                title="Average External Score",
                range=[
                    0,
                    min(
                        1,
                        score_df[
                            "AVERAGE_EXTERNAL_SCORE"
                        ].max() + 0.15
                    )
                ]
            ),

            height=550
        )


        # ----------------------------------------------------
        # DISPLAY GRAPH
        # ----------------------------------------------------

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ----------------------------------------------------
        # DISPLAY STATISTICS TABLE
        # ----------------------------------------------------

        display_stats = grouped_stats.copy()

        display_stats["TARGET"] = (
            display_stats["TARGET"]
            .map({
                0: "Non-Default",
                1: "Default"
            })
        )

        display_stats.columns = [
            "TARGET",
            "Mean",
            "Median",
            "Minimum",
            "Maximum"
        ]

        st.markdown(
            "#### 📌 External Score Statistics"
        )

        st.dataframe(
            display_stats.style.format({
                "Mean": "{:.3f}",
                "Median": "{:.3f}",
                "Minimum": "{:.3f}",
                "Maximum": "{:.3f}"
            }),
            use_container_width=True
        )


    else:

        st.warning(
            "No valid external score data available."
        )

else:

    st.warning(
        "AVERAGE_EXTERNAL_SCORE column is not available."
    )


# ============================================================
# POTENTIAL RISK FACTORS
# ============================================================

st.subheader("⚠️ Potential Risk Factors")


risk_factors = [
    "Low External Credit Score",
    "High Credit-to-Income Ratio",
    "High Annuity-to-Income Ratio",
    "Certain Occupations",
    "Certain Income Types",
    "Younger Age Groups",
    "Regional Risk Rating",
    "Employment History"
]


for factor in risk_factors:

    st.write(
        "🔴",
        factor
    )


# ============================================================
# KEY INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("📌 Key Insights")


# ============================================================
# EMPTY DATA CHECK
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
        if len(df)
        else 0
    )


    # ========================================================
    # STRONGEST CORRELATION WITH TARGET
    # ========================================================

    target_corr_abs = (
        correlation_df
        .assign(
            AbsCorrelation=lambda x:
            x["Correlation"].abs()
        )
        .sort_values(
            "AbsCorrelation",
            ascending=False
        )
    )


    if len(target_corr_abs) > 0:

        strongest_feature = (
            target_corr_abs
            .iloc[0]["Feature"]
        )

        strongest_corr = (
            target_corr_abs
            .iloc[0]["Correlation"]
        )

    else:

        strongest_feature = "N/A"

        strongest_corr = 0


    # ========================================================
    # MOST POSITIVE CORRELATION
    # ========================================================

    positive_corr = correlation_df[
        correlation_df["Correlation"] > 0
    ]


    if len(positive_corr) > 0:

        strongest_positive = (
            positive_corr
            .sort_values(
                "Correlation",
                ascending=False
            )
            .iloc[0]
        )

        positive_feature = (
            strongest_positive["Feature"]
        )

        positive_value = (
            strongest_positive["Correlation"]
        )

    else:

        positive_feature = "N/A"

        positive_value = 0


    # ========================================================
    # MOST NEGATIVE CORRELATION
    # ========================================================

    negative_corr = correlation_df[
        correlation_df["Correlation"] < 0
    ]


    if len(negative_corr) > 0:

        strongest_negative = (
            negative_corr
            .sort_values(
                "Correlation"
            )
            .iloc[0]
        )

        negative_feature = (
            strongest_negative["Feature"]
        )

        negative_value = (
            strongest_negative["Correlation"]
        )

    else:

        negative_feature = "N/A"

        negative_value = 0


    # ========================================================
    # EXTERNAL SCORE INSIGHT
    # ========================================================

    external_score_insight = ""


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
            and
            pd.notna(non_default_score)
        ):

            if default_score < non_default_score:

                external_score_insight = (
                    f"Default customers have a lower "
                    f"average external score "
                    f"(**{default_score:.3f}**) compared "
                    f"with non-default customers "
                    f"(**{non_default_score:.3f}**)."
                )

            else:

                external_score_insight = (
                    f"Default customers have an average "
                    f"external score of "
                    f"**{default_score:.3f}**, compared "
                    f"with **{non_default_score:.3f}** "
                    f"for non-default customers."
                )


    # ========================================================
    # CREDIT / INCOME INSIGHT
    # ========================================================

    ratio_insight = ""


    if "CREDIT_INCOME_RATIO" in df.columns:

        avg_ratio_default = df.loc[
            df["TARGET"] == 1,
            "CREDIT_INCOME_RATIO"
        ].mean()


        avg_ratio_non_default = df.loc[
            df["TARGET"] == 0,
            "CREDIT_INCOME_RATIO"
        ].mean()


        if (
            pd.notna(avg_ratio_default)
            and
            pd.notna(avg_ratio_non_default)
        ):

            ratio_insight = (
                f"Default customers have an average "
                f"credit-to-income ratio of "
                f"**{avg_ratio_default:.2f}**, compared "
                f"with **{avg_ratio_non_default:.2f}** "
                f"for non-default customers."
            )


    # ========================================================
    # AGE INSIGHT
    # ========================================================

    age_insight = ""


    if "AGE" in df.columns:

        default_age = df.loc[
            df["TARGET"] == 1,
            "AGE"
        ].mean()


        non_default_age = df.loc[
            df["TARGET"] == 0,
            "AGE"
        ].mean()


        if (
            pd.notna(default_age)
            and
            pd.notna(non_default_age)
        ):

            age_insight = (
                f"Average age is **{default_age:.1f} years** "
                f"for default customers and "
                f"**{non_default_age:.1f} years** "
                f"for non-default customers."
            )


    # ========================================================
    # KPI INSIGHTS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Customers",
        f"{total_customers:,}"
    )


    c2.metric(
        "Default Rate",
        f"{default_rate:.2f}%"
    )


    c3.metric(
        "Strongest Correlation",
        f"{strongest_corr:.2f}"
    )


    c4.metric(
        "Risk Factor",
        strongest_feature
    )


    # ========================================================
    # INSIGHT CARDS
    # ========================================================

    col1, col2 = st.columns(2)


    # ========================================================
    # LEFT COLUMN
    # ========================================================

    with col1:

        st.info(
            f"🔎 **Strongest Risk Relationship**\n\n"
            f"**{strongest_feature}** has the strongest "
            f"absolute correlation with TARGET, with "
            f"a correlation of **{strongest_corr:.3f}**."
        )


        if positive_feature != "N/A":

            st.warning(
                f"⬆️ **Positive Risk Factor**\n\n"
                f"**{positive_feature}** has the strongest "
                f"positive correlation with TARGET "
                f"(**{positive_value:.3f}**)."
            )


        if ratio_insight:

            st.success(
                f"💳 **Credit Burden**\n\n"
                f"{ratio_insight}"
            )


    # ========================================================
    # RIGHT COLUMN
    # ========================================================

    with col2:

        if negative_feature != "N/A":

            st.info(
                f"⬇️ **Negative Relationship**\n\n"
                f"**{negative_feature}** has the strongest "
                f"negative correlation with TARGET "
                f"(**{negative_value:.3f}**)."
            )


        if external_score_insight:

            st.warning(
                f"📊 **External Score Risk**\n\n"
                f"{external_score_insight}"
            )


        if age_insight:

            st.info(
                f"👥 **Age Pattern**\n\n"
                f"{age_insight}"
            )


    # ========================================================
    # BUSINESS INTERPRETATION
    # ========================================================

    st.markdown(
        "### 💡 Business Interpretation"
    )


    if strongest_corr > 0:

        st.write(
            f"🔴 **{strongest_feature}** shows the strongest "
            f"positive relationship with loan default in "
            f"the current filtered dataset."
        )


    elif strongest_corr < 0:

        st.write(
            f"🟢 **{strongest_feature}** shows the strongest "
            f"negative relationship with loan default. "
            f"Higher values are associated with lower "
            f"default probability."
        )


    else:

        st.write(
            "⚪ No strong linear relationship with TARGET "
            "was identified among the selected numerical "
            "features."
        )


    st.write(
        f"📌 The current filtered population contains "
        f"**{default_rate:.2f}% defaults**. "
        f"Correlation should be interpreted as an association "
        f"rather than proof of causation."
    )