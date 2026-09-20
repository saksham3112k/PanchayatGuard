import sqlite3
conn = sqlite3.connect('panchayat.db')
cursor = conn.cursor()
cursor.execute("UPDATE users SET name = 'System Administrator' WHERE name LIKE '%Saksham%'")
conn.commit()
print(f"Updated {cursor.rowcount} rows")
conn.close()
