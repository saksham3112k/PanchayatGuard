import sqlite3

conn = sqlite3.connect('backend/panchayatguard.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS grievances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grievance_id VARCHAR UNIQUE,
    subject VARCHAR,
    description TEXT,
    panchayat_id INTEGER,
    category VARCHAR,
    submitted_by VARCHAR,
    priority VARCHAR,
    status VARCHAR DEFAULT 'Open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(panchayat_id) REFERENCES panchayats(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR,
    message TEXT,
    type VARCHAR,
    is_read BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
print("Tables created successfully.")
