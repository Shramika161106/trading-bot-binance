# Trading Bot — Binance Futures Testnet (USDT-M)

A lightweight Python CLI application to place **MARKET**, **LIMIT**, and **STOP_MARKET** orders on Binance Futures Testnet. Structured with a clean client/API layer, full logging, and robust input validation.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # Package marker
│   ├── client.py            # Binance REST API wrapper (signing, HTTP)
│   ├── orders.py            # Order placement logic + response formatter
│   ├── validators.py        # Input validation functions
│   └── logging_config.py   # Logging setup (file + console)
├── logs/                    # Auto-created; contains daily .log files
├── cli.py                   # CLI entry point (argparse)
├── .env.example             # Template for API credentials
├── requirements.txt
└── README.md
```

---

## Setup Steps

### 1 — Get Binance Futures Testnet credentials

1. Go to **https://testnet.binancefuture.com**
2. Click **"Log In with GitHub"** (or register)
3. Once logged in, go to **API Key** section (top-right menu)
4. Click **"Generate Key"** — copy the **API Key** and **Secret Key** immediately (the secret is shown only once)

### 2 — Install Python dependencies

Make sure you have Python 3.8 or newer installed, then run:

```bash
# (Optional but recommended) create a virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3 — Set up your API credentials

```bash
# Copy the example file
cp .env.example .env
```

Open `.env` in any text editor and replace the placeholder values:

```
BINANCE_API_KEY=paste_your_api_key_here
BINANCE_API_SECRET=paste_your_secret_key_here
```

---

## How to Run

All commands are run from inside the `trading_bot/` folder.

### Place a MARKET order

```bash
# BUY 0.001 BTC at market price
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# SELL 0.001 BTC at market price
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### Place a LIMIT order

```bash
# BUY 0.001 BTC at limit price 50000 USDT
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000

# SELL 0.001 BTC at limit price 100000 USDT
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000
```

### Place a STOP_MARKET order (Bonus)

```bash
# Sell 0.001 BTC if price drops to 29000
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 29000
```

### See all options

```bash
python cli.py --help
```

---

## Sample Output

```
==================================================
          ORDER REQUEST SUMMARY
==================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Order Type : MARKET
  Quantity   : 0.001
==================================================

==================================================
          ORDER RESPONSE SUMMARY
==================================================
  Order ID    : 3280557246
  Symbol      : BTCUSDT
  Side        : BUY
  Type        : MARKET
  Status      : FILLED
  Orig Qty    : 0.001
  Executed Qty: 0.001
  Avg Price   : 65123.40
  Time in Force: GTC
==================================================

✅  Order placed successfully!
```

---

## Log Files

Logs are written automatically to `logs/trading_bot_YYYYMMDD.log`.

Each log entry records:
- Outgoing API request parameters
- Raw HTTP response
- Validation steps
- Errors with full context

Log files from test runs are included in the `logs/` folder of this submission.

---

## Assumptions

- Only **USDT-M Futures Testnet** is targeted (`https://testnet.binancefuture.com`).
- Minimum quantity for BTCUSDT on testnet is **0.001 BTC**.
- LIMIT orders use **GTC** (Good Till Cancelled) time-in-force by default.
- Credentials are stored in a local `.env` file (never hard-coded).
- No position or balance checks are performed before order placement; the Binance API returns a clear error if funds are insufficient.

---

## Bonus Features Implemented

- ✅ **STOP_MARKET** order type (third order type beyond MARKET and LIMIT)
- ✅ **Structured validation** with descriptive error messages for every field
- ✅ **Dual logging** — console (INFO+) and file (DEBUG+) simultaneously
