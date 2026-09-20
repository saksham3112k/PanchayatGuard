from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, extract
from datetime import datetime

from ..database import get_db
from ..models import RiskAlert, ProcurementTransaction, Vendor, Panchayat
from ..auth import get_current_user

router = APIRouter(prefix="/api/risk", tags=["Risk Analysis"])

@router.get("/summary")
def get_risk_summary(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    total_tx = db.query(ProcurementTransaction).count() or 1
    
    # Risk Distribution
    high_critical = db.query(RiskAlert).filter(RiskAlert.severity.in_(['High', 'Critical', 'HIGH', 'CRITICAL'])).count()
    medium = db.query(RiskAlert).filter(RiskAlert.severity.in_(['Medium', 'MEDIUM'])).count()
    low = total_tx - (high_critical + medium)
    if low < 0: low = 0
    
    # Average Risk Score
    avg_score = db.query(func.avg(RiskAlert.risk_score)).scalar() or 0.0
    
    # Risk Trend
    trend_data = db.query(
        extract('month', RiskAlert.detected_at).label('month'),
        func.avg(RiskAlert.risk_score).label('avg_score'),
        func.count(RiskAlert.id).label('count')
    ).filter(
        extract('year', RiskAlert.detected_at) == 2024
    ).group_by('month').all()
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    trend_chart = []
    for i, m in enumerate(months, 1):
        found = next((x for x in trend_data if x.month == i), None)
        trend_chart.append({
            "month": m,
            "avg_score": round(found.avg_score, 1) if found else 0,
            "alerts": found.count if found else 0
        })
        
    # By Category
    cat_risk = db.query(
        ProcurementTransaction.procurement_category,
        func.avg(RiskAlert.risk_score).label('avg_score')
    ).join(RiskAlert, RiskAlert.transaction_id == ProcurementTransaction.id)\
     .group_by(ProcurementTransaction.procurement_category).all()
     
    # By Vendor (Top 5 Risky)
    vendor_risk = db.query(
        Vendor.vendor_name,
        func.avg(RiskAlert.risk_score).label('avg_score'),
        func.count(RiskAlert.id).label('count')
    ).join(RiskAlert, RiskAlert.vendor_id == Vendor.id)\
     .group_by(Vendor.vendor_name)\
     .order_by(desc('avg_score'))\
     .limit(5).all()

    # Critical Alerts
    critical_alerts = db.query(RiskAlert, Vendor.vendor_name, ProcurementTransaction.transaction_id)\
                        .join(Vendor, RiskAlert.vendor_id == Vendor.id)\
                        .join(ProcurementTransaction, RiskAlert.transaction_id == ProcurementTransaction.id)\
                        .filter(RiskAlert.severity.in_(['Critical', 'CRITICAL']))\
                        .order_by(desc(RiskAlert.detected_at))\
                        .limit(5).all()

    return {
        "overall_score": round(avg_score, 1),
        "distribution": {
            "critical_high": high_critical,
            "medium": medium,
            "low": low
        },
        "trend": trend_chart,
        "by_category": [{"name": c[0], "score": round(c[1], 1)} for c in cat_risk],
        "by_vendor": [{"name": v[0], "score": round(v[1], 1), "alerts": v[2]} for v in vendor_risk],
        "critical_alerts": [
            {
                "id": a[0].id,
                "type": a[0].alert_type,
                "explanation": a[0].explanation,
                "score": a[0].risk_score,
                "vendor": a[1],
                "transaction": a[2],
                "date": a[0].detected_at
            } for a in critical_alerts
        ]
    }
