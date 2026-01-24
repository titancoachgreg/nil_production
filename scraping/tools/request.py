import requests, random, time
from urllib.parse import urlparse
from collections import defaultdict

class Request:

    HEADERS_LIST = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/117.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                          "Version/16.6 Safari/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        },
    ]

    PROXIES = []

    MAX_RETRIES = 3
    TIMEOUT = 5
    DELAY_RANGE = (0.4, 1.2)
    SLEEP_ENABLED = True

    _domain_last_hit = defaultdict(float)
    _sessions = {}

    @classmethod
    def _get_session(cls, proxy):
        if proxy not in cls._sessions:
            session = requests.Session()
            cls._sessions[proxy] = session
        return cls._sessions[proxy]
    
    @classmethod
    def _throttle(cls, domain):
        last = cls._domain_last_hit[domain]
        delay = random.uniform(*cls.DELAY_RANGE)
        elapsed = time.time() - last

        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        cls._domain_last_hit[domain] = time.time()

    @classmethod
    def _pick_proxy(cls):
        return random.choice(cls.PROXIES) if cls.PROXIES else None
    
    @classmethod
    def _pick_headers(cls, domain):
        headers = random.choice(cls.HEADERS_LIST).copy()
        headers['Referer'] = f"https://{domain}/"
        return headers

    @classmethod
    def get_data(cls, url, sleep_enabled=True, params=None, timeout=10):
        domain = urlparse(url).netloc

        if sleep_enabled is None:
            sleep_enabled = cls.SLEEP_ENABLED
        
        if sleep_enabled:
            cls._throttle(domain)

        proxy = cls._pick_proxy()

        proxies = {'http': proxy, 'https': proxy} if proxy else None
        headers = cls._pick_headers(domain)

        for attempt in range(cls.MAX_RETRIES):
            try:
                resp = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    timeout=timeout or cls.TIMEOUT,
                )
            
                if resp.status_code in (403, 429):
                    time.sleep(random.uniform(3, 8))
                    continue

                resp.raise_for_status()
                return resp
        
            except requests.RequestException:
                if attempt == cls.MAX_RETRIES - 1:
                    return None
                time.sleep(random.uniform(1, 3))
