import plotly.express as px
import plotly.graph_objects as go

# -------------------------------
# 📈 Line Chart (Time Series)
# -------------------------------
def plot_time_series(df, date_col, value_col, title="Time Series"):
    fig = px.line(df, x=date_col, y=value_col, title=title)
    return fig


# -------------------------------
# 📊 Bar Chart
# -------------------------------
def plot_bar(df, x_col, y_col, title="Bar Chart"):
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    return fig


# -------------------------------
# 📊 Histogram
# -------------------------------
def plot_histogram(df, col, title="Distribution"):
    fig = px.histogram(df, x=col, nbins=50, title=title)
    return fig


# -------------------------------
# 📦 Box Plot
# -------------------------------
def plot_box(df, col, title="Box Plot"):
    fig = px.box(df, y=col, title=title)
    return fig


# -------------------------------
# 🔗 Correlation Heatmap
# -------------------------------
def plot_correlation(df):
    corr = df.corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )
    return fig


# -------------------------------
# 📈 Forecast Plot
# -------------------------------
def plot_forecast(train, test, pred, future_index, future_pred):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=train.index, y=train, name="Train"))
    fig.add_trace(go.Scatter(x=test.index, y=test, name="Test"))
    fig.add_trace(go.Scatter(x=test.index, y=pred, name="Predicted"))
    fig.add_trace(go.Scatter(x=future_index, y=future_pred, name="Forecast"))

    fig.update_layout(title="Forecast vs Actual")

    return fig