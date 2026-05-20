from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger()


def place_market_order(client: BinanceClient, symbol: str, side: str, quantity: float) -> dict:
    """Place a MARKET order."""
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
    }
    logger.info(f"Market order request — symbol={symbol}, side={side}, qty={quantity}")
    return client.place_order(params)


def place_limit_order(
    client: BinanceClient, symbol: str, side: str, quantity: float, price: float
) -> dict:
    """Place a LIMIT order (GTC time-in-force)."""
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": "GTC",
    }
    logger.info(f"Limit order request — symbol={symbol}, side={side}, qty={quantity}, price={price}")
    return client.place_order(params)


def place_stop_market_order(
    client: BinanceClient, symbol: str, side: str, quantity: float, stop_price: float
) -> dict:
    """Place a STOP_MARKET order (bonus order type)."""
    params = {
        "symbol": symbol,
        "side": side,
        "type": "STOP_MARKET",
        "quantity": quantity,
        "stopPrice": stop_price,
    }
    logger.info(
        f"Stop-Market order request — symbol={symbol}, side={side}, qty={quantity}, stopPrice={stop_price}"
    )
    return client.place_order(params)


def format_response(response: dict) -> str:
    """Return a human-readable summary of an order response."""
    lines = [
        "",
        "=" * 50,
        "          ORDER RESPONSE SUMMARY",
        "=" * 50,
        f"  Order ID    : {response.get('orderId', 'N/A')}",
        f"  Symbol      : {response.get('symbol', 'N/A')}",
        f"  Side        : {response.get('side', 'N/A')}",
        f"  Type        : {response.get('type', 'N/A')}",
        f"  Status      : {response.get('status', 'N/A')}",
        f"  Orig Qty    : {response.get('origQty', 'N/A')}",
        f"  Executed Qty: {response.get('executedQty', 'N/A')}",
        f"  Avg Price   : {response.get('avgPrice', response.get('price', 'N/A'))}",
        f"  Time in Force: {response.get('timeInForce', 'N/A')}",
        "=" * 50,
    ]
    return "\n".join(lines)
