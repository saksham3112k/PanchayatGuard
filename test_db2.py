import sqlite3

conn = sqlite3.connect('backend/panchayatguard.db')
c = conn.cursor()
c.execute('PRAGMA table_info(risk_alerts)')
print("Risk Alerts Columns:", c.fetchall())
