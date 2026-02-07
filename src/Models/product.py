from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    productName: str
    url: str
    price: Optional[float] = None
    dateObserved: Optional[str] = None