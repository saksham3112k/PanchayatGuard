import sys
import re

with open('backend/app/routers/vendors_router.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure BaseModel is imported
if 'from pydantic import BaseModel' not in content:
    content = content.replace('from sqlalchemy.orm import Session', 'from sqlalchemy.orm import Session\nfrom pydantic import BaseModel\nimport random')

new_route = """
class VendorCreate(BaseModel):
    vendor_name: str
    category: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

@router.post("")
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    code = f"VEND-{random.randint(1000, 9999)}"
    new_vendor = Vendor(
        vendor_code=code,
        vendor_name=vendor.vendor_name,
        category=vendor.category,
        contact_email=vendor.contact_email,
        contact_phone=vendor.contact_phone,
        status="Active",
        risk_score=0,
        risk_level="Low",
        total_procurement_value=0,
        transaction_count=0
    )
    db.add(new_vendor)
    db.add(AuditLog(
        user_id=current_user.id, action="CREATE", entity_type="Vendor",
        new_value=f"Created vendor {vendor.vendor_name}"
    ))
    db.commit()
    return {"message": "Vendor created successfully", "id": new_vendor.id}
"""

if 'def create_vendor' not in content:
    content += new_route

with open('backend/app/routers/vendors_router.py', 'w', encoding='utf-8') as f:
    f.write(content)
