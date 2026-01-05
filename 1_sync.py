import json
import time
import requests
from general import ( log, init_log,
    get_header,
    get_endpoint_binance_tickers,
    get_endpoint_binance_candles,
    get_percentage,
    get_candle_type,
    DEFAULT_TAKE, LIMIT_REQUESTS,
    has_ticker_data,
)

init_log(__file__)

def get_closes_by_period(ticker:str, periods:int=10, interval:str = '1d') -> tuple[float, float]:
    response=requests.get(get_endpoint_binance_candles(ticker, periods, interval), headers=get_header())
    if response.status_code != 200:
        Exception('Ticker not found.')

    candles = json.loads(response.text)
    first_close_of_period, last_close_of_period=float(candles[0][4]), float(candles[periods-1][4])
    return first_close_of_period, last_close_of_period

def get_binance_tickers() -> list:
    tickers=[]
    start=1
    wanted=0

    for i in range(1, LIMIT_REQUESTS) :
        endpoint=get_endpoint_binance_tickers(start=start)
        response=requests.get(endpoint, headers=get_header())

        if response.status_code != 200 or not has_ticker_data(json_response:=json.loads(response.text)):
            raise Exception('Wait! ', response.status_code)

        data_tickers=json_response['data']['body']['data']
        for data_ticker in data_tickers:
            tickers.append( str(data_ticker['symbol']).upper().strip())

        if DEFAULT_TAKE > len(data_tickers):
            log.info('Finished process to looking for Binance tickets.')
            break

        start = DEFAULT_TAKE + 1
        wanted=DEFAULT_TAKE*i
    log.info(f'Tickers wanted:: {wanted}')
    return tickers

def main():
    tickers=get_binance_tickers()
    log.debug(f"Tickets to look for: {len(tickers)} ")
    log.debug("-------------------------------------------")
    log.debug("Ticker | Candle | %")
    stop=10

    for i, ticker in enumerate(tickers, 1):
        try:
            closes = get_closes_by_period(ticker)

            if i > stop:
                break

            percentage=get_percentage(closes[0], closes[1])
            candle=get_candle_type(closes[1]-closes[0])
            log.debug(f"{ticker} | {percentage} | {candle}")
        except Exception as e:
            log.debug(f"Ticker not found:: {ticker}")
            stop+=1


if __name__ == "__main__":
    t1=time.perf_counter()
    main()
    t2=time.perf_counter()
    log.info(f"Finished in {t2-t1:.2f} seconds")
