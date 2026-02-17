import logging
import aiohttp

from exceptions.ticker import ExceptionTickerNotFound, ExceptionBinance
from general import (
    get_endpoint_binance_tickers,
    has_ticker_data,
    get_endpoint_binance_candles,
)
from model.closing_prices import ClosingPrices


async def get_binance_tickers(session: aiohttp.ClientSession, page: int, take: int) -> list[str]:
    """Obtiene una lista de símbolos de tickers de Binance para una página dada."""
    start = (1000*page)+1 if page > 0 else 1
    logging.debug(f"Pagina de inicio {start} and take {take}")
    endpoint = get_endpoint_binance_tickers(start=start, take=take)

    async with session.get(endpoint) as response:

        if response.status != 200:
            raise ExceptionBinance(status=response.status)

        json_response= await response.json()
        if not has_ticker_data(json_response):
            raise ExceptionBinance(message="Invalid format.")

        data_tickers = json_response["data"]["body"]["data"]

    return [str(data["symbol"]).upper().strip() for data in data_tickers]


async def get_binance_ticker(
    session: aiohttp.ClientSession, ticker: str, periods: int = 10, interval: str = "1d"
) -> ClosingPrices:
    """Obtiene los precios de cierre para un ticker específico."""
    url=get_endpoint_binance_candles(ticker, periods, interval)

    async with session.get(url) as response:
        if response.status != 200:
            raise ExceptionTickerNotFound(ticker)

        candles = await response.json()
    return ClosingPrices(ticker, float(candles[0][4]), float(candles[-1][4]))