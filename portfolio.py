from datetime import datetime
from typing import Optional

import pandas as pd
import requests
import yfinance as yf
from requests.exceptions import RequestException

server_base_url = "http://127.0.01:5000"


class Portfolio:
    def __init__(self) -> None:
        # self.positions = self.initialize_portfolio_dataframe()
        # self.orders = self.initialize_orders_dataframe()
        pass

    def _validate_date(self, date: Optional[str] = None) -> str:  # tuple[str, str]:
        """
        Validate and process date

        Parameters
        ----------
        date : str
            The date to process
        """
        if date is None:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"Invalid date format: current format: {date}, allowed format: %Y-%m-%d"
            )

        if parsed_date > datetime.now():
            raise ValueError(
                f"Invalid date: the provided date is in the future: {date} > {datetime.now().strftime('%Y-%m-%d')}"
            )
        return date

    def _get_lastest_price(self, ticker: str) -> float:
        """
        Get the latest price of an asset

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset
        """
        try:
            current_data = yf.Ticker(ticker).history(period="1d")
            if current_data.empty:
                raise ValueError(f"price fetch failed for '{ticker}'.")
            price = current_data["Close"].iloc[-1]
            return price
        except Exception as err:
            raise ValueError(f"price fetch failed for '{ticker}': {str(err)}")

    def buy_order(
        self,
        ticker: str,
        quantity: int,
        price: Optional[float] = None,
        date: Optional[str] = None,
        currency: str = "USD",
    ):
        """
        Insert a buy order

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset
        quantity : int
            The number of contracts traded in the transaction
        price : float
            The price of the asset during the trade. If not provided it is obtained from yahoo! finance
        date : datetime
            The date of the trade. If not provided it is set to datetime.now (current datetime)
        currency : str
            The currency used in the transaction. It defaults to USD (United States Dollar)
        """
        if not ticker:
            raise ValueError("buy order failed: ticker symbol is required")

        if price is not None and price < 0:
            raise ValueError(
                f"buy order failed: price must be positive: invalid price: {price}"
            )

        if quantity <= 0:
            raise ValueError(
                f"buy order failed: quantity must be a positive number greater than zero: invalid quantity: {quantity}"
            )
        transaction_date = self._validate_date(date)
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if price is None:
            price = self._get_lastest_price(ticker)
        elif price < 0:
            raise ValueError(
                f"buy order failed: price must be a positive number: invalid price: {price}"
            )

        cost_basis = quantity * price

        order_data = {
            "ticker": ticker,
            "order_type": "BUY",
            "quantity": quantity,
            "currency": currency,
            "transaction_date": transaction_date,
            "price": round(price, 3),
            "transaction_value": round(cost_basis, 3),
            "created_date": created_date,
            "last_updated_date": created_date,
        }

        try:
            # checks if we already own the asset
            response = requests.get(f"{server_base_url}/portfolio")
            portfolio = response.json()
            existing_position = next(
                (pos for pos in portfolio if pos["ticker"] == ticker), None
            )
            if existing_position:
                new_quantity = existing_position["quantity"] + quantity
                new_cost_basis = existing_position["cost_basis"] + cost_basis
                new_avg_buy_price = new_cost_basis / new_quantity
                market_price = self._get_lastest_price(ticker)
                market_value = new_quantity * market_price
                portfolio_data = {
                    "ticker": ticker,
                    "quantity": new_quantity,
                    "currency": currency,
                    "transaction_date": transaction_date,
                    "avg_buy_price": round(new_avg_buy_price, 3),
                    "cost_basis": round(new_cost_basis, 3),
                    "market_price": round(market_price, 3),
                    "market_value": round(market_value, 3),
                    "pl": round(market_value - new_cost_basis, 3),
                    "pl_pct": round(((market_value / new_cost_basis) - 1), 6),
                    "created_date": existing_position["created_date"],
                    "last_updated_date": created_date,
                }
            else:
                portfolio_data = {
                    "ticker": ticker,
                    "quantity": quantity,
                    "currency": currency,
                    "transaction_date": transaction_date,
                    "avg_buy_price": round(price, 3),
                    "cost_basis": round(cost_basis, 3),
                    "market_price": round(price, 3),
                    "market_value": round(cost_basis, 3),
                    "pl": 0.0,
                    "pl_pct": 0.0,
                    "created_date": created_date,
                    "last_updated_date": created_date,
                }

            response = requests.post(f"{server_base_url}/orders", json=order_data)
            if response.status_code != 200:
                raise ValueError(f"failed to insert buy order: {response.text}")
            print(f"Server response: {response.json()}")
            response = requests.post(
                f"{server_base_url}/portfolio", json=portfolio_data
            )
            if response.status_code != 200:
                raise ValueError(f"failed to update portfolio: {response.text}")
            print(f"Server response: {response.json()}")
            print(f"Buy order of {quantity} for {ticker}: {price:.3f} {currency}")
        except RequestException as err:
            raise RequestException(f"failed to communicate with server: {str(err)}")

    def sell_order(
        self,
        ticker: str,
        quantity: int,
        price: Optional[float] = None,
        date: Optional[str] = None,
        currency: str = "USD",
    ):
        """
        Insert a sell order

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset
        quantity : int
            The number of contracts traded in the transaction
        price : float
            The price of the asset during the trade. If not provided it is obtained from yahoo! finance
        date : datetime
            The date of the trade. If not provided it is set to datetime.now (current datetime)
        currency : str
            The currency used in the transaction. It defaults to USD (United States Dollar)
        """
        if not ticker:
            raise ValueError(f"sell order failed: ticker symbol is required.")

        if price is not None and price < 0:
            raise ValueError(
                f"sell order failed: price must be positive: invalid price: {price}"
            )

        if quantity <= 0:
            raise ValueError(
                f"sell order failed: quantity must be a positive number greater than zero: invalid quantity: {quantity}"
            )
        transaction_date = self._validate_date(date)
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if price is None:
            price = self._get_lastest_price(ticker)
        elif price < 0:
            raise ValueError(
                f"buy order failed: price must be a positive number: invalid price: {price}"
            )

        try:
            response = requests.get(f"{server_base_url}/portfolio")
            portfolio = response.json()
            existing_position = next(
                (pos for pos in portfolio if pos["ticker"] == ticker), None
            )

            if existing_position:
                # update existing position
                new_quantity = existing_position["quantity"] - quantity
                cost_basis = quantity * existing_position["avg_buy_price"]
                order_data = {
                    "ticker": ticker,
                    "order_type": "SELL",
                    "quantity": quantity,
                    "currency": currency,
                    "transaction_date": transaction_date,
                    "price": round(price, 3),
                    "transaction_value": round(price * quantity, 3),
                    "created_date": created_date,
                    "last_updated_date": created_date,
                }
                if new_quantity > 0:
                    new_cost_basis = existing_position["cost_basis"] - cost_basis
                    new_avg_buy_price = new_cost_basis / new_quantity
                    market_value = new_quantity * price
                    portfolio_data = {
                        "ticker": ticker,
                        "quantity": new_quantity,
                        "currency": currency,
                        "transaction_date": transaction_date,
                        "avg_buy_price": round(new_avg_buy_price, 3),
                        "cost_basis": round(new_cost_basis, 3),
                        "market_price": round(price, 3),
                        "market_value": round(market_value, 3),
                        "pl": round(market_value - new_cost_basis, 3),
                        "pl_pct": round(((market_value / new_cost_basis) - 1), 6),
                        "created_date": existing_position["created_date"],
                        "last_updated_date": created_date,
                    }
                else:
                    portfolio_data = {
                        "ticker": ticker,
                        "quantity": new_quantity,
                        "currency": currency,
                        "transaction_date": transaction_date,
                        "avg_buy_price": 0.0,
                        "cost_basis": 0.0,
                        "market_price": 0.0,
                        "market_value": 0.0,
                        "pl": 0.0,
                        "pl_pct": 0.0,
                        "created_date": existing_position["created_date"],
                        "last_updated_date": created_date,
                    }
            else:
                raise ValueError(
                    f"sell order failed: no existing position found for ticker {ticker}."
                )

            response = requests.post(f"{server_base_url}/orders", json=order_data)
            if response.status_code != 200:
                raise ValueError(f"failed to insert buy order: {response.text}")
            print(f"Server response: {response.json()}")
            response = requests.post(
                f"{server_base_url}/portfolio", json=portfolio_data
            )
            if response.status_code != 200:
                raise ValueError(f"failed to update portfolio: {response.text}")
            print(f"Server response: {response.json()}")
            print(f"Sell order of {quantity} for {ticker}: {price:.3f} {currency}")
        except RequestException as err:
            raise RequestException(f"failed to communicate with server: {str(err)}")

    def update_portfolio_positions(self):
        """
        Update portfolio positions obtaining latest market price and updating market value, P&L and P&L percentage
        """
        last_updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            response = requests.get(f"{server_base_url}/portfolio")
            portfolio = response.json()
            for position in portfolio:
                ticker = position["ticker"]
                market_price = self._get_lastest_price(ticker)
                market_value = position["quantity"] * market_price
                portfolio_data = {
                    "ticker": ticker,
                    "quantity": position["quantity"],
                    "currency": position["currency"],
                    "transaction_date": position["transaction_date"],
                    "avg_buy_price": position["avg_buy_price"],
                    "cost_basis": position["cost_basis"],
                    "market_price": round(market_price, 3),
                    "market_value": round(market_value, 3),
                    "pl": round(market_value - position["cost_basis"], 3),
                    "pl_pct": round(((market_value / position["cost_basis"]) - 1), 6),
                    "created_date": position["created_date"],
                    "last_updated_date": last_updated_date,
                }
                response = requests.post(
                    f"{server_base_url}/portfolio", json=portfolio_data
                )
                if response.status_code != 200:
                    raise ValueError(f"failed to update portfolio: {response.text}")
                print(
                    f"Updated position for {ticker}; server response: {response.json()}"
                )
        except RequestException as err:
            raise RequestException(f"failed to communicate with server: {str(err)}")

    def total_cost_basis(self):
        """
        Calculates the total value invested in the portfolio
        """
        response = requests.get(f"{server_base_url}/portfolio")
        df = pd.DataFrame(response.json())
        return df["cost_basis"].sum()

    def total_market_value(self):
        """
        Calculates the total market value of the portfolio
        """
        response = requests.get(f"{server_base_url}/portfolio")
        df = pd.DataFrame(response.json())
        return df["market_value"].sum()

    def total_pl(self):
        """
        Calculates the total P&L of the portfolio
        """
        response = requests.get(f"{server_base_url}/portfolio")
        df = pd.DataFrame(response.json())
        return df["pl"].sum()

    def assets_weights(self):
        """
        Calculates weights for each asset and returns a dataframe that contains two columns: ticker and weights
        """
        response = requests.get(f"{server_base_url}/portfolio")
        df = pd.DataFrame(response.json())
        total_market_val = self.total_market_value()
        weights = df["market_value"] / total_market_val
        return pd.DataFrame({"ticker": df["ticker"], "weight": weights})

    def portfolio_return(self):
        """
        Calculates portfolio return
        """
        response = requests.get(f"{server_base_url}/portfolio")
        df = pd.DataFrame(response.json())
        w = self.assets_weights()
        new_df = df.merge(w, on="ticker")
        return round(sum(new_df["pl_pct"] * new_df["weight"]), 3)
