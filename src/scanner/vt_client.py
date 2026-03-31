"""
VirusTotal API Client with rate-limit handling.
"""

import os
import time
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..utils.logger import get_logger
from ..utils.config import get_api_key

logger = get_logger(__name__)


class RateLimitExceeded(Exception):
    """Raised when API rate limit is exceeded."""
    pass


class VTClient:
    """
    VirusTotal API Client with built-in rate limiting and retry logic.
    
    Free API limits:
    - 4 requests per minute
    - 500 requests per day
    """
    
    BASE_URL = "https://www.virustotal.com/api/v3"
    RATE_LIMIT_REQUESTS = 4
    RATE_LIMIT_WINDOW = 60
    DAILY_LIMIT = 500
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or get_api_key()
        
        if not self.api_key:
            raise ValueError(
                "VirusTotal API key not found. Set VT_API_KEY environment variable."
            )
            
        self.headers = {
            "x-apikey": self.api_key,
            "Accept": "application/json"
        }
        
        self._request_times: list = []
        self._daily_count = 0
        self._daily_reset = datetime.now().date()
        
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        logger.info("VTClient initialized")
        
    def _check_rate_limit(self) -> None:
        """Check and enforce rate limits."""
        now = datetime.now()
        
        if now.date() > self._daily_reset:
            self._daily_count = 0
            self._daily_reset = now.date()
            logger.info("Daily rate limit reset")
            
        if self._daily_count >= self.DAILY_LIMIT:
            raise RateLimitExceeded(
                f"Daily limit of {self.DAILY_LIMIT} requests exceeded"
            )
            
        cutoff = now - timedelta(seconds=self.RATE_LIMIT_WINDOW)
        self._request_times = [t for t in self._request_times if t > cutoff]
        
        if len(self._request_times) >= self.RATE_LIMIT_REQUESTS:
            wait_time = self.RATE_LIMIT_WINDOW - (now - self._request_times[0]).seconds
            if wait_time > 0:
                logger.warning(f"Rate limit reached. Waiting {wait_time}s")
                time.sleep(wait_time)
                
        self._request_times.append(now)
        self._daily_count += 1
        
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response with error checking."""
        if response.status_code == 429:
            raise RateLimitExceeded("API rate limit exceeded (429)")
        elif response.status_code == 401:
            raise ValueError("Invalid API key")
        elif response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        elif response.status_code >= 400:
            raise ValueError(f"API error: {response.status_code}")
            
        return response.json()
        
    def get_file_report(self, file_hash: str) -> Dict[str, Any]:
        """Get report for a file by hash."""
        self._check_rate_limit()
        
        url = f"{self.BASE_URL}/files/{file_hash}"
        response = self.session.get(url, headers=self.headers)
        
        return self._handle_response(response)
        
    def get_url_report(self, url: str) -> Dict[str, Any]:
        """Get report for a URL."""
        self._check_rate_limit()
        
        import base64
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        
        url = f"{self.BASE_URL}/urls/{url_id}"
        response = self.session.get(url, headers=self.headers)
        
        return self._handle_response(response)
        
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Upload and scan a file."""
        self._check_rate_limit()
        
        url = f"{self.BASE_URL}/files"
        files = {"file": open(file_path, "rb")}
        response = self.session.post(url, headers=self.headers, files=files)
        
        return self._handle_response(response)
        
    def scan_url(self, url: str) -> Dict[str, Any]:
        """Submit URL for scanning."""
        self._check_rate_limit()
        
        scan_url = f"{self.BASE_URL}/urls"
        data = {"url": url}
        response = self.session.post(scan_url, headers=self.headers, data=data)
        
        return self._handle_response(response)
        
    def calculate_file_hash(self, file_path: str) -> Dict[str, str]:
        """Calculate file hashes for lookup."""
        hashes = {
            "md5": hashlib.md5(),
            "sha1": hashlib.sha1(),
            "sha256": hashlib.sha256()
        }
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                for h in hashes.values():
                    h.update(chunk)
                    
        return {name: h.hexdigest() for name, h in hashes.items()}
