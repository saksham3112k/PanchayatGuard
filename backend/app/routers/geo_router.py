from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from typing import Optional

from ..database import get_db
from ..models import Panchayat, ProcurementTransaction, RiskAlert, Vendor
from ..auth import get_current_user

router = APIRouter(prefix="/api/geo", tags=["Geographic View"])

@router.get("/panchayats")
def get_geo_panchayats(
    district: Optional[str] = None,
    risk_level: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Base query for panchayats
    query = db.query(Panchayat)
    if district:
        query = query.filter(Panchayat.district == district)
        
    panchayats = query.all()
    results = []
    
    for p in panchayats:
        # Get total procurement & tx count
        stats = db.query(
            func.sum(ProcurementTransaction.amount).label('total'),
            func.count(ProcurementTransaction.id).label('count')
        ).filter(ProcurementTransaction.panchayat_id == p.id).first()
        
        total_amount = stats.total or 0
        tx_count = stats.count or 0
        
        # Apply amount filters
        if min_amount and total_amount < min_amount:
            continue
        if max_amount and total_amount > max_amount:
            continue
            
        # Get Risk Score (max or average risk from alerts for this panchayat)
        risk = db.query(func.max(RiskAlert.risk_score))\
                 .join(ProcurementTransaction, RiskAlert.transaction_id == ProcurementTransaction.id)\
                 .filter(ProcurementTransaction.panchayat_id == p.id).scalar() or 0.0
                 
        if risk >= 85: r_level = "Critical"
        elif risk >= 70: r_level = "High"
        elif risk >= 40: r_level = "Medium"
        else: r_level = "Low"
        
        if risk_level and risk_level != "All Risk Levels":
            # Match the filter logic exactly
            if "High" in risk_level and r_level not in ["High", "Critical"]: continue
            if "Medium" in risk_level and r_level != "Medium": continue
            if "Low" in risk_level and r_level != "Low": continue

        # Get top vendor
        top_vendor = db.query(Vendor.vendor_name)\
                       .join(ProcurementTransaction, ProcurementTransaction.vendor_id == Vendor.id)\
                       .filter(ProcurementTransaction.panchayat_id == p.id)\
                       .group_by(Vendor.vendor_name)\
                       .order_by(desc(func.sum(ProcurementTransaction.amount)))\
                       .first()
                       
        results.append({
            "id": p.id,
            "name": p.name,
            "district": p.district,
            "lat": p.latitude or 26.5,
            "lng": p.longitude or 80.5,
            "total_procurement": total_amount,
            "transaction_count": tx_count,
            "risk_score": risk,
            "risk_level": r_level,
            "top_vendor": top_vendor[0] if top_vendor else "None"
        })
        
    return results

@router.get("/summary")
def get_geo_summary(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    total_panchayats = db.query(Panchayat).count()
    total_procurement = db.query(func.sum(ProcurementTransaction.amount)).scalar() or 0
    districts_covered = db.query(func.count(func.distinct(Panchayat.district))).scalar() or 0
    
    # Calculate high risk panchayats
    # A panchayat is high risk if it has any transaction with risk >= 70
    high_risk_panchayats = db.query(func.count(func.distinct(ProcurementTransaction.panchayat_id)))\
                             .join(RiskAlert, RiskAlert.transaction_id == ProcurementTransaction.id)\
                             .filter(RiskAlert.risk_score >= 70).scalar() or 0
                             
    return {
        "total_panchayats": total_panchayats,
        "total_procurement": total_procurement,
        "high_risk_panchayats": high_risk_panchayats,
        "districts_covered": districts_covered,
        "total_districts": 75 # Standard for UP
    }
