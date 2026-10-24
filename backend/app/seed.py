from app.database import SessionLocal
from app import models

STOCKS = [
    ("RELIANCE.NS", "Reliance Industries"),
    ("TCS.NS", "Tata Consultancy Services"),
    ("HDFCBANK.NS", "HDFC Bank"),
    ("INFY.NS", "Infosys"),
    ("ICICIBANK.NS", "ICICI Bank"),
    ("HINDUNILVR.NS", "Hindustan Unilever"),
    ("ITC.NS", "ITC"),
    ("SBIN.NS", "State Bank of India"),
    ("BHARTIARTL.NS", "Bharti Airtel"),
    ("KOTAKBANK.NS", "Kotak Mahindra Bank"),
    ("LT.NS", "Larsen & Toubro"),
    ("AXISBANK.NS", "Axis Bank"),
    ("ASIANPAINT.NS", "Asian Paints"),
    ("MARUTI.NS", "Maruti Suzuki"),
    ("SUNPHARMA.NS", "Sun Pharma"),
    ("TITAN.NS", "Titan Company"),
    ("BAJFINANCE.NS", "Bajaj Finance"),
    ("WIPRO.NS", "Wipro"),
    ("HCLTECH.NS", "HCL Technologies"),
    ("NTPC.NS", "NTPC"),
]


def seed():
    db = SessionLocal()
    try:
        existing = {symbol for (symbol,) in db.query(models.Stock.symbol).all()}
        added = 0
        for symbol, name in STOCKS:
            if symbol not in existing:
                db.add(models.Stock(symbol=symbol, name=name))
                added += 1
        db.commit()
        print(f"Added {added} stocks")
    finally:
        db.close()


if __name__ == "__main__":
    seed()