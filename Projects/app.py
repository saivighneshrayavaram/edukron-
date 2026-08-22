import streamlit as st

from utils.data_loader import load_data


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Home Credit Default Risk Dashboard",
    page_icon="🏦",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🏦 Home Credit Default Risk Dashboard")

st.markdown("""
Welcome to the **Home Credit Default Risk Analytics Dashboard**.

This dashboard analyzes loan applicants and identifies patterns
associated with customer default risk.

Use the pages from the sidebar to explore customer demographics,
financial characteristics, credit behavior, employment,
housing, regional patterns, and major risk factors.
""")


# ============================================================
# DASHBOARD OVERVIEW
# ============================================================

with st.expander("📋 Dashboard Overview", expanded=True):

    st.markdown("""
### Available Pages

1. 📈 Executive Overview
2. ⚠️ Default Analysis
3. 👥 Demographic Analysis
4. 🎂 Age Analysis
5. ⚧️ Gender Analysis
6. 💰 Income Analysis
7. 💳 Credit Analysis
8. 💵 Annuity Analysis
9. 🎓 Education Analysis
10. 💼 Employment Analysis
11. 👨‍👩‍👧 Family Analysis
12. 🏠 Housing Analysis
13. 📑 Contract Type Analysis
14. 📊 External Score Analysis
15. 🌍 Regional Analysis
16. 🧹 Missing Value Analysis
17. 🔗 Correlation Analysis
18. 🔎 Customer Risk Explorer
19. 🚀 Advanced Insights
20. 📋 Data Explorer
""")


# ============================================================
# DATASET INFORMATION
# ============================================================

with st.expander("📊 Dataset Information"):

    st.markdown("""
### Dataset

**Source:** Home Credit Default Risk Dataset

### Target Variable

- `TARGET = 0` → Customer repaid loan successfully
- `TARGET = 1` → Customer faced payment difficulties

### Major Analysis Areas

- 👥 Customer Demographics
- 💰 Income Information
- 💳 Credit Information
- 💵 Annuity Information
- 💼 Employment Information
- 🎓 Education Information
- 👨‍👩‍👧 Family Information
- 🏠 Housing Information
- 📊 External Credit Scores
- 🌍 Regional Characteristics
""")


# ============================================================
# BUSINESS PROBLEM
# ============================================================

with st.expander("🎯 Business Problem"):

    st.markdown("""
Home Credit provides loans to individuals with limited or
insufficient credit history.

The objective of this project is to analyze applicant
characteristics and identify patterns associated with
payment difficulties.

### The dashboard helps to:

✅ Understand customer demographics

✅ Analyze financial characteristics

✅ Explore loan and credit behavior

✅ Identify high-risk customer groups

✅ Understand factors associated with default

✅ Support data-driven lending decisions
""")


# ============================================================
# TECHNOLOGY STACK
# ============================================================

with st.expander("⚙️ Technology Stack"):

    st.markdown("""
### Tools & Technologies

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Scikit-Learn
- Exploratory Data Analysis
- Data Visualization
""")


# ============================================================
# DATASET SUMMARY
# ============================================================

st.header("📈 Dataset Summary")

try:

    # Load dataset
    df = load_data()

    # --------------------------------------------------------
    # Dataset statistics
    # --------------------------------------------------------

    total_records = len(df)

    total_features = len(df.columns)

    default_count = (
        df["TARGET"] == 1
    ).sum()

    default_rate = (
        df["TARGET"].mean() * 100
    )

    missing_values = (
        df.isnull().sum().sum()
    )

    missing_rate = (
        missing_values /
        (df.shape[0] * df.shape[1])
        * 100
    )

    # --------------------------------------------------------
    # KPI Cards
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        f"{total_records:,}"
    )

    col2.metric(
        "Total Features",
        f"{total_features:,}"
    )

    col3.metric(
        "Default Rate",
        f"{default_rate:.2f}%"
    )

    col4.metric(
        "Missing Values",
        f"{missing_rate:.2f}%"
    )

    # --------------------------------------------------------
    # Additional Dataset Information
    # --------------------------------------------------------

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📌 Default Summary")

        st.write(
            f"Total Applicants: **{total_records:,}**"
        )

        st.write(
            f"Customers with Payment Difficulties: "
            f"**{default_count:,}**"
        )

        st.write(
            f"Customers without Payment Difficulties: "
            f"**{total_records - default_count:,}**"
        )

    with col2:

        st.subheader("📌 Data Quality")

        columns_with_missing = (
            df.isna().sum() > 0
        ).sum()

        st.write(
            f"Columns with Missing Values: "
            f"**{columns_with_missing:,}**"
        )

        st.write(
            f"Total Missing Values: "
            f"**{missing_values:,}**"
        )

        st.write(
            f"Overall Missing Percentage: "
            f"**{missing_rate:.2f}%**"
        )


except Exception as e:

    st.error(
        f"❌ Error Loading Dataset: {e}"
    )


# ============================================================
# KEY BUSINESS INSIGHTS
# ============================================================

st.markdown("---")

st.header("💡 Key Business Insights")

st.info("""
### What this dashboard helps answer

🔹 Which customer groups have higher default rates?

🔹 Does income level affect repayment risk?

🔹 How does credit amount compare with customer income?

🔹 Does annuity burden relate to default risk?

🔹 Which occupations and income types show higher risk?

🔹 Which age groups have higher payment difficulties?

🔹 How do external credit scores relate to default?

🔹 Does housing and asset ownership show different risk patterns?

🔹 Are certain regions associated with higher default rates?

🔹 Which individual customers require closer risk evaluation?
""")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏦 Home Credit Default Risk Dashboard • "
    "Built using Python, Pandas, Plotly and Streamlit"
)