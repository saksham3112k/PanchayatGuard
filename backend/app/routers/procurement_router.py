from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, extract, func
from typing import List, Optional
from datetime import datetime
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
import random

from ..database import get_db
from ..models import (
    ProcurementTransaction, Vendor, Panchayat, RiskAlert, AuditLog, User
)
from ..transaction_schemas import (
    TransactionCreate, TransactionUpdate, TransactionResponse, PaginatedTransactionResponse
)
from ..auth import get_current_user

router = APIRouter(prefix="/api/procurement", tags=["Procurement"])



def log_audit(session: Session, user_id: int, action: str, entity_type: str, entity_id: int, details: str):
    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id,
        new_value=details
    )
    session.add(log)

@router.get("/summary")
def get_procurement_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_count = db.query(ProcurementTransaction).count()
    total_val = db.query(func.sum(ProcurementTransaction.amount)).scalar() or 0.0
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    month_count = db.query(ProcurementTransaction).filter(
        extract('month', ProcurementTransaction.procurement_date) == current_month,
        extract('year', ProcurementTransaction.procurement_date) == current_year
    ).count()
    
    high_risk_count = db.query(ProcurementTransaction).join(RiskAlert).filter(
        RiskAlert.severity == 'High'
    ).count()

    return {
        "total_transactions": total_count,
        "total_value": total_val,
        "this_month": month_count,
        "high_risk_transactions": high_risk_count
    }

@router.get("/transactions", response_model=PaginatedTransactionResponse)
def get_transactions(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    panchayat_id: Optional[int] = None,
    vendor_id: Optional[int] = None,
    category: Optional[str] = None,
    risk_level: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ProcurementTransaction, Panchayat.name.label('panchayat_name'), Vendor.vendor_name.label('vendor_name'))\
              .join(Panchayat, ProcurementTransaction.panchayat_id == Panchayat.id)\
              .join(Vendor, ProcurementTransaction.vendor_id == Vendor.id)
    
    if search:
        query = query.filter(or_(
            ProcurementTransaction.transaction_id.ilike(f"%{search}%"),
            ProcurementTransaction.description.ilike(f"%{search}%"),
            Panchayat.name.ilike(f"%{search}%"),
            Vendor.vendor_name.ilike(f"%{search}%")
        ))
    if panchayat_id:
        query = query.filter(ProcurementTransaction.panchayat_id == panchayat_id)
    if vendor_id:
        query = query.filter(ProcurementTransaction.vendor_id == vendor_id)
    if category:
        query = query.filter(ProcurementTransaction.procurement_category == category)
    if start_date:
        query = query.filter(ProcurementTransaction.procurement_date >= start_date)
    if end_date:
        query = query.filter(ProcurementTransaction.procurement_date <= end_date)

    # Note: risk_level requires a join with RiskAlert or computing. For phase 3 we use a heuristic based on existing alerts
    
    total = query.count()
    results = query.order_by(desc(ProcurementTransaction.procurement_date))\
                   .offset((page - 1) * page_size)\
                   .limit(page_size)\
                   .all()

    data = []
    for tx, p_name, v_name in results:
        alert = db.query(RiskAlert).filter(RiskAlert.transaction_id == tx.id).first()
        risk_score = alert.risk_score if alert else 0.0
        r_level = alert.severity if alert else "Low"
        
        tx_dict = {c.name: getattr(tx, c.name) for c in tx.__table__.columns}
        tx_dict["panchayat_name"] = p_name
        tx_dict["vendor_name"] = v_name
        tx_dict["risk_score"] = risk_score
        tx_dict["risk_level"] = r_level
        data.append(tx_dict)

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": data
    }

@router.get("/export")
def export_transactions(
    search: Optional[str] = None,
    panchayat_id: Optional[int] = None,
    vendor_id: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ProcurementTransaction, Panchayat.name, Vendor.vendor_name)\
              .join(Panchayat)\
              .join(Vendor)
    
    if search:
        query = query.filter(or_(
            ProcurementTransaction.transaction_id.ilike(f"%{search}%"),
            Panchayat.name.ilike(f"%{search}%"),
            Vendor.vendor_name.ilike(f"%{search}%")
        ))
    if panchayat_id:
        query = query.filter(ProcurementTransaction.panchayat_id == panchayat_id)
    if vendor_id:
        query = query.filter(ProcurementTransaction.vendor_id == vendor_id)
    if category:
        query = query.filter(ProcurementTransaction.procurement_category == category)
        
    results = query.all()
    
    f = StringIO()
    writer = csv.writer(f)
    writer.writerow(['Transaction ID', 'Date', 'Panchayat', 'Vendor', 'Category', 'Description', 'Amount', 'Method', 'Payment Status'])
    
    for tx, p_name, v_name in results:
        writer.writerow([
            tx.transaction_id,
            tx.procurement_date.strftime("%Y-%m-%d"),
            p_name,
            v_name,
            tx.procurement_category,
            tx.description,
            tx.amount,
            tx.procurement_method,
            tx.payment_status
        ])
    
    f.seek(0)
    return StreamingResponse(f, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=transactions.csv"})

@router.get("/dropdowns")
def get_dropdowns(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    panchayats = db.query(Panchayat).all()
    vendors = db.query(Vendor).all()
    categories = db.query(ProcurementTransaction.procurement_category).distinct().all()
    return {
        "panchayats": [{"id": p.id, "name": p.name} for p in panchayats],
        "vendors": [{"id": v.id, "name": v.vendor_name} for v in vendors],
        "categories": [c[0] for c in categories if c[0]]
    }

@router.get("/transactions/{id}")
def get_transaction(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tx = db.query(ProcurementTransaction).filter(ProcurementTransaction.id == id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    p_name = db.query(Panchayat.name).filter(Panchayat.id == tx.panchayat_id).scalar()
    v_name = db.query(Vendor.vendor_name).filter(Vendor.id == tx.vendor_id).scalar()
    alert = db.query(RiskAlert).filter(RiskAlert.transaction_id == tx.id).first()
    
    res = {c.name: getattr(tx, c.name) for c in tx.__table__.columns}
    res["panchayat_name"] = p_name
    res["vendor_name"] = v_name
    res["risk_score"] = alert.risk_score if alert else 0.0
    res["risk_level"] = alert.severity if alert else "Low"
    res["alerts"] = [
        {"type": alert.alert_type, "severity": alert.severity, "description": alert.explanation, "date": alert.detected_at}
    ] if alert else []
    
    audit_logs = db.query(AuditLog).filter(AuditLog.entity_type == "Transaction", AuditLog.entity_id == id).order_by(desc(AuditLog.timestamp)).all()
    res["audit_history"] = [{"action": l.action, "details": l.new_value, "date": l.timestamp} for l in audit_logs]
    
    return res

@router.post("/transactions", response_model=dict)
def create_transaction(tx_in: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    exists = db.query(ProcurementTransaction).filter(ProcurementTransaction.transaction_id == tx_in.transaction_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Transaction ID already exists")
        
    db_tx = ProcurementTransaction(
        **tx_in.dict(),
        created_by=current_user.id
    )
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    
    # Calculate Risk using Deterministic Engine
    from ..risk_engine import analyze_transaction_risk
    
    risk_analysis = analyze_transaction_risk(db_tx, db)
    score = risk_analysis["risk_score"]
    level = risk_analysis["risk_level"]
    
    if score >= 40:
        for signal in risk_analysis["signals"]:
            db_alert = RiskAlert(
                transaction_id=db_tx.id,
                vendor_id=db_tx.vendor_id,
                alert_type=signal["type"],
                risk_score=signal.get("score", risk_analysis["risk_score"]),
                severity=signal["severity"],
                explanation=signal["explanation"]
            )
            db.add(db_alert)
            
            if signal["severity"] in ["Critical", "CRITICAL"]:
                from ..models import Notification
                db.add(Notification(
                    title="New critical risk alert generated",
                    message=f"Transaction {db_tx.transaction_id}",
                    type="alert"
                ))
                
        db.commit()
        
    # Update Vendor Stats
    vendor = db.query(Vendor).filter(Vendor.id == db_tx.vendor_id).first()
    if vendor:
        vendor.transaction_count = (vendor.transaction_count or 0) + 1
        vendor.total_procurement_value = (vendor.total_procurement_value or 0) + db_tx.amount
        # update vendor overall risk score (moving average or max)
        vendor.risk_score = max(vendor.risk_score or 0, score)
    
    log_audit(db, current_user.id, "CREATE", "Transaction", db_tx.id, f"Created transaction {db_tx.transaction_id}")
    db.commit()
    
    return {"message": "Transaction created successfully", "id": db_tx.id}

@router.put("/transactions/{id}")
def update_transaction(id: int, tx_in: TransactionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_tx = db.query(ProcurementTransaction).filter(ProcurementTransaction.id == id).first()
    if not db_tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    update_data = tx_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tx, key, value)
        
    db_tx.updated_at = datetime.utcnow()
    log_audit(db, current_user.id, "UPDATE", "Transaction", db_tx.id, f"Updated transaction {db_tx.transaction_id}")
    db.commit()
    return {"message": "Transaction updated successfully"}

@router.delete("/transactions/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_tx = db.query(ProcurementTransaction).filter(ProcurementTransaction.id == id).first()
    if not db_tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    tx_id_str = db_tx.transaction_id
    db.query(RiskAlert).filter(RiskAlert.transaction_id == id).delete()
    db.delete(db_tx)
    
    log_audit(db, current_user.id, "DELETE", "Transaction", id, f"Deleted transaction {tx_id_str}")
    db.commit()
    return {"message": "Transaction deleted successfully"}
