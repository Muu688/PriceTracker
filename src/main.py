from tkinter import *
from tkinter import ttk
from database import addPriceTracker, getAllRecordsFromDB
from urllib.parse import urlparse
from datetime import datetime

from utils.fetcher import fetch_product_page
from utils.price_extractor import extract_bunnings_product_details
from product import Product

def build_tracked_products_tab(parent):
    columns = ("name", "latest_price", "last_seen")

    tree = ttk.Treeview(
        parent,
        columns=columns,
        show="headings",
        height=20
    )

    tree.heading("name", text="Product")
    tree.heading("latest_price", text="Latest Price ($)")
    tree.heading("last_seen", text="Last Seen")

    tree.column("name", width=400)
    tree.column("latest_price", width=120, anchor="e")
    tree.column("last_seen", width=120)

    tree.pack(fill="both", expand=True)
    return tree

def load_products(tree):
    tree.delete(*tree.get_children())
    records = getAllRecordsFromDB()
    for record in records:
        print(record)
        latest = record["history"][-1]
        tree.insert(
            "",
            END,
            iid=record.doc_id,
            values=(
                record["productName"],
                latest["price"],
                latest["dateObserved"]
            )
        )

def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme in ("http", "https"), parsed.netloc])

def is_bunnings_url(url: str) -> bool:
    return "bunnings.com.au" in url.lower()

def handle_add_tracking():
    url = url_var.get().strip()

    # A: empty
    if not url:
        status_label.config(text="URL cannot be empty", foreground="red")
        return

    # B: valid URL
    if not is_valid_url(url):
        status_label.config(text="Please enter a valid URL", foreground="red")
        return

    # C: Bunnings only
    if not is_bunnings_url(url):
        status_label.config(text="Only Bunnings URLs are supported", foreground="red")
        return

    status_label.config(text="Fetching product details...", foreground="black")
    tab_add.update_idletasks()

    try:
        # ---- your existing flow ----
        html = fetch_product_page(url)
        product_name, price = extract_bunnings_product_details(html)
        product = Product(
            productName=product_name,
            url=url,
            price=price,
            dateObserved=datetime.today().strftime('%Y-%m-%d'),
        )

        addPriceTracker(product)
        
        status_label.config(text="Product added successfully", foreground="green")
        load_products(tree)
        url_var.set("")

    except Exception as e:
        status_label.config(text=str(e), foreground="red")
        
root = Tk()
root.title("Price Tracker")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_add = ttk.Frame(notebook, padding=10)
tab_table = ttk.Frame(notebook, padding=10)
tab_graph = ttk.Frame(notebook, padding=10)

notebook.add(tab_add, text="Add Product")
notebook.add(tab_table, text="Tracked Products")
notebook.add(tab_graph, text="Price Trend")

ttk.Label(tab_add, text="Add product tab").pack()
ttk.Label(tab_table, text="Tracked products tab").pack()
ttk.Label(tab_graph, text="Graph tab").pack()
tree = build_tracked_products_tab(tab_table)
load_products(tree)

ttk.Label(tab_add, text="Add New Product", font=("Calibri", 16, "bold")).pack(pady=(0, 10))
ttk.Label(tab_add, text="URL to Add (Supports Bunnings Only)").pack(anchor="w")

url_var = StringVar()
url_entry = ttk.Entry(tab_add, textvariable=url_var, width=80)
url_entry.focus()
url_entry.pack(pady=5)
url_entry.bind("<Return>", lambda e: handle_add_tracking())

status_label = ttk.Label(tab_add, text="", foreground="red")
status_label.pack(anchor="w")

ttk.Button(
    tab_add,
    text="Add Price Tracking",
    command=handle_add_tracking
).pack(pady=10)
root.mainloop()