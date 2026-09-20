from backend.app.database import SessionLocal
from backend.app.models import RiskAlert, ProcurementTransaction, Vendor, Panchayat

db = SessionLocal()
print(db.query(RiskAlert).count())
print(db.query(RiskAlert).join(ProcurementTransaction).count())
print(db.query(RiskAlert).join(ProcurementTransaction).join(Vendor, RiskAlert.vendor_id == Vendor.id).count())
