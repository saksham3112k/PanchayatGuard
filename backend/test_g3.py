from app.database import SessionLocal
from app.models import User
from app.auth import create_access_token
import requests

db = SessionLocal()
user = db.query(User).filter(User.email == 'admin@panchayatguard.gov.in').first()
token = create_access_token({"sub": user.email})

payload = {
    'subject': 'Test UI',
    'description': 'Desc',
    'panchayat_id': 1,
    'category': 'Corruption',
    'priority': 'High',
    'submitted_by': 'User',
    'grievance_id': 'GRV-1234'
}

res = requests.post(
    'http://127.0.0.1:8000/api/grievances/', 
    json=payload,
    headers={'Authorization': f'Bearer {token}'}
)
print(res.status_code)
print(res.text)
