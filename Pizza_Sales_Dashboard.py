import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback_context

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("pizza_sales.csv")

# -----------------------------
# DATA CLEANING
# -----------------------------
df = df.drop_duplicates()
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df = df.dropna()

# -----------------------------
# DATA PREPROCESSING
# -----------------------------
df["day_name"] = df["order_date"].dt.day_name()
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.month_name()

# -----------------------------
# DASH APP
# -----------------------------
app = Dash(__name__)

app.layout = html.Div([

    html.H1("Pizza Sales Dashboard", style={"textAlign": "center"}),

    # KPI CARDS
    html.Div(id="kpi_cards"),

    # CHARTS
    dcc.Graph(id="daily_chart"),
    dcc.Graph(id="monthly_chart"),
    dcc.Graph(id="category_chart"),
    dcc.Graph(id="size_chart"),
    dcc.Graph(id="funnel_chart"),
    dcc.Graph(id="top_revenue_chart"),
    dcc.Graph(id="top_quantity_chart"),
    dcc.Graph(id="top_orders_chart"),
    dcc.Graph(id="bottom_revenue_chart"),
    dcc.Graph(id="bottom_quantity_chart"),
    dcc.Graph(id="bottom_orders_chart")

])

# -----------------------------
# CALLBACK
# -----------------------------
@app.callback(

[
Output("kpi_cards","children"),
Output("daily_chart","figure"),
Output("monthly_chart","figure"),
Output("category_chart","figure"),
Output("size_chart","figure"),
Output("funnel_chart","figure"),
Output("top_revenue_chart","figure"),
Output("top_quantity_chart","figure"),
Output("top_orders_chart","figure"),
Output("bottom_revenue_chart","figure"),
Output("bottom_quantity_chart","figure"),
Output("bottom_orders_chart","figure")
],

[
Input("category_chart","clickData"),
Input("daily_chart","clickData"),
Input("monthly_chart","clickData")
]

)

def update_dashboard(category_click, day_click, month_click):

    filtered_df = df.copy()

    ctx = callback_context

    if ctx.triggered:

        chart_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # CATEGORY FILTER
        if chart_id == "category_chart" and category_click:
            category = category_click["points"][0]["label"]
            filtered_df = filtered_df[filtered_df["pizza_category"] == category]

        # DAY FILTER
        elif chart_id == "daily_chart" and day_click:
            day = day_click["points"][0]["x"]
            filtered_df = filtered_df[filtered_df["day_name"] == day]

        # MONTH FILTER
        elif chart_id == "monthly_chart" and month_click:
            month = month_click["points"][0]["x"]
            filtered_df = filtered_df[filtered_df["month_name"] == month]

    # -----------------------------
    # KPI CALCULATIONS
    # -----------------------------
    total_revenue = filtered_df["total_price"].sum()
    total_orders = filtered_df["order_id"].nunique()
    total_pizzas_sold = filtered_df["quantity"].sum()

    avg_order_value = total_revenue / total_orders if total_orders else 0
    avg_pizzas_per_order = total_pizzas_sold / total_orders if total_orders else 0

    kpis = html.Div([

        html.Div([
            html.H3("Total Revenue"),
            html.H2(f"${total_revenue:,.2f}")
        ], style={"width":"20%","display":"inline-block","textAlign":"center"}),

        html.Div([
            html.H3("Total Orders"),
            html.H2(total_orders)
        ], style={"width":"20%","display":"inline-block","textAlign":"center"}),

        html.Div([
            html.H3("Total Pizzas Sold"),
            html.H2(total_pizzas_sold)
        ], style={"width":"20%","display":"inline-block","textAlign":"center"}),

        html.Div([
            html.H3("Avg Order Value"),
            html.H2(f"${avg_order_value:.2f}")
        ], style={"width":"20%","display":"inline-block","textAlign":"center"}),

        html.Div([
            html.H3("Avg Pizzas / Order"),
            html.H2(round(avg_pizzas_per_order,2))
        ], style={"width":"20%","display":"inline-block","textAlign":"center"})

    ])

    # -----------------------------
    # CHART DATA
    # -----------------------------
    daily_orders = filtered_df.groupby("day_name")["order_id"].nunique().reset_index()

    daily_orders["day_name"] = pd.Categorical(
        daily_orders["day_name"],
        categories=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        ordered=True
    )

    daily_orders = daily_orders.sort_values("day_name")

    monthly = filtered_df.groupby(["month","month_name"])["order_id"].nunique().reset_index()
    monthly = monthly.sort_values("month")

    category_sales = filtered_df.groupby("pizza_category")["total_price"].sum().reset_index()
    size_sales = filtered_df.groupby("pizza_size")["total_price"].sum().reset_index()

    category_qty = filtered_df.groupby("pizza_category")["quantity"].sum().reset_index()
    category_qty = category_qty.sort_values(by="quantity", ascending=False)

    top_revenue = filtered_df.groupby("pizza_name")["total_price"].sum().reset_index()
    top_revenue = top_revenue.sort_values(by="total_price", ascending=False).head(5)

    top_quantity = filtered_df.groupby("pizza_name")["quantity"].sum().reset_index()
    top_quantity = top_quantity.sort_values(by="quantity", ascending=False).head(5)

    top_orders = filtered_df.groupby("pizza_name")["order_id"].count().reset_index()
    top_orders = top_orders.sort_values(by="order_id", ascending=False).head(5)

    bottom_revenue = filtered_df.groupby("pizza_name")["total_price"].sum().reset_index()
    bottom_revenue = bottom_revenue.sort_values(by="total_price").head(5)

    bottom_quantity = filtered_df.groupby("pizza_name")["quantity"].sum().reset_index()
    bottom_quantity = bottom_quantity.sort_values(by="quantity").head(5)

    bottom_orders = filtered_df.groupby("pizza_name")["order_id"].count().reset_index()
    bottom_orders = bottom_orders.sort_values(by="order_id").head(5)

    # -----------------------------
    # CREATE CHARTS
    # -----------------------------
    fig_daily = px.bar(daily_orders,x="day_name",y="order_id",
                       title="Daily Trend for Total Orders")

    fig_monthly = px.line(monthly,x="month_name",y="order_id",
                          markers=True,
                          title="Monthly Trend for Total Orders")

    fig_category = px.pie(category_sales,
                          values="total_price",
                          names="pizza_category",
                          title="Percentage of Sales by Pizza Category")

    fig_size = px.pie(size_sales,
                      values="total_price",
                      names="pizza_size",
                      title="Percentage of Sales by Pizza Size")

    fig_funnel = px.funnel(category_qty,
                           x="quantity",
                           y="pizza_category",
                           title="Total Pizzas Sold by Category")

    fig_top_revenue = px.bar(top_revenue,
                             x="pizza_name",
                             y="total_price",
                             title="Top 5 Pizzas by Revenue")

    fig_top_quantity = px.bar(top_quantity,
                              x="pizza_name",
                              y="quantity",
                              title="Top 5 Pizzas by Quantity")

    fig_top_orders = px.bar(top_orders,
                            x="pizza_name",
                            y="order_id",
                            title="Top 5 Pizzas by Orders")

    fig_bottom_revenue = px.bar(bottom_revenue,
                                x="pizza_name",
                                y="total_price",
                                title="Bottom 5 Pizzas by Revenue")

    fig_bottom_quantity = px.bar(bottom_quantity,
                                 x="pizza_name",
                                 y="quantity",
                                 title="Bottom 5 Pizzas by Quantity")

    fig_bottom_orders = px.bar(bottom_orders,
                               x="pizza_name",
                               y="order_id",
                               title="Bottom 5 Pizzas by Orders")

    return (kpis, fig_daily, fig_monthly, fig_category, fig_size,
            fig_funnel, fig_top_revenue, fig_top_quantity, fig_top_orders,
            fig_bottom_revenue, fig_bottom_quantity, fig_bottom_orders)

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
