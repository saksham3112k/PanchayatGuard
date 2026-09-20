from backend.app.database import SessionLocal
from backend.app.models import RiskAlert, ProcurementTransaction, Vendor, Panchayat
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db = SessionLocal()
query = db.query(RiskAlert, ProcurementTransaction, Vendor.vendor_name, Panchayat.name.label("panchayat_name"))\
           .join(ProcurementTransaction, RiskAlert.transaction_id == ProcurementTransaction.id)\
           .join(Vendor, RiskAlert.vendor_id == Vendor.id)\
           .join(Panchayat, ProcurementTransaction.panchayat_id == Panchayat.id)\
           .limit(5)
print(query)
