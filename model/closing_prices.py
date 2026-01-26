from abc import abstractproperty


class ClosingPrices:
    ticker: str
    first: float
    last: float
    error:str

    def __init__(self, ticker: str, first: float, last: float) -> None:
        self.ticker = ticker
        self.first = first
        self.last = last

    def __str__(self) -> str:
        return f"{self.ticker} | {self.percentage} | {self.candle}"

    @property
    def percentage(self) -> str:
        return f"{round((self.last*100/self.first)-100,2)}%"

    @property
    def candle(self) -> str:
        if (self.last-self.first) == 0:
            return 'Doji'

        return 'Bullish' if (self.last-self.first) > 0 else 'Bearish'

