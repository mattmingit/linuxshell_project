import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


def init_db():
    try:
        with sqlite3.connect("securities_master.db") as conn:
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker VARCHAR(32) NOT NULL,
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
        print("securities_master database was initialized correctly")
    except Exception as err:
        raise RuntimeError(f"Failed to init securities_master database: {str(err)}")


@app.route("/orders", methods=["GET"])
def list_orders():
    try:
        with sqlite3.connect("securities_master.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders ORDER BY transaction_date ASC")
            # orders = cur.fetchall()
            orders = [dict(row) for row in cur.fetchall()]
            # return jsonify(dict(row) for row in orders), 200
            return jsonify(orders), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@app.route("/portfolio", methods=["GET"])
def list_portfolio():
    try:
        with sqlite3.connect("securities_master.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM portfolio")
            # portfolio = cur.fetchall()
            portfolio = [dict(row) for row in cur.fetchall()]
            # return jsonify(dict(row) for row in portfolio), 200
            return jsonify(portfolio), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@app.route("/orders", methods=["POST"])
def add_order():
    data = request.get_json()
    required_fileds = [
        "ticker",
        "order_type",
        "quantity",
        "currency",
        "transaction_date",
        "price",
        "transaction_value",
        "created_date",
        "last_updated_date",
    ]
    if not all(field in data for field in required_fileds):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        with sqlite3.connect("securities_master.db") as conn:
            conn.execute(
                """
            INSERT OR REPLACE INTO orders 
            (ticker, order_type, quantity, currency, transaction_date, price, transaction_value, created_date, last_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    data["ticker"],
                    data["order_type"],
                    data["quantity"],
                    data["currency"],
                    data["transaction_date"],
                    data["price"],
                    data["transaction_value"],
                    data["created_date"],
                    data["last_updated_date"],
                ),
            )
        return jsonify({"message": "Order added successfully"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@app.route("/portfolio", methods=["POST"])
def update_portfolio():
    data = request.get_json()
    required_fields = [
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
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"error", "Missing required fields"}), 400

    try:
        with sqlite3.connect("securities_master.db") as conn:
            conn.execute(
                """
            INSERT OR REPLACE INTO portfolio 
            (ticker, quantity, currency, transaction_date, avg_buy_price, cost_basis, market_price, market_value, pl, pl_pct, created_date, last_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    data["ticker"],
                    data["quantity"],
                    data["currency"],
                    data["transaction_date"],
                    data["avg_buy_price"],
                    data["cost_basis"],
                    data["market_price"],
                    data["market_value"],
                    data["pl"],
                    data["pl_pct"],
                    data["created_date"],
                    data["last_updated_date"],
                ),
            )
        return jsonify({"message": "Portfolio updated successfully"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
