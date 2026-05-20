#!/usr/bin/env python3
"""
Trading Bot CLI — Binance Futures Testnet
Usage examples are in README.md
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.orders import (
    format_response,
    place_limit_order,
    place_market_order,
    place_stop_market_order,
)
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

load_dotenv()
logger = setup_logger()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  # Market BUY\n"
            "  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001\n\n"
            "  # Limit SELL\n"
            "  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000\n\n"
            "  # Stop-Market SELL (bonus)\n"
            "  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 29000\n"
        ),
    )
    parser.add_argument("--symbol",     required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",       required=True, help="BUY or SELL")
    parser.add_argument("--type",       required=True, dest="order_type", help="MARKET | LIMIT | STOP_MARKET")
    parser.add_argument("--quantity",   required=True, help="Order quantity, e.g. 0.001")
    parser.add_argument("--price",      required=False, default=None, help="Limit price (required for LIMIT orders)")
    parser.add_argument("--stop-price", required=False, default=None, dest="stop_price",
                        help="Stop trigger price (required for STOP_MARKET orders)")
    return parser


def print_request_summary(symbol: str, side: str, order_type: str, quantity: float,
                          price: float = None, stop_price: float = None) -> None:
    print()
    print("=" * 50)
    print("          ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Order Type : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price is not None:
        print(f"  Price      : {price}")
    if stop_price is not None:
        print(f"  Stop Price : {stop_price}")
    print("=" * 50)
    print()


def main():
    parser = build_parser()
    args = parser.parse_args()

    # ── Validate inputs ────────────────────────────────────────────────
    try:
        symbol     = validate_symbol(args.symbol)
        side       = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity   = validate_quantity(args.quantity)

        price      = None
        stop_price = None

        if order_type == "LIMIT":
            if args.price is None:
                parser.error("--price is required for LIMIT orders.")
            price = validate_price(args.price)

        if order_type == "STOP_MARKET":
            if args.stop_price is None:
                parser.error("--stop-price is required for STOP_MARKET orders.")
            stop_price = validate_stop_price(args.stop_price)

    except ValueError as exc:
        logger.error(f"Input validation failed: {exc}")
        print(f"\n❌  Validation error: {exc}\n")
        sys.exit(1)

    # ── Load credentials ───────────────────────────────────────────────
    api_key    = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        msg = (
            "API key/secret not found.\n"
            "Create a .env file with:\n"
            "  BINANCE_API_KEY=your_key\n"
            "  BINANCE_API_SECRET=your_secret\n"
        )
        logger.error(msg)
        print(f"\n❌  {msg}")
        sys.exit(1)

    # ── Print request summary ──────────────────────────────────────────
    print_request_summary(symbol, side, order_type, quantity, price, stop_price)

    # ── Place order ────────────────────────────────────────────────────
    try:
        client = BinanceClient(api_key, api_secret)

        if order_type == "MARKET":
            response = place_market_order(client, symbol, side, quantity)
        elif order_type == "LIMIT":
            response = place_limit_order(client, symbol, side, quantity, price)
        elif order_type == "STOP_MARKET":
            response = place_stop_market_order(client, symbol, side, quantity, stop_price)
        else:
            raise ValueError(f"Unsupported order type: {order_type}")

        print(format_response(response))
        print("\n✅  Order placed successfully!\n")
        logger.info("Order placed successfully.")

    except (ConnectionError, TimeoutError, RuntimeError) as exc:
        logger.error(f"Order failed: {exc}")
        print(f"\n❌  Order failed: {exc}\n")
        sys.exit(1)
    except Exception as exc:
        logger.exception(f"Unexpected error: {exc}")
        print(f"\n❌  Unexpected error: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
