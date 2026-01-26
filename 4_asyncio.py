import asyncio
import time

from business import get_binance_tickers, get_binance_ticker
from exceptions.ticker import ExceptionTickerNotFound, ExceptionBinance
from general import (
    log,
    init_log,
    LIMIT_TICKERS,
    print_table,
    get_stop_tickers,
)
from model.closing_prices import ClosingPrices

init_log(__file__)

def get_closes_ticker(tickers_to_search:list[str]) -> list[ClosingPrices]:
    closing_prices: list[ClosingPrices] =[]

    # Apply asyncIO

    return closing_prices

def get_tickers(limit_tickets:int) -> list[str]:
    tickers_found: list[str] = []

    # Apply asyncIO

    return tickers_found


async def main() -> None:
    t1=time.perf_counter()

    # La palabra reservada await (objeto esperable) implementa el metodo reservado __await__()
    # Funcionamiento
    #       Le indico que pause la ejecucion de la funcion y le cedo el control al EventLoop.
    #       La funcion quedara suspendida hasta se complete.
    #       El EventLoop puede continuar ejecutando otras tareas.
    # Hay 3 tipos de objetos a esperar
    #   Corutines, se crea cuando se llama a una funcion asincrona
    #   Tasks, son envoltorios de Corutines
    #   Futures, objetos de bajo nivel que representan resultados eventuales (promesa)

    asyncio.create_task(get_binance_tickers(LIMIT_TICKERS))

    tickers = await get_tickers(LIMIT_TICKERS)
    tickers = tickers[:LIMIT_TICKERS]

    closes_by_ticker = get_closes_ticker(tickers)
    print_table(len(closes_by_ticker))

    for closes in closes_by_ticker:
        log.debug(closes)

    t2=time.perf_counter()
    log.info(f"Finished in {t2-t1:.2f} seconds")


if __name__ == "__main__":
    # Se inicia el bucle de eventos llamando a una funcion asincrona.
    # Dicho bucle es el motor que ejecuta y administra las funciones asincronas.
    # El motor va ejecutando una tarea tras otra pero mantiene la escucha de la respuesta de las tareas ejecutadas.
    asyncio.run(main())
