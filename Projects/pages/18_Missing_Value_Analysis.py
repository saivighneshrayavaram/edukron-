import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_data


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🧹 Missing Value Analysis")


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()


# ============================================================
# BASIC CALCULATIONS
# ============================================================

total_rows = len(df)

total_columns = len(df.columns)

total_missing = df.isna().sum().sum()

missing_columns = (
    df.isna().sum() > 0
).sum()

more_than_50 = (
    df.isna().mean() > 0.50
).sum()


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)


c1.metric(
    "Total Rows",
    f"{total_rows:,}"
)

c2.metric(
    "Total Columns",
    f"{total_columns:,}"
)

c3.metric(
    "Total Missing Values",
    f"{total_missing:,}"
)

c4.metric(
    "Columns with Missing",
    f"{missing_columns:,}"
)

c5.metric(
    ">50% Missing",
    f"{more_than_50:,}"
)


st.markdown("---")


# ============================================================
# MISSING VALUE SUMMARY
# ============================================================

missing = pd.DataFrame({

    "Column": df.columns,

    "Missing Count": df.isna().sum().values,

    "Missing %": (
        df.isna().mean().values * 100
    ),

    "Data Type": df.dtypes.astype(str).values

})


missing = missing.sort_values(
    "Missing Count",
    ascending=False
)


st.subheader("📋 Missing Value Summary")


st.dataframe(
    missing,
    use_container_width=True
)


# ============================================================
# TOP 20 MISSING COLUMNS
# ============================================================

top20 = missing.head(20)


# ============================================================
# GRAPH 1
# TOP 20 COLUMNS WITH MISSING VALUES
# ============================================================

fig = px.bar(
    top20,
    x="Missing Count",
    y="Column",
    orientation="h",
    title="Top 20 Columns with Missing Values",
    text="Missing Count"
)


fig.update_traces(
    textposition="inside",
    texttemplate="%{x:,}",
    insidetextanchor="middle"
)


fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="show",
    xaxis_title="Missing Count",
    yaxis_title="Column"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# GRAPH 2
# TOP 20 MISSING PERCENTAGE
# ============================================================

fig = px.bar(
    top20,
    x="Missing %",
    y="Column",
    orientation="h",
    title="Top 20 Missing Percentage",
    text="Missing %"
)


fig.update_traces(
    textposition="inside",
    texttemplate="%{x:.2f}%",
    insidetextanchor="middle"
)


fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="show",
    xaxis_title="Missing Percentage (%)",
    yaxis_title="Column"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# MISSING BY DATA TYPE
# ============================================================

dtype_missing = (
    missing.groupby("Data Type")["Missing Count"]
    .sum()
    .reset_index()
)


# ============================================================
# GRAPH 3
# MISSING VALUES BY DATA TYPE
# ============================================================

fig = px.bar(
    dtype_missing,
    x="Data Type",
    y="Missing Count",
    title="Missing Values by Data Type",
    text="Missing Count"
)


fig.update_traces(
    textposition="inside",
    texttemplate="%{y:,}",
    insidetextanchor="middle"
)


fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="show",
    xaxis_title="Data Type",
    yaxis_title="Missing Count"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# RECOMMENDED TREATMENT
# ============================================================

st.subheader("⚙️ Recommended Treatment")


treatment = missing.copy()


def recommend(row):

    if row["Missing %"] == 0:

        return "No Missing Values"

    if row["Missing %"] > 50:

        return "Consider Drop"

    if (
        "float" in row["Data Type"]
        or "int" in row["Data Type"]
    ):

        return "Median / Missing Indicator"

    return "Mode / Unknown"


treatment["Recommended Action"] = treatment.apply(
    recommend,
    axis=1
)


st.dataframe(
    treatment,
    use_container_width=True
)


# ============================================================
# 📌 KEY MISSING VALUE INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("📌 Key Missing Value Insights")


# ============================================================
# BASIC CALCULATIONS
# ============================================================

columns_with_missing = missing[
    missing["Missing Count"] > 0
]


columns_without_missing = missing[
    missing["Missing Count"] == 0
]


if len(columns_with_missing) > 0:

    # ========================================================
    # HIGHEST MISSING COLUMN
    # ========================================================

    highest_missing = (
        missing
        .sort_values(
            "Missing %",
            ascending=False
        )
        .iloc[0]
    )


    highest_column = (
        highest_missing["Column"]
    )


    highest_percentage = (
        highest_missing["Missing %"]
    )


    highest_count = (
        highest_missing["Missing Count"]
    )


    # ========================================================
    # TOTAL MISSING PERCENTAGE
    # ========================================================

    total_cells = (
        total_rows * total_columns
    )


    overall_missing_percentage = (

        total_missing / total_cells * 100

        if total_cells > 0

        else 0

    )


    # ========================================================
    # AVERAGE MISSING PERCENTAGE
    # ========================================================

    average_missing_percentage = (
        columns_with_missing["Missing %"].mean()
    )


    # ========================================================
    # NUMERIC COLUMNS WITH MISSING
    # ========================================================

    numeric_missing = columns_with_missing[

        columns_with_missing["Data Type"].str.contains(
            "int|float",
            case=False,
            regex=True
        )

    ]


    # ========================================================
    # CATEGORICAL COLUMNS WITH MISSING
    # ========================================================

    categorical_missing = columns_with_missing[

        ~columns_with_missing["Data Type"].str.contains(
            "int|float",
            case=False,
            regex=True
        )

    ]


    # ========================================================
    # CRITICAL COLUMNS
    # MORE THAN 50%
    # ========================================================

    critical_columns = missing[
        missing["Missing %"] > 50
    ]


    # ========================================================
    # MODERATE COLUMNS
    # 20% - 50%
    # ========================================================

    moderate_columns = missing[

        (missing["Missing %"] >= 20)

        &

        (missing["Missing %"] <= 50)

    ]


    # ========================================================
    # LOW MISSING COLUMNS
    # LESS THAN 20%
    # ========================================================

    low_missing_columns = missing[

        (missing["Missing %"] > 0)

        &

        (missing["Missing %"] < 20)

    ]


    # ========================================================
    # INSIGHT KPI CARDS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Overall Missing %",
        f"{overall_missing_percentage:.2f}%"
    )


    c2.metric(
        "Highest Missing %",
        f"{highest_percentage:.2f}%"
    )


    c3.metric(
        "Critical Columns",
        f"{len(critical_columns):,}"
    )


    c4.metric(
        "Complete Columns",
        f"{len(columns_without_missing):,}"
    )


    # ========================================================
    # INSIGHT CARDS
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.warning(

            f"⚠️ **Highest Missing Column**\n\n"

            f"**{highest_column}** contains "

            f"**{highest_count:,}** missing values "

            f"(**{highest_percentage:.2f}%** of rows)."

        )


        if len(critical_columns) > 0:

            critical_names = ", ".join(

                critical_columns["Column"]
                .head(5)
                .astype(str)
                .tolist()

            )


            st.error(

                f"🚨 **Critical Missing Data**\n\n"

                f"**{len(critical_columns)}** columns have "

                f"more than 50% missing values. "

                f"Examples: **{critical_names}**."

            )

        else:

            st.success(

                "✅ **No Critical Columns**\n\n"

                "No column contains more than 50% "

                "missing values."

            )


    with col2:

        st.info(

            f"📊 **Overall Data Quality**\n\n"

            f"Approximately **{overall_missing_percentage:.2f}%** "

            f"of all cells in the dataset are missing."

        )


        st.info(

            f"🔢 **Affected Data Types**\n\n"

            f"**{len(numeric_missing)}** numeric columns and "

            f"**{len(categorical_missing)}** categorical columns "

            f"contain missing values."

        )


    # ========================================================
    # DISTRIBUTION OF MISSINGNESS
    # ========================================================

    st.markdown(
        "### 🔍 Missingness Distribution"
    )


    d1, d2, d3 = st.columns(3)


    d1.metric(
        "Low Missingness (<20%)",
        f"{len(low_missing_columns):,}"
    )


    d2.metric(
        "Moderate (20–50%)",
        f"{len(moderate_columns):,}"
    )


    d3.metric(
        "High (>50%)",
        f"{len(critical_columns):,}"
    )


    # ========================================================
    # TOP PROBLEMATIC COLUMNS
    # ========================================================

    st.markdown(
        "### 🚨 Top Problematic Columns"
    )


    top_problematic = (

        missing[
            missing["Missing Count"] > 0
        ]

        .sort_values(
            "Missing %",
            ascending=False
        )

        .head(10)

        [

            [
                "Column",
                "Missing Count",
                "Missing %",
                "Data Type"
            ]

        ]

    )


    st.dataframe(
        top_problematic,
        use_container_width=True
    )


    # ========================================================
    # AUTOMATIC RECOMMENDATION
    # ========================================================

    st.markdown(
        "### 💡 Data Quality Recommendation"
    )


    if len(critical_columns) > 0:

        st.error(

            f"🚨 **Action Required:** "

            f"{len(critical_columns)} columns have more than "

            f"50% missing values. These columns should be "

            f"carefully evaluated for removal or alternative "

            f"feature engineering."

        )


    elif len(moderate_columns) > 0:

        st.warning(

            f"⚠️ **Moderate Missingness:** "

            f"{len(moderate_columns)} columns contain between "

            f"20% and 50% missing values. Consider using "

            f"domain-based imputation or missing-value indicators."

        )


    elif len(low_missing_columns) > 0:

        st.success(

            f"✅ **Manageable Missingness:** "

            f"Most missing values are below 20%. "

            f"Median imputation for numerical features and "

            f"mode/'Unknown' treatment for categorical features "

            f"may be appropriate."

        )


    else:

        st.success(

            "🎉 **Excellent Data Quality:** "

            "No missing values were detected in the dataset."

        )


else:

    # ========================================================
    # NO MISSING VALUES
    # ========================================================

    st.success(

        "🎉 **No Missing Values Found**\n\n"

        "The dataset is complete and does not require "

        "missing-value treatment."

    )