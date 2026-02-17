import asyncio
import time
import aiohttp

from business.business_async import get_binance_tickers, get_binance_ticker
from general import (
    log,
    init_log,
    LIMIT_TICKERS,
    print_table,
    get_limit_page,
    get_header,
    get_tickers_by_page
)
from model.closing_prices import ClosingPrices

init_log(__file__)

async def main(limit_tickets:int=LIMIT_TICKERS) -> None:
    t1=time.perf_counter()

    closing_prices_valid : list[ClosingPrices] = []
    async with aiohttp.ClientSession(headers=get_header()) as session:

        tickers_list=[]

        log.info("Generando tareas concurrentes para obtener los tickers...")
        log.info(f"Cantidad de paginas {get_limit_page(limit_tickets)}")

        tasks_tickers = [
            get_binance_tickers(session, start, number_ticker)
            for start, number_ticker in get_tickers_by_page(limit_tickets).items()
        ]

        log.info(f"Disparando {len(tasks_tickers)} peticiones concurrentes para obtener los tickers...")
        result_tasks = await asyncio.gather(*tasks_tickers, return_exceptions=True)
        for result in result_tasks:
            if isinstance(result, list):
                tickers_list.extend(result)

        #------------------------------------------------------------------------------------

        log.info(f"Generando {len(tickers_list)} tareas concurrentes para obtener los precios...")
        tasks_closing_prices = [
            get_binance_ticker(session, ticker) for ticker in tickers_list[:limit_tickets]
        ]

        log.info(f"Disparando {len(tasks_closing_prices)} peticiones concurrentes para obtener los datos...")
        closing_prices = await asyncio.gather(*tasks_closing_prices, return_exceptions=True)

        log.info("Obteniendo datos de precios de tickers validos...")
        closing_prices_valid = [p for p in closing_prices if  isinstance(p, ClosingPrices)]

    print_table(len(closing_prices_valid))

    for closes in closing_prices_valid:
        log.debug(closes)

    t2=time.perf_counter()
    log.info(f"Finished in {t2-t1:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main(10))
