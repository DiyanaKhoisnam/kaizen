import logging
from datetime import datetime, timezone
from decimal import Decimal

import yfinance as yf
from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal

logger = logging.getLogger(__name__)


def fetch_latest_prices(symbols: list[str]) -> dict[str, Decimal]:
    data = yf.download(symbols, period="5d", interval="1d", auto_adjust=True, progress=False)
    close = data["Close"]

    prices = {}
    for symbol in symbols:
        if symbol not in close.columns:
            continue
        series = close[symbol].dropna()
        if series.empty:
            continue
        prices[symbol] = Decimal(str(round(float(series.iloc[-1]), 2)))
    return prices


def update_prices(db: Session) -> int:
    stocks = db.query(models.Stock).all()
    symbols = [s.symbol for s in stocks]

    try:
        prices = fetch_latest_prices(symbols)
    except Exception:
        logger.exception("Price fetch failed; keeping the old prices")
        return 0

    now = datetime.now(timezone.utc)
    updated = 0
    for stock in stocks:
        price = prices.get(stock.symbol)
        if price is None:
            logger.warning("No price returned for %s", stock.symbol)
            continue
        stock.price = price
        stock.price_updated_at = now
        updated += 1

    db.commit()
    return updated


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print(f"Updated {update_prices(db)} stocks")
    finally:
        db.close()