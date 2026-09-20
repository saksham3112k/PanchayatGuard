import requests
import json

api_key = "rnd_IADQemwljZhstyUBuSVEXYoUYUda"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
owner_id = "tea-danssjugekts73a2cdng"
repo = "https://github.com/saksham3112k/PanchayatGuard"
db_url = "postgresql://panchayat_db_zdb8_user:QQQtXyb1s5K2K5KEDUE4i07BWemt3Gt4@dpg-dantf1v40ujc73d46em0-a/panchayat_db_zdb8"

backend_data = {
    "type": "web_service",
    "name": "panchayatguard-api",
    "ownerId": owner_id,
    "repo": repo,
    "branch": "main",
    "env": "python",
    "plan": "free",
    "region": "oregon",
    "serviceDetails": {
        "env": "python",
        "envSpecificDetails": {
            "buildCommand": "cd backend && pip install -r requirements.txt",
            "startCommand": "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
        },
        "numInstances": 1
    }
}

res = requests.post("https://api.render.com/v1/services", headers=headers, json=backend_data)
print("Backend status:", res.status_code)
print(res.text)
