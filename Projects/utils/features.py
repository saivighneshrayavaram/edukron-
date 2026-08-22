import numpy as np
import pandas as pd


def create_features(df):

    df = df.copy()

    # ========================================================
    # 1. AGE
    # ========================================================

    if "DAYS_BIRTH" in df.columns:

        df["AGE"] = abs(df["DAYS_BIRTH"]) / 365

        df["AGE_GROUP"] = pd.cut(
            df["AGE"],
            bins=[0, 20, 30, 40, 50, 60, 70, 100],
            labels=[
                "0-20",
                "21-30",
                "31-40",
                "41-50",
                "51-60",
                "61-70",
                "71+"
            ],
            include_lowest=True
        )

    # ========================================================
    # 2. EMPLOYMENT YEARS
    # ========================================================

    if "DAYS_EMPLOYED" in df.columns:

        df["EMPLOYMENT_YEARS"] = np.where(
            df["DAYS_EMPLOYED"] < 0,
            abs(df["DAYS_EMPLOYED"]) / 365,
            np.nan
        )

    # ========================================================
    # 3. INCOME GROUP
    # ========================================================

    if "AMT_INCOME_TOTAL" in df.columns:

        df["INCOME_GROUP"] = pd.cut(
            df["AMT_INCOME_TOTAL"],
            bins=[
                0,
                100000,
                200000,
                300000,
                500000,
                1000000,
                float("inf")
            ],
            labels=[
                "Low",
                "Lower-Middle",
                "Middle",
                "Upper-Middle",
                "High",
                "Very High"
            ],
            include_lowest=True
        )

    # ========================================================
    # 4. CREDIT TO INCOME RATIO
    # ========================================================

    if (
        "AMT_CREDIT" in df.columns
        and "AMT_INCOME_TOTAL" in df.columns
    ):

        df["CREDIT_INCOME_RATIO"] = (
            df["AMT_CREDIT"] /
            df["AMT_INCOME_TOTAL"].replace(0, np.nan)
        )

    # ========================================================
    # 5. ANNUITY TO INCOME RATIO
    # ========================================================

    if (
        "AMT_ANNUITY" in df.columns
        and "AMT_INCOME_TOTAL" in df.columns
    ):

        df["ANNUITY_INCOME_RATIO"] = (
            df["AMT_ANNUITY"] /
            df["AMT_INCOME_TOTAL"].replace(0, np.nan)
        )

        # ====================================================
        # 5A. ANNUITY BURDEN GROUP
        # ====================================================

        df["ANNUITY_BURDEN_GROUP"] = pd.cut(
            df["ANNUITY_INCOME_RATIO"],
            bins=[
                -np.inf,
                0.10,
                0.20,
                0.30,
                0.40,
                np.inf
            ],
            labels=[
                "Very Low (<10%)",
                "Low (10-20%)",
                "Medium (20-30%)",
                "High (30-40%)",
                "Very High (>40%)"
            ],
            include_lowest=True
        )

    # ========================================================
    # 6. CREDIT TO GOODS RATIO
    # ========================================================

    if (
        "AMT_CREDIT" in df.columns
        and "AMT_GOODS_PRICE" in df.columns
    ):

        df["CREDIT_GOODS_RATIO"] = (
            df["AMT_CREDIT"] /
            df["AMT_GOODS_PRICE"].replace(0, np.nan)
        )

    # ========================================================
    # 7. AVERAGE EXTERNAL CREDIT SCORE
    # ========================================================

    external_columns = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]

    available_columns = [
        column
        for column in external_columns
        if column in df.columns
    ]

    if len(available_columns) > 0:

        df["AVERAGE_EXTERNAL_SCORE"] = (
            df[available_columns].mean(axis=1)
        )

        # ====================================================
        # 7A. EXTERNAL SCORE GROUP
        # ====================================================

        df["EXTERNAL_SCORE_GROUP"] = pd.cut(
            df["AVERAGE_EXTERNAL_SCORE"],
            bins=[
                -np.inf,
                0.30,
                0.50,
                0.70,
                np.inf
            ],
            labels=[
                "Low",
                "Medium",
                "High",
                "Very High"
            ],
            include_lowest=True
        )

    # ========================================================
    # 8. CREDIT GROUP
    # ========================================================

    if "AMT_CREDIT" in df.columns:

        df["CREDIT_GROUP"] = pd.cut(
            df["AMT_CREDIT"],
            bins=[
                0,
                100000,
                250000,
                500000,
                750000,
                1000000,
                float("inf")
            ],
            labels=[
                "0-1L",
                "1L-2.5L",
                "2.5L-5L",
                "5L-7.5L",
                "7.5L-10L",
                "10L+"
            ],
            include_lowest=True
        )

    # ========================================================
    # 9. TOTAL DOCUMENT COUNT
    # ========================================================

    document_columns = [
        "FLAG_DOCUMENT_2",
        "FLAG_DOCUMENT_3",
        "FLAG_DOCUMENT_4",
        "FLAG_DOCUMENT_5",
        "FLAG_DOCUMENT_6",
        "FLAG_DOCUMENT_7",
        "FLAG_DOCUMENT_8",
        "FLAG_DOCUMENT_9",
        "FLAG_DOCUMENT_10",
        "FLAG_DOCUMENT_11",
        "FLAG_DOCUMENT_12",
        "FLAG_DOCUMENT_13",
        "FLAG_DOCUMENT_14",
        "FLAG_DOCUMENT_15",
        "FLAG_DOCUMENT_16",
        "FLAG_DOCUMENT_17",
        "FLAG_DOCUMENT_18",
        "FLAG_DOCUMENT_19",
        "FLAG_DOCUMENT_20",
        "FLAG_DOCUMENT_21"
    ]

    available_documents = [
        column
        for column in document_columns
        if column in df.columns
    ]

    if len(available_documents) > 0:

        df["TOTAL_DOCUMENTS"] = (
            df[available_documents].sum(axis=1)
        )

    # ========================================================
    # 10. FAMILY MEMBERS
    # ========================================================

    if "CNT_FAM_MEMBERS" in df.columns:

        df["FAMILY_SIZE_GROUP"] = pd.cut(
            df["CNT_FAM_MEMBERS"],
            bins=[
                -np.inf,
                1,
                2,
                4,
                6,
                np.inf
            ],
            labels=[
                "Single",
                "Small",
                "Medium",
                "Large",
                "Very Large"
            ],
            include_lowest=True
        )

    # ========================================================
    # 11. CHILDREN GROUP
    # ========================================================

    if "CNT_CHILDREN" in df.columns:

        df["CHILDREN_GROUP"] = pd.cut(
            df["CNT_CHILDREN"],
            bins=[
                -np.inf,
                0,
                1,
                2,
                np.inf
            ],
            labels=[
                "No Children",
                "1 Child",
                "2 Children",
                "3+ Children"
            ],
            include_lowest=True
        )

    # ========================================================
    # 12. INCOME PER FAMILY MEMBER
    # ========================================================

    if (
        "AMT_INCOME_TOTAL" in df.columns
        and "CNT_FAM_MEMBERS" in df.columns
    ):

        df["INCOME_PER_FAMILY_MEMBER"] = (
            df["AMT_INCOME_TOTAL"] /
            df["CNT_FAM_MEMBERS"].replace(0, np.nan)
        )

    # ========================================================
    # 13. CREDIT PER FAMILY MEMBER
    # ========================================================

    if (
        "AMT_CREDIT" in df.columns
        and "CNT_FAM_MEMBERS" in df.columns
    ):

        df["CREDIT_PER_FAMILY_MEMBER"] = (
            df["AMT_CREDIT"] /
            df["CNT_FAM_MEMBERS"].replace(0, np.nan)
        )

    # ========================================================
    # 14. EMPLOYMENT GROUP
    # ========================================================

    if "EMPLOYMENT_YEARS" in df.columns:

        df["EMPLOYMENT_GROUP"] = pd.cut(
            df["EMPLOYMENT_YEARS"],
            bins=[
                -np.inf,
                1,
                3,
                5,
                10,
                20,
                np.inf
            ],
            labels=[
                "<1 Year",
                "1-3 Years",
                "3-5 Years",
                "5-10 Years",
                "10-20 Years",
                "20+ Years"
            ],
            include_lowest=True
        )

    # ========================================================
    # 15. RETURN DATAFRAME
    # ========================================================

    return df