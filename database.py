import sqlite3


def init_db():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            name TEXT,
            target_price REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_product(url, name, target_price):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (url, name, target_price) VALUES (?, ?, ?)",
                   (url, name, target_price))
    conn.commit()
    conn.close()


def get_all_products():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_product(product_id):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def save_price(product_id, price, date):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO price_history (product_id, price, date) VALUES (?, ?, ?)",
                   (product_id, price, date))
    conn.commit()
    conn.close()