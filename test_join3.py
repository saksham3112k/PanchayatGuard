import sqlite3
conn = sqlite3.connect('backend/panchayatguard.db')
c = conn.cursor()
c.execute('''
SELECT risk_alerts.id, risk_alerts.transaction_id, risk_alerts.vendor_id
FROM risk_alerts 
JOIN procurement_transactions ON risk_alerts.transaction_id = procurement_transactions.id 
JOIN vendors ON risk_alerts.vendor_id = vendors.id 
JOIN panchayats ON procurement_transactions.panchayat_id = panchayats.id
LIMIT 5
''')
print("Joined rows:", c.fetchall())
