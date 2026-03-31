"""
File scanning functionality with directory monitoring.
"""

import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .vt_client import VTClient
from ..utils.logger import get_logger
from ..utils.export import ExportManager
from ..models.scan_result import ScanResult

logger = get_logger(__name__)


class FileScanHandler(FileSystemEventHandler):
    """Handle file system events for directory monitoring."""
    
    def __init__(self, scanner: 'FileScanner'):
        self.scanner = scanner
        
    def on_created(self, event):
        if not event.is_directory:
            self.scanner.scan_file(Path(event.src_path))
            
    def on_modified(self, event):
        if not event.is_directory:
            self.scanner.scan_file(Path(event.src_path))


class FileScanner:
    """File scanner with VirusTotal integration."""
    
    def __init__(self, vt_client: VTClient, history_file: str = "scan_history.json"):
        self.vt_client = vt_client
        self.history_file = Path(history_file)
        self.scan_history = self._load_history()
        self.observer = None
        
    def _load_history(self) -> Dict[str, Any]:
        """Load scan history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                logger.warning("Could not load scan history")
        return {"scans": [], "file_hashes": {}}
        
    def _save_history(self) -> None:
        """Save scan history to file."""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.scan_history, f, indent=2, default=str)
        except IOError as e:
            logger.error(f"Could not save scan history: {e}")
            
    def _is_already_scanned(self, file_hash: str, max_age_hours: int = 24) -> bool:
        """Check if file was already scanned recently."""
        if file_hash not in self.scan_history.get("file_hashes", {}):
            return False
            
        scan_time = self.scan_history["file_hashes"][file_hash]
        age = datetime.now() - datetime.fromisoformat(scan_time)
        
        return age.total_seconds() < max_age_hours * 3600
        
    def _record_scan(self, file_hash: str, result: ScanResult) -> None:
        """Record a scan in history."""
        self.scan_history["file_hashes"][file_hash] = datetime.now().isoformat()
        self.scan_history["scans"].append(result.to_dict())
        self._save_history()
        
    def scan_file(self, file_path: Path) -> Optional[ScanResult]:
        """Scan a single file."""
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
            
        try:
            # CORRECTION: file_hashes est un dict, file_hash est la valeur sha256
            file_hashes = self.vt_client.calculate_file_hash(str(file_path))
            file_hash = file_hashes["sha256"]
            
            if self._is_already_scanned(file_hash):
                logger.info(f"File already scanned recently: {file_path}")
                return None
                
            report = self.vt_client.get_file_report(file_hash)
            
            if report.get("data"):
                # CORRECTION: file_hash est déjà une string, pas un dict
                result = ScanResult.from_api_response(
                    report, "file", str(file_path), file_hash
                )
            else:
                logger.info(f"Uploading file for scan: {file_path}")
                scan_response = self.vt_client.scan_file(str(file_path))
                # CORRECTION: file_hash est déjà une string, pas un dict
                result = ScanResult.from_api_response(
                    scan_response, "file", str(file_path), file_hash
                )
                
            self._record_scan(file_hash, result)
            logger.info(f"Scan complete: {result.positives}/{result.total} detections")
            
            return result
            
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
            return None
            
    def scan_directory(
        self, 
        dir_path: Path, 
        recursive: bool = True,
        extensions: Optional[List[str]] = None
    ) -> List[ScanResult]:
        """Scan all files in a directory."""
        results = []
        
        if not dir_path.exists() or not dir_path.is_dir():
            logger.error(f"Directory not found: {dir_path}")
            return results
            
        files = dir_path.rglob("*") if recursive else dir_path.glob("*")
        
        for file_path in files:
            if file_path.is_file():
                if extensions and file_path.suffix not in extensions:
                    continue
                    
                result = self.scan_file(file_path)
                if result:
                    results.append(result)
                    
        logger.info(f"Directory scan complete: {len(results)} files scanned")
        return results
        
    def start_monitoring(
        self, 
        dir_path: Path, 
        interval: int = 3600
    ) -> None:
        """Start monitoring a directory for new/modified files."""
        event_handler = FileScanHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(dir_path), recursive=True)
        self.observer.start()
        
        logger.info(f"Started monitoring: {dir_path}")
        
    def stop_monitoring(self) -> None:
        """Stop directory monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Stopped monitoring")
            
    def export_results(
        self, 
        results: List[ScanResult], 
        format: str = "json",
        output_path: Optional[Path] = None
    ) -> Path:
        """Export scan results to file."""
        exporter = ExportManager()
        return exporter.export(results, format, output_path)
