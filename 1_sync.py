import math
import time

from business import get_binance_tickers, get_binance_ticker
from exceptions.ticker import ExceptionTickerNotFound
from general import (
    log,
    init_log,
    DEFAULT_TAKE,
    LIMIT_TICKERS,
    print_table,
    get_stop_tickers,
)
from model.closing_prices import ClosingPrices

init_log(__file__)

def get_closes_ticker(tickers_to_search:list[str]) -> list[ClosingPrices]:
    closing_prices: list[ClosingPrices] =[]

    for ticker in tickers_to_search:
        try:
            closing_prices.append(get_binance_ticker(ticker))
        except ExceptionTickerNotFound as e:
            log.debug(e)
        except Exception as e:
            log.error(f"Error:: {e}")

    return closing_prices

def get_tickers(limit_tickets:int) -> list:
    tickers_found: list[str] = []

    for i in range(0, get_stop_tickers(limit_tickets)) :
        partial_tickers=get_binance_tickers(i)

        if DEFAULT_TAKE > len(partial_tickers):
            log.info('Finished process to looking for Binance tickets.')
            break

        tickers_found.extend(partial_tickers)
    return tickers_found

if __name__ == "__main__":
    t1=time.perf_counter()

    tickers=get_tickers(LIMIT_TICKERS)
    tickers = tickers[:LIMIT_TICKERS]

    closes_by_ticker = get_closes_ticker(tickers)
    print_table(len(closes_by_ticker))

    for closes in closes_by_ticker:
        log.debug(closes)

    t2=time.perf_counter()
    log.info(f"Finished in {t2-t1:.2f} seconds")
