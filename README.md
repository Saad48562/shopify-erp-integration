# Shopify ↔ ERP Integration (Demo)

## Setup
1. python -m venv venv
2. source venv/bin/activate   # or .\venv\Scripts\activate (Windows)
3. pip install -r requirements.txt
4. python seed_db.py
5. python app.py

## Endpoints
- GET /inventory
- POST /inventory/update  (JSON: { "sku":"...", "qty": ... })
- POST /shopify/order     (Shopify-like order webhook)

## Notes
- Use ngrok to expose http://localhost:5000 for webhook testing.
- Do not commit erp.db or secrets to Git.
