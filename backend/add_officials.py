from app.database import SessionLocal
from app.models import User, RoleEnum
from app.auth import get_password_hash

db = SessionLocal()
officials = [
    {"name": "Ramesh Kumar (BDO)", "email": "ramesh.kumar@gov.in", "role": RoleEnum.Administrator},
    {"name": "Priya Sharma (Auditor)", "email": "priya.sharma@gov.in", "role": RoleEnum.Auditor},
    {"name": "Vikram Singh (DM)", "email": "dm.vikram@gov.in", "role": RoleEnum.Viewer}
]

for u in officials:
    existing = db.query(User).filter(User.email == u['email']).first()
    if not existing:
        new_user = User(
            name=u['name'],
            email=u['email'],
            password_hash=get_password_hash('SecurePassword123!'),
            role=u['role'],
            department="District Administration"
        )
        db.add(new_user)
db.commit()
db.close()
print('Added officials')
