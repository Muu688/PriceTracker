import json
import logging
from typing import Optional, Tuple
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class PriceNotFoundError(Exception):
    pass

def extractor(url: str, html: str):
    if ("bunnings.com.au" in url.lower()):
        return extract_bunnings_product_details(html)
    elif("jbhifi.com.au" in url.lower()):
        return extract_jbhifi_product_details(html)
    else:
        print("Error. URL Unsupported")

def extract_jbhifi_product_details(html: str) -> tuple[str, float]:
    soup = BeautifulSoup(html, "html.parser")

    # Find script containing Shopify meta object
    scripts = soup.find_all("script")

    for script in scripts:
        if script.string and "var meta =" in script.string:
            match = re.search(r"var meta = ({.*?});", script.string, re.DOTALL)
            if not match:
                continue

            meta_json = match.group(1)
            data = json.loads(meta_json)

            product = data.get("product")
            if not product:
                continue

            variants = product.get("variants", [])
            if not variants:
                continue

            variant = variants[0]

            title = variant.get("name")
            price_cents = variant.get("price")

            if title and price_cents is not None:
                return title, price_cents / 100

    raise PriceNotFoundError("Could not extract product details from Shopify meta block")

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
