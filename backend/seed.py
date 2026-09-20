from app.database import SessionLocal, engine, Base
from app.models import User, RoleEnum
from app.auth import get_password_hash
import sys

def seed_users():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    users = [
        {"name": "Admin User", "email": "admin@panchayatguard.gov.in", "role": RoleEnum.Administrator},
        {"name": "Analyst User", "email": "analyst@panchayatguard.gov.in", "role": RoleEnum.Analyst},
        {"name": "Auditor User", "email": "auditor@panchayatguard.gov.in", "role": RoleEnum.Auditor},
        {"name": "Viewer User", "email": "viewer@panchayatguard.gov.in", "role": RoleEnum.Viewer},
    ]
    
    for u in users:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            new_user = User(
                name=u["name"],
                email=u["email"],
                password_hash=get_password_hash("SecurePassword123!"),
                role=u["role"],
                department="Central"
            )
            db.add(new_user)
            print(f"Created {u['email']}")
        else:
            print(f"User {u['email']} already exists.")
            
    db.commit()
    db.close()

if __name__ == "__main__":
    print("Seeding database...")
    seed_users()
    print("Seeding complete.")
