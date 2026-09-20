import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/panchayatguard.db')
print("Risk Alert:")
print(pd.read_sql_query('SELECT * FROM risk_alerts LIMIT 1', conn))
print("\nProcurement Transaction:")
print(pd.read_sql_query('SELECT id, transaction_id, vendor_id, panchayat_id FROM procurement_transactions LIMIT 1', conn))
