from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta
from .models import ProcurementTransaction, Vendor

def analyze_transaction_risk(tx, session: Session):
    score = 0
    signals = []
    
    # 1. High-value transaction
    if tx.amount >= 5000000:
        score += 40
        signals.append({"type": "HIGH_VALUE", "severity": "CRITICAL", "explanation": "Transaction exceeds ₹ 50 Lakh."})
    elif tx.amount >= 1000000:
        score += 20
        signals.append({"type": "HIGH_VALUE", "severity": "HIGH", "explanation": "Transaction exceeds ₹ 10 Lakh."})
        
    # 2. Price Anomaly
    # Get average unit price for this category
    avg_price = session.query(func.avg(ProcurementTransaction.unit_price))\
                       .filter(ProcurementTransaction.procurement_category == tx.procurement_category)\
                       .filter(ProcurementTransaction.id != getattr(tx, 'id', -1))\
                       .scalar()
    
    if avg_price and avg_price > 0:
        ratio = tx.unit_price / avg_price
        if ratio > 2.0:
            score += 35
            signals.append({"type": "PRICE_ANOMALY", "severity": "HIGH", "explanation": f"Unit price is {ratio:.1f}x higher than category average."})
        elif ratio > 1.5:
            score += 15
            signals.append({"type": "PRICE_ANOMALY", "severity": "MEDIUM", "explanation": f"Unit price is {ratio:.1f}x higher than category average."})
            
    # 3. Transaction Splitting
    # Transactions to the same vendor, from same panchayat, in same category, within 7 days
    recent_split_count = session.query(ProcurementTransaction).filter(
        ProcurementTransaction.vendor_id == tx.vendor_id,
        ProcurementTransaction.panchayat_id == tx.panchayat_id,
        ProcurementTransaction.procurement_category == tx.procurement_category,
        ProcurementTransaction.procurement_date >= (tx.procurement_date - timedelta(days=7)),
        ProcurementTransaction.procurement_date <= (tx.procurement_date + timedelta(days=7)),
        ProcurementTransaction.id != getattr(tx, 'id', -1)
    ).count()
    
    if recent_split_count >= 2:
        score += 45
        signals.append({"type": "TRANSACTION_SPLITTING", "severity": "CRITICAL", "explanation": f"Found {recent_split_count} similar transactions within a 7-day window."})
    elif recent_split_count == 1:
        score += 25
        signals.append({"type": "TRANSACTION_SPLITTING", "severity": "HIGH", "explanation": "Possible transaction splitting detected (1 similar transaction within 7 days)."})

    # 4. Unusual Transaction Frequency
    # Vendor has > 3 transactions across anywhere in the same day
    same_day_count = session.query(ProcurementTransaction).filter(
        ProcurementTransaction.vendor_id == tx.vendor_id,
        func.date(ProcurementTransaction.procurement_date) == tx.procurement_date.date(),
        ProcurementTransaction.id != getattr(tx, 'id', -1)
    ).count()
    
    if same_day_count >= 3:
        score += 30
        signals.append({"type": "UNUSUAL_FREQUENCY", "severity": "HIGH", "explanation": f"Vendor has {same_day_count} other transactions on the same day."})

    # 5. Duplicate Billing (same invoice number from same vendor)
    if tx.invoice_number:
        dup_invoice = session.query(ProcurementTransaction).filter(
            ProcurementTransaction.vendor_id == tx.vendor_id,
            ProcurementTransaction.invoice_number == tx.invoice_number,
            ProcurementTransaction.id != getattr(tx, 'id', -1)
        ).first()
        if dup_invoice:
            score += 50
            signals.append({"type": "DUPLICATE_BILLING", "severity": "CRITICAL", "explanation": f"Invoice number '{tx.invoice_number}' has already been used."})

    # 6. Vendor Concentration
    # Is this vendor taking > 50% of this panchayat's total budget?
    panchayat_total = session.query(func.sum(ProcurementTransaction.amount))\
                             .filter(ProcurementTransaction.panchayat_id == tx.panchayat_id).scalar() or 0
    panchayat_vendor_total = session.query(func.sum(ProcurementTransaction.amount))\
                                    .filter(ProcurementTransaction.panchayat_id == tx.panchayat_id, ProcurementTransaction.vendor_id == tx.vendor_id).scalar() or 0
    
    new_p_total = panchayat_total + tx.amount
    new_v_total = panchayat_vendor_total + tx.amount
    
    if new_p_total > 500000 and (new_v_total / new_p_total) > 0.5:
        score += 20
        signals.append({"type": "VENDOR_CONCENTRATION", "severity": "MEDIUM", "explanation": f"Vendor controls >50% of Panchayat's total procurement value."})

    # Cap score at 100
    final_score = min(score, 100)
    
    # Determine level
    if final_score <= 39:
        level = "Low"
    elif final_score <= 69:
        level = "Medium"
    elif final_score <= 84:
        level = "High"
    else:
        level = "Critical"
        
    return {
        "risk_score": final_score,
        "risk_level": level,
        "signals": signals
    }
