from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..database import get_db
from ..models import AuditLog, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/audit-logs", tags=["Audit Logs"])

@router.get("/")
def get_audit_logs(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    logs = db.query(AuditLog, User.name.label("user_name"))\
             .outerjoin(User, User.id == AuditLog.user_id)\
             .order_by(desc(AuditLog.timestamp))\
             .limit(100).all()
             
    return [
        {
            "id": l.AuditLog.id,
            "timestamp": l.AuditLog.timestamp,
            "user": l.user_name or "System",
            "action": l.AuditLog.action,
            "entity_type": l.AuditLog.entity_type,
            "entity_id": l.AuditLog.entity_id,
            "details": l.AuditLog.new_value
        }
        for l in logs
    ]
