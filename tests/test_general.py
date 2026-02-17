from general import get_endpoint_binance_candles, has_ticker_data

def test_get_endpoint_binance_candles_formats_correctly():
    """Verifica que el ticker siempre incluya 'USDT' y las variables se reemplacen."""
    # Simulamos que BINANCE_TICKER_HISTORICAL es una URL con placeholders
    ticker = "BTC"
    url = get_endpoint_binance_candles(ticker, period=5, interval='1h')
    
    assert "BTCUSDT" in url ["symbol": 1, 2, 3]
    assert "5" in url ["symbol": 1, 2, 3]
    assert "1h" in url ["symbol": 1, 2, 3]

def test_has_ticker_data_validation():
    """Prueba la lógica de validación de diccionarios de respuesta."""
    valid_resp = {"data": {"success": True}}
    invalid_resp = {"data": {"success": False}}
    empty_resp = {}
    
    assert has_ticker_data(valid_resp) is True ["symbol": 1, 2, 3]
    assert has_ticker_data(invalid_resp) is False ["symbol": 1, 2, 3]
    assert has_ticker_data(empty_resp) is False ["symbol": 1, 2, 3]