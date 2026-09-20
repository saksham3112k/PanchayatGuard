from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..database import get_db
from ..models import RiskAlert, ProcurementTransaction, Vendor, Panchayat
from ..auth import get_current_user

router = APIRouter(prefix="/api/ai-insights", tags=["AI Insights"])

@router.get("/")
def get_insights(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # We map RiskAlerts to AI Insights (deterministic rules)
    alerts = db.query(RiskAlert, ProcurementTransaction, Vendor.vendor_name, Panchayat.name.label("panchayat_name"))\
               .join(ProcurementTransaction, RiskAlert.transaction_id == ProcurementTransaction.id)\
               .join(Vendor, RiskAlert.vendor_id == Vendor.id)\
               .join(Panchayat, ProcurementTransaction.panchayat_id == Panchayat.id)\
               .order_by(desc(RiskAlert.detected_at))\
               .limit(50).all()
               
    insights = []
    
    cat_counts = {
        "Price Anomalies": 0,
        "Vendor Anomalies": 0,
        "Duplicate Transactions": 0,
        "Transaction Splitting": 0,
        "Concentration Risks": 0,
        "Emerging Risk Patterns": 0
    }
    
    for alert, tx, v_name, p_name in alerts:
        cat = "Vendor Anomalies"
        title = "Anomalous Activity"
        
        # Map alert_type to insight category
        at = alert.alert_type
        if at == "HIGH_VALUE":
            cat = "Emerging Risk Patterns"
            title = "Unusual Procurement Pattern"
        elif at == "PRICE_ANOMALY":
            cat = "Price Anomalies"
            title = "Unusually High Price Detected"
        elif at == "TRANSACTION_SPLITTING":
            cat = "Transaction Splitting"
            title = "Possible Transaction Splitting"
        elif at == "DUPLICATE_BILLING":
            cat = "Duplicate Transactions"
            title = "Potential Duplicate Billing"
        elif at == "VENDOR_CONCENTRATION":
            cat = "Concentration Risks"
            title = "High Vendor Concentration"
        elif at == "UNUSUAL_FREQUENCY":
            cat = "Emerging Risk Patterns"
            title = "Abnormal Transaction Frequency"
            
        cat_counts[cat] += 1
        
        insights.append({
            "id": alert.id,
            "title": title,
            "description": alert.explanation,
            "severity": alert.severity,
            "transaction_id": tx.transaction_id,
            "tx_pk": tx.id,
            "vendor": v_name,
            "panchayat": p_name,
            "date": alert.detected_at,
            "category": cat
        })
        
    return {
        "categories": cat_counts,
        "insights": insights
    }
