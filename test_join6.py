from backend.app.database import SessionLocal
from backend.app.models import RiskAlert, ProcurementTransaction, Vendor, Panchayat

db = SessionLocal()
alerts = db.query(RiskAlert, ProcurementTransaction, Vendor.vendor_name, Panchayat.name.label("panchayat_name"))\
           .join(ProcurementTransaction, RiskAlert.transaction_id == ProcurementTransaction.id)\
           .join(Vendor, RiskAlert.vendor_id == Vendor.id)\
           .join(Panchayat, ProcurementTransaction.panchayat_id == Panchayat.id)\
           .all()
print(f"Total rows found: {len(alerts)}")
