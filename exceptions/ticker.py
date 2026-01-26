class ExceptionTickerNotFound(Exception):
    ticker: str

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def __str__(self) -> str:
        return f"{self.ticker} not found."


class ExceptionBinance(Exception):
    status: int
    message: str

    def __init__(self, status:int=200, message:str='' ) -> None:
        self.status = status
        self.message = message

    def __str__(self) -> str:
        if self.message:
            return f"{self.message}"

        return f"Error API: {self.status}"