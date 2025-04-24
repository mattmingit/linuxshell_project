import sqlite3

from flask import Flask, jsonify, request

DATABASE = "securities_master.db"

app = Flask(__name__)


def init_db():
    """
    Initialize the database and create tables if they do not exist.
    """
    try:
        with sqlite3.connect(DATABASE) as conn:
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
            print("Database 'securities_master' initialized successfully.")
    except Exception as err:
        raise RuntimeError(f"Failed to initialize database: {str(err)}")


@app.route("/orders", methods=["GET"])
def list_orders():
    """
    Retrieve all orders, sorted by transaction date.
    """
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders ORDER BY transaction_date ASC")
            orders = [dict(row) for row in cur.fetchall()]
            return jsonify(orders), 200
    except Exception as err:
        return jsonify({"error": f"Unable to fetch orders: {str(err)}"}), 500


@app.route("/portfolio", methods=["GET"])
def list_portfolio():
    """
    Retrieve the current state of the portfolio.
    """
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM portfolio")
            portfolio = [dict(row) for row in cur.fetchall()]
            return jsonify(portfolio), 200
    except Exception as err:
        return jsonify({"error": f"Unable to fetch portfolio: {str(err)}"}), 500


@app.route("/orders", methods=["POST"])
def add_order():
    """
    Add a new order to orders table.
    """
    data = request.get_json()
    required_fields = [
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

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return (
            jsonify(
                {
                    "error": "Missing required fields",
                    "details": f"Missing fields: {', '.join(missing_fields)}",
                }
            ),
            400,
        )

    try:
        with sqlite3.connect(DATABASE) as conn:
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
        return jsonify({"error": f"Failed to insert order: {str(err)}"}), 500


@app.route("/portfolio", methods=["POST"])
def update_portfolio():
    """
    Create, update or delete portfolio position.
    """
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
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return (
            jsonify(
                {
                    "error": "Missing required fields",
                    "details": f"Missing fields: {', '.join(missing_fields)}",
                }
            ),
            400,
        )

    try:
        with sqlite3.connect(DATABASE) as conn:
            if data["quantity"] == 0:
                conn.execute(
                    "DELETE FROM portfolio WHERE ticker = ?", (data["ticker"],)
                )
                return (
                    jsonify(
                        {
                            "message": f"Closed {data['ticker']} position. Removed from portfolio."
                        }
                    ),
                    200,
                )
            else:
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
        return jsonify({"error": f"Failed to updated portfolio: {str(err)}"}), 500


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
