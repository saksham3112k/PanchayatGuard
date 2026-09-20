import sqlite3
conn = sqlite3.connect('panchayatguard.db')
cursor = conn.cursor()
cursor.execute("UPDATE users SET name = 'System Administrator' WHERE name LIKE '%Saksham%'")
conn.commit()
print(f"Updated {cursor.rowcount} user(s)")

# Let's add more realistic grievances
grievances_data = [
    ("GR-2024-001", "Delay in payment for solar panels", "Vendor complaining about a 3 month delay for solar panels delivered to Gram Panchayat.", 1, "Payment Delay", "vendor@example.com", "Open", "High"),
    ("GR-2024-002", "Quality of cement supplied is poor", "The recent batch of cement bags provided for the community hall construction were hardened.", 2, "Quality Issue", "sarpanch@example.com", "Under Review", "High"),
    ("GR-2024-003", "Missing items in medical supply delivery", "Invoice claims 500 items but only 450 were received at the primary health center.", 1, "Missing Goods", "health.officer@gov.in", "Resolved", "Medium"),
    ("GR-2024-004", "Suspicious duplicate billing", "Noticed two invoices with the exact same amount and items submitted by the same vendor within 3 days.", 3, "Fraud/Corruption", "auditor@gov.in", "Under Review", "Critical"),
    ("GR-2024-005", "Unresponsive vendor for maintenance", "Vendor is not responding to calls for the RO water plant maintenance as per the AMC contract.", 1, "Contract Violation", "panchayat.sec@gov.in", "Open", "Medium"),
    ("GR-2024-006", "Overpricing of computer equipment", "The laptops supplied are billed at 2x the market rate. Requesting an audit of this transaction.", 2, "Overpricing", "vigilance@gov.in", "Open", "High")
]

for g in grievances_data:
    try:
        cursor.execute('''INSERT INTO grievances 
                       (grievance_id, subject, description, panchayat_id, category, submitted_by, status, priority) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', g)
    except Exception as e:
        print(f"Skipping {g[0]} due to {e}")
conn.commit()
print("Added extra grievances")

conn.close()
