from pydantic import BaseModel, EmailStr, Field, ConfigDict
from decimal import Decimal

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class WalletOut(BaseModel):
    balance: Decimal
    ledger_total: Decimal
    consistent: bool