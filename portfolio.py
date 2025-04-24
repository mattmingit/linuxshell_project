from csv import QUOTE_NONE
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from requests.exceptions import RequestException
from yfinance.screener.screener import PREDEFINED_SCREENER_BODY_DEFAULTS

SERVER_BASE_URL = "http://127.0.01:5000"


class Portfolio:
    def __init__(self) -> None:
        """Initializes an empty Portfolio instance"""
        pass

    def _validate_date(self, date: Optional[str] = None) -> str:
        """
        Validate and process date

        Parameters
        ----------
        date : Optional[str]
            The date string in 'YYYY-MM-DD' format. If not provided, uses today's date.

        Returns
        -------
        str
            A validated and properly formatted date string.

        Raises
        ------
        ValueError
            If the date format is incorrect or if the date is in the future.
        """
        if date is None:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {date}. Expected format: %Y-%m-%d")

        if parsed_date > datetime.now():
            raise ValueError(
                f"Invalid date: future date provided: {date} > {datetime.now().strftime('%Y-%m-%d')}"
            )
        return date

    def _get_lastest_price(self, ticker: str) -> float:
        """
        Retrieves the lates closing price of a specified asset using yahoo! finance.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset.

        Returns
        -------
        float
            The most recent closing price.

        Raises
        ------
        ValueError
            If price data retrieval fails.
        """
        try:
            current_data = yf.Ticker(ticker).history(period="1d")
            if current_data.empty:
                raise ValueError(f"price fetch failed for '{ticker}'.")
            price = current_data["Close"].iloc[-1]
            return price
        except Exception as err:
            raise RuntimeError(f"Could not retrieve price for '{ticker}': {str(err)}")

    def _fetch_portfolio_data(self) -> dict:
        """
        Fetches the current portfolio data from the backend server.

        Returns
        -------
        dict
            The portfolio data as JSON object.

        Raises
        ------
        RequestException
            If the server request fails.
        """
        try:
            response = requests.get(f"{SERVER_BASE_URL}/portfolio")
            response.raise_for_status()
            return response.json()
        except RequestException as err:
            raise RequestException(f"Failed to fetch portfolio data: {str(err)}")

    def _fetch_orders_data(self) -> dict:
        """
        Fetches all order data from backend server.

        Returns
        -------
        dict
            The orders data as JSON object.

        Raise
        -----
        RequestException
            If the server request fails.
        """
        try:
            response = requests.get(f"{SERVER_BASE_URL}/orders")
            response.raise_for_status()
            return response.json()
        except RequestException as err:
            raise RequestException(f"Failed to fetch orders data: {str(err)}")

    def _post_to_server(self, endpoint: str, data: dict):
        """
        Internal helper to post JSON data to server and return the JSON sever response

        Parameters
        ----------
        endpoint : str
            The API endpoint.
        data : dict
            The JSON data to send.

        Returns
        -------
        dict
            The server's JSON response.

        Raises
        ------
        RequestException
            If the POST request fails.
        """
        try:
            url = f"{SERVER_BASE_URL}/{endpoint}"
            response = requests.post(url, json=data)
            response.raise_for_status()
            print(f"server response: {response.json()}")
            return response.json()
        except RequestException as err:
            raise RequestException(f"Failed to post data to '{endpoint}': {str(err)}")

    def buy_order(
        self,
        ticker: str,
        quantity: int,
        price: Optional[float] = None,
        date: Optional[str] = None,
        currency: str = "USD",
    ) -> None:
        """
        Executes a buy order for a given asset and updates portfolio state.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset.
        quantity : int
            Number of contracts bought.
        price : Optional[float]
            Purchase price per contract. Fetched from yahoo! finance if not provided.
        date : Optional[datetime]
            Transaction date in 'YYYY-MM-DD' format. Defaults to current date if not provided.
        currency : str
            Currency of the transaction. Defaults to 'USD' (United States Dollar).

        Raises
        ------
        ValueError
            If parameters are invalid.
        RequestException
            If the server communication fails.
        """
        if not ticker:
            raise ValueError("Buy order failed: ticker symbol must not be empty.")

        if price is not None and price < 0:
            raise ValueError(
                f"Buy order failed: price must be a non-negative number: Received: {price}"
            )

        if quantity <= 0:
            raise ValueError(
                f"Buy order failed: quantity must be a positive integer: Received: {quantity}"
            )
        transaction_date = self._validate_date(date)
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if price is None:
            price = self._get_lastest_price(ticker)

        cost_basis = quantity * price

        ticker = ticker.upper()
        currency = currency.upper()
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
            portfolio = self._fetch_portfolio_data()
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

            self._post_to_server("orders", data=order_data)
            self._post_to_server("portfolio", data=portfolio_data)
            print(
                f"Buy order placed: {quantity} contracts of {ticker} at {price:.3f} {currency}"
            )
        except RequestException as err:
            raise RequestException(
                f"Buy order failed: unable to communicate with server: {str(err)}"
            )

    def sell_order(
        self,
        ticker: str,
        quantity: int,
        price: Optional[float] = None,
        date: Optional[str] = None,
        currency: str = "USD",
    ) -> None:
        """
        Executes a sell order for a given asset and updates the portfolio state.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset.
        quantity : int
            Number of contracts sold.
        price : Optional[float]
            Sale price per contract. Fetched from yahoo! finance if not provided.
        date : Optional[datetime]
            Transaction date. Defaults to current date.
        currency : str
            Currency of the transaction. Defaults to 'USD' (United States Dollar).

        Raises
        ------
        ValueError
            If parameters are invalid or the asset is not in the portfolio.
        RequestException
            If server communication fails.
        """
        if not ticker:
            raise ValueError(f"Sell order failed: ticker symbol must not be empty.")

        if price is not None and price < 0:
            raise ValueError(
                f"Sell order failed: price must be a non-negative number: Received: {price}"
            )

        if quantity <= 0:
            raise ValueError(
                f"Sell order failed: quantity must be a positive integer: Received: {quantity}"
            )
        transaction_date = self._validate_date(date)
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if price is None:
            price = self._get_lastest_price(ticker)

        ticker = ticker.upper()
        currency = currency.upper()

        try:
            portfolio = self._fetch_portfolio_data()
            existing_position = next(
                (pos for pos in portfolio if pos["ticker"] == ticker), None
            )

            if not existing_position:
                raise ValueError(
                    f"Sell order failed: no existing position found for ticker '{ticker}'"
                )

            # update existing position
            new_quantity = existing_position["quantity"] - quantity
            if new_quantity < 0:
                raise ValueError(
                    f"Sell order failed: attempting to sell more contracts than currently held ({quantity} > {existing_position['quantity']})."
                )
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

            self._post_to_server("orders", data=order_data)
            self._post_to_server("portfolio", data=portfolio_data)
            print(
                f"Sell order placed: {quantity} contracts of {ticker} at {price:.3f} {currency}"
            )
        except RequestException as err:
            raise RequestException(
                f"Sell order failed: unable to communicate with server: {str(err)}"
            )

    def update_portfolio_positions(self) -> None:
        """
        Updates all assets in the portfolio with the lastest market price, recalculating market value, P&L and P&L percentage.

        Raises
        ------
        RequestException
            If server communication fails.
        """
        last_updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            portfolio = self._fetch_portfolio_data()
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
                self._post_to_server("portfolio", data=portfolio_data)
        except RequestException as err:
            raise RequestException(
                f"Portfolio update failed: unable to communicate with server: {str(err)}"
            )

    def _generate_orders_dataframe(self) -> pd.DataFrame:
        """
        Generates a pandas DataFrame containing order history.

        Returns
        -------
        pd.DataFrame
            DataFrame of order records
        """
        return pd.DataFrame(requests.get(f"{SERVER_BASE_URL}/orders").json())

    def _generate_portfolio_dataframe(self) -> pd.DataFrame:
        """
        Generates a pandas DataFrame containing current portfolio positions.

        Returns
        -------
        pd.DataFrame
            DataFrame of portfolio holdings.
        """
        return pd.DataFrame(requests.get(f"{SERVER_BASE_URL}/portfolio").json())

    def total_cost_basis(self) -> float:
        """
        Calculates the total cost basis of all holdings.

        Returns
        -------
        float
            Sum of cost basis for all assets.
        """
        return self._generate_portfolio_dataframe()["cost_basis"].sum()

    def total_market_value(self) -> float:
        """
        Calculates the current total market value of the portfolio.

        Returns
        -------
        float
            Market value of all assets combined.
        """
        return self._generate_portfolio_dataframe()["market_value"].sum()

    def total_pl(self) -> float:
        """
        Calculates the total P&L of the portfolio.

        Returns
        -------
        float
            Net gain or loss across all holdings.
        """
        return self._generate_portfolio_dataframe()["pl"].sum()

    def assets_weights(self) -> pd.DataFrame:
        """
        Calculates the weight of each asset in the portfolio.

        Returns
        -------
        pd.DataFrame
            DataFrame with tickers and their respective weights in the portfolio.
        """
        df = self._generate_portfolio_dataframe()
        total_value = self.total_market_value()
        weights = round(df["market_value"] / total_value, 3)
        return pd.DataFrame({"ticker": df["ticker"], "weight": weights})

    def portfolio_return(self) -> float:
        """
        Calculates the weighted average return of the portfolio.

        Returns
        -------
        float
            Portfolio return as a weighted average of individual asset returns.
        """
        df = self._generate_portfolio_dataframe()
        weights = self.assets_weights()
        merged = df.merge(weights, on="ticker")
        return round(sum(merged["pl_pct"] * merged["weight"]), 3)

    def annualized_portfolio_volatility(self) -> float:
        """
        Computes annualized volatility of the portfolio.

        Returns
        -------
        float
            Annualized standard deviation of portfolio returns.
        """
        df = self._generate_portfolio_dataframe()
        weights = self.assets_weights()
        tickers = df["ticker"].to_list()
        returns = (
            yf.download(tickers, period="10y", interval="1mo", progress=False)["Close"]
            .pct_change(fill_method=None)
            .dropna()
        )
        cov_matrix = returns.cov()
        vol = np.sqrt(np.dot(weights["weight"], np.dot(cov_matrix, weights["weight"])))
        return round(vol * np.sqrt(12), 3)

    def assets_correlation(self) -> pd.DataFrame:
        """
        Calculate correlation between assets in the portfolio

        Returns
        -------
        pd.DataFrame
            Correlation matrix of asset returns
        """
        tickers = self._generate_portfolio_dataframe()["ticker"].tolist()
        returns = (
            yf.download(tickers, period="10y", interval="1mo", progress=False)["Close"]
            .pct_change(fill_method=None)
            .dropna()
        )
        return returns.corr()

    def portfolio_cumulative_return(self) -> pd.Series:
        """
        Calculate cumulative returns of the portfolio over the past year.

        Returns
        -------
        pd.Series
            Time series of cumulative returns.
        """
        df = self._generate_portfolio_dataframe()
        tickers = df["ticker"].tolist()
        weights = self.assets_weights().set_index("ticker")["weight"]
        returns = (
            yf.download(tickers, period="ytd", interval="1d", progress=False)["Close"]
            .pct_change(fill_method=None)
            .dropna()
        )
        weighted_returns = weights * returns
        portfolio_returns = weighted_returns.sum(axis=1)
        cumulative_returns = (1 + portfolio_returns).cumprod() - 1
        return cumulative_returns

    def portfolio_stats(self) -> pd.DataFrame:
        """
        Caculates some portfolio statistics

        Returns
        -------
        pd.DataFrame
            DataFrame that contains portfolio statistics
        """
        df = self._generate_portfolio_dataframe()
        tickers = df["ticker"].tolist()
        quantity = df[["ticker", "quantity"]]
        df = yf.download(tickers, period="1y", interval="1d", progress=False)["Close"]
        for t in quantity["ticker"]:
            df[t] = df[t] * quantity.loc[quantity["ticker"] == t, "quantity"].values[0]
        df = df.dropna()
        df = df.sum(axis=1)
        result_df = pd.DataFrame(
            {
                "portfolio cost basis": [self.total_cost_basis()],
                "portfolio market value": [self.total_market_value()],
                "portfolio P&L": [self.total_pl()],
                "portfolio return (%)": [self.portfolio_return() * 100],
                "portfolio ann. volatility (%)": [
                    self.annualized_portfolio_volatility() * 100
                ],
                "52wk max value": [max(df)],
                "52wk min value": [min(df)],
            }
        )
        result_df = round(result_df.T, 3)
        result_df.columns = ["stats"]
        return result_df
