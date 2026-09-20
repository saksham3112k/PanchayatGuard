from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, extract, func
from typing import Optional, List
from datetime import datetime

from ..database import get_db
from ..models import Vendor, ProcurementTransaction, RiskAlert, AuditLog, Panchayat
from ..auth import get_current_user

router = APIRouter(prefix="/api/vendors", tags=["Vendors"])

@router.get("")
def list_vendors(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(Vendor)
    
    if search:
        query = query.filter(or_(
            Vendor.vendor_name.ilike(f"%{search}%"),
            Vendor.vendor_code.ilike(f"%{search}%"),
            Vendor.registration_number.ilike(f"%{search}%")
        ))
    if category:
        query = query.filter(Vendor.category == category)
    if status:
        query = query.filter(Vendor.status == status)
        
    total = query.count()
    results = query.order_by(desc(Vendor.total_procurement_value))\
                   .offset((page - 1) * page_size)\
                   .limit(page_size)\
                   .all()
                   
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": results
    }

@router.get("/{id}")
def get_vendor_details(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    vendor = db.query(Vendor).filter(Vendor.id == id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
        
    # Stats
    total_proc = db.query(func.sum(ProcurementTransaction.amount)).scalar() or 0
    proc_share = round((vendor.total_procurement_value / total_proc * 100) if total_proc > 0 else 0, 1)
    avg_tx = round((vendor.total_procurement_value / vendor.transaction_count) if vendor.transaction_count > 0 else 0, 2)
    
    # Monthly
    monthly_data = db.query(
        extract('month', ProcurementTransaction.procurement_date).label('month'),
        func.sum(ProcurementTransaction.amount).label('total'),
        func.count(ProcurementTransaction.id).label('count')
    ).filter(
        ProcurementTransaction.vendor_id == id,
        extract('year', ProcurementTransaction.procurement_date) == 2024
    ).group_by('month').all()
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_chart = []
    for i, m in enumerate(months, 1):
        found = next((x for x in monthly_data if x.month == i), None)
        monthly_chart.append({
            "month": m,
            "value": found.total if found else 0,
            "count": found.count if found else 0
        })
        
    # Category Distribution
    cat_data = db.query(
        ProcurementTransaction.procurement_category,
        func.sum(ProcurementTransaction.amount).label('total')
    ).filter(ProcurementTransaction.vendor_id == id).group_by(ProcurementTransaction.procurement_category).all()
    
    cat_chart = [{"name": c[0], "value": c[1]} for c in cat_data]
    
    # Recent Transactions
    recent_tx = db.query(ProcurementTransaction, Panchayat.name)\
                  .join(Panchayat)\
                  .filter(ProcurementTransaction.vendor_id == id)\
                  .order_by(desc(ProcurementTransaction.procurement_date))\
                  .limit(5).all()
                  
    recent_tx_list = []
    for tx, p_name in recent_tx:
        alert = db.query(RiskAlert).filter(RiskAlert.transaction_id == tx.id).first()
        recent_tx_list.append({
            "id": tx.id,
            "transaction_id": tx.transaction_id,
            "date": tx.procurement_date,
            "panchayat": p_name,
            "category": tx.procurement_category,
            "amount": tx.amount,
            "risk_score": alert.risk_score if alert else 0,
            "status": alert.severity if alert else "Low"
        })
        
    # Risk Alerts
    alerts = db.query(RiskAlert).filter(RiskAlert.vendor_id == id).order_by(desc(RiskAlert.detected_at)).limit(5).all()
    
    # Panchayats Served
    panchayats_served_count = db.query(func.count(func.distinct(ProcurementTransaction.panchayat_id))).filter(ProcurementTransaction.vendor_id == id).scalar() or 0
    districts_served_count = db.query(func.count(func.distinct(Panchayat.district)))\
                               .join(ProcurementTransaction)\
                               .filter(ProcurementTransaction.vendor_id == id).scalar() or 0
                               
    return {
        "id": vendor.id,
        "vendor_code": vendor.vendor_code,
        "vendor_name": vendor.vendor_name,
        "registration_number": vendor.registration_number,
        "category": vendor.category,
        "address": vendor.address,
        "district": vendor.district,
        "state": vendor.state,
        "contact_email": vendor.contact_email,
        "contact_phone": vendor.contact_phone,
        "status": vendor.status,
        "total_procurement_value": vendor.total_procurement_value,
        "transaction_count": vendor.transaction_count,
        "risk_score": vendor.risk_score,
        "risk_level": vendor.risk_level,
        "avg_transaction": avg_tx,
        "procurement_share": proc_share,
        "panchayats_served": panchayats_served_count,
        "districts_served": districts_served_count,
        "monthly_chart": monthly_chart,
        "category_chart": cat_chart,
        "recent_transactions": recent_tx_list,
        "risk_alerts": [{"type": a.alert_type, "severity": a.severity, "explanation": a.explanation, "date": a.detected_at} for a in alerts]
    }
from pydantic import BaseModel
import random
class VendorCreate(BaseModel):
    vendor_name: str
    category: str
    contact_email: str = None
    contact_phone: str = None

@router.post("")
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    code = f"VEND-{random.randint(1000, 9999)}"
    new_vendor = Vendor(
        vendor_code=code,
        vendor_name=vendor.vendor_name,
        category=vendor.category,
        contact_email=vendor.contact_email,
        contact_phone=vendor.contact_phone,
        status="Active",
        risk_score=0,
        risk_level="Low"
    )
    db.add(new_vendor)
    db.add(AuditLog(
        user_id=current_user.id, action="CREATE", entity_type="Vendor",
        new_value=f"Created vendor {vendor.vendor_name}"
    ))
    db.commit()
    return {"message": "Vendor created successfully", "id": new_vendor.id}
