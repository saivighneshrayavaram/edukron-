import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🏠 Housing & Asset Analysis")


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()
df = clean_data(df)
df = create_features(df)
df = apply_sidebar_filters(df)


# ============================================================
# CHECK EMPTY DATA
# ============================================================

if len(df) == 0:

    st.warning(
        "No customers match the selected filters."
    )

    st.stop()


# ============================================================
# BASIC OWNERSHIP CALCULATIONS
# ============================================================

car_owners = (
    df["FLAG_OWN_CAR"] == "Y"
).sum()

property_owners = (
    df["FLAG_OWN_REALTY"] == "Y"
).sum()

both = (
    (df["FLAG_OWN_CAR"] == "Y") &
    (df["FLAG_OWN_REALTY"] == "Y")
).sum()


property_default = (
    df.loc[
        df["FLAG_OWN_REALTY"] == "Y",
        "TARGET"
    ].mean() * 100
)


# ============================================================
# TOP KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Car Owners",
    f"{car_owners:,}"
)

c2.metric(
    "Property Owners",
    f"{property_owners:,}"
)

c3.metric(
    "Own Both",
    f"{both:,}"
)

c4.metric(
    "Property Owner Default Rate",
    f"{property_default:.2f}%"
)


# ============================================================
# 🚗 CAR & PROPERTY OWNERSHIP DISTRIBUTION
# ============================================================

for column, title in [
    (
        "FLAG_OWN_CAR",
        "Car Ownership Distribution"
    ),
    (
        "FLAG_OWN_REALTY",
        "Property Ownership Distribution"
    )
]:

    data = (
        df[column]
        .value_counts()
        .reset_index()
    )

    data.columns = [
        column,
        "Customers"
    ]

    fig = px.pie(
        data,
        names=column,
        values="Customers",
        title=title,
        hole=0.3
    )

    # Show value + percentage inside pie
    fig.update_traces(
        textinfo="label+value+percent",
        textposition="inside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 🚗 DEFAULT RATE BY CAR / PROPERTY OWNERSHIP
# ============================================================

for column, title in [
    (
        "FLAG_OWN_CAR",
        "Default Rate by Car Ownership"
    ),
    (
        "FLAG_OWN_REALTY",
        "Default Rate by Property Ownership"
    )
]:

    data = (
        df.groupby(column)["TARGET"]
        .mean()
        .mul(100)
        .reset_index()
    )

    data.columns = [
        column,
        "Default Rate"
    ]

    fig = px.bar(
        data,
        x=column,
        y="Default Rate",
        title=title,
        text="Default Rate"
    )

    # Show percentage on bars
    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Default Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 🏠 APPLICANTS BY HOUSING TYPE
# ============================================================

data = (
    df["NAME_HOUSING_TYPE"]
    .value_counts()
    .reset_index()
)

data.columns = [
    "Housing Type",
    "Applications"
]

fig = px.bar(
    data,
    x="Housing Type",
    y="Applications",
    title="Applicants by Housing Type",
    text="Applications"
)

# Show application count on bars
fig.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Applications"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 🏠 DEFAULT RATE BY HOUSING TYPE
# ============================================================

data = (
    df.groupby("NAME_HOUSING_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .reset_index()
)

data.columns = [
    "Housing Type",
    "Default Rate"
]

fig = px.bar(
    data,
    x="Housing Type",
    y="Default Rate",
    title="Default Rate by Housing Type",
    text="Default Rate"
)

# Show default rate on bars
fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Default Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 💰 AVERAGE CREDIT BY HOUSING TYPE
# ============================================================

data = (
    df.groupby("NAME_HOUSING_TYPE")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

fig = px.bar(
    data,
    x="NAME_HOUSING_TYPE",
    y="AMT_CREDIT",
    title="Average Credit by Housing Type",
    text="AMT_CREDIT"
)

# Show average credit on bars
fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Average Credit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 📌 HOUSING & ASSET KEY INSIGHTS
# ============================================================

st.markdown("---")

st.subheader(
    "📌 Housing & Asset Key Insights"
)


# ============================================================
# BASIC STATISTICS
# ============================================================

total_customers = len(df)

overall_default_rate = (
    df["TARGET"].mean() * 100
)


# ============================================================
# OWNERSHIP PERCENTAGES
# ============================================================

car_owner_percentage = (
    car_owners /
    total_customers *
    100
    if total_customers
    else 0
)

property_owner_percentage = (
    property_owners /
    total_customers *
    100
    if total_customers
    else 0
)

both_percentage = (
    both /
    total_customers *
    100
    if total_customers
    else 0
)


# ============================================================
# 🚗 CAR DEFAULT RATES
# ============================================================

car_risk = (
    df.groupby("FLAG_OWN_CAR")["TARGET"]
    .mean()
    .mul(100)
)

car_owner_default = car_risk.get(
    "Y",
    0
)

car_non_owner_default = car_risk.get(
    "N",
    0
)


# ============================================================
# 🏡 PROPERTY DEFAULT RATES
# ============================================================

property_risk = (
    df.groupby("FLAG_OWN_REALTY")["TARGET"]
    .mean()
    .mul(100)
)

property_owner_default = (
    property_risk.get(
        "Y",
        0
    )
)

property_non_owner_default = (
    property_risk.get(
        "N",
        0
    )
)


# ============================================================
# 🏠 HOUSING RISK
# ============================================================

housing_risk = (
    df.groupby("NAME_HOUSING_TYPE")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
)

highest_risk_housing = (
    housing_risk.index[0]
)

highest_housing_default = (
    housing_risk.iloc[0]
)

lowest_risk_housing = (
    housing_risk.index[-1]
)

lowest_housing_default = (
    housing_risk.iloc[-1]
)


# ============================================================
# MOST COMMON HOUSING
# ============================================================

housing_counts = (
    df["NAME_HOUSING_TYPE"]
    .value_counts()
)

most_common_housing = (
    housing_counts.index[0]
)

most_common_housing_count = (
    housing_counts.iloc[0]
)


# ============================================================
# 💰 AVERAGE CREDIT BY OWNERSHIP
# ============================================================

car_credit = (
    df.groupby("FLAG_OWN_CAR")[
        "AMT_CREDIT"
    ]
    .mean()
)

property_credit = (
    df.groupby("FLAG_OWN_REALTY")[
        "AMT_CREDIT"
    ]
    .mean()
)


# ============================================================
# 💎 COMBINED ASSET GROUP
# ============================================================

df["ASSET_GROUP"] = "No Assets"


df.loc[
    (df["FLAG_OWN_CAR"] == "Y") &
    (df["FLAG_OWN_REALTY"] == "N"),
    "ASSET_GROUP"
] = "Car Only"


df.loc[
    (df["FLAG_OWN_CAR"] == "N") &
    (df["FLAG_OWN_REALTY"] == "Y"),
    "ASSET_GROUP"
] = "Property Only"


df.loc[
    (df["FLAG_OWN_CAR"] == "Y") &
    (df["FLAG_OWN_REALTY"] == "Y"),
    "ASSET_GROUP"
] = "Car + Property"


# ============================================================
# ASSET RISK
# ============================================================

asset_risk = (
    df.groupby("ASSET_GROUP")["TARGET"]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
)

asset_counts = (
    df["ASSET_GROUP"]
    .value_counts()
)

highest_asset_risk_group = (
    asset_risk.index[0]
)

highest_asset_risk_rate = (
    asset_risk.iloc[0]
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Car Ownership",
    f"{car_owner_percentage:.2f}%"
)

c2.metric(
    "Property Ownership",
    f"{property_owner_percentage:.2f}%"
)

c3.metric(
    "Own Both Assets",
    f"{both_percentage:.2f}%"
)

c4.metric(
    "Overall Default Rate",
    f"{overall_default_rate:.2f}%"
)


# ============================================================
# 💡 INSIGHT CARDS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.info(
        f"🏠 **Most Common Housing Type**\n\n"
        f"**{most_common_housing}** is the most common "
        f"housing type with **{most_common_housing_count:,} "
        f"customers**."
    )

    st.error(
        f"🚨 **Highest-Risk Housing Type**\n\n"
        f"**{highest_risk_housing}** has the highest "
        f"default rate at "
        f"**{highest_housing_default:.2f}%**."
    )

    st.success(
        f"🟢 **Lowest-Risk Housing Type**\n\n"
        f"**{lowest_risk_housing}** has the lowest "
        f"default rate at "
        f"**{lowest_housing_default:.2f}%**."
    )


with col2:

    if car_owner_default > car_non_owner_default:

        st.warning(
            f"🚗 **Car Ownership Risk**\n\n"
            f"Car owners have a default rate of "
            f"**{car_owner_default:.2f}%**, compared "
            f"with **{car_non_owner_default:.2f}%** "
            f"for non-car owners."
        )

    else:

        st.success(
            f"🚗 **Car Ownership Risk**\n\n"
            f"Car owners have a default rate of "
            f"**{car_owner_default:.2f}%**, compared "
            f"with **{car_non_owner_default:.2f}%** "
            f"for non-car owners."
        )


    if property_owner_default > property_non_owner_default:

        st.warning(
            f"🏡 **Property Ownership Risk**\n\n"
            f"Property owners have a default rate of "
            f"**{property_owner_default:.2f}%**, compared "
            f"with **{property_non_owner_default:.2f}%** "
            f"for non-property owners."
        )

    else:

        st.success(
            f"🏡 **Property Ownership Risk**\n\n"
            f"Property owners have a default rate of "
            f"**{property_owner_default:.2f}%**, compared "
            f"with **{property_non_owner_default:.2f}%** "
            f"for non-property owners."
        )


    st.warning(
        f"💎 **Highest-Risk Asset Group**\n\n"
        f"**{highest_asset_risk_group}** has the highest "
        f"default rate at "
        f"**{highest_asset_risk_rate:.2f}%**."
    )


# ============================================================
# 💎 ASSET GROUP ANALYSIS
# ============================================================

st.markdown("---")

st.subheader(
    "💎 Asset Ownership Risk Analysis"
)


asset_summary = (
    df.groupby("ASSET_GROUP")
    .agg(
        Customers=(
            "SK_ID_CURR",
            "count"
        ),
        Default_Rate=(
            "TARGET",
            "mean"
        ),
        Avg_Credit=(
            "AMT_CREDIT",
            "mean"
        ),
        Avg_Income=(
            "AMT_INCOME_TOTAL",
            "mean"
        ),
        Avg_Annuity=(
            "AMT_ANNUITY",
            "mean"
        )
    )
    .reset_index()
)


asset_summary["Default_Rate"] *= 100


# ============================================================
# ASSET SUMMARY TABLE
# ============================================================

st.dataframe(
    asset_summary,
    use_container_width=True
)


# ============================================================
# ASSET GROUP DEFAULT RATE CHART
# ============================================================

fig = px.bar(
    asset_summary,
    x="ASSET_GROUP",
    y="Default_Rate",
    title="Default Rate by Asset Ownership Group",
    text="Default_Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Default Rate (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 🏠 HOUSING RISK TABLE
# ============================================================

st.markdown("---")

st.subheader(
    "🏠 Housing Risk Summary"
)


housing_summary = (
    df.groupby("NAME_HOUSING_TYPE")
    .agg(
        Customers=(
            "SK_ID_CURR",
            "count"
        ),
        Default_Rate=(
            "TARGET",
            "mean"
        ),
        Avg_Credit=(
            "AMT_CREDIT",
            "mean"
        ),
        Avg_Income=(
            "AMT_INCOME_TOTAL",
            "mean"
        )
    )
    .reset_index()
)


housing_summary["Default_Rate"] *= 100


housing_summary = (
    housing_summary
    .sort_values(
        "Default_Rate",
        ascending=False
    )
)


# ============================================================
# HOUSING SUMMARY TABLE
# ============================================================

st.dataframe(
    housing_summary,
    use_container_width=True
)


# ============================================================
# 📝 BUSINESS SUMMARY
# ============================================================

st.markdown("---")

st.subheader(
    "📝 Housing & Asset Summary"
)


st.write(
    f"• The filtered dataset contains "
    f"**{total_customers:,} customers** with an overall "
    f"default rate of **{overall_default_rate:.2f}%**."
)


st.write(
    f"• **{car_owner_percentage:.2f}%** of customers "
    f"own a car, while **{property_owner_percentage:.2f}%** "
    f"own property."
)


st.write(
    f"• **{both_percentage:.2f}%** of customers own "
    f"both a car and property."
)


st.write(
    f"• **{most_common_housing}** is the most common "
    f"housing type."
)


st.write(
    f"• **{highest_risk_housing}** has the highest "
    f"observed housing-related default rate of "
    f"**{highest_housing_default:.2f}%**."
)


st.write(
    f"• The **{highest_asset_risk_group}** asset group "
    f"has the highest observed default rate of "
    f"**{highest_asset_risk_rate:.2f}%**."
)


# ============================================================
# 💡 BUSINESS RECOMMENDATION
# ============================================================

st.markdown(
    "### 💡 Business Recommendation"
)


if (
    highest_housing_default
    > overall_default_rate
):

    st.warning(
        f"🔴 **{highest_risk_housing}** shows a default "
        f"rate above the overall portfolio average. "
        f"This housing segment may require additional "
        f"risk monitoring."
    )

else:

    st.success(
        "🟢 Housing-type default rates are generally "
        "within the overall portfolio range."
    )


if (
    highest_asset_risk_rate
    > overall_default_rate
):

    st.warning(
        f"⚠️ The **{highest_asset_risk_group}** asset "
        f"group has a default rate above the portfolio "
        f"average and could be examined as a separate "
        f"risk segment."
    )

else:

    st.info(
        "📊 Asset ownership groups do not show a "
        "default rate substantially above the overall "
        "portfolio average."
    )


# ============================================================
# NOTE
# ============================================================

st.caption(
    "Note: Housing and asset ownership are observed "
    "associations with default behavior and should not "
    "be interpreted as causal relationships."
)