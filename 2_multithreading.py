import concurrent.futures
import time

from business import get_binance_tickers, get_binance_ticker
from exceptions.ticker import ExceptionTickerNotFound, ExceptionBinance
from general import (
    log,
    init_log,
    LIMIT_TICKERS,
    print_table,
    get_limit_page,
)
from model.closing_prices import ClosingPrices

init_log(__file__)

def get_closes_ticker(tickers_to_search:list[str]) -> list[ClosingPrices]:
    closing_prices: list[ClosingPrices] =[]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results=[executor.submit(get_binance_ticker, ticker) for ticker in tickers_to_search]
        for result in concurrent.futures.as_completed(results):
            try:
                closing_prices.append(result.result())
            except ExceptionTickerNotFound as e:
                log.debug(e)
            except Exception as e:
                log.error(f"Error:: {e}")

    return closing_prices

def get_tickers(limit_tickets:int) -> list[str]:
    tickers_found: list[str] = []

    with (concurrent.futures.ThreadPoolExecutor() as executor):
        results=[executor.submit(get_binance_tickers, start) for start in range(0, get_limit_page(limit_tickets)) ]
        for result in concurrent.futures.as_completed(results):
            try:
                tickers_found.extend(result.result())
            except ExceptionBinance as e:
                log.debug(e)
            except Exception as e:
                log.error(f"Error:: {e}")
    return tickers_found


if __name__ == "__main__":
    t1=time.perf_counter()

    tickers = get_tickers(LIMIT_TICKERS)
    tickers = tickers[:LIMIT_TICKERS]

    closes_by_ticker = get_closes_ticker(tickers)
    print_table(len(closes_by_ticker))

    for closes in closes_by_ticker:
        log.debug(closes)

    t2=time.perf_counter()
    log.info(f"Finished in {t2-t1:.2f} seconds")
