from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("", response_model=schemas.WalletOut)
def get_wallet(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    ledger_total = (
        db.query(func.coalesce(func.sum(models.LedgerEntry.amount), 0))
        .filter(models.LedgerEntry.wallet_id == wallet.id)
        .scalar()
    )
    return {
        "balance": wallet.balance,
        "ledger_total": ledger_total,
        "consistent": wallet.balance == ledger_total,
    }