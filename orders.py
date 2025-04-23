import streamlit as st

from portfolio import Portfolio

portfolio = Portfolio()
st.title("Orders dashboard")


@st.dialog("Order dialog")
def order_dialog():
    """
    Generate the dialog to insert a new order
    """
    st.write("Place an order")
    ticker = st.text_input(label="Insert ticker", placeholder="Ticker")
    quantity = int(
        st.number_input(
            label="Insert quantity", placeholder="Quantity", value=0, min_value=0
        )
    )
    price = st.number_input(label="Insert price", placeholder="Price", value=None)
    date = st.text_input(
        label="Insert date", placeholder="Date (YYYY-MM-DD)", value=None
    )
    order_type = st.selectbox(
        label="Insert order type",
        index=None,
        placeholder="Order type (BUY-SELL)",
        options=("BUY", "SELL"),
    )
    currency = st.text_input(
        label="Inser trade currency", value="USD", placeholder="Currency"
    )
    if st.button("Submit order"):
        if order_type == "BUY":
            portfolio.buy_order(
                ticker=ticker,
                quantity=quantity,
                price=price,
                date=date,
                currency=currency,
            )
            st.rerun()
        elif order_type == "SELL":
            portfolio.sell_order(
                ticker=ticker,
                quantity=quantity,
                price=price,
                date=date,
                currency=currency,
            )
            st.rerun()


# if place order button is pressed, open order dialog
if st.button("Place order"):
    order_dialog()

# displays order table
st.dataframe(
    data=portfolio._generate_orders_dataframe().drop(
        columns=["created_date", "last_updated_date", "id"]
    ),
    height=500,
)
