OVERVIEW

This project simulates an integration between Shopify and an ERP warehouse system.
It’s designed to demonstrate how real-world 3PL and warehouse operations can sync data between eCommerce and ERP backends using Python, Flask, and APIs.
When a Shopify order is placed, the system:
 
*  Automatically receives the order through a Shopify webhook.
*  Saves the order in a local ERP database.
*  Updates warehouse stock levels.
*  Exposes API endpoints for inventory management and updates.

TECH STACK

*  Backend: Python (Flask)
*  Database: SQLite
*  API Tools: Postman, Shopify Webhooks, REST API
*  Local Testing: Ngrok
*  Version Control: Git & GitHub

FEATURES

*  REST API for ERP warehouse management
*  Shopify webhook integration for order synchronization
*  Automatic stock deduction on order receipt
*  Local ERP database with seeded products
*  Ready for extension (putaway, picking, goods receipt, and 3PL logic)

SETUP INSTRUCTIONS

1. Clone the repository
git clone https://github.com/YOUR_USERNAME/shopify-erp-integration.git
cd shopify-erp-integration

2. Set up virtual environment
python -m venv venv
.\venv\Scripts\activate    # Windows
# or
source venv/bin/activate   # Mac/Linux

3. Install dependencies
pip install -r requirements.txt

4. Seed the database
python seed_db.py

5. Run the Flask app
python app.py

6. (Optional) Expose to internet via ngrok
ngrok http 5000

API ENDPOINTS

Endpoint	            Method	    Description	Example                                 Input
/inventory	          GET	        View all products in ERP inventory	                  —
/inventory/update     POST	      Update stock quantity	                  {"sku":"SKU-CR-001","qty":110}
/shopify/order	      POST	      Receive Shopify order (webhook)              Shopify order payload
