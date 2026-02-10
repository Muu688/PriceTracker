from Models.product import Product
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class PriceComparison:
    old_price: Optional[float]
    new_price: float
    onSale: bool
    difference: Optional[float] = None


from Models.product import Product

def compare_price(new: Product, old: Product) -> PriceComparison:
    if old.price is None:
        return PriceComparison(
            old_price=None,
            new_price=new.price,
            onSale=False,
            difference=None
        )

    difference = old.price - new.price
    return PriceComparison(
        old_price=old.price,
        new_price=new.price,
        onSale=new.price < old.price,
        difference=difference
    )