import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# TITLE
# ============================================================

st.title("👥 Customer Demographic Analysis")


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
    "Customers",
    f"{len(df):,}"
)


c2.metric(
    "Average Age",
    f"{df['AGE'].mean():.1f}"
)


c3.metric(
    "Male Customers",
    f"{(df['CODE_GENDER'] == 'M').sum():,}"
)


c4.metric(
    "Female Customers",
    f"{(df['CODE_GENDER'] == 'F').sum():,}"
)


c5.metric(
    "Average Family Size",
    f"{df['CNT_FAM_MEMBERS'].mean():.2f}"
)


st.markdown("---")


# ============================================================
# CUSTOMER DEMOGRAPHIC DISTRIBUTION
# ============================================================

st.subheader("👥 Customer Demographic Distribution")


columns = [
    ("CODE_GENDER", "Customers by Gender"),
    ("AGE_GROUP", "Customers by Age Group"),
    ("NAME_FAMILY_STATUS", "Customers by Family Status"),
    ("NAME_EDUCATION_TYPE", "Customers by Education"),
    ("NAME_HOUSING_TYPE", "Customers by Housing Type")
]


for column, title in columns:

    # --------------------------------------------------------
    # Check column
    # --------------------------------------------------------

    if column not in df.columns:
        continue


    # --------------------------------------------------------
    # Create data
    # --------------------------------------------------------

    data = (
        df[column]
        .value_counts()
        .reset_index()
    )


    data.columns = [
        column,
        "Customers"
    ]


    # --------------------------------------------------------
    # Bar Chart
    # --------------------------------------------------------

    fig = px.bar(
        data,
        x=column,
        y="Customers",
        title=title,
        text="Customers"
    )


    # --------------------------------------------------------
    # VALUES INSIDE BAR
    # --------------------------------------------------------

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="inside",
        insidetextanchor="middle"
    )


    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode="show"
    )


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DEFAULT BY DEMOGRAPHICS
# ============================================================

st.subheader("📊 Default Rate by Demographic Group")


for column in [
    "CODE_GENDER",
    "NAME_FAMILY_STATUS",
    "NAME_EDUCATION_TYPE",
    "NAME_HOUSING_TYPE"
]:

    # --------------------------------------------------------
    # Check column
    # --------------------------------------------------------

    if column not in df.columns:
        continue


    # --------------------------------------------------------
    # Calculate Default Rate
    # --------------------------------------------------------

    data = (
        df.groupby(column)["TARGET"]
        .mean()
        .mul(100)
        .sort_values(
            ascending=False
        )
        .reset_index()
    )


    data.columns = [
        column,
        "Default Rate"
    ]


    # --------------------------------------------------------
    # Bar Chart
    # --------------------------------------------------------

    fig = px.bar(
        data,
        x=column,
        y="Default Rate",
        title=f"Default Rate by {column}",
        text="Default Rate"
    )


    # --------------------------------------------------------
    # VALUES INSIDE BAR
    # --------------------------------------------------------

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="inside",
        insidetextanchor="middle"
    )


    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode="show"
    )


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

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
# 1. GENDER INSIGHT
# ============================================================

gender_default = (
    df.groupby("CODE_GENDER")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
)


if len(gender_default) > 0:

    highest_gender = (
        gender_default.index[0]
    )

    highest_gender_rate = (
        gender_default.iloc[0]
    )

    st.write(
        f"👤 **Gender Risk:** "
        f"{highest_gender} has the highest default rate "
        f"at **{highest_gender_rate:.2f}%**."
    )


# ============================================================
# 2. AGE INSIGHT
# ============================================================

if "AGE" in df.columns:

    average_age = (
        df["AGE"].mean()
    )

    youngest_age = (
        df["AGE"].min()
    )

    oldest_age = (
        df["AGE"].max()
    )

    st.write(
        f"🎂 **Age Insight:** "
        f"The average customer age is **{average_age:.1f} years**, "
        f"with customers ranging from approximately "
        f"**{youngest_age:.1f} to {oldest_age:.1f} years**."
    )


# ============================================================
# 3. FAMILY STATUS INSIGHT
# ============================================================

family_default = (
    df.groupby("NAME_FAMILY_STATUS")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
)


if len(family_default) > 0:

    highest_family = (
        family_default.index[0]
    )

    highest_family_rate = (
        family_default.iloc[0]
    )

    st.write(
        f"👨‍👩‍👧 **Family Status Risk:** "
        f"**{highest_family}** has the highest default rate "
        f"at **{highest_family_rate:.2f}%**."
    )


# ============================================================
# 4. EDUCATION INSIGHT
# ============================================================

education_default = (
    df.groupby("NAME_EDUCATION_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
)


if len(education_default) > 0:

    highest_education = (
        education_default.index[0]
    )

    highest_education_rate = (
        education_default.iloc[0]
    )

    lowest_education = (
        education_default.index[-1]
    )

    lowest_education_rate = (
        education_default.iloc[-1]
    )

    st.write(
        f"🎓 **Education Risk:** "
        f"**{highest_education}** has the highest default rate "
        f"at **{highest_education_rate:.2f}%**, while "
        f"**{lowest_education}** has the lowest at "
        f"**{lowest_education_rate:.2f}%**."
    )


# ============================================================
# 5. HOUSING INSIGHT
# ============================================================

housing_default = (
    df.groupby("NAME_HOUSING_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
)


if len(housing_default) > 0:

    highest_housing = (
        housing_default.index[0]
    )

    highest_housing_rate = (
        housing_default.iloc[0]
    )

    st.write(
        f"🏠 **Housing Risk:** "
        f"Customers with **{highest_housing}** housing type "
        f"show the highest default rate at "
        f"**{highest_housing_rate:.2f}%**."
    )


# ============================================================
# 6. CHILDREN INSIGHT
# ============================================================

if "CNT_CHILDREN" in df.columns:

    average_children = (
        df["CNT_CHILDREN"].mean()
    )

    customers_with_children = (
        df["CNT_CHILDREN"] > 0
    ).sum()

    customers_without_children = (
        df["CNT_CHILDREN"] == 0
    ).sum()

    st.write(
        f"👶 **Children Insight:** "
        f"Customers have an average of **{average_children:.2f} "
        f"children**. "
        f"**{customers_with_children:,}** customers have children, "
        f"while **{customers_without_children:,}** have no children."
    )


# ============================================================
# 7. FAMILY SIZE INSIGHT
# ============================================================

if "CNT_FAM_MEMBERS" in df.columns:

    largest_family = (
        df["CNT_FAM_MEMBERS"].max()
    )

    st.write(
        f"👨‍👩‍👧‍👦 **Family Size Insight:** "
        f"The largest recorded family size is "
        f"**{largest_family:.0f} members**."
    )


# ============================================================
# 8. OVERALL DEMOGRAPHIC RISK
# ============================================================

overall_default_rate = (
    df["TARGET"].mean() * 100
)


st.write(
    f"⚠️ **Overall Demographic Risk:** "
    f"The filtered customer population has an overall "
    f"default rate of **{overall_default_rate:.2f}%**."
)