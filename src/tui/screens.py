"""
TUI Screen definitions for VT Scanner.
"""

from textual.screen import Screen
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import (
    Button, Label, Static, Input, 
    DataTable, DirectoryTree, ProgressBar
)
from textual.binding import Binding
from pathlib import Path
from datetime import datetime


class MainScreen(Screen):
    """Main menu screen."""
    
    BINDINGS = [
        Binding("f", "scan_file", "Scan File"),
        Binding("d", "scan_dir", "Scan Directory"),
        Binding("u", "scan_url", "Scan URL"),
        Binding("r", "view_results", "Results"),
        Binding("s", "settings", "Settings"),
    ]
    
    def compose(self):
        yield Static("🛡️  VT TUI Scanner", classes="title")
        yield Static("VirusTotal Community Scanner", classes="subtitle")
        yield Static("")
        yield Button("📁 Scan File", id="btn-scan-file", classes="menu-button")
        yield Button("📂 Scan Directory", id="btn-scan-dir", classes="menu-button")
        yield Button("🔗 Scan URL", id="btn-scan-url", classes="menu-button")
        yield Button("📊 View Results", id="btn-results", classes="menu-button")
        yield Button("⚙️  Settings", id="btn-settings", classes="menu-button")
        yield Button("❌ Quit", id="btn-quit", classes="menu-button")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        
        if button_id == "btn-scan-file":
            self.app.push_screen(ScanScreen(scan_type="file"))
        elif button_id == "btn-scan-dir":
            self.app.push_screen(ScanScreen(scan_type="directory"))
        elif button_id == "btn-scan-url":
            self.app.push_screen(ScanScreen(scan_type="url"))
        elif button_id == "btn-results":
            self.app.push_screen(ResultsScreen(self.app.get_scan_results()))
        elif button_id == "btn-settings":
            self.app.push_screen(SettingsScreen(self.app.config))
        elif button_id == "btn-quit":
            self.app.exit()
            
    def action_scan_file(self) -> None:
        self.app.push_screen(ScanScreen(scan_type="file"))
        
    def action_scan_dir(self) -> None:
        self.app.push_screen(ScanScreen(scan_type="directory"))
        
    def action_scan_url(self) -> None:
        self.app.push_screen(ScanScreen(scan_type="url"))
        
    def action_view_results(self) -> None:
        self.app.push_screen(ResultsScreen(self.app.get_scan_results()))
        
    def action_settings(self) -> None:
        self.app.push_screen(SettingsScreen(self.app.config))


class ScanScreen(Screen):
    """Scan operation screen."""
    
    def __init__(self, scan_type: str = "file"):
        super().__init__()
        self.scan_type = scan_type
        
    def compose(self):
        yield Static(f"🔍 Scan {self.scan_type.title()}", classes="title")
        
        if self.scan_type == "file":
            yield Input(placeholder="Enter file path or click to browse...", id="file-path")
            yield Button("📁 Browse", id="btn-browse-file")
        elif self.scan_type == "directory":
            yield Input(placeholder="Enter directory path...", id="dir-path")
            yield Button("📁 Browse", id="btn-browse-dir")
            yield Input(placeholder="Watch interval (minutes)", id="watch-interval", value="60")
        elif self.scan_type == "url":
            yield Input(placeholder="Enter URL to scan...", id="url-input")
            
        yield Button("🚀 Start Scan", id="btn-start-scan", variant="primary")
        yield Button("⬅️ Back", id="btn-back")
        yield Static("", id="scan-status")
        yield ProgressBar(id="scan-progress", show_eta=False)
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button events."""
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-start-scan":
            self._start_scan()
            
    def _start_scan(self):
        """Initiate scan operation."""
        # Implementation calls scanner module
        pass


class ResultsScreen(Screen):
    """Results display screen."""
    
    def __init__(self, results: list):
        super().__init__()
        self.results = results or []
        
    def compose(self):
        yield Static("📊 Scan Results", classes="title")
        
        table = DataTable(id="results-table")
        table.add_column("Date", width=20)
        table.add_column("Type", width=10)
        table.add_column("Target", width=40)
        table.add_column("Detections", width=12)
        table.add_column("Status", width=15)
        
        for result in self.results:
            table.add_row(
                result.get("timestamp", "N/A")[:19],
                result.get("type", "N/A"),
                result.get("target", "N/A")[:38],
                f"{result.get('positives', 0)}/{result.get('total', 0)}",
                result.get("status", "N/A")
            )
            
        yield table
        yield Button("💾 Export", id="btn-export")
        yield Button("⬅️ Back", id="btn-back")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-export":
            self._export_results()
            
    def _export_results(self):
        """Export results to file."""
        pass


class SettingsScreen(Screen):
    """Settings configuration screen."""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def compose(self):
        yield Static("⚙️  Settings", classes="title")
        yield Label("API Key:")
        yield Input(placeholder="VT_API_KEY", id="api-key", password=True)
        yield Label("Scan Interval (minutes):")
        yield Input(value="60", id="scan-interval")
        yield Label("Auto-export:")
        yield Button("Enabled", id="btn-auto-export-on", variant="primary")
        yield Button("Disabled", id="btn-auto-export-off")
        yield Button("💾 Save Settings", id="btn-save", variant="success")
        yield Button("⬅️ Back", id="btn-back")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-save":
            self._save_settings()
            
    def _save_settings(self):
        """Save settings to config."""
        pass
