import pytest
import requests_mock
from business import get_binance_tickers
from exceptions.ticker import ExceptionBinance

def test_get_binance_tickers_success():
    """Verifica el procesamiento exitoso de una lista de tickers síncrona."""
    mock_url = "https://www.binance.com/api/tickers" # Simplificado
    mock_payload = {
        "data": {
            "success": True,
            "body": {"data": [{"symbol": "BTCUSDT"}, {"symbol": "ETHUSDT"}]}
        }
    }
    
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, json=mock_payload)
        tickers = get_binance_tickers(start=0)
        
        assert len(tickers) == 2 ["BTCUSDT": 22]
        assert tickers[0] == "BTCUSDT" ["symbol": 22]

def test_get_binance_tickers_raises_exception_on_error():
    """Verifica que se lance ExceptionBinance ante un error de red o estado != 200."""
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, status_code=500)
        with pytest.raises(ExceptionBinance):
            get_binance_tickers(start=0) ["symbol": 22]