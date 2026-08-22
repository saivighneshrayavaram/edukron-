import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features

st.title("🔎 Customer Risk Explorer")

df = load_data()
df = clean_data(df)
df = create_features(df)

# =====================================
# SEARCH
# =====================================

st.sidebar.header("🔎 Customer Search")

customer_id = st.sidebar.text_input(
    "Search Customer ID"
)

if customer_id:

    try:

        customer_id = int(customer_id)

        df = df[
            df["SK_ID_CURR"] == customer_id
        ]

    except ValueError:

        st.sidebar.error(
            "Enter a valid Customer ID"
        )


# =====================================
# FILTERS
# =====================================

target = st.sidebar.multiselect(
    "TARGET",
    sorted(df["TARGET"].dropna().unique()),
    default=sorted(df["TARGET"].dropna().unique())
)

if target:
    df = df[df["TARGET"].isin(target)]

gender = st.sidebar.multiselect(
    "Gender",
    sorted(
        df["CODE_GENDER"]
        .dropna()
        .unique()
    )
)

if gender:
    df = df[
        df["CODE_GENDER"].isin(gender)
    ]

education = st.sidebar.multiselect(
    "Education",
    sorted(
        df["NAME_EDUCATION_TYPE"]
        .dropna()
        .unique()
    )
)

if education:
    df = df[
        df["NAME_EDUCATION_TYPE"].isin(
            education
        )
    ]

income_type = st.sidebar.multiselect(
    "Income Type",
    sorted(
        df["NAME_INCOME_TYPE"]
        .dropna()
        .unique()
    )
)

if income_type:
    df = df[
        df["NAME_INCOME_TYPE"].isin(
            income_type
        )
    ]

occupation = st.sidebar.multiselect(
    "Occupation",
    sorted(
        df["OCCUPATION_TYPE"]
        .dropna()
        .unique()
    )
)

if occupation:
    df = df[
        df["OCCUPATION_TYPE"].isin(
            occupation
        )
    ]

contract = st.sidebar.multiselect(
    "Contract Type",
    sorted(
        df["NAME_CONTRACT_TYPE"]
        .dropna()
        .unique()
    )
)

if contract:
    df = df[
        df["NAME_CONTRACT_TYPE"].isin(
            contract
        )
    ]

housing = st.sidebar.multiselect(
    "Housing Type",
    sorted(
        df["NAME_HOUSING_TYPE"]
        .dropna()
        .unique()
    )
)

if housing:
    df = df[
        df["NAME_HOUSING_TYPE"].isin(
            housing
        )
    ]


# =====================================
# KPI
# =====================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Filtered Customers",
    f"{len(df):,}"
)

c2.metric(
    "Defaults",
    f"{(df['TARGET'] == 1).sum():,}"
)

c3.metric(
    "Default Rate",
    f"{df['TARGET'].mean() * 100:.2f}%"
    if len(df) else "0%"
)

c4.metric(
    "Average Credit",
    f"{df['AMT_CREDIT'].mean():,.0f}"
    if len(df) else "0"
)

st.markdown("---")


# =====================================
# CUSTOMER RISK PROFILE
# =====================================

if len(df) == 1:

    customer = df.iloc[0]

    st.subheader(
        f"👤 Customer {customer['SK_ID_CURR']}"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "TARGET",
        str(customer["TARGET"])
    )

    c2.metric(
        "Age",
        f"{customer['AGE']:.1f}"
    )

    c3.metric(
        "Income",
        f"{customer['AMT_INCOME_TOTAL']:,.0f}"
    )

    c4.metric(
        "Credit",
        f"{customer['AMT_CREDIT']:,.0f}"
    )

    st.subheader("Customer Information")

    information = {
        "Customer ID": customer["SK_ID_CURR"],
        "TARGET": customer["TARGET"],
        "Age": customer["AGE"],
        "Gender": customer["CODE_GENDER"],
        "Income": customer["AMT_INCOME_TOTAL"],
        "Credit": customer["AMT_CREDIT"],
        "Annuity": customer["AMT_ANNUITY"],
        "Education": customer["NAME_EDUCATION_TYPE"],
        "Occupation": customer["OCCUPATION_TYPE"],
        "Family Status": customer["NAME_FAMILY_STATUS"],
        "Children": customer["CNT_CHILDREN"],
        "Housing": customer["NAME_HOUSING_TYPE"],
        "Car Ownership": customer["FLAG_OWN_CAR"],
        "Property Ownership": customer["FLAG_OWN_REALTY"]
    }

    st.dataframe(
        pd.DataFrame(
            information.items(),
            columns=["Feature", "Value"]
        ),
        use_container_width=True
    )

    st.subheader("📊 Risk Indicators")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Credit / Income",
        f"{customer['CREDIT_INCOME_RATIO']:.2f}"
    )

    c2.metric(
        "Annuity / Income",
        f"{customer['ANNUITY_INCOME_RATIO']:.3f}"
    )

    c3.metric(
        "Credit / Goods",
        f"{customer['CREDIT_GOODS_RATIO']:.2f}"
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Employment Years",
        f"{customer['EMPLOYMENT_YEARS']:.1f}"
    )

    c2.metric(
        "Average External Score",
        f"{customer['AVERAGE_EXTERNAL_SCORE']:.3f}"
    )


# =====================================
# FILTERED DATA
# =====================================

else:

    st.subheader("📋 Filtered Applicant Records")

    display_columns = [
        "SK_ID_CURR",
        "TARGET",
        "AGE",
        "CODE_GENDER",
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "NAME_EDUCATION_TYPE",
        "OCCUPATION_TYPE",
        "NAME_FAMILY_STATUS",
        "CNT_CHILDREN",
        "NAME_HOUSING_TYPE",
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3",
        "CREDIT_INCOME_RATIO",
        "ANNUITY_INCOME_RATIO",
        "CREDIT_GOODS_RATIO",
        "EMPLOYMENT_YEARS",
        "AVERAGE_EXTERNAL_SCORE"
    ]

    display_columns = [
        col for col in display_columns
        if col in df.columns
    ]

    st.dataframe(
        df[display_columns],
        use_container_width=True
    )


# =====================================
# DOWNLOADS
# =====================================

st.markdown("---")

st.subheader("⬇️ Download Data")

csv_all = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download Filtered Customers",
    csv_all,
    "filtered_customers.csv",
    "text/csv"
)

default_df = df[
    df["TARGET"] == 1
]

csv_default = default_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download Default Customers",
    csv_default,
    "default_customers.csv",
    "text/csv"
)

high_risk_df = df[
    (
        df["CREDIT_INCOME_RATIO"] > 6
    )
    |
    (
        df["ANNUITY_INCOME_RATIO"] > 0.30
    )
]

csv_high = high_risk_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download High-Risk Customers",
    csv_high,
    "high_risk_customers.csv",
    "text/csv"
)

summary = pd.DataFrame({
    "Metric": [
        "Customers",
        "Defaults",
        "Default Rate",
        "Average Income",
        "Average Credit",
        "Average Annuity"
    ],
    "Value": [
        len(df),
        (df["TARGET"] == 1).sum(),
        df["TARGET"].mean() * 100 if len(df) else 0,
        df["AMT_INCOME_TOTAL"].mean() if len(df) else 0,
        df["AMT_CREDIT"].mean() if len(df) else 0,
        df["AMT_ANNUITY"].mean() if len(df) else 0
    ]
})

csv_summary = summary.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download Summary CSV",
    csv_summary,
    "risk_summary.csv",
    "text/csv"
)

# =====================================
# 📌 KEY INSIGHTS
# =====================================

st.subheader("📌 Key Insights")

if len(df) == 0:

    st.warning("No customers match the selected filters.")

else:

    # -------------------------------------
    # BASIC CALCULATIONS
    # -------------------------------------

    total_customers = len(df)

    defaults = int(
        (df["TARGET"] == 1).sum()
    )

    non_defaults = int(
        (df["TARGET"] == 0).sum()
    )

    default_rate = (
        df["TARGET"].mean() * 100
        if len(df)
        else 0
    )

    avg_income = (
        df["AMT_INCOME_TOTAL"].mean()
        if "AMT_INCOME_TOTAL" in df.columns
        else 0
    )

    avg_credit = (
        df["AMT_CREDIT"].mean()
        if "AMT_CREDIT" in df.columns
        else 0
    )

    avg_annuity = (
        df["AMT_ANNUITY"].mean()
        if "AMT_ANNUITY" in df.columns
        else 0
    )


    # -------------------------------------
    # HIGH RISK CUSTOMERS
    # -------------------------------------

    high_risk = df[
        (
            df["CREDIT_INCOME_RATIO"] > 6
        )
        |
        (
            df["ANNUITY_INCOME_RATIO"] > 0.30
        )
    ]

    high_risk_count = len(high_risk)

    high_risk_percentage = (
        high_risk_count / total_customers * 100
        if total_customers
        else 0
    )


    # -------------------------------------
    # AVERAGE EXTERNAL SCORE
    # -------------------------------------

    if "AVERAGE_EXTERNAL_SCORE" in df.columns:

        avg_external_score = (
            df["AVERAGE_EXTERNAL_SCORE"]
            .mean()
        )

    else:

        avg_external_score = 0


    # -------------------------------------
    # DEFAULT BY GENDER
    # -------------------------------------

    gender_insight = ""

    if "CODE_GENDER" in df.columns:

        gender_default = (
            df.groupby("CODE_GENDER")["TARGET"]
            .mean()
            .sort_values(ascending=False)
        )

        if len(gender_default) > 0:

            highest_gender = (
                gender_default.index[0]
            )

            highest_gender_rate = (
                gender_default.iloc[0] * 100
            )

            gender_insight = (
                f"Gender **{highest_gender}** "
                f"has the highest default rate "
                f"at **{highest_gender_rate:.2f}%**."
            )


    # -------------------------------------
    # DEFAULT BY EDUCATION
    # -------------------------------------

    education_insight = ""

    if "NAME_EDUCATION_TYPE" in df.columns:

        education_default = (
            df.groupby("NAME_EDUCATION_TYPE")["TARGET"]
            .mean()
            .sort_values(ascending=False)
        )

        if len(education_default) > 0:

            highest_education = (
                education_default.index[0]
            )

            education_rate = (
                education_default.iloc[0] * 100
            )

            education_insight = (
                f"Highest default rate is observed "
                f"among **{highest_education}** "
                f"at **{education_rate:.2f}%**."
            )


    # -------------------------------------
    # INCOME TYPE INSIGHT
    # -------------------------------------

    income_insight = ""

    if "NAME_INCOME_TYPE" in df.columns:

        income_default = (
            df.groupby("NAME_INCOME_TYPE")["TARGET"]
            .mean()
            .sort_values(ascending=False)
        )

        if len(income_default) > 0:

            highest_income_type = (
                income_default.index[0]
            )

            income_rate = (
                income_default.iloc[0] * 100
            )

            income_insight = (
                f"**{highest_income_type}** income group "
                f"shows the highest default rate "
                f"of **{income_rate:.2f}%**."
            )


    # -------------------------------------
    # CREDIT / INCOME INSIGHT
    # -------------------------------------

    ratio_insight = ""

    if "CREDIT_INCOME_RATIO" in df.columns:

        avg_credit_income_ratio = (
            df["CREDIT_INCOME_RATIO"].mean()
        )

        ratio_insight = (
            f"Average credit-to-income ratio is "
            f"**{avg_credit_income_ratio:.2f}**, "
            f"indicating the average credit burden "
            f"relative to customer income."
        )


    # -------------------------------------
    # DISPLAY INSIGHTS
    # -------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"👥 **Customer Base**\n\n"
            f"There are **{total_customers:,}** "
            f"customers matching the selected filters."
        )

        st.warning(
            f"⚠️ **Default Risk**\n\n"
            f"**{defaults:,}** customers are defaults, "
            f"giving a default rate of "
            f"**{default_rate:.2f}%**."
        )

        st.error(
            f"🚨 **High-Risk Customers**\n\n"
            f"**{high_risk_count:,}** customers "
            f"(**{high_risk_percentage:.2f}%**) "
            f"have a high credit/annuity burden."
        )

        if gender_insight:
            st.success(
                f"👤 **Gender Insight**\n\n"
                f"{gender_insight}"
            )


    with col2:

        st.info(
            f"💰 **Average Income**\n\n"
            f"Average customer income is "
            f"**{avg_income:,.0f}**."
        )

        st.info(
            f"💳 **Average Credit**\n\n"
            f"Average credit amount is "
            f"**{avg_credit:,.0f}**."
        )

        st.info(
            f"📊 **External Score**\n\n"
            f"Average external risk score is "
            f"**{avg_external_score:.3f}**."
        )

        if education_insight:
            st.success(
                f"🎓 **Education Insight**\n\n"
                f"{education_insight}"
            )


    # -------------------------------------
    # ADDITIONAL INSIGHTS
    # -------------------------------------

    st.markdown("### 🔍 Additional Risk Insights")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        st.write(
            f"• **{non_defaults:,}** customers "
            f"are non-default customers."
        )

        st.write(
            f"• Average annuity is "
            f"**{avg_annuity:,.0f}**."
        )

        st.write(
            f"• {ratio_insight}"
        )


    with insight_col2:

        if income_insight:

            st.write(
                f"• {income_insight}"
            )

        if "AGE" in df.columns:

            avg_age = df["AGE"].mean()

            st.write(
                f"• Average customer age is "
                f"**{avg_age:.1f} years**."
            )

        if "CNT_CHILDREN" in df.columns:

            avg_children = (
                df["CNT_CHILDREN"].mean()
            )

            st.write(
                f"• Average number of children is "
                f"**{avg_children:.1f}**."
            )