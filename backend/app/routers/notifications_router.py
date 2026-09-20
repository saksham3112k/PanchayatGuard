from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..database import get_db
from ..models import Notification
from ..auth import get_current_user

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])

@router.get("/")
def get_notifications(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    notifs = db.query(Notification).order_by(desc(Notification.created_at)).limit(20).all()
    unread_count = db.query(Notification).filter(Notification.is_read == 0).count()
    return {
        "unread_count": unread_count,
        "notifications": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "type": n.type,
                "is_read": bool(n.is_read),
                "created_at": n.created_at
            } for n in notifs
        ]
    }

@router.put("/{id}/read")
def mark_read(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    n = db.query(Notification).filter(Notification.id == id).first()
    if n:
        n.is_read = 1
        db.commit()
    return {"message": "Marked as read"}

@router.put("/read-all")
def mark_all_read(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db.query(Notification).filter(Notification.is_read == 0).update({"is_read": 1})
    db.commit()
    return {"message": "All marked as read"}
