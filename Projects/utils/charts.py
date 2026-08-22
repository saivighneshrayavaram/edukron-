import plotly.express as px


# ============================================================
# BAR CHART
# ============================================================

def bar_chart(data, x, y, title):

    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        text=y
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="inside",
        insidetextanchor="middle"
    )

    return fig


# ============================================================
# PIE CHART
# ============================================================

def pie_chart(data, names, values, title):

    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+value"
    )

    return fig


# ============================================================
# DONUT CHART
# ============================================================

def donut_chart(data, names, values, title):

    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title,
        hole=0.5
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+value"
    )

    return fig


# ============================================================
# HISTOGRAM
# ============================================================

def histogram(data, x, title):

    fig = px.histogram(
        data,
        x=x,
        title=title,
        text_auto=True
    )

    fig.update_traces(
        textposition="inside"
    )

    return fig


# ============================================================
# SCATTER CHART
# ============================================================

def scatter_chart(
    data,
    x,
    y,
    color=None,
    title=""
):

    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        title=title
    )

    # Show Y value near each point
    fig.update_traces(
        texttemplate="%{y:.2f}",
        textposition="top center"
    )

    return fig