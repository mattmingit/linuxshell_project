from time import sleep

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
        label="Insert trade currency", value="USD", placeholder="Currency"
    )
    try:
        if st.button("Submit order"):
            if not all([ticker, quantity, order_type, currency]):
                st.error("All fields except 'Date' and 'Price' are required.")
                return
            if order_type == "BUY":
                portfolio.buy_order(
                    ticker=ticker,
                    quantity=quantity,
                    price=price,
                    date=date,
                    currency=currency,
                )
            elif order_type == "SELL":
                portfolio.sell_order(
                    ticker=ticker,
                    quantity=quantity,
                    price=price,
                    date=date,
                    currency=currency,
                )
            st.success("Order placed successfully!")
            sleep(1)
            st.rerun()
    except ValueError as e:
        st.error(f"Invalid input: {str(e)}")
    except Exception as err:
        st.error(f"Failed to submit order: {str(err)}")


# if place order button is pressed, open order dialog
if st.button("Place order"):
    order_dialog()

# displays order table
st.header("Recent Orders (Last 15)", divider=True)
try:
    data = portfolio._generate_orders_dataframe()
    if data.empty:
        st.warning("No orders found. Start by placing a BUY or SELL order.")
    st.dataframe(
        # data=portfolio._generate_orders_dataframe()
        data=data.drop(columns=["created_date", "last_updated_date", "id"]).tail(15),
        height=563,
        hide_index=True,
        column_order=[
            "id",
            "ticker",
            "transaction_date",
            "order_type",
            "quantity",
            "currency",
            "price",
            "created_date",
            "last_updated_date",
        ],
    )
except Exception as err:
    st.error(f"Unable to load the orders table: {str(err)}")
    st.info("Check if any orders have been recorded.")
