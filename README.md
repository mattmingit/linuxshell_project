<h1 align="center">
    <img src="./assets/linuxshell.png" width="100" alt="linuxshell"/>
    <br/>
    Linuxshell progetto esame
</h1>

<p align="center">
<strong>&#x26A0; Il codice scritto finora e la seguente relazione possono essere oggetto di modifiche in qualsiasi momento. La versione definitiva sará disponibile a progetto concluso.</strong>
</p>

Il presente progetto ha lo scopo di sviluppare un'applicazione in Python per la gestione di un portafoglio finanziario. L'applicazione consente di inserire ordini di acquisto e vendita di strumenti finanziari, tenere traccia delle posizioni aperte e calcolare alcune metriche utili per l'analisi del portfaglio, come il valore totale, il profitto/perdita del portfaglio e la distribuzione degli investimenti.

L'idea nasce con l'intento di applicare le conoscenze acquisite durante il corso di Python. Il progetto è sviluppato in linguaggio **Python**, utilizzando librerie standard e alcune librerie esterne per la _gestione dei dati_, l'_elaborazione numerica_ e la _visualizzazione grafica_.

Le librerie principali utilizzate sono:

- **Pandas**: per la gestione e manipolazione dei dati in formato tabellare;
- **NumPy**: per il calcolo numerico e l'elaborazione di array;
- **sqlite3**: per la gestione e il mantenimento di un database;
- **yfinance**: per ottenere dati finanziari;
- **altair**: per la creazione di grafici e visualizzazioni delle performance;
- **requests** e **jsonify**: per la gestione delle richieste HTTP e la serializzazione dei dati in formato JSON;
- **Flask**: per l'implementazione di un server in grado di dialogare con un client;
- **Streamlit**: per l'implementazione di un'interfaccia grafica per mostrare i dati e interagire facilmente con il server;

Grazie all'integrazione di queste tecnologie, l'applicazione è in grado di eseguire differenti operazioni che vanno dalla raccolta dati, alla loro elaborazione e visualizzazione, fino alla comunicazione tramite API.

### Funzionalità principali

L'applicazione offre una serie di funzionalità progettate per simulare la gestione di un portfoglio finanziario in modo semplice, interattivo e accessibile via web. Le principali funzionalità implementate sono:

1. **inserimento di ordini di acquisto e vendita**: l'utente può registrare _ordini di acquisto_ (**buy**) e _vendita_ (**sell**) specificando il ticker del titolo (es. `AAPL` per Apple), la quantità desiderata, il prezzo, la data dell'operazione di acquisto/vendita e la valuta con cui è stata eseguita la transazione. Gli ordini vengono elaborati dal backend e utilizzati per aggiornare la composizione del portafoglio in tempo reale.

2. **recupero dati di mercato**: attraverso la libreria `yfinance`, l'applicazione recupera informazioni aggiornate sui titoli azionari, tra cui:

   - prezzo corrente;
   - storico dei prezzi.

3. **calcolo delle metriche di portafoglio**: l'applicazione calcola automaticamente alcune delle metriche di portafoglio, tra cui:

   - valore attuale del portafoglio;
   - profitto/perdita (P&L) individuale e complessivo;
   - prezzo medio di carico;
   - distribuzione percentuale del capitale investito.

4. **visualizzazione grafica**: utilizzando `streamlit` come frontend e la libreria `altair`, l'applicazione genera grafici che permettono di visualizzare l'andamento e le metriche di portafoglio.

5. **interfaccia web con architettura client-server**: l'interfaccia utente è realizzata con `streamlit`, che funge da client interattivo. Per la gestione dei dati è stato realizzato un server con `Flask`, il quale gestisce:

   - richieste HTTP inviate dal frontend;
   - recupero, aggiornamento e salvataggio dei dati in un database (_securities_master.db_);
   - invio dei dati al frontend per la visualizzazione.

6. **salvataggio ed esportazione dati**: gli ordini e lo stato del portfaglio vengono salvati in un database, facilitando la persistenza e il caricamento dei dati tra diverse sessioni. Inoltre, grazie a funzionalità _built-in_ di `streamlit`, è possibile esportare i **dati in CSV** per analisi esterne o backup.

### Struttura del progetto

Il progetto è organizzato in modo modulare. Non è stato necessario creare un struttura complessa in quanto si tratta di un progetto semplice e di piccole dimensioni.

Di seguito viene riportata la struttura del progetto con la descrizione dei principali file che lo compongono:

```bash
linuxshell_project
    |- server.py        # Applicazione Flask per la gestione delle API.
    |- portfolio.py     # Gestione del portafoglio (ordini, calcoli, metriche)
    |- securities_master.db # Database per il salvataggio dei dati
    |- home.py          # Home page della web app
    |- orders.py        # Orders page della web app
    |- main.py          # Entrypoint della web app
    |- requirements.txt # Librerie e dependencies del progetto
    |- README.md        # Documentazione principale
```

Descrizione dei file:

- `server.py`: contiene il server Flask che espone gli endpoint per l'interazione con il portafoglio. Riceve richieste dal frontend (`streamlit`), esegue operazioni sul database e restituisce risposte in formato JSON.
- `portfolio.py`: modulo centrale che contiene la classe `Portfolio` nella quale sono implementate le funzioni per la gestione degli ordini, calcolo delle metriche e l'aggiornamento dello stato del portafoglio con i più recenti dati di mercato (grazie a `yfinance`).
- `securities_master.db`: database in cui vengono inseriti i dati riguardanti gli ordini e lo stato del portafoglio. Il database è generato e gestito mediante la libreria `sqlite3`. Il database è composto da due tabelle:
  - `portfolio`: contiene i dati inerenti le varie posizioni che compongono il portafoglio;
  - `orders`: contiene i dati inerenti ogni singolo ordine eseguito dall'utente.
- `home.py`: definisce l'interfaccia grafica della sezione principale della web app.
- `orders.py`: definisce l'interfaccia grafica della sezione riguardante gli ordini del portafoglio.
- `main.py`: funge da entrypoint in cui importare le varie sezioni della web app. Si occupa di eseguire l'app.
- `requirements.txt`: contiene la lista delle principali librerie installate e importate.

### Analisi del codice

Di seguito è riportata un'analisi del codice implementato, suddividendolo per file descriverò i vari componenti di quest'ultimo:

#### `server.py`

Il file `server.py` rappresenta il **backend** dell'applicazione, sviluppato utilizzando `Flask`. Esso espone gli endpoint che consentono al client di interagire con il database SQLite, registrando ordini e aggiornando lo stato del portafoglio. Tutte le operazioni con il database vengono eseguite all'interno di blocchi `with sqlite3.connect()`, che garantiscono la gestione sicura delle connessioni. Inoltre, viene impostata `row_factory` per convertire le righe del database in dizionari Python, in modo da facilitare la conversione in JSON.

Il database è composto da due tabelle:

- `orders`: registra ogni ordine di acquisto o vendita eseguito.
    <details>
    <summary>tabella ordini</summary>

  ```sql
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
  ```

    </details>

- `portfolio`: matiene lo stato attuale del portafoglio, aggiornato dopo ogni operazione.
    <details>
    <summary>tabella portfolio</summary>

  ```sql
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
  ```

    </details>

Entrambe le tabelle vengono create, se non esistono, alla partenza dell'applicazione tramite la funzione `init_db()`.

#### Funzionalità principali del server Flask

- `init_db()`
   <details>
   <summary>codice</summary>

  ```python
  def init_db():
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
           print("securities_master database was initialized correctly")
   except Exception as err:
       raise RuntimeError(f"Failed to init securities_master database: {str(err)}")
  ```

   </details>

  Inizializza il database SQLite e crea le tabelle `portfolio` e `orders` in caso non esistano già. La fuzione è utile per avviare il progetto senza configurazioni manuali iniziali. Mediante il metodo `sqlite3.connect() as conn` si crea la connessione al database e mediante `conn.execute()` vengono eseguite le queries.

- `list_orders()`
  <details>
     <summary>codice</summary>

  ```python
    @app.route("/orders", methods=["GET"])
    def list_orders():
        try:
            with sqlite3.connect(DATABASE) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM orders ORDER BY transaction_date ASC")
                orders = [dict(row) for row in cur.fetchall()]
                return jsonify(orders), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 500
  ```

   </details>

  Recupera e restituisce in formato JSON l’elenco di tutti gli ordini registrati, ordinati per data di transazione. Viene usato dal frontend per visualizzare la cronologia operazioni.

- `list_portfolio()`
  <details>
  <summary>codice</summary>

  ```python
  @app.route("/portfolio", methods=["GET"])
  def list_portfolio():
      try:
          with sqlite3.connect(DATABASE) as conn:
              conn.row_factory = sqlite3.Row
              cur = conn.cursor()
              cur.execute("SELECT * FROM portfolio")
              portfolio = [dict(row) for row in cur.fetchall()]
              return jsonify(portfolio), 200
      except Exception as err:
          return jsonify({"error": str(err)}), 500
  ```

  </details>

  Restituisce lo stato attuale del portafoglio, con tutti i titoli attualmente posseduti. Include dati come quantità, prezzo medio, valore di mercato e P&L.

- `add_order()`
  <details>
  <summary>codice</summary>

  ```python
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
          return jsonify({"error": str(err)}), 500
  ```

  </details>

  Permette di inviare un nuovo ordine (acquisto o vendita) dal frontend. I dati dell'ordine vengono validati e poi inseriti nella tabella del database `orders`.

  Richiede i seguenti campi nel payload della richiesta: `ticker`, `order_type`, `quantity`, `currency`, `transaction_date`, `price`, `transaction_value`, `created_date`, `last_updated_date`

- `update_portfolio()`
   <details>
   <summary>codice</summary>

  ```python
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
             with sqlite3.connect(DATABASE) as conn:
                 if data["quantity"] == 0:
                     conn.execute(
                     "DELETE FROM portfolio WHERE ticker = ?", (data["ticker"],)
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
             return jsonify({"error": str(err)}), 500
  ```

    </details>

  Consente di aggiornare o eliminare (se la quantità è zero) una posizione nel portafoglio. Se il titolo esiste già, i valori vengono sovrascritti con quelli aggiornati.

  Richiede i seguenti campi nel payload della richiesta: `ticker`, `quantity`, `currency`, `transaction_date`, `avg_buy_price`, `cost_basis`, `market_price`, `market_value`, `pl`, `pl_pct`, `created_date`, `last_updated_date`.

- avvio del server
    <details>
    <summary>codice</summary>

  ```python
  if __name__ == "__main__":
      init_db()
      app.run(debug=True)
  ```

    </details>

  Viene eseguita l'inizializzazione del database e avviato il server Flask in modalità debug.

<details>
<summary>codice completo</summary>

```python
import sqlite3
from flask import Flask, jsonify, request

DATABASE = "securities_master.db"

app = Flask(__name__)

def init_db():
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
          print("securities_master database was initialized correctly")
  except Exception as err:
      raise RuntimeError(f"Failed to init securities_master database: {str(err)}")


@app.route("/orders", methods=["GET"])
def list_orders():
  try:
      with sqlite3.connect(DATABASE) as conn:
          conn.row_factory = sqlite3.Row
          cur = conn.cursor()
          cur.execute("SELECT * FROM orders ORDER BY transaction_date ASC")
          orders = [dict(row) for row in cur.fetchall()]
          return jsonify(orders), 200
  except Exception as err:
      return jsonify({"error": str(err)}), 500


@app.route("/portfolio", methods=["GET"])
def list_portfolio():
  try:
      with sqlite3.connect(DATABASE) as conn:
          conn.row_factory = sqlite3.Row
          cur = conn.cursor()
          cur.execute("SELECT * FROM portfolio")
          portfolio = [dict(row) for row in cur.fetchall()]
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
      with sqlite3.connect(DATABASE) as conn:
          if data["quantity"] == 0:
              conn.execute(
                  "DELETE FROM portfolio WHERE ticker = ?", (data["ticker"],)
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
      return jsonify({"error": str(err)}), 500


if __name__ == "__main__":
  init_db()
  app.run(debug=True)
```

</details>

#### `portfolio.py`

Il file `portfolio.py` contiene la classe `Portfolio`. La classe `Portfolio` rappresenta una simulazione di un portafoglio di investimenti, capace di interagire con il server, gestire ordini di acquisto e vendita e calcolare metriche finanziarie.

La classe `Portfolio` viene inizializzata da:

```python
def __init__(self) -> None:
    pass
```

Attualmente il costruttore non ha parametri necessari per l'inizializzazione, ma può essere esteso per includere configurazioni future.

#### Funzionalità principali della classe `Portfolio`

- `buy_order()`
    <details>
    <summary>codice</summary>

  ```python
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
  ```

    </details>

  Simula un ordine di acquisto. Valida gli input inseriti dall'utente. Recupera il prezzo di mercato (mediante `yfinance`) se non fornito. Calcola il `cost_basis` (prezzo$\times$ quantità). Aggiorna o crea una posizione nel portafoglio. Invia l'ordine al server.

- `sell_order()`
    <details>
    <summary>codice</summary>

  ```python
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
          print(f"Sell order of {quantity} for {ticker}: {price:.3f} {currency}")
      except RequestException as err:
          raise RequestException(
              f"Sell order failed: unable to communicate with server: {str(err)}"
          )
  ```

    </details>
    Simula un ordine di vendita. Valid gli input inseriti dall'utente e verifica l'esistenza del titolo nel portafoglio. Calcola la quantità residua e aggiorna la posizione. Se la posizione viene chiusa vendendo tutti i contratti in possesso, azzera i valori. Invia l'ordine al server.

- `update_portfolio_positions()`
    <details>
    <summary>codice</summary>

  ```python
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
  ```

    </details>

  Aggiorna i prezzi di mercato dei vari titoli detenuti e ricalcola le metriche di portafoglio (`valore di mercato` e `P&L`).

- `total_cost_basis()`
    <details>
    <summary>codice</summary>

  ```python
  def total_cost_basis(self) -> float:
      """
      Calculates the total cost basis of all holdings.

      Returns
      -------
      float
          Sum of cost basis for all assets.
      """
      return self._generate_portfolio_dataframe()["cost_basis"].sum()
  ```

    </details>
    Calcola il totale del capitale investito nel portafoglio.

- `total_market_value()`
    <details>
    <summary>codice</summary>

  ```python
  def total_market_value(self) -> float:
      """
      Calculates the current total market value of the portfolio.

      Returns
      -------
      float
          Market value of all assets combined.
      """
      return self._generate_portfolio_dataframe()["market_value"].sum()
  ```

    </details>
    Calcola il controvalore totale di mercato del portafoglio.

- `total_pl()`
    <details>
    <summary>codice</summary>

  ```python
  def total_pl(self) -> float:
      """
      Calculates the total P&L of the portfolio.

      Returns
      -------
      float
          Net gain or loss across all holdings.
      """
      return self._generate_portfolio_dataframe()["pl"].sum()
  ```

    </details>
    Calcola il profitto/perdita (P&L) totale del portafoglio.

- `assets_weights()`
    <details>
    <summary>codice</summary>

  ```python
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
      weights = df["market_value"] / total_value
      return pd.DataFrame({"ticker": df["ticker"], "weight": weights})
  ```

    </details>

  Calcola il peso relativo di ogni asset e restituisce un `DataFrame` composto dai `ticker` e i rispettivi pesi (`weights`).

- `portfolio_return()`
    <details>
    <summary>codice</summary>

  ```python
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
  ```

    </details>

  Calcola il rendimento medio ponderato del portafoglio.

- `annualized_portfolio_volatility()`
    <details>
    <summary>codice</summary>

  ```python
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
          yf.download(tickers, period="10y", interval="1mo")["Close"]
          .pct_change(fill_method=None)
          .dropna()
      )
      cov_matrix = returns.cov()
      vol = np.sqrt(np.dot(weights["weight"], np.dot(cov_matrix, weights["weight"])))
      return round(vol * np.sqrt(12), 3)
  ```

    </details>

  Calcola la volatilità annualizzata stimata.

- `assets_correlation()`
    <details>
    <summary>codice</summary>

  ```python
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
          yf.download(tickers, period="10y", interval="1mo")["Close"]
          .pct_change(fill_method=None)
          .dropna()
      )
      return returns.corr()
  ```

    </details>

  Calcola la correlazione tra gli asset.

- `portfolio_cumulative_return()`
    <details>
    <summary>codice</summary>

  ```python
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
          yf.download(tickers, period="1y", interval="1d")["Close"]
          .pct_change(fill_method=None)
          .dropna()
      )
      weighted_returns = weights * returns
      portfolio_returns = weighted_returns.sum(axis=1)
      cumulative_returns = (1 + portfolio_returns).cumprod() - 1
      return cumulative_returns
  ```

    </details>

    Restituisce la serie storica dei rendimenti cumulativi giornalieri dell'ultimo anno.

La classe `Portfolio` possiede, inoltre, alcune funzioni "helper" (sono caratterizzate dal `_` che precede il loro nome, consistono in funzioni interne non accessibili utilizzate per "aiutare" le funzioni principali).
Queste sono:
- `_validate_date`: verifica che la data fornita sia nel formato corretto (`YYYY-MM-DD`) e non sia nel futuro.
- `_get_latest_price`: ottiene il prezzo di chiusura più recente grazie alla libreria `yfinance`.
- `_fetch_portfolio_data`, `_fetch_orders_data`: ottengono i dati di portafoglio e degli ordini dal backend.
- `_post_to_server`: invia i dati al server.

<details>
<summary>codice completo</summary>

```python
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from requests.exceptions import RequestException

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
            print(f"Sell order of {quantity} for {ticker}: {price:.3f} {currency}")
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
        df = pd.DataFrame(requests.get(f"{SERVER_BASE_URL}/orders").json())
        df = df[
            [
                "id",
                "ticker",
                "transaction_date",
                "order_type",
                "quantity",
                "currency",
                "price",
                "created_date",
                "last_updated_date",
            ]
        ]
        return df

    def _generate_portfolio_dataframe(self) -> pd.DataFrame:
        """
        Generates a pandas DataFrame containing current portfolio positions.

        Returns
        -------
        pd.DataFrame
            DataFrame of portfolio holdings.
        """
        df = pd.DataFrame(requests.get(f"{SERVER_BASE_URL}/portfolio").json())
        df = df[
            [
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
        ]
        return df

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
        weights = df["market_value"] / total_value
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
            yf.download(tickers, period="10y", interval="1mo")["Close"]
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
            yf.download(tickers, period="10y", interval="1mo")["Close"]
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
            yf.download(tickers, period="1y", interval="1d")["Close"]
            .pct_change(fill_method=None)
            .dropna()
        )
        weighted_returns = weights * returns
        portfolio_returns = weighted_returns.sum(axis=1)
        cumulative_returns = (1 + portfolio_returns).cumprod() - 1
        return cumulative_returns
```

</details>

<p align="center">
<strong>&#x26A0; Il codice scritto finora e la seguente relazione possono essere oggetto di modifiche in qualsiasi momento. La versione definitiva sarà disponibile a progetto concluso.</strong>
</p>
