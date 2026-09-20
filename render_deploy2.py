import requests
import json
import secrets

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
        "envSpecificDetails": {
            "buildCommand": "cd backend && pip install -r requirements.txt",
            "startCommand": "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
        },
        "numInstances": 1
    },
    "envVars": [
        {"key": "DATABASE_URL", "value": db_url},
        {"key": "SECRET_KEY", "value": secrets.token_hex(32)},
        {"key": "CORS_ORIGINS", "value": "*"}
    ]
}

res = requests.post("https://api.render.com/v1/services", headers=headers, json=backend_data)
print("Backend status:", res.status_code)
if res.status_code != 201:
    print(res.text)
    exit(1)
backend = res.json()
backend_id = backend['id']
backend_url = backend['service']['url']
print("Backend URL:", backend_url)

frontend_data = {
    "type": "static_site",
    "name": "panchayatguard-web",
    "ownerId": owner_id,
    "repo": repo,
    "branch": "main",
    "env": "static",
    "plan": "free",
    "region": "oregon",
    "serviceDetails": {
        "buildCommand": "cd frontend && npm install && npm run build",
        "publishPath": "frontend/dist",
        "pullRequestPreviewsEnabled": "no"
    },
    "envVars": [
        {"key": "VITE_API_URL", "value": backend_url + "/api"}
    ]
}

res = requests.post("https://api.render.com/v1/services", headers=headers, json=frontend_data)
print("Frontend status:", res.status_code)
if res.status_code != 201:
    print(res.text)
    exit(1)
frontend = res.json()
frontend_id = frontend['id']
frontend_url = frontend['service']['url']
print("Frontend URL:", frontend_url)

backend_update = {
    "envVars": [
        {"key": "DATABASE_URL", "value": db_url},
        {"key": "SECRET_KEY", "value": secrets.token_hex(32)},
        {"key": "CORS_ORIGINS", "value": frontend_url}
    ]
}
res = requests.put(f"https://api.render.com/v1/services/{backend_id}/env-vars", headers=headers, json=backend_update)
print("Backend update status:", res.status_code)
