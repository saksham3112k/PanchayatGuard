from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.auth import get_current_user

def override_get_current_user():
    return {"id": 1, "role": "admin"}

app.dependency_overrides[get_current_user] = override_get_current_user
client = TestClient(app)

print("--- AI Insights ---")
res = client.get("/api/ai-insights")
print(res.status_code)
if res.status_code != 200: print(res.text)

print("\n--- Grievances ---")
res = client.get("/api/grievances")
print(res.status_code)
if res.status_code != 200: print(res.text)

print("\n--- Audit Logs ---")
res = client.get("/api/audit")
print(res.status_code)
if res.status_code != 200: print(res.text)
