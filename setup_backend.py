import os

backend_dir = r"c:\Users\Dell\OneDrive\Desktop\PANCHAYATGUARD\panchayatguard\backend"
app_dir = os.path.join(backend_dir, "app")
os.makedirs(app_dir, exist_ok=True)
os.makedirs(os.path.join(app_dir, "routers"), exist_ok=True)

# 1. database.py
with open(os.path.join(app_dir, "database.py"), "w") as f:
    f.write("""from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./panchayatguard.db")

# SQLite needs connect_args={"check_same_thread": False}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

# 2. models.py
with open(os.path.join(app_dir, "models.py"), "w") as f:
    f.write("""from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class RoleEnum(str, enum.Enum):
    Administrator = "Administrator"
    Analyst = "Analyst"
    Auditor = "Auditor"
    Viewer = "Viewer"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.Viewer)
    department = Column(String, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    transactions = relationship("ProcurementTransaction", back_populates="creator")
    audit_logs = relationship("AuditLog", back_populates="user")

class Panchayat(Base):
    __tablename__ = "panchayats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    district = Column(String)
    block = Column(String)
    state = Column(String)
    population = Column(Integer, nullable=True)
    contact = Column(String, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    transactions = relationship("ProcurementTransaction", back_populates="panchayat")

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, index=True)
    vendor_code = Column(String, unique=True, index=True)
    vendor_name = Column(String, index=True)
    registration_number = Column(String)
    category = Column(String)
    address = Column(Text)
    district = Column(String)
    state = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
    total_procurement_value = Column(Float, default=0.0)
    transaction_count = Column(Integer, default=0)
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String, default="Low")
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    transactions = relationship("ProcurementTransaction", back_populates="vendor")

class ProcurementTransaction(Base):
    __tablename__ = "procurement_transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    panchayat_id = Column(Integer, ForeignKey("panchayats.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    procurement_category = Column(String)
    description = Column(Text)
    amount = Column(Float)
    quantity = Column(Integer)
    unit_price = Column(Float)
    procurement_date = Column(DateTime(timezone=True))
    invoice_number = Column(String)
    tender_number = Column(String, nullable=True)
    payment_status = Column(String)
    procurement_method = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    panchayat = relationship("Panchayat", back_populates="transactions")
    vendor = relationship("Vendor", back_populates="transactions")
    creator = relationship("User", back_populates="transactions")
    risk_alerts = relationship("RiskAlert", back_populates="transaction")

class RiskAlert(Base):
    __tablename__ = "risk_alerts"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("procurement_transactions.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    alert_type = Column(String)
    risk_score = Column(Float)
    severity = Column(String)
    explanation = Column(Text)
    status = Column(String, default="open")
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    transaction = relationship("ProcurementTransaction", back_populates="risk_alerts")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(Integer)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String, nullable=True)
    
    user = relationship("User", back_populates="audit_logs")
""")

# 3. schemas.py
with open(os.path.join(app_dir, "schemas.py"), "w") as f:
    f.write("""from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import RoleEnum

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum
    department: Optional[str] = None
    status: str = "active"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
""")

# 4. auth.py
with open(os.path.join(app_dir, "auth.py"), "w") as f:
    f.write("""from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, database, schemas
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "fallback_secret_key_if_missing_123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def require_role(roles: list[str]):
    def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role.value not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return current_user
    return role_checker
""")

# 5. auth_router.py
with open(os.path.join(app_dir, "routers", "auth_router.py"), "w") as f:
    f.write("""from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from .. import schemas, models, database, auth

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.post("/logout")
def logout():
    # In a stateless JWT setup, logout is mostly handled client-side by deleting the token.
    # We can just return success here.
    return {"message": "Successfully logged out"}
""")

# 6. main.py
with open(os.path.join(app_dir, "main.py"), "w") as f:
    f.write("""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth_router
import os
from dotenv import load_dotenv

load_dotenv()

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PanchayatGuard API", 
    description="Backend API for PanchayatGuard Procurement Intelligence Platform",
    version="1.0.0"
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)

@app.get("/")
def root():
    return {"message": "PanchayatGuard API is running. Access /docs for API documentation."}
""")

# 7. seed.py
with open(os.path.join(backend_dir, "seed.py"), "w") as f:
    f.write("""from app.database import SessionLocal, engine, Base
from app.models import User, RoleEnum
from app.auth import get_password_hash
import sys

def seed_users():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    users = [
        {"name": "Admin User", "email": "admin@panchayatguard.gov.in", "role": RoleEnum.Administrator},
        {"name": "Analyst User", "email": "analyst@panchayatguard.gov.in", "role": RoleEnum.Analyst},
        {"name": "Auditor User", "email": "auditor@panchayatguard.gov.in", "role": RoleEnum.Auditor},
        {"name": "Viewer User", "email": "viewer@panchayatguard.gov.in", "role": RoleEnum.Viewer},
    ]
    
    for u in users:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            new_user = User(
                name=u["name"],
                email=u["email"],
                password_hash=get_password_hash("SecurePassword123!"),
                role=u["role"],
                department="Central"
            )
            db.add(new_user)
            print(f"Created {u['email']}")
        else:
            print(f"User {u['email']} already exists.")
            
    db.commit()
    db.close()

if __name__ == "__main__":
    print("Seeding database...")
    seed_users()
    print("Seeding complete.")
""")

print("Backend files generated successfully!")
