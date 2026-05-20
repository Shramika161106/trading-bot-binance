import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger

logger = setup_logger()

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    """Low-level wrapper around Binance Futures Testnet REST API."""

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("API key and secret must not be empty.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-MBX-APIKEY": self.api_key,
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        logger.info("BinanceClient initialised (Testnet).")

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    def _sign(self, params: dict) -> dict:
        """Attach a HMAC-SHA256 signature to the params dict."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(self, endpoint: str, params: dict) -> dict:
        """Sign and POST to an endpoint; return parsed JSON."""
        signed_params = self._sign(params)
        url = f"{BASE_URL}{endpoint}"
        logger.debug(f"POST {url} | params: { {k: v for k, v in signed_params.items() if k != 'signature'} }")

        try:
            response = self.session.post(url, data=signed_params, timeout=10)
            logger.debug(f"HTTP {response.status_code} | body: {response.text[:500]}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as exc:
            logger.error(f"Network error connecting to Binance: {exc}")
            raise ConnectionError(f"Cannot reach Binance testnet. Check your internet connection.\n{exc}") from exc
        except requests.exceptions.Timeout:
            logger.error("Request timed out.")
            raise TimeoutError("Request to Binance timed out. Try again.")
        except requests.exceptions.HTTPError as exc:
            error_body = exc.response.text if exc.response is not None else "no body"
            logger.error(f"HTTP error {exc.response.status_code}: {error_body}")
            raise RuntimeError(f"Binance API error {exc.response.status_code}: {error_body}") from exc

    # ------------------------------------------------------------------ #
    #  Public API calls                                                    #
    # ------------------------------------------------------------------ #

    def place_order(self, params: dict) -> dict:
        """Place a futures order and return the full response dict."""
        logger.info(f"Placing order: {params}")
        result = self._post("/fapi/v1/order", params)
        logger.info(f"Order response: {result}")
        return result
