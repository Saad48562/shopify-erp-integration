from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

# ------------------ DATABASE SETUP ------------------
# Initialize SQLite DB (ERP Mock)
def init_db():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    # Products table
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        sku TEXT UNIQUE,
        stock_qty INTEGER,
        location TEXT
    )''')
    # Orders table
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shopify_order_id TEXT,
        status TEXT,
        created_at TEXT
    )''')
    # Order items
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        qty INTEGER
    )''')
    conn.commit()
    conn.close()

init_db()

# ------------------ ERP INVENTORY APIs ------------------
@app.route('/inventory', methods=['GET'])
def get_inventory():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

@app.route('/inventory/update', methods=['POST'])
def update_inventory():
    data = request.get_json()
    sku = data['sku']
    qty = data['qty']
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET stock_qty=? WHERE sku=?", (qty, sku))
    conn.commit()
    conn.close()
    return jsonify({"message": "Inventory updated"})

# ------------------ SHOPIFY ORDER WEBHOOK ------------------
@app.route('/shopify/order', methods=['POST'])
def shopify_order_webhook():
    data = request.get_json()
    shopify_order_id = data.get("id")
    line_items = data.get("line_items", [])

    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (shopify_order_id, status, created_at) VALUES (?, ?, datetime('now'))",
                   (shopify_order_id, "NEW"))
    order_id = cursor.lastrowid

    for item in line_items:
        sku = item.get("sku")
        qty = item.get("quantity")
        cursor.execute("SELECT id, stock_qty FROM products WHERE sku=?", (sku,))
        product = cursor.fetchone()
        if product:
            product_id, stock_qty = product
            # Deduct stock
            new_qty = max(stock_qty - qty, 0)
            cursor.execute("UPDATE products SET stock_qty=? WHERE id=?", (new_qty, product_id))
            cursor.execute("INSERT INTO order_items (order_id, product_id, qty) VALUES (?, ?, ?)",
                           (order_id, product_id, qty))

    conn.commit()
    conn.close()

    return jsonify({"message": "Order saved to ERP and stock updated"})

# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True)
