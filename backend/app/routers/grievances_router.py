from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from pydantic import BaseModel

from ..database import get_db
from ..models import Grievance, Panchayat, AuditLog
from ..auth import get_current_user

router = APIRouter(prefix="/api/grievances", tags=["Grievances"])

class GrievanceCreate(BaseModel):
    grievance_id: str
    subject: str
    description: str
    panchayat_id: int
    category: str
    submitted_by: str
    priority: str

class GrievanceUpdate(BaseModel):
    status: str

def log_audit(session: Session, user_id: int, action: str, entity_type: str, entity_id: int, details: str):
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        new_value=details
    )
    session.add(log)
    
from ..models import Notification

def create_notification(session: Session, title: str, message: str, type: str):
    notif = Notification(title=title, message=message, type=type)
    session.add(notif)
    session.commit()

@router.get("/")
def get_grievances(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(Grievance, Panchayat.name.label("panchayat_name")).join(Panchayat)
    
    if status and status != "All":
        query = query.filter(Grievance.status == status)
    if priority and priority != "All":
        query = query.filter(Grievance.priority == priority)
    if search:
        query = query.filter(Grievance.grievance_id.ilike(f"%{search}%") | Grievance.subject.ilike(f"%{search}%"))
        
    results = query.order_by(desc(Grievance.created_at)).all()
    
    return [
        {
            "id": g.Grievance.id,
            "grievance_id": g.Grievance.grievance_id,
            "subject": g.Grievance.subject,
            "description": g.Grievance.description,
            "category": g.Grievance.category,
            "submitted_by": g.Grievance.submitted_by,
            "priority": g.Grievance.priority,
            "status": g.Grievance.status,
            "date": g.Grievance.created_at,
            "panchayat_name": g.panchayat_name
        }
        for g in results
    ]

@router.post("/")
def create_grievance(grievance: GrievanceCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_g = Grievance(**grievance.dict())
    db.add(db_g)
    db.commit()
    db.refresh(db_g)
    
    log_audit(db, current_user.id, "CREATE", "Grievance", db_g.id, f"Created grievance {db_g.grievance_id}")
    create_notification(db, "New Grievance Submitted", f"Grievance {db_g.grievance_id} requires attention.", "alert")
    
    db.commit()
    return {"message": "Grievance created successfully", "id": db_g.id}

@router.put("/{id}")
def update_grievance(id: int, grievance_update: GrievanceUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_g = db.query(Grievance).filter(Grievance.id == id).first()
    if not db_g:
        raise HTTPException(status_code=404, detail="Grievance not found")
        
    db_g.status = grievance_update.status
    log_audit(db, current_user.id, "UPDATE", "Grievance", db_g.id, f"Updated grievance status to {db_g.status}")
    db.commit()
    return {"message": "Grievance updated successfully"}
