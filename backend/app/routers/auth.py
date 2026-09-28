from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Holding
from app.models.goal import Goal
from app.schemas.user import UserCreate, UserOut, UserUpdate, Token
from app.utils.auth import hash_password, verify_password, create_access_token, get_current_user
from app.services.audit import record_audit_event
from app.config import settings

router = APIRouter(prefix='/auth', tags=['Authentication'])


def _request_meta(request: Request):
    return getattr(request.state, 'request_id', None), request.client.host if request.client else None


@router.post('/register', response_model=Token)
def register(data: UserCreate, request: Request, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail='Email already registered')
    user = User(name=data.name, email=data.email, hashed_pw=hash_password(data.password), risk=data.risk, horizon=data.horizon, monthly_sip=data.monthly_sip)
    db.add(user)
    db.flush()
    if settings.SEED_DEMO_DATA:
        db.add_all([
            Holding(user_id=user.id, symbol='RELIANCE', name='Reliance Industries', qty='15', avg_price='2420', sector='Energy', buy_date='2024-01-15'),
            Holding(user_id=user.id, symbol='INFY', name='Infosys Ltd.', qty='30', avg_price='1380', sector='IT', buy_date='2024-01-12'),
            Goal(user_id=user.id, name='Own a Home', icon='Home', target='5000000', saved='1240000', monthly='25000', years=7, risk='Moderate', color='#4d9fff'),
        ])
    request_id, ip = _request_meta(request)
    record_audit_event(db, 'auth.register', user_id=user.id, request_id=request_id, ip_address=ip)
    db.commit()
    db.refresh(user)
    return {'access_token': create_access_token({'sub': user.email}), 'token_type': 'bearer', 'user': user}


@router.post('/login', response_model=Token)
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    request_id, ip = _request_meta(request)
    if not user or not verify_password(form.password, user.hashed_pw):
        record_audit_event(db, 'auth.login', outcome='failure', request_id=request_id, ip_address=ip, metadata={'email': form.username[:255]})
        db.commit()
        raise HTTPException(status_code=401, detail='Invalid email or password')
    if not user.is_active:
        record_audit_event(db, 'auth.login', user_id=user.id, outcome='blocked', request_id=request_id, ip_address=ip)
        db.commit()
        raise HTTPException(status_code=403, detail='Account disabled')
    record_audit_event(db, 'auth.login', user_id=user.id, request_id=request_id, ip_address=ip)
    db.commit()
    return {'access_token': create_access_token({'sub': user.email}), 'token_type': 'bearer', 'user': user}


@router.get('/me', response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.put('/profile', response_model=UserOut)
def update_profile(data: UserUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
