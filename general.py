import math
import os
import logging as log
from dotenv import load_dotenv

# Settings

load_dotenv(verbose=True)

HEADER = {"User-Agent": os.getenv("USER_AGENT")}
LOG_MIN_LEVEL = int(os.getenv("LOG_MIN_LEVEL"))


DEFAULT_TAKE = int(os.getenv("BINANCE_TICKERS_TAKE"))
LIMIT_TICKERS = int(os.getenv("BINANCE_TICKERS_LIMIT"))
BINANCE_TICKERS = str(os.getenv('BINANCE_TICKERS'))
BINANCE_TICKER_HISTORICAL = str(os.getenv('BINANCE_TICKER_HISTORICAL'))

def get_header() -> dict:
    return HEADER

def init_log(path:str):
    filename=os.path.splitext(os.path.basename(path))[0]
    log.basicConfig(level=LOG_MIN_LEVEL,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=f'log/{filename}.log', filemode='w')



def get_endpoint_binance_tickers(start:int, take:int=DEFAULT_TAKE) -> str:
    return BINANCE_TICKERS.replace('TAKE', str(take)).replace('START', str(start))

def get_endpoint_binance_candles(ticker:str, period:int=10, interval:str = '1d') -> str:
    ticker += 'USDT'
    return BINANCE_TICKER_HISTORICAL.replace('TICKER', ticker).replace('PERIOD', str(period)).replace('INTERVAL', interval)

def has_ticker_data(response:dict) -> bool:
    return "data" in response and response["data"]["success"]

def get_stop_tickers(limit_tickets:int) -> int:
    return 1 if limit_tickets < DEFAULT_TAKE else math.ceil(limit_tickets/LIMIT_TICKERS)-1

def print_table(number:int):
    log.debug(f"Tickets to look for: {number} ")
    log.debug("-------------------------------------------")
    log.debug("Ticker | Candle | %")