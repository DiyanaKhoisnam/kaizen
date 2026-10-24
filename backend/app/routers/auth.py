from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

STARTING_CASH = Decimal("1000000.00")


@router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    email = payload.email.lower()

    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = models.User(email=email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.flush()  # assigns user.id without committing yet

    wallet = models.Wallet(user_id=user.id, balance=STARTING_CASH)
    db.add(wallet)
    db.flush()

    db.add(models.LedgerEntry(wallet_id=wallet.id, amount=STARTING_CASH, entry_type="SIGNUP_BONUS"))

    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form.username.lower()).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user