from datetime import datetime
from typing import Optional
from tinydb import TinyDB, Query
from Models.product import Product

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

def get_most_recent_record(productName: str) -> Optional[Product]:
    record = prices.get(ProductQuery.productName == productName)

    if not record:
        return None

    history = record.get("history", [])
    if not history:
        return None

    latest = history[-1]  # append-only = most recent

    return Product(
        productName=record["productName"],
        url=record["url"],
        price=latest["price"],
        dateObserved=latest["dateObserved"]
    )