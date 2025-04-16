import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


def init_db():
    with sqlite3.connect("securities_master.db") as conn:
        conn.execute(
            """
        CREATE TABLE IF NOT EXISTS orders (
            ticker VARCHAR(32) NOT NULL PRIMARY KEY,
            order_type VARCHAR(32) NOT NULL,
            quantity INTEGER NOT NULL,
            currency VARCHAR(32) NOT NULL,
            transaction_date DATE NOT NULL,
            price DECIMAL(19, 3),
            transaction_value DECIMAL(19, 3),
            created_date DATETIME NOT NULL,
            last_updated_date DATETIME NOT NULL 
        )
        """
        )
        conn.execute(
            """
        CREATE TABLE IF NOT EXISTS portfolio (
            ticker VARCHAR(32) NOT NULL PRIMARY KEY,
            quantity INTEGER NOT NULL,
            currency VARCHAR(32) NOT NULL,
            transaction_date DATE NOT NULL,
            avg_buy_price DECIMAL(19, 3) NOT NULL,
            cost_basis DECIMAL(19, 3) NOT NULL,
            market_price DECIMAL(19, 3),
            market_value DECIMAL(19, 3),
            pl DECIMAL(19, 3),
            pl_pct DECIMAL(19, 3),
            created_date DATETIME NOT NULL,
            last_updated_date DATETIME NOT NULL
        )
        """
        )


@app.route("/orders", methods=["GET"])
def list_orders():
    with sqlite3.connect("securities_master.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders ORDER BY transaction_date ASC")
        orders = cur.fetchall()
        return jsonify(orders)


@app.route("/portfolio", methods=["GET"])
def list_portfolio():
    with sqlite3.connect("securities_master.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM portfolio")
        portfolio = cur.fetchall()
        return portfolio


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
