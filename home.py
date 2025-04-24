import altair as alt
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from portfolio import Portfolio

# automatically refresh app every 10 secs
st_autorefresh(interval=10 * 1000)

# init portfolio instance
portfolio = Portfolio()

# write home page title
st.title("Portfolio Dashboard")

# calculate portfolio cumulative returns and generate chart
try:
    cum_ret = portfolio.portfolio_cumulative_return()
    chart_data = cum_ret.reset_index()
    chart_data.columns = ["date", "cumulative return"]
    line_chart = (
        alt.Chart(chart_data)
        .mark_line()
        .encode(
            x=alt.X("date", axis=alt.Axis(format="%b %d", grid=True)),
            y=alt.Y("cumulative return:Q", axis=alt.Axis(format=".0%")),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("cumulative return:Q", title="Return", format=".3%"),
            ],
        )
        .properties(title="Year-To-Date portfolio cumulative returns (%)", height=500)
        .configure_axis(grid=True)
    )
    st.altair_chart(line_chart)
except:
    st.error("Unable to generate cumulative returns chart.")
    st.info("There is no return data available. Your portfolio may currently be empty.")

#  portfolio metrics header
st.header("Portfolio metrics", divider=True)

# update portfolio positions and display portfolio dataframe
portfolio.update_portfolio_positions()
try:
    data = portfolio._generate_portfolio_dataframe()
    if data.empty:
        st.warning(
            "Your portfolio is currently empty. Add some assets to begin tracking performance."
        )
    st.dataframe(
        data=data.drop(columns=["created_date", "last_updated_date"]),
        column_config={
            "ticker": st.column_config.TextColumn(help="Asset ticker"),
            "quantity": st.column_config.NumberColumn(help="Asset quantity owned"),
            "currency": st.column_config.TextColumn(help="Currency of the trade"),
            "transaction_date": st.column_config.TextColumn(
                label="last transaction date", help="Trade execution day"
            ),
            "avg_buy_price": st.column_config.NumberColumn(
                label="average buy price",
                help="Average price paid for a single contract",
            ),
            "cost_basis": st.column_config.NumberColumn(
                label="cost basis",
                help="Total amount invested for the single position",
            ),
            "market_price": st.column_config.NumberColumn(
                label="market price", help="Current market price of the asset"
            ),
            "market_value": st.column_config.NumberColumn(
                label="market value", help="Total market value of the single position"
            ),
            "pl": st.column_config.NumberColumn(label="P&L", help="Profit & Loss"),
            "pl_pct": st.column_config.NumberColumn(
                label="P&L (%)", format="percent", help="P&L percentage"
            ),
        },
        hide_index=True,
        column_order=[
            "ticker",
            "quantity",
            "currency",
            "transaction_date",
            "avg_buy_price",
            "cost_basis",
            "market_price",
            "market_value",
            "pl",
            "pl_pct",
            "created_date",
            "last_updated_date",
        ],
    )
except:
    st.error(f"Failed to load portfolio details.")
    st.info("Ensure assets have been added to the portfolio to view metrics.")

# display portfolio stats, assets correlationa and portfolio allocation
try:
    # correlation data and chart
    correlation_data = portfolio.assets_correlation().reset_index()
    correlation_data = correlation_data.melt(
        "Ticker", var_name="Ticker2", value_name="Correlation"
    )
    correlation_chart = (
        alt.Chart(correlation_data)
        .mark_rect()
        .encode(
            x="Ticker:O",
            y="Ticker2:O",
            color=alt.Color(
                "Correlation:Q", scale=alt.Scale(scheme="redyellowblue", domain=[-1, 1])
            ),
            tooltip=["Ticker", "Ticker2", alt.Tooltip("Correlation:Q", format=".2")],
        )
        .properties(title="Asset Correlaton Matrix", height=400)
    )
    correlation_text = correlation_chart.mark_text(baseline="middle").encode(
        text=alt.Text("Correlation:Q", format=".2f"),
        color=alt.value("black"),
    )
    correlation_chart = correlation_chart + correlation_text

    # composition data and chart
    portfolio_composition = portfolio.assets_weights()
    weights_chart = (
        alt.Chart(portfolio_composition)
        .mark_arc()
        .encode(
            theta="weight",
            color="ticker",
            tooltip=[alt.Tooltip("ticker"), alt.Tooltip("weight:Q", format=".2%")],
        )
        .properties(title="Portfolio Allocation", height=400)
    )
    weights_text = weights_chart.mark_text(
        radius=110, size=12, align="center", baseline="middle"
    ).encode(
        text="ticker:N",
        color=alt.value("black"),
        theta=alt.Theta("weight:Q", stack=True),
    )
    weights_chart = weights_chart + weights_text

    # display stats, correlation and composition into container
    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.dataframe(portfolio.portfolio_stats(), height=353, row_height=45)
        col2.altair_chart(correlation_chart)
        col3.altair_chart(weights_chart)
except:
    st.error(f"Unable to load portfolio insights.")
    st.info(
        "Please ensure your portfolio contains data to generate these visualizations."
    )
