import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/panchayatguard.db')
print(pd.read_sql_query('SELECT * FROM notifications', conn))
