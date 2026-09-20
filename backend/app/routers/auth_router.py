from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from .. import schemas, models, database, auth

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    
    # Audit log
    audit_log = models.AuditLog(
        user_id=user.id,
        action="LOGIN",
        entity_type="User",
        entity_id=user.id,
        new_value="User logged in"
    )
    db.add(audit_log)
    db.commit()
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.post("/logout")
def logout(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="LOGOUT",
        entity_type="User",
        entity_id=current_user.id,
        new_value="User logged out"
    )
    db.add(audit_log)
    db.commit()
    return {"message": "Successfully logged out"}
