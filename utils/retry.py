import time
import logging

logger = logging.getLogger(__name__)

def retry_with_backoff(func, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            logger.warning(f"Retry {attempt + 1}/{retries} failed: {e}")
            print(f"Retry {attempt + 1}/{retries} failed: {e}")
            time.sleep(delay * (attempt + 1))
    raise RuntimeError("All retries failed")