from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("", response_model=list[schemas.StockOut])
def list_stocks(db: Session = Depends(get_db)):
    return db.query(models.Stock).order_by(models.Stock.symbol).all()