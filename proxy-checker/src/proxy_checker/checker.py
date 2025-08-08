import logging
import requests
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import ProxyError, Timeout, RequestException

from .models import Proxy, ProxyStatus


def check_proxy(proxy: Proxy, test_url: str, timeout: int) -> Proxy:
    logging.info(f"Testing {proxy.url}...")
    proxies = {"http": proxy.url, "https": proxy.url}
    
    try:
        r = requests.get(test_url, proxies=proxies, timeout=timeout)
        r.raise_for_status()
        
        try:
            response_ip = r.json().get("ip")
            if response_ip == proxy.host:
                proxy.status = ProxyStatus.FUNCTIONAL
            else:
                logging.warning(f"{proxy.address} is transparent or misleading. Returned IP: {response_ip}")
                proxy.status = ProxyStatus.NOT_FUNCTIONAL
        except requests.exceptions.JSONDecodeError:
            proxy.status = ProxyStatus.INVALID_RESPONSE

    except (ProxyError, Timeout, RequestException) as e:
        logging.warning(f"Error testing {proxy.address}: {e.__class__.__name__}")
        proxy.status = ProxyStatus.ERROR
        
    logging.info(f"Result for {proxy.address}: {proxy.status.value}")
    return proxy


def run_checks_concurrently(proxies: List[Proxy], test_url: str, timeout: int, max_workers: int) -> List[Proxy]:
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(check_proxy, p, test_url, timeout): p for p in proxies}
        
        for future in as_completed(future_to_proxy):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                proxy = future_to_proxy[future]
                logging.error(f"An unexpected error occurred while testing {proxy.url}: {e}")

    return results