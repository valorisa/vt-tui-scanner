"""
Export functionality for scan results.
"""

import json
import csv
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from ..models.scan_result import ScanResult
from .logger import get_logger

logger = get_logger(__name__)


class ExportManager:
    """Manage export of scan results to various formats."""
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def export(
        self,
        results: List[ScanResult],
        format: str = "json",
        output_path: Optional[Path] = None
    ) -> Path:
        """Export results to file."""
        if format == "json":
            return self.export_json(results, output_path)
        elif format == "csv":
            return self.export_csv(results, output_path)
        elif format == "both":
            json_path = self.export_json(results, output_path)
            csv_path = self.export_csv(results, output_path)
            logger.info(f"Exported to {json_path} and {csv_path}")
            return json_path
        else:
            raise ValueError(f"Unsupported export format: {format}")
            
    def export_json(
        self,
        results: List[ScanResult],
        output_path: Optional[Path] = None
    ) -> Path:
        """Export results to JSON."""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"scan_results_{timestamp}.json"
            
        data = {
            "export_date": datetime.now().isoformat(),
            "total_scans": len(results),
            "results": [r.to_dict() for r in results]
        }
        
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2, default=str)
            
        logger.info(f"Exported {len(results)} results to {output_path}")
        return output_path
        
    def export_csv(
        self,
        results: List[ScanResult],
        output_path: Optional[Path] = None
    ) -> Path:
        """Export results to CSV."""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"scan_results_{timestamp}.csv"
            
        fieldnames = [
            "timestamp", "type", "target", "hash",
            "positives", "total", "status", "permalink"
        ]
        
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                row = result.to_dict()
                writer.writerow({k: row.get(k, "") for k in fieldnames})
                
        logger.info(f"Exported {len(results)} results to {output_path}")
        return output_path
