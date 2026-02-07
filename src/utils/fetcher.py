import logging
import requests

from config.config import REQUEST_TIMEOUT_SECONDS, USER_AGENT

logger = logging.getLogger(__name__)


class PageFetchError(Exception):
    """Raised when the product page cannot be fetched."""


def fetch_product_page(url: str) -> str:
    """
    Fetches the HTML content of the given product page URL.

    Returns:
        HTML content as a string

    Raises:
        PageFetchError: if the page cannot be fetched
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html",
    }

    try:
        logger.info("Fetching product page")
        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

        logger.info(
            "Successfully fetched page (status=%s, bytes=%s)",
            response.status_code,
            len(response.text),
        )

        return response.text

    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        raise PageFetchError("Timed out while fetching product page")

    except requests.exceptions.HTTPError as exc:
        logger.error("HTTP error occurred: %s", exc)
        raise PageFetchError(f"HTTP error occurred: {exc}")

    except requests.exceptions.RequestException as exc:
        logger.error("Network error occurred: %s", exc)
        raise PageFetchError(f"Network error occurred: {exc}")