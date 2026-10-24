from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from app.database import SessionLocal
from app.price_service import update_prices
from app.routers import auth, stocks, wallet


def refresh_prices_job():
    db = SessionLocal()
    try:
        update_prices(db)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(refresh_prices_job, "interval", minutes=5, max_instances=1, coalesce=True)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="kaizen", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(stocks.router)


@app.get("/health")
def health():
    return {"status": "ok"}