import altair as alt
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from portfolio import Portfolio

# automatically refresh app every 10 secs
st_autorefresh(interval=10 * 1000)

# init portfolio instance
portfolio = Portfolio()

# write home page title
st.title("Portfolio dashboard")

# calculate portfolio cumulative returns and generate chart
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
    .properties(title="portfolio cumulative returns (%)", height=500)
    .configure_axis(grid=True)
)
st.altair_chart(line_chart)

# update portfolio positions and display portfolio dataframe
portfolio.update_portfolio_positions()
st.dataframe(
    data=portfolio._generate_portfolio_dataframe().drop(
        columns=["created_date", "last_updated_date"]
    ),
    column_config={
        "ticker": st.column_config.TextColumn(help="Asset ticker"),
        "quantity": st.column_config.NumberColumn(help="Asset quantity owned"),
        "currency": st.column_config.TextColumn(help="Currency of the trade"),
        "transaction_date": st.column_config.TextColumn(help="Trade execution day"),
        "avg_buy_price": st.column_config.NumberColumn(
            help="Average price paid for a single contract"
        ),
        "cost_basis": st.column_config.NumberColumn(
            help="Total amount invested for the single position"
        ),
        "market_price": st.column_config.NumberColumn(
            help="Current market price of the asset"
        ),
        "market_value": st.column_config.NumberColumn(
            help="Total market value of the single position"
        ),
        "pl": st.column_config.NumberColumn(help="Profit & Loss"),
        "pl_pct": st.column_config.NumberColumn(
            format="percent", help="P&L percentage"
        ),
    },
)

# TODO: display portfolio metrics and portfolio composition
