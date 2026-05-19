import requests
import time

class RobustAPIClient:
    def __init__(self, base_url, timeout=3.0):
        self.base_url = base_url
        self.timeout = timeout

    def request(self, endpoint, params=None):
        """
        Effectue une requete GET avec gestion de timeout, 
        de retry (1 max) et mesure de la latence.
        """
        url = f"{self.base_url}{endpoint}"
        retries = 1
        
        for attempt in range(retries + 1):
            start_time = time.perf_counter()
            try:
                response = requests.get(url, params=params, timeout=self.timeout)
                latency_ms = (time.perf_counter() - start_time) * 1000
                
                # Gestion du Rate Limiting (429) ou des erreurs serveurs (5xx)
                if response.status_code == 429:
                    time.sleep(1) # Attente (backoff simple) avant re-tentative
                    if attempt < retries:
                        continue
                
                return {
                    "status_code": response.status_code,
                    "headers": response.headers,
                    "json": response.json() if "application/json" in response.headers.get("Content-Type", "") else None,
                    "latency_ms": latency_ms,
                    "error": None
                }
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                latency_ms = (time.perf_counter() - start_time) * 1000
                if attempt < retries:
                    time.sleep(0.5) # Temporisation courte avant retry
                    continue
                return {
                    "status_code": 0,
                    "headers": {},
                    "json": None,
                    "latency_ms": latency_ms,
                    "error": str(e)
                }