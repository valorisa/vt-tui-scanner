"""
URL scanning functionality.
"""

from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime

from .vt_client import VTClient
from ..utils.logger import get_logger
from ..models.scan_result import ScanResult

logger = get_logger(__name__)


class URLScanner:
    """URL scanner with VirusTotal integration."""
    
    def __init__(self, vt_client: VTClient):
        self.vt_client = vt_client
        
    def scan_url(self, url: str) -> Optional[ScanResult]:
        """Scan a URL."""
        try:
            report = self.vt_client.get_url_report(url)
            
            if report.get("data"):
                result = ScanResult.from_api_response(
                    report, "url", url, self._hash_url(url)
                )
            else:
                logger.info(f"Submitting URL for scan: {url}")
                scan_response = self.vt_client.scan_url(url)
                result = ScanResult.from_api_response(
                    scan_response, "url", url, self._hash_url(url)
                )
                
            logger.info(f"URL scan complete: {result.positives}/{result.total} detections")
            return result
            
        except Exception as e:
            logger.error(f"Error scanning URL {url}: {e}")
            return None
            
    def _hash_url(self, url: str) -> str:
        """Create a hash identifier for URL."""
        import hashlib
        return hashlib.sha256(url.encode()).hexdigest()
        
    def scan_url_list(
        self, 
        urls: list, 
        output_file: Optional[Path] = None
    ) -> list:
        """Scan multiple URLs."""
        results = []
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Scanning URL {i}/{len(urls)}: {url}")
            result = self.scan_url(url)
            if result:
                results.append(result)
                
        if output_file and results:
            self._export_results(results, output_file)
            
        return results
        
    def _export_results(self, results: list, output_file: Path) -> None:
        """Export results to JSON file."""
        import json
        
        with open(output_file, "w") as f:
            json.dump(
                [r.to_dict() for r in results], 
                f, 
                indent=2, 
                default=str
            )
        logger.info(f"Results exported to {output_file}")
