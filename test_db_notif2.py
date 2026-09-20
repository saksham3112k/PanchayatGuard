import sqlite3

conn = sqlite3.connect('backend/panchayatguard.db')
c = conn.cursor()
c.execute('SELECT id, created_at FROM notifications LIMIT 10')
for row in c.fetchall():
    print(row)
