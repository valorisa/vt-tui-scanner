"""
Custom TUI widgets for VT Scanner.
"""

from textual.widget import Widget
from textual.widgets import Static, ProgressBar, DataTable
from textual.reactive import reactive
from rich.text import Text


class ScanProgressBar(ProgressBar):
    """Custom progress bar for scan operations."""
    
    def update_progress(self, current: int, total: int) -> None:
        """Update progress bar."""
        self.progress = (current / total) * 100 if total > 0 else 0


class ResultTable(DataTable):
    """Custom data table for scan results."""
    
    def add_result(self, result: dict) -> None:
        """Add a scan result row."""
        self.add_row(
            result.get("timestamp", "N/A")[:19],
            result.get("type", "N/A"),
            result.get("target", "N/A")[:38],
            f"{result.get('positives', 0)}/{result.get('total', 0)}",
            result.get("status", "N/A")
        )


class LogViewer(Static):
    """Widget for displaying log output."""
    
    logs = reactive([])
    
    def __init__(self):
        super().__init__()
        self.max_lines = 100
        
    def add_log(self, message: str, level: str = "INFO") -> None:
        """Add a log entry."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        self.logs.append(log_entry)
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)
            
        self.update_display()
        
    def update_display(self) -> None:
        """Update the display with current logs."""
        self.update("\n".join(self.logs[-50:]))
        
    def clear_logs(self) -> None:
        """Clear all logs."""
        self.logs = []
        self.update("")
