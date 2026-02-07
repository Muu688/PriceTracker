from tinydb import TinyDB, Query
from product import Product

db = TinyDB('prices.json')
prices = db.table("price_checks")

def getAllRecordsFromDB():
    return prices.all()

ProductQuery = Query()

def addPriceTracker(product: Product):
    """
    Adds a 'Product' to the Database
    """
    existing = prices.get(ProductQuery.url == product.url)

    observation = {
        "price": product.price,
        "dateObserved": product.dateObserved
    }

    if existing:
        # Append to history
        history = existing.get("history", [])
        history.append(observation)

        prices.update(
            {"history": history},
            doc_ids=[existing.doc_id]
        )
    else:
        # Create new product entry
        prices.insert({
            "productName": product.productName,
            "url": product.url,
            "history": [observation]
        })

def get_most_recent_record(productName: str):
    # Work in progress - non functional - should return the most recent record
    records = prices.search(
        lambda r: r["productName"] == productName
    )

    if not records:
        return None

    records.sort(key=lambda r: r["timestamp"], reverse=True)
    return records[0]