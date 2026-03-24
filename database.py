import sqlite3

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
)
""")

cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount INTEGER
)
""")

# Insert data
customers_data = [
    (1, 'Aman', 'Delhi'),
    (2, 'Riya', 'Mumbai'),
    (3, 'Rahul', 'Kolkata'),
    (4, 'Sneha', 'Bangalore')
]

orders_data = [
    (1, 1, 500),
    (2, 2, 1000),
    (3, 1, 700),
    (4, 3, 1200)
]

cursor.executemany("INSERT INTO customers VALUES (?, ?, ?)", customers_data)
cursor.executemany("INSERT INTO orders VALUES (?, ?, ?)", orders_data)

conn.commit()
conn.close()