from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..models import User, AuditLog
from ..auth import get_current_user, get_password_hash, verify_password

router = APIRouter(prefix="/api/settings", tags=["Settings"])

class ProfileUpdate(BaseModel):
    name: str
    department: str

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

@router.put("/profile")
def update_profile(profile: ProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    old_val = f"Name: {user.name}, Dept: {user.department}"
    user.name = profile.name
    user.department = profile.department
    
    db.add(AuditLog(
        user_id=user.id, action="UPDATE", entity_type="User", entity_id=user.id,
        old_value=old_val, new_value=f"Name: {user.name}, Dept: {user.department}"
    ))
    db.commit()
    return {"message": "Profile updated successfully"}

@router.put("/password")
def update_password(pw: PasswordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not verify_password(pw.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect current password")
        
    user.password_hash = get_password_hash(pw.new_password)
    
    db.add(AuditLog(
        user_id=user.id, action="UPDATE", entity_type="User", entity_id=user.id,
        new_value="Password changed"
    ))
    db.commit()
    return {"message": "Password updated successfully"}
