from urllib.parse import urlparse

PRODUCT_URL = "https://www.bunnings.com.au/gerni-7000-2175psi-2300w-high-pressure-washer_p0235520"

REQUEST_TIMEOUT_SECONDS = 10

USER_AGENT = (
    "Mozilla/5.0 (compatible; PriceTracker/1.0; +https://example.com/bot-info)"
)


def validate_product_url(url: str) -> None:
    """
    Validates that the provided URL is a well-formed HTTPS URL
    pointing to the Bunnings domain.
    Raises ValueError if invalid.
    """
    parsed = urlparse(url)

    if parsed.scheme != "https":
        raise ValueError("Product URL must use HTTPS")

    if not parsed.netloc:
        raise ValueError("Product URL must have a valid domain")

    if "bunnings.com.au" not in parsed.netloc:
        raise ValueError("Product URL must be a bunnings.com.au domain")