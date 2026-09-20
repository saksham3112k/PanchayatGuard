import requests
import datetime
import json
import uuid

# Configuration
API_URL = "http://localhost:8000/api"
LOGIN_DATA = {"username": "admin@panchayatguard.gov.in", "password": "SecurePassword123!"}

def get_token():
    response = requests.post(f"{API_URL}/auth/login", data=LOGIN_DATA)
    if response.status_code == 200:
        return response.json()["access_token"]
    raise Exception(f"Login failed: {response.text}")

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

print("--- Testing Deterministic Risk Engine ---")

# We need to get some IDs to use. Let's get vendors and panchayats
dropdowns = requests.get(f"{API_URL}/procurement/dropdowns", headers=headers).json()
panchayat_id = dropdowns["panchayats"][0]["id"]
vendor_1 = dropdowns["vendors"][0]["id"]
vendor_2 = dropdowns["vendors"][1]["id"]
vendor_3 = dropdowns["vendors"][2]["id"]
category = dropdowns["categories"][0]

base_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
base_invoice = f"INV-{uuid.uuid4().hex[:6]}"

def create_tx(amount, unit_price, qty, v_id, cat, desc, date, inv):
    tx_id = f"TXN-TEST-{uuid.uuid4().hex[:6]}"
    payload = {
        "transaction_id": tx_id,
        "panchayat_id": panchayat_id,
        "vendor_id": v_id,
        "procurement_category": cat,
        "description": desc,
        "amount": amount,
        "quantity": qty,
        "unit_price": unit_price,
        "procurement_date": date,
        "invoice_number": inv,
        "procurement_method": "Direct Purchase",
        "payment_status": "Pending"
    }
    res = requests.post(f"{API_URL}/procurement/transactions", json=payload, headers=headers)
    if res.status_code != 200:
        print(f"Error creating TX: {res.text}")
        return None
    return res.json()

print("\n1. Test Normal Transaction (Low Risk expected)")
tx1 = create_tx(50000, 500, 100, vendor_1, category, "Normal stationary purchase", base_date, base_invoice + "-1")
print(f"Response: {tx1}")

print("\n2. Test High-Value Transaction (> 50 Lakh, should add 40 pts -> CRITICAL expected if others compound, or at least 40 Medium)")
tx2 = create_tx(5500000, 5500, 1000, vendor_2, category, "High value purchase", base_date, base_invoice + "-2")
print(f"Response: {tx2}")

print("\n3. Test Duplicate Billing (Same invoice as tx1, should add 50 pts)")
tx3 = create_tx(50000, 500, 100, vendor_1, category, "Duplicate billing attempt", base_date, base_invoice + "-1")
print(f"Response: {tx3}")

print("\n4. Test Transaction Splitting (Same vendor, same panchayat, same category within 7 days)")
tx4 = create_tx(50000, 500, 100, vendor_1, category, "Split part 2", base_date, base_invoice + "-4")
tx5 = create_tx(50000, 500, 100, vendor_1, category, "Split part 3", base_date, base_invoice + "-5")
print(f"Tx4 Response: {tx4}")
print(f"Tx5 Response (Should flag splitting + frequency): {tx5}")

print("\n5. Test Unusual Transaction Frequency (Vendor 1 already has 4 tx on the same day now)")
tx6 = create_tx(50000, 500, 100, vendor_1, category, "Frequency test", base_date, base_invoice + "-6")
print(f"Tx6 Response: {tx6}")

print("\n6. Test Price Anomaly (> 2x Category Avg)")
# Assuming average is around 500 from above txs
tx7 = create_tx(150000, 1500, 100, vendor_3, category, "Price anomaly test", base_date, base_invoice + "-7")
print(f"Tx7 Response: {tx7}")

# Verify recent alerts
print("\n--- Recent Alerts ---")
alerts = requests.get(f"{API_URL}/risk/summary", headers=headers).json()
for a in alerts.get("critical_alerts", []):
    print(f"Alert: {a['type']} (Score: {a['score']}) - {a['explanation']}")
