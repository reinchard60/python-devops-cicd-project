import logging
import requests

logger = logging.getLogger(__name__)

def check_urls(urls: list[str], timeout: int = 5) -> dict[str, str]:
    """
    Checks a list of URLs and returns their status.

    Args:
        urls (list[str]): A silt of URL trings to check.
        timeout (int, optional): Maximum time in seconds to wait for each request. Defaults to 5.

    Returns:
        dict[str, str]: A dictionary mapping each URL to its status string.
    """
    logger.info(f"Starting chegck for {len(urls)} URLs with a timeout of {timeout}")
    results = {} 

    for url in urls:
        status = "UNKNOWN"

        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)

            status = f"{response.status_code} {response.reason}"
            if response.ok:
                status = f"{response.status_code} OK"
            
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning(f"Request to {url} timed out.")
        except requests.exceptions.ConnectionError:
            status = "CONNECTION_ERROR"
            logger.warning(f"Connection error for {url}.")
        except requests.exceptions.RequestException as e:
            status = f"REQUEST_ERROR: {type(e).__name__}"
            logger.error(f"An unexpected request error occured for {url}: {e}", exc_info=True)

        results[url] = status
        logger.debug(f"Cocked: {url:<40} -> {status}")

    logger.info("URL check finished.")
    return results