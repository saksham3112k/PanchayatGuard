from app.database import SessionLocal
from app.models import User
from app.auth import create_access_token
import requests

db = SessionLocal()
user = db.query(User).filter(User.email == 'admin@panchayatguard.gov.in').first()
token = create_access_token({"sub": str(user.id)})

res = requests.post(
    'http://127.0.0.1:8000/api/grievances/', 
    json={'grievance_id': 'GRV-9999', 'subject': 'Test', 'description': 'Test', 'panchayat_id': 1, 'category': 'Delay', 'submitted_by': 'Test', 'priority': 'Low'},
    headers={'Authorization': f'Bearer {token}'}
)
print(res.status_code)
print(res.text)
