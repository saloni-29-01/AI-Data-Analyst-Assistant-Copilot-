import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("sales.db")
c = conn.cursor()

# Create tables
c.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL,
    date TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    payment_method TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT
);
""")

# Sample data
customers = [
    (1, "Rahul Sharma", "Delhi"), (2, "Priya Singh", "Mumbai"),
    (3, "Amit Kumar", "Kolkata"), (4, "Sneha Patel", "Ahmedabad"),
    (5, "Vikram Rao", "Bangalore"), (6, "Neha Gupta", "Delhi"),
    (7, "Rohit Verma", "Chennai"), (8, "Anjali Mehta", "Pune"),
]

products = [
    (1, "Laptop", 55000), (2, "Phone", 25000), (3, "Tablet", 18000),
    (4, "Headphones", 3500), (5, "Keyboard", 1500), (6, "Mouse", 800),
]

employees = [
    (1, "Suresh Kumar", "Sales"), (2, "Meena Joshi", "HR"),
    (3, "Arun Nair", "Tech"), (4, "Pooja Iyer", "Finance"),
    (5, "Karan Malhotra", "Sales"),
]

payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"]
statuses = ["Completed", "Pending", "Failed"]

c.executemany("INSERT OR IGNORE INTO customers VALUES (?,?,?)", customers)
c.executemany("INSERT OR IGNORE INTO products VALUES (?,?,?)", products)
c.executemany("INSERT OR IGNORE INTO employees VALUES (?,?,?)", employees)

# Generate orders
for i in range(1, 51):
    cust_id = random.randint(1, 8)
    amount = round(random.uniform(500, 80000), 2)
    date = (datetime.now() - timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d")
    c.execute("INSERT OR IGNORE INTO orders VALUES (?,?,?,?)", (i, cust_id, amount, date))

# Generate order_items
for i in range(1, 101):
    c.execute("INSERT OR IGNORE INTO order_items VALUES (?,?,?,?)",
              (i, random.randint(1, 50), random.randint(1, 6), random.randint(1, 5)))

# Generate payments
for i in range(1, 51):
    c.execute("INSERT OR IGNORE INTO payments VALUES (?,?,?,?)",
              (i, i, random.choice(payment_methods), random.choice(statuses)))

conn.commit()
conn.close()
print("Database created successfully with sample data!")
