import sqlite3

conn = sqlite3.connect('backend/panchayatguard.db')
c = conn.cursor()
c.execute('SELECT id, transaction_id, vendor_id FROM risk_alerts LIMIT 5')
print("Risk Alerts:")
for row in c.fetchall():
    print(row)

c.execute('SELECT id, transaction_id, vendor_id, panchayat_id FROM procurement_transactions LIMIT 5')
print("\nProcurement Transactions:")
for row in c.fetchall():
    print(row)
