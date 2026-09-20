from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional
from datetime import datetime
import csv
from io import StringIO
from fastapi.responses import StreamingResponse

from ..database import get_db
from ..models import ProcurementTransaction, Vendor, Panchayat, RiskAlert
from ..auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/generate")
def generate_report(
    type: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    district: Optional[str] = None,
    panchayat_id: Optional[int] = None,
    vendor_id: Optional[int] = None,
    risk_level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(ProcurementTransaction, Vendor.vendor_name, Panchayat.name, Panchayat.district, RiskAlert.severity, RiskAlert.risk_score)\
              .select_from(ProcurementTransaction)\
              .join(Vendor)\
              .join(Panchayat)\
              .outerjoin(RiskAlert, RiskAlert.transaction_id == ProcurementTransaction.id)
              
    if district:
        query = query.filter(Panchayat.district == district)
    if panchayat_id:
        query = query.filter(Panchayat.id == panchayat_id)
    if vendor_id:
        query = query.filter(Vendor.id == vendor_id)
    if start_date:
        query = query.filter(ProcurementTransaction.procurement_date >= datetime.fromisoformat(start_date.replace('Z', '+00:00')))
    if end_date:
        query = query.filter(ProcurementTransaction.procurement_date <= datetime.fromisoformat(end_date.replace('Z', '+00:00')))
    if risk_level and risk_level != "All":
        if "High" in risk_level or "Critical" in risk_level:
            query = query.filter(RiskAlert.severity.in_(['High', 'Critical', 'HIGH', 'CRITICAL']))
        elif "Medium" in risk_level:
            query = query.filter(RiskAlert.severity.in_(['Medium', 'MEDIUM']))
        elif "Low" in risk_level:
            query = query.filter(RiskAlert.risk_score < 40)
        
    results = query.all()
    
    data = []
    total_val = 0
    for tx, v_name, p_name, dist, risk_sev, risk_score in results:
        total_val += tx.amount
        data.append({
            "Transaction ID": tx.transaction_id,
            "Date": tx.procurement_date.strftime("%Y-%m-%d"),
            "Vendor": v_name,
            "Panchayat": p_name,
            "District": dist,
            "Category": tx.procurement_category,
            "Amount": tx.amount,
            "Status": tx.payment_status,
            "Risk": f"{risk_score or 0} ({risk_sev or 'Low'})"
        })
        
    # Audit & Notification
    from ..models import AuditLog, Notification
    db.add(AuditLog(
        user_id=current_user.id, action="REPORT_GENERATED", entity_type="Report", entity_id=0, new_value=f"Generated {type}"
    ))
    db.add(Notification(
        title="Report generated successfully", message=f"{type}", type="report"
    ))
    db.commit()

    return {
        "report_type": type,
        "count": len(data),
        "total_value": total_val,
        "data": data[:100] # preview limit
    }

@router.get("/export/csv")
def export_csv(
    type: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    district: Optional[str] = None,
    panchayat_id: Optional[int] = None,
    vendor_id: Optional[int] = None,
    risk_level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(ProcurementTransaction, Vendor.vendor_name, Panchayat.name, Panchayat.district, RiskAlert.severity, RiskAlert.risk_score)\
              .select_from(ProcurementTransaction)\
              .join(Vendor)\
              .join(Panchayat)\
              .outerjoin(RiskAlert, RiskAlert.transaction_id == ProcurementTransaction.id)
              
    if district:
        query = query.filter(Panchayat.district == district)
    if panchayat_id:
        query = query.filter(Panchayat.id == panchayat_id)
    if vendor_id:
        query = query.filter(Vendor.id == vendor_id)
    if start_date:
        query = query.filter(ProcurementTransaction.procurement_date >= datetime.fromisoformat(start_date.replace('Z', '+00:00')))
    if end_date:
        query = query.filter(ProcurementTransaction.procurement_date <= datetime.fromisoformat(end_date.replace('Z', '+00:00')))
    if risk_level and risk_level != "All":
        if "High" in risk_level or "Critical" in risk_level:
            query = query.filter(RiskAlert.severity.in_(['High', 'Critical', 'HIGH', 'CRITICAL']))
        elif "Medium" in risk_level:
            query = query.filter(RiskAlert.severity.in_(['Medium', 'MEDIUM']))
        elif "Low" in risk_level:
            query = query.filter(RiskAlert.risk_score < 40)
        
    results = query.all()
    
    f = StringIO()
    writer = csv.writer(f)
    writer.writerow(["Transaction ID", "Date", "Vendor", "Panchayat", "District", "Category", "Amount", "Status", "Risk"])
    
    for tx, v_name, p_name, dist, risk_sev, risk_score in results:
        writer.writerow([tx.transaction_id, tx.procurement_date.strftime("%Y-%m-%d"), v_name, p_name, dist, tx.procurement_category, tx.amount, tx.payment_status, f"{risk_score or 0} ({risk_sev or 'Low'})"])
        
    f.seek(0)
    return StreamingResponse(
        iter([f.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=panchayatguard_{type.replace(' ', '_')}_report.csv"}
    )
