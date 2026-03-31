"""
Scan result data model.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class ScanResult:
    """Represents a scan result from VirusTotal."""
    
    timestamp: str
    scan_type: str
    target: str
    hash: str
    positives: int = 0
    total: int = 0
    status: str = "unknown"
    permalink: str = ""
    engine_results: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.engine_results is None:
            self.engine_results = {}
            
    @classmethod
    def from_api_response(
        cls,
        response: Dict[str, Any],
        scan_type: str,
        target: str,
        hash_value: str
    ) -> 'ScanResult':
        """Create ScanResult from VirusTotal API response."""
        data = response.get("data", {})
        attributes = data.get("attributes", {})
        
        stats = attributes.get("last_analysis_stats", {})
        positives = stats.get("malicious", 0) + stats.get("suspicious", 0)
        total = sum(stats.values()) if stats else 0
        
        permalink = data.get("links", {}).get("self", "")
        
        return cls(
            timestamp=datetime.now().isoformat(),
            scan_type=scan_type,
            target=target,
            hash=hash_value,
            positives=positives,
            total=total,
            status="completed",
            permalink=permalink,
            engine_results=attributes.get("last_analysis_results", {})
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
        
    def is_malicious(self, threshold: int = 1) -> bool:
        """Check if result is considered malicious."""
        return self.positives >= threshold
        
    def get_risk_level(self) -> str:
        """Get risk level based on detections."""
        if self.positives == 0:
            return "clean"
        elif self.positives < 5:
            return "low"
        elif self.positives < 10:
            return "medium"
        else:
            return "high"
