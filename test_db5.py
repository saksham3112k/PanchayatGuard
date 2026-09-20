import sqlite3
conn = sqlite3.connect('backend/panchayatguard.db')
c = conn.cursor()
c.execute('SELECT id, vendor_name FROM vendors LIMIT 5')
print("Vendors:")
for row in c.fetchall(): print(row)

c.execute('SELECT id, name FROM panchayats LIMIT 5')
print("\nPanchayats:")
for row in c.fetchall(): print(row)
