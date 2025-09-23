# seed_db.py
import sqlite3

SAMPLE_PRODUCTS = [
    ("Classic Rug", "SKU-CR-001", 120, "A1-01"),
    ("Runner Rug", "SKU-RR-002", 60, "A1-02"),
    ("Persian Large", "SKU-PL-003", 30, "B2-01"),
    ("Carpet Sample Pack", "SKU-SP-004", 250, "C3-01"),
]

def seed():
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()

    # Ensure tables exist (if you used the app.py starter it already creates them)
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        sku TEXT UNIQUE,
        stock_qty INTEGER,
        location TEXT
    )''')

    # Insert sample products only if products table empty
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    if count == 0:
        for name, sku, qty, loc in SAMPLE_PRODUCTS:
            cursor.execute(
                "INSERT OR IGNORE INTO products (name, sku, stock_qty, location) VALUES (?, ?, ?, ?)",
                (name, sku, qty, loc)
            )
        conn.commit()
        print(f"Seeded {len(SAMPLE_PRODUCTS)} products.")
    else:
        print("Products table already seeded. Remove erp.db if you want a fresh DB.")

    conn.close()

if __name__ == "__main__":
    seed()
