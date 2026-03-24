import sqlite3

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Show tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Show data
cursor.execute("SELECT * FROM customers")
print("Customers:", cursor.fetchall())

conn.close()