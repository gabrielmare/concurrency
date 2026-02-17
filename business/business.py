import requests

from exceptions.ticker import ExceptionTickerNotFound, ExceptionBinance
from general import (
    get_header,
    get_endpoint_binance_tickers,
    has_ticker_data,
    get_endpoint_binance_candles,
)
from model.closing_prices import ClosingPrices

session=requests.Session()
session.headers.update(get_header())


def get_binance_tickers(page:int) -> list[str]:
    tickers = []
    start = (1000*page)+1 if page > 0 else 1

    endpoint = get_endpoint_binance_tickers(start=start)
    response = session.get(endpoint)

    if response.status_code != 200:
        raise ExceptionBinance(status=response.status_code)

    json_response=response.json()
    if not has_ticker_data(json_response):
        raise ExceptionBinance(message="Invalid format.")

    data_tickers = json_response["data"]["body"]["data"]
    for data_ticker in data_tickers:
        tickers.append(str(data_ticker["symbol"]).upper().strip())

    return [str(data["symbol"]).upper().strip() for data in data_tickers]


def get_binance_ticker(ticker:str, periods:int=10, interval:str = '1d') -> ClosingPrices:
    url=get_endpoint_binance_candles(ticker, periods, interval)
    response = session.get(url)

    if response.status_code != 200:
        raise ExceptionTickerNotFound(ticker)

    candles = response.json()
    return ClosingPrices(ticker, float(candles[0][4]), float(candles[-1][4]))