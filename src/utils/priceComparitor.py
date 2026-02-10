from Models.product import Product

def comparePrice(new: Product, old: Product) -> bool:
    """
    Returns True if the new price is lower than the old price
    """
    if old.price is None:
        return False
    return new.price < old.price