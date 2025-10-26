import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import json 
import os
import pathlib # <-- NEW IMPORT

# --- 1. App & Database Setup ---
app = Flask(__name__)

# --- NEW DATABASE PATH ---
# Get the user's AppData folder (e.g., C:\Users\YourName\AppData\Roaming)
app_data_folder = os.getenv('APPDATA') or os.path.expanduser('~')
# Create a new folder inside it for our app
database_folder = pathlib.Path(app_data_folder) / "StockManager"
database_folder.mkdir(exist_ok=True) # Create the folder if it doesn't exist
# Define the full path to the database
DATABASE = str(database_folder / "inventory.db")
print(f"Database will be stored at: {DATABASE}")
# --- END NEW PATH ---

def get_db():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DATABASE) # This now uses the new path
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the 'products' table if it doesn't exist."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                style TEXT NOT NULL,
                color TEXT NOT NULL,
                size TEXT NOT NULL,
                quantity INTEGER NOT NULL
            );
        ''')
        db.commit()
        print("Database initialized.")

# --- 3. Application Routes (The "Logic") ---
# (All your @app.route functions are unchanged)
@app.route('/')
def index():
    """Main dashboard page with stats and graph."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    db.close()
    total_stock = 0
    low_stock_items = []
    stock_by_style = {} 
    for p in products:
        total_stock += p['quantity']
        if p['quantity'] <= 10:
            low_stock_items.append(p)
        style = p['style']
        quantity = p['quantity']
        if style in stock_by_style:
            stock_by_style[style] += quantity
        else:
            stock_by_style[style] = quantity
    total_products = len(products)
    low_stock_count = len(low_stock_items)
    graph_labels = list(stock_by_style.keys())
    graph_data = list(stock_by_style.values())
    return render_template('index.html', 
                           total_stock=total_stock, 
                           total_products=total_products, 
                           low_stock_count=low_stock_count, 
                           low_stock_items=low_stock_items,
                           graph_labels=json.dumps(graph_labels),
                           graph_data=json.dumps(graph_data)
                           )

@app.route('/inventory')
def inventory():
    """Page to display and manage all inventory."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products ORDER BY name, style, color, size")
    products = cursor.fetchall()
    db.close()
    all_names = set()
    all_styles = set()
    all_colors = set()
    all_sizes = set()
    for p in products:
        all_names.add(p['name'])
        all_styles.add(p['style'])
        all_colors.add(p['color'])
        all_sizes.add(p['size'])
    return render_template('inventory.html', 
                           products=products,
                           all_names=all_names,
                           all_styles=all_styles,
                           all_colors=all_colors,
                           all_sizes=all_sizes
                           )

@app.route('/add', methods=['POST'])
def add_product():
    """Handles the 'Add New Product' form submission."""
    name = request.form['name']
    style = request.form['style']
    color = request.form['color']
    size = request.form['size']
    dozens = int(request.form['dozens'] or 0)
    pieces = int(request.form['pieces'] or 0)
    initial_quantity_in_pieces = (dozens * 12) + pieces
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO products (name, style, color, size, quantity) VALUES (?, ?, ?, ?, ?)",
        (name, style, color, size, initial_quantity_in_pieces)
    )
    db.commit()
    db.close()
    return redirect(url_for('inventory'))

@app.route('/update', methods=['POST'])
def update_stock():
    """Handles the 'Update Stock Level' form submission."""
    product_id = request.form['product_id']
    dozens_change = int(request.form['dozens'] or 0)
    pieces_change = int(request.form['pieces'] or 0)
    total_change_in_pieces = (dozens_change * 12) + pieces_change
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE products SET quantity = max(0, quantity + ?) WHERE id = ?",
        (total_change_in_pieces, product_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('inventory'))

@app.route('/delete', methods=['POST'])
def delete_product():
    """Handles the 'Delete' button submission."""
    product_id = request.form['product_id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    db.close()
    return redirect(url_for('inventory'))