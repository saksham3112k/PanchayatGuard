import sqlite3

conn = sqlite3.connect('backend/panchayatguard.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM risk_alerts')
print("Risk Alerts:", c.fetchone()[0])
