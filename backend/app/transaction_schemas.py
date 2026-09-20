from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class TransactionBase(BaseModel):
    transaction_id: str
    panchayat_id: int
    vendor_id: int
    procurement_category: str
    description: str
    amount: float = Field(..., gt=0)
    quantity: int = Field(default=1, gt=0)
    unit_price: float = Field(..., gt=0)
    procurement_date: datetime
    invoice_number: str
    tender_number: Optional[str] = None
    payment_status: str
    procurement_method: str

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    panchayat_id: Optional[int] = None
    vendor_id: Optional[int] = None
    procurement_category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[float] = Field(None, gt=0)
    procurement_date: Optional[datetime] = None
    invoice_number: Optional[str] = None
    tender_number: Optional[str] = None
    payment_status: Optional[str] = None
    procurement_method: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    panchayat_name: Optional[str] = None
    vendor_name: Optional[str] = None
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None

    class Config:
        from_attributes = True

class PaginatedTransactionResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[TransactionResponse]
    summary: Any = None
