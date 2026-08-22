import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import clean_data
from utils.features import create_features
from utils.filters import apply_sidebar_filters


st.title("⚥ Gender Analysis")


df = load_data()

df = clean_data(df)

df = create_features(df)

df = apply_sidebar_filters(df)


summary = df.groupby("CODE_GENDER").agg(

    Customers=("SK_ID_CURR", "count"),

    Defaults=("TARGET", "sum"),

    Default_Rate=("TARGET", "mean"),

    Avg_Income=("AMT_INCOME_TOTAL", "mean"),

    Avg_Credit=("AMT_CREDIT", "mean"),

    Avg_Annuity=("AMT_ANNUITY", "mean")

).reset_index()


summary["Default_Rate"] *= 100


# ============================================================
# 1. APPLICANTS BY GENDER
# ============================================================

c1, c2 = st.columns(2)


with c1:

    fig = px.bar(
        summary,
        x="CODE_GENDER",
        y="Customers",
        title="Applicants by Gender",
        text="Customers"
    )

    # VALUES INSIDE BAR
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="inside",
        insidetextanchor="middle"
    )

    fig.update_layout(
        uniformtext_minsize=10,
        uniformtext_mode="hide"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 2. DEFAULT CUSTOMERS BY GENDER
# ============================================================

with c2:

    fig = px.bar(
        summary,
        x="CODE_GENDER",
        y="Defaults",
        title="Default Customers by Gender",
        text="Defaults"
    )

    # VALUES INSIDE BAR
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="inside",
        insidetextanchor="middle"
    )

    fig.update_layout(
        uniformtext_minsize=10,
        uniformtext_mode="hide"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# 3. DEFAULT RATE BY GENDER
# ============================================================

fig = px.bar(
    summary,
    x="CODE_GENDER",
    y="Default_Rate",
    title="Default Rate by Gender",
    text="Default_Rate"
)

# VALUES INSIDE BAR
fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 4. AVERAGE INCOME BY GENDER
# ============================================================

fig = px.bar(
    summary,
    x="CODE_GENDER",
    y="Avg_Income",
    title="Average Income by Gender",
    text="Avg_Income"
)

# VALUES INSIDE BAR
fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 5. AVERAGE CREDIT BY GENDER
# ============================================================

fig = px.bar(
    summary,
    x="CODE_GENDER",
    y="Avg_Credit",
    title="Average Credit by Gender",
    text="Avg_Credit"
)

# VALUES INSIDE BAR
fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 6. AVERAGE ANNUITY BY GENDER
# ============================================================

fig = px.bar(
    summary,
    x="CODE_GENDER",
    y="Avg_Annuity",
    title="Average Annuity by Gender",
    text="Avg_Annuity"
)

# VALUES INSIDE BAR
fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# GENDER COMPARISON TABLE
# ============================================================

st.subheader("Gender Comparison Table")

st.dataframe(
    summary,
    use_container_width=True
)