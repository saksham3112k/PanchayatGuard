from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum
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
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
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

class Grievance(Base):
    __tablename__ = "grievances"
    id = Column(Integer, primary_key=True, index=True)
    grievance_id = Column(String, unique=True, index=True)
    subject = Column(String)
    description = Column(Text)
    panchayat_id = Column(Integer, ForeignKey("panchayats.id"))
    category = Column(String)
    submitted_by = Column(String)
    priority = Column(String)
    status = Column(String, default="Open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    panchayat = relationship("Panchayat")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(Text)
    type = Column(String)
    is_read = Column(Integer, default=0) # boolean via integer in SQLite
    created_at = Column(DateTime(timezone=True), server_default=func.now())
