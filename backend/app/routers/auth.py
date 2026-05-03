"""
routers/auth.py
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Holding
from app.models.goal import Goal
from app.schemas.user import UserCreate, UserOut, Token
from app.utils.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=data.name, email=data.email,
        hashed_pw=hash_password(data.password),
        risk=data.risk, horizon=data.horizon, monthly_sip=data.monthly_sip
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Seed demo data
    demo_holdings = [
        Holding(user_id=user.id, symbol="RELIANCE", name="Reliance Industries", qty=15, avg_price=2420, sector="Energy",  buy_date="2024-01-15"),
        Holding(user_id=user.id, symbol="INFY",     name="Infosys Ltd.",        qty=30, avg_price=1380, sector="IT",      buy_date="2024-01-12"),
        Holding(user_id=user.id, symbol="HDFCBANK", name="HDFC Bank",           qty=20, avg_price=1580, sector="Banking", buy_date="2024-03-01"),
        Holding(user_id=user.id, symbol="WIPRO",    name="Wipro Ltd.",          qty=45, avg_price=420,  sector="IT",      buy_date="2025-11-10"),
    ]
    demo_goals = [
        Goal(user_id=user.id, name="Own a Home",      icon="🏠", target=5000000,  saved=1240000, monthly=25000, years=7,  risk="Moderate",    color="#4d9fff"),
        Goal(user_id=user.id, name="Early Retirement", icon="🌴", target=20000000, saved=5800000, monthly=50000, years=18, risk="Aggressive",  color="#00e5a0"),
    ]
    db.add_all(demo_holdings + demo_goals)
    db.commit()

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_pw):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.put("/profile")
def update_profile(data: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"name", "risk", "horizon", "monthly_sip"}
    for k, v in data.items():
        if k in allowed and hasattr(user, k):
            setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user
