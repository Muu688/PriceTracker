import json
import logging
from typing import Optional, Tuple
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class PriceNotFoundError(Exception):
    pass

def extract_bunnings_product_details(html: str) -> tuple[str, float]:
    soup = BeautifulSoup(html, "html.parser")

    script = soup.find("script", id="__NEXT_DATA__", type="application/json")
    if not script or not script.string:
        raise PriceNotFoundError("__NEXT_DATA__ not found")

    data = json.loads(script.string)

    dehydrated = (
        data
        .get("props", {})
        .get("pageProps", {})
        .get("dehydratedState", {})
    )

    product_name = None
    price_value = None

    for query in dehydrated.get("queries", []):
        state = query.get("state", {})
        data_obj = state.get("data")

        if not isinstance(data_obj, dict):
            continue

        # Product name
        if not product_name and "name" in data_obj:
            product_name = data_obj["name"]

        # Price
        if not price_value and "value" in data_obj and "formattedValue" in data_obj:
            price_value = data_obj["value"]

        if product_name and price_value is not None:
            return product_name, float(price_value)

    raise PriceNotFoundError("Could not extract product name and price")
