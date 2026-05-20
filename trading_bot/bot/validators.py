from bot.logging_config import setup_logger

logger = setup_logger()

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s:
        raise ValueError("Symbol cannot be empty.")
    if not s.isalpha():
        raise ValueError(f"Symbol '{s}' must contain only letters (e.g. BTCUSDT).")
    logger.debug(f"Symbol validated: {s}")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValueError(f"Side '{s}' is invalid. Choose from: {', '.join(VALID_SIDES)}.")
    logger.debug(f"Side validated: {s}")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type '{t}' is invalid. Choose from: {', '.join(VALID_ORDER_TYPES)}.")
    logger.debug(f"Order type validated: {t}")
    return t


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except (ValueError, TypeError):
        raise ValueError(f"Quantity '{quantity}' must be a number (e.g. 0.001).")
    if q <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {q}")
    logger.debug(f"Quantity validated: {q}")
    return q


def validate_price(price: str) -> float:
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValueError(f"Price '{price}' must be a number (e.g. 30000.5).")
    if p <= 0:
        raise ValueError(f"Price must be greater than 0. Got: {p}")
    logger.debug(f"Price validated: {p}")
    return p


def validate_stop_price(stop_price: str) -> float:
    try:
        sp = float(stop_price)
    except (ValueError, TypeError):
        raise ValueError(f"Stop price '{stop_price}' must be a number.")
    if sp <= 0:
        raise ValueError(f"Stop price must be greater than 0. Got: {sp}")
    logger.debug(f"Stop price validated: {sp}")
    return sp
