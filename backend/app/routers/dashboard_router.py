from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, extract
from .. import models, database, auth
from typing import List, Dict, Any

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_summary(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    total_procurement = db.query(func.sum(models.ProcurementTransaction.amount)).scalar() or 0
    transactions_analyzed = db.query(func.count(models.ProcurementTransaction.id)).scalar() or 0
    high_risk_alerts = db.query(func.count(models.RiskAlert.id)).filter(models.RiskAlert.severity == "High").scalar() or 0

    return {
        "total_procurement": total_procurement,
        "transactions_analyzed": transactions_analyzed,
        "high_risk_alerts": high_risk_alerts,
        "procurement_change": "+18.4%", # Mocked trend
        "transaction_change": "+27.6%", # Mocked trend
        "alert_change": "+12.5%" # Mocked trend
    }

@router.get("/risk-trend")
def get_risk_trend(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Calculate average risk score by month for 2024
    results = db.query(
        extract('month', models.RiskAlert.detected_at).label('month'),
        func.avg(models.RiskAlert.risk_score).label('avg_risk')
    ).filter(
        extract('year', models.RiskAlert.detected_at) == 2024
    ).group_by(
        extract('month', models.RiskAlert.detected_at)
    ).order_by('month').all()
    
    # Fill missing months
    trend_dict = {int(r.month): round(r.avg_risk, 1) for r in results}
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    formatted_trend = []
    for i, m in enumerate(months, 1):
        formatted_trend.append({
            "month": m,
            "risk_score": trend_dict.get(i, 0)
        })
        
    return formatted_trend

@router.get("/vendor-concentration")
def get_vendor_concentration(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    total_val = db.query(func.sum(models.ProcurementTransaction.amount)).scalar() or 1
    
    results = db.query(
        models.Vendor.vendor_name,
        func.sum(models.ProcurementTransaction.amount).label('total')
    ).join(
        models.ProcurementTransaction, models.Vendor.id == models.ProcurementTransaction.vendor_id
    ).group_by(
        models.Vendor.vendor_name
    ).order_by(
        desc('total')
    ).all()
    
    concentration = []
    other_sum = 0
    for i, r in enumerate(results):
        if i < 4:
            concentration.append({
                "name": r.vendor_name,
                "value": r.total,
                "percentage": round((r.total / total_val) * 100)
            })
        else:
            other_sum += r.total
            
    if other_sum > 0:
        concentration.append({
            "name": "Others",
            "value": other_sum,
            "percentage": round((other_sum / total_val) * 100)
        })
        
    return concentration

@router.get("/flagged-transactions")
def get_flagged_transactions(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    alerts = db.query(
        models.RiskAlert, 
        models.ProcurementTransaction,
        models.Panchayat
    ).join(
        models.ProcurementTransaction, models.RiskAlert.transaction_id == models.ProcurementTransaction.id
    ).join(
        models.Panchayat, models.ProcurementTransaction.panchayat_id == models.Panchayat.id
    ).order_by(
        desc(models.RiskAlert.risk_score)
    ).limit(5).all()

    return [{
        "id": a.ProcurementTransaction.id,
        "risk_score": a.RiskAlert.risk_score,
        "description": a.ProcurementTransaction.description,
        "panchayat_name": a.Panchayat.name,
        "amount": a.ProcurementTransaction.amount,
        "date": a.ProcurementTransaction.procurement_date.strftime("%d %b %Y"),
        "alert_type": a.RiskAlert.alert_type,
        "severity": a.RiskAlert.severity
    } for a in alerts]

@router.get("/high-risk-vendors")
def get_high_risk_vendors(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    vendors = db.query(models.Vendor).order_by(desc(models.Vendor.risk_score)).limit(5).all()
    
    return [{
        "id": v.id,
        "vendor_name": v.vendor_name,
        "total_value": v.total_procurement_value,
        "transactions": v.transaction_count,
        "risk_score": v.risk_score,
        "status": v.risk_level
    } for v in vendors]

@router.get("/procurement-by-category")
def get_procurement_by_category(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    total_val = db.query(func.sum(models.ProcurementTransaction.amount)).scalar() or 1
    
    results = db.query(
        models.ProcurementTransaction.procurement_category,
        func.sum(models.ProcurementTransaction.amount).label('total')
    ).group_by(
        models.ProcurementTransaction.procurement_category
    ).order_by(
        desc('total')
    ).all()
    
    return [{
        "category": r.procurement_category,
        "value": r.total,
        "percentage": round((r.total / total_val) * 100)
    } for r in results]

@router.get("/insights")
def get_insights(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return [
        {"icon": "TrendingUp", "text": "Price anomaly detected in road construction tenders in 3 Gram Panchayats."},
        {"icon": "AlertCircle", "text": "Vendor Sharma Construction has 62% higher pricing compared to district average."},
        {"icon": "Link", "text": "Unusual transaction splitting detected in 5 procurements (this quarter)."},
        {"icon": "PieChart", "text": "Concentration risk: 48% of total procurement value with top 2 vendors."},
        {"icon": "Lightbulb", "text": "Recommendation: Initiate detailed audit for high-risk transactions."}
    ]

@router.get("/search")
def global_search(q: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not q or len(q) < 2:
        return []
    
    term = f"%{q}%"
    
    vendors = db.query(models.Vendor).filter(models.Vendor.vendor_name.ilike(term)).limit(3).all()
    panchayats = db.query(models.Panchayat).filter(models.Panchayat.name.ilike(term)).limit(3).all()
    txs = db.query(models.ProcurementTransaction).filter(models.ProcurementTransaction.description.ilike(term)).limit(3).all()
    
    results = []
    for v in vendors:
        results.append({"type": "Vendor", "title": v.vendor_name, "id": v.id})
    for p in panchayats:
        results.append({"type": "Panchayat", "title": p.name, "id": p.id})
    for t in txs:
        results.append({"type": "Transaction", "title": t.description, "id": t.id})
        
    return results
