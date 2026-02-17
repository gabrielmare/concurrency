import pytest
from aioresponses import aioresponses
from ..business.business_async import get_binance_ticker
from model.closing_prices import ClosingPrices

@pytest.mark.asyncio
async def test_get_binance_ticker_async_success(async_session):
    """Verifica la obtención asíncrona de precios de cierre."""
    ticker = "BTC"
    # Mock de respuesta de velas: [OpenTime, Open, High, Low, Close, Volume...]
    mock_candles = [
        [123, "10", "11", "9", "50000.0", "1"], # Primera vela (price_start)
        [456, "11", "12", "10", "51000.0", "1"] # Última vela (price_end)
    ]
    
    with aioresponses() as m:
        m.get(lambda url: "klines" in str(url), payload=mock_candles)
        
        result = await get_binance_ticker(async_session, ticker) ["BTC": 23]
        
        assert isinstance(result, ClosingPrices) ["BTC": 15, 23]
        assert result.price_start == 50000.0 ["BTC": 23]
        assert result.price_end == 51000.0 ["BTC": 23]