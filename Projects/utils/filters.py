import streamlit as st


def apply_sidebar_filters(df):

    filtered_df = df.copy()

    st.sidebar.header("🔎 Filters")

    # TARGET
    target_options = st.sidebar.multiselect(
        "TARGET",
        sorted(df["TARGET"].dropna().unique()),
        default=sorted(df["TARGET"].dropna().unique())
    )

    if target_options:
        filtered_df = filtered_df[
            filtered_df["TARGET"].isin(target_options)
        ]

    # Gender
    if "CODE_GENDER" in df.columns:

        gender_options = st.sidebar.multiselect(
            "Gender",
            sorted(df["CODE_GENDER"].dropna().unique()),
            default=sorted(df["CODE_GENDER"].dropna().unique())
        )

        if gender_options:
            filtered_df = filtered_df[
                filtered_df["CODE_GENDER"].isin(gender_options)
            ]

    # Education
    if "NAME_EDUCATION_TYPE" in df.columns:

        education_options = st.sidebar.multiselect(
            "Education",
            sorted(
                df["NAME_EDUCATION_TYPE"]
                .dropna()
                .unique()
            )
        )

        if education_options:
            filtered_df = filtered_df[
                filtered_df["NAME_EDUCATION_TYPE"]
                .isin(education_options)
            ]

    # Income Type
    if "NAME_INCOME_TYPE" in df.columns:

        income_options = st.sidebar.multiselect(
            "Income Type",
            sorted(
                df["NAME_INCOME_TYPE"]
                .dropna()
                .unique()
            )
        )

        if income_options:
            filtered_df = filtered_df[
                filtered_df["NAME_INCOME_TYPE"]
                .isin(income_options)
            ]

    # Contract Type
    if "NAME_CONTRACT_TYPE" in df.columns:

        contract_options = st.sidebar.multiselect(
            "Contract Type",
            sorted(
                df["NAME_CONTRACT_TYPE"]
                .dropna()
                .unique()
            )
        )

        if contract_options:
            filtered_df = filtered_df[
                filtered_df["NAME_CONTRACT_TYPE"]
                .isin(contract_options)
            ]

    return filtered_df