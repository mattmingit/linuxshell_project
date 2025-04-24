import streamlit as st

from portfolio import Portfolio

portfolio = Portfolio()

# set page config
st.set_page_config(
    page_title="Portfolio management",
    layout="wide",
    page_icon="./assets/linuxshell.png",
)

# call and display the home page
home = st.Page("home.py", title="Home", icon=":material/home:")

# call and display the orders page
orders = st.Page("orders.py", title="Orders", icon=":material/list:")

# set app navigation
pg = st.navigation([home, orders])

# run app
pg.run()
