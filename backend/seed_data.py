from app.database import SessionLocal, engine, Base
from app.models import User, RoleEnum, Panchayat, Vendor, ProcurementTransaction, RiskAlert
from datetime import datetime, timedelta
import random

def seed_dashboard_data():
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(Panchayat).first():
        print("Data already seeded.")
        db.close()
        return

    admin_user = db.query(User).filter(User.role == RoleEnum.Administrator).first()
    user_id = admin_user.id if admin_user else 1

    # 1. Panchayats
    panchayats_data = [
        {"name": "Bhadora", "district": "Varanasi", "block": "Block A", "state": "Uttar Pradesh"},
        {"name": "Karanpur", "district": "Varanasi", "block": "Block B", "state": "Uttar Pradesh"},
        {"name": "Rampur", "district": "Jaunpur", "block": "Block C", "state": "Uttar Pradesh"},
        {"name": "Nandpur", "district": "Ghazipur", "block": "Block D", "state": "Uttar Pradesh"},
        {"name": "Devgram", "district": "Azamgarh", "block": "Block E", "state": "Uttar Pradesh"},
    ]
    panchayats = []
    for pd in panchayats_data:
        p = Panchayat(**pd)
        db.add(p)
        panchayats.append(p)
    db.commit()

    # 2. Vendors
    vendors_data = [
        {"vendor_code": "V001", "vendor_name": "Sharma Construction", "category": "Construction", "risk_score": 92.0, "risk_level": "High Risk", "total_procurement_value": 52400000, "transaction_count": 48},
        {"vendor_code": "V002", "vendor_name": "R.K. Enterprises", "category": "Supplies", "risk_score": 87.0, "risk_level": "High Risk", "total_procurement_value": 21200000, "transaction_count": 36},
        {"vendor_code": "V003", "vendor_name": "Jai Maa Traders", "category": "Supplies", "risk_score": 68.0, "risk_level": "Medium Risk", "total_procurement_value": 10800000, "transaction_count": 25},
        {"vendor_code": "V004", "vendor_name": "Grameen Supplies", "category": "Supplies", "risk_score": 61.0, "risk_level": "Medium Risk", "total_procurement_value": 9600000, "transaction_count": 32},
        {"vendor_code": "V005", "vendor_name": "Patel Infra Works", "category": "Construction", "risk_score": 33.0, "risk_level": "Low Risk", "total_procurement_value": 7400000, "transaction_count": 18},
    ]
    vendors = []
    for vd in vendors_data:
        v = Vendor(**vd, registration_number="REG"+str(random.randint(1000, 9999)), district="Varanasi", state="Uttar Pradesh", contact_email="contact@example.com", contact_phone="9999999999")
        db.add(v)
        vendors.append(v)
    db.commit()

    # 3. Procurement Transactions & Risk Alerts
    categories = ["Construction & Civil Work", "Supplies & Materials", "Machinery & Equipment", "Furniture & Fixtures", "Solar / Electrical", "Others"]
    
    # We want a trend over 12 months (Jan - Dec 2024)
    base_date = datetime(2024, 1, 1)
    
    # Predefined high risk transactions to match UI
    specific_txs = [
        {"desc": "Road Construction Work", "p_idx": 0, "v_idx": 0, "amount": 1840000, "cat": "Construction & Civil Work", "date": datetime(2024, 9, 12), "alert": "Duplicate Billing", "score": 92},
        {"desc": "Pipe Supply Purchase", "p_idx": 1, "v_idx": 1, "amount": 750000, "cat": "Supplies & Materials", "date": datetime(2024, 9, 10), "alert": "Price Anomaly", "score": 87},
        {"desc": "School Building Repair", "p_idx": 2, "v_idx": 2, "amount": 1220000, "cat": "Construction & Civil Work", "date": datetime(2024, 9, 8), "alert": "Single Vendor", "score": 68},
        {"desc": "Furniture Supply", "p_idx": 3, "v_idx": 3, "amount": 480000, "cat": "Furniture & Fixtures", "date": datetime(2024, 9, 5), "alert": "Unusual Split", "score": 64},
        {"desc": "Solar Light Installation", "p_idx": 4, "v_idx": 4, "amount": 615000, "cat": "Solar / Electrical", "date": datetime(2024, 9, 2), "alert": None, "score": 28},
    ]

    tx_id_counter = 1000
    for stx in specific_txs:
        tx = ProcurementTransaction(
            transaction_id=f"TXN{tx_id_counter}",
            panchayat_id=panchayats[stx["p_idx"]].id,
            vendor_id=vendors[stx["v_idx"]].id,
            procurement_category=stx["cat"],
            description=stx["desc"],
            amount=stx["amount"],
            quantity=1,
            unit_price=stx["amount"],
            procurement_date=stx["date"],
            invoice_number=f"INV{tx_id_counter}",
            payment_status="Completed",
            procurement_method="Direct",
            created_by=user_id
        )
        db.add(tx)
        db.commit()
        
        if stx["alert"]:
            alert = RiskAlert(
                transaction_id=tx.id,
                vendor_id=vendors[stx["v_idx"]].id,
                alert_type=stx["alert"],
                risk_score=stx["score"],
                severity="High" if stx["score"] >= 80 else ("Medium" if stx["score"] >= 50 else "Low"),
                explanation=f"Detected {stx['alert']} anomaly."
            )
            db.add(alert)
        tx_id_counter += 1

    # Bulk generic transactions to fill out stats
    # To reach ~12.48 Cr, we need to generate remaining data appropriately.
    # Total from UI: 12.48 Cr = 124,800,000
    current_sum = sum([stx["amount"] for stx in specific_txs])
    target_sum = 124800000
    
    # Add random transactions spread across the year
    # Risk trend in UI peaks in Sept.
    months_risk_weights = [15, 25, 28, 45, 35, 48, 40, 50, 72, 60, 40, 20] # Jan-Dec weights for risk
    
    while current_sum < target_sum:
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        tx_date = datetime(2024, month, day)
        
        amount = random.randint(50000, 500000)
        if current_sum + amount > target_sum:
            amount = target_sum - current_sum
            
        v = random.choice(vendors)
        p = random.choice(panchayats)
        cat = random.choice(categories)
        
        tx = ProcurementTransaction(
            transaction_id=f"TXN{tx_id_counter}",
            panchayat_id=p.id,
            vendor_id=v.id,
            procurement_category=cat,
            description=f"General {cat} purchase",
            amount=amount,
            quantity=1,
            unit_price=amount,
            procurement_date=tx_date,
            invoice_number=f"INV{tx_id_counter}",
            payment_status="Completed",
            procurement_method="Tender",
            created_by=user_id
        )
        db.add(tx)
        db.commit()
        
        # Randomly generate risk alerts to match the risk curve
        risk_chance = months_risk_weights[month-1]
        if random.randint(1, 100) < (risk_chance / 2): # roughly scale down so not everything is risky
            base_score = risk_chance + random.randint(-10, 20)
            score = min(max(base_score, 10), 99)
            alert = RiskAlert(
                transaction_id=tx.id,
                vendor_id=v.id,
                alert_type=random.choice(["Price Anomaly", "Duplicate Billing", "Single Vendor", "Unusual Split"]),
                risk_score=score,
                severity="High" if score >= 80 else ("Medium" if score >= 50 else "Low"),
                explanation="Automated system detection.",
                detected_at=tx_date
            )
            db.add(alert)

        current_sum += amount
        tx_id_counter += 1

    db.commit()
    db.close()
    print("Database seeded with realistic Phase 2 data.")

if __name__ == "__main__":
    seed_dashboard_data()
