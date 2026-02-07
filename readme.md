# 🛒 Price Tracker (Bunnings)

A lightweight desktop application for tracking product prices on **Bunnings Australia**, built with **Python**, **Tkinter**, and **TinyDB**.

The app allows users to:
- Add a Bunnings product via URL
- Automatically extract the product name and current price
- Store historical price observations
- View tracked products in a table
- Visualise price trends over time

---

## Get Started:
Requires Python 3.9.6 (Maybe it works on older, maybe it works on newer, I just developed on this version)
Run the command `pip install -r requirements.txt ` to install the required packages from pip.
Next: Run `main.py` located in the `/src` folder.
It should then pop up the GUI. It will accept only Bunnings URLs at the moment.
Some features are not yet developed, such as 
- Tracking/comparing the price against previous prices
- Sending custom alerts to the user when price drops below the most recent recorded price.
- Plotting prices to show trend
- Ability to add other links (Not Bunnings)

## 📐 High-Level Architecture

The application is split into **four clear layers**:
┌───────────────┐
│ Tkinter UI │
└───────┬───────┘
│
┌───────▼────────┐
│ Application │ (event handlers / orchestration)
│ Logic │
└───────┬────────┘
│
┌───────▼────────┐
│ Price Extractor│ (HTML → product data)
└───────┬────────┘
│
┌───────▼────────┐
│ TinyDB Storage │
└────────────────┘

This separation keeps the UI simple, the scraper robust, and the storage flexible.

---

## 🖥️ User Interface (Tkinter)

The UI is built using **Tkinter + ttk**, organised into tabs via a `Notebook`:

### Tabs
1. **Add Product**
   - Accepts a Bunnings product URL
   - Validates input
   - Triggers price extraction and storage

2. **Tracked Products**
   - Displays all tracked products
   - Shows latest price and last seen date
   - Implemented using `ttk.Treeview`

3. **Price Trend**
   - Displays historical price changes
   - Intended for matplotlib-based visualisation

The UI layer contains **no scraping or database logic** — it only coordinates user actions.

---

## 🔍 Price Extraction Logic

Note: Currently the Price extraction logic is specific to Bunnings only due
to the fact that each HTML fetched from a different domain is different.
In future, as the need arises, I will need to create a new price extraction function
for each domain (i.e Bunnings, JB-Hifi, Katmandu)
Bunnings is built using **Next.js**, which embeds all product data inside a `<script id="__NEXT_DATA__">` JSON blob.

### Key characteristics:
- Product data is **split across multiple queries**
- Product name, price, stock, and metadata are fetched separately
- There is **no single “product” object**

### Extraction strategy:
1. Parse `__NEXT_DATA__`
2. Walk `dehydratedState["queries"]`
3. Collect:
   - `name` from the product details query
   - `value` from the price query
4. Return once both are found

This makes the extractor resilient to query order changes and unrelated data.

---

## 🗃️ Data Storage (TinyDB)

Data is stored locally using **TinyDB** (JSON-backed, schema-less).
So, no need to connect to any external DB service like Mongo, since the database won't grow huge in size, 
can just store in the application.

### Schema

```json
{
  "productName": "Gerni 7000 2175PSI 2300W High Pressure Washer",
  "url": "https://www.bunnings.com.au/...",
  "history": [
    { "price": 549.0, "dateObserved": "2026-02-01" },
    { "price": 499.0, "dateObserved": "2026-02-06" }
  ]
}