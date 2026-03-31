"""
TUI Screen definitions for VT Scanner.
"""

from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import (
    Button, Label, Static, Input, 
    DataTable, ProgressBar
)
from textual.binding import Binding
from textual.app import ComposeResult
from pathlib import Path
from datetime import datetime

import tkinter as tk
from tkinter import filedialog


class MainScreen(Screen):
    """Main menu screen."""
    
    BINDINGS = [
        Binding("f", "scan_file", "Scan File"),
        Binding("d", "scan_dir", "Scan Directory"),
        Binding("u", "scan_url", "Scan URL"),
        Binding("h", "history", "History"),
        Binding("r", "view_results", "Results"),
        Binding("s", "settings", "Settings"),
        Binding("q", "quit", "Quit"),
    ]
    
    CSS = """
    MainScreen {
        align: center top;
        padding: 2;
    }
    
    .title {
        text-style: bold;
        text-align: center;
        width: 100%;
        padding: 2 0;
    }
    
    .subtitle {
        color: $text-muted;
        text-align: center;
        width: 100%;
        padding: 0 0 2 0;
    }
    
    MainScreen Button {
        width: 100%;
        max-width: 50;
        margin: 1 0;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Static("VT TUI Scanner", classes="title")
        yield Static("VirusTotal Community Scanner", classes="subtitle")
        
        with Vertical():
            yield Button("📁 Scan File", id="btn-scan-file")
            yield Button("📂 Scan Directory", id="btn-scan-dir")
            yield Button("🔗 Scan URL", id="btn-scan-url")
            yield Button("📜 View History", id="btn-history", variant="primary")
            yield Button("📊 View Results", id="btn-results")
            yield Button("⚙️  Settings", id="btn-settings")
            yield Button("❌ Quit", id="btn-quit", variant="error")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        
        if button_id == "btn-scan-file":
            self.app.push_screen(ScanScreen(scan_type="file"))
        elif button_id == "btn-scan-dir":
            self.app.push_screen(ScanScreen(scan_type="directory"))
        elif button_id == "btn-scan-url":
            self.app.push_screen(ScanScreen(scan_type="url"))
        elif button_id == "btn-history":
            self.app.push_screen(HistoryScreen())
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
        
    def action_history(self) -> None:
        self.app.push_screen(HistoryScreen())
        
    def action_view_results(self) -> None:
        self.app.push_screen(ResultsScreen(self.app.get_scan_results()))
        
    def action_settings(self) -> None:
        self.app.push_screen(SettingsScreen(self.app.config))
        
    def action_quit(self) -> None:
        self.app.exit()


class HistoryScreen(Screen):
    """Display scan history from scan_history.json."""
    
    BINDINGS = [
        Binding("q", "app.pop_screen", "Back"),
        Binding("r", "refresh", "Refresh"),
    ]
    
    CSS = """
    HistoryScreen {
        align: center top;
        padding: 2;
    }
    
    .title {
        text-style: bold;
        text-align: center;
        width: 100%;
        padding: 1 0;
    }
    
    .subtitle {
        color: $text-muted;
        text-align: center;
        width: 100%;
    }
    
    HistoryScreen DataTable {
        width: 100%;
        height: 20;
        margin: 1 0;
    }
    
    HistoryScreen Button {
        width: 20;
        margin: 1 2;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Static("Scan History", classes="title")
        yield Static("From scan_history.json", classes="subtitle")
        
        history_file = Path("scan_history.json")
        
        if not history_file.exists():
            yield Static("[yellow]No scan history found yet[/]")
        else:
            try:
                import json
                with open(history_file, "r") as f:
                    history = json.load(f)
                
                scans = history.get("scans", [])
                
                if not scans:
                    yield Static("[yellow]No scans recorded yet[/]")
                else:
                    recent_scans = scans[-50:][::-1]
                    yield Static(f"[dim]Total: {len(scans)} | Showing: {len(recent_scans)}[/]")
                    
                    table = DataTable(id="history-table")
                    table.add_column("Date", width=19)
                    table.add_column("Type", width=8)
                    table.add_column("Target", width=40)
                    table.add_column("Detections", width=12)
                    
                    for scan in recent_scans:
                        target = scan.get("target", "N/A")
                        if len(target) > 38:
                            target = "..." + target[-35:]
                        
                        positives = scan.get("positives", 0)
                        total = scan.get("total", 0)
                        
                        if positives == 0:
                            detections = f"[green]{positives}/{total}[/]"
                        elif positives < 5:
                            detections = f"[yellow]{positives}/{total}[/]"
                        else:
                            detections = f"[red]{positives}/{total}[/]"
                        
                        table.add_row(
                            scan.get("timestamp", "N/A")[:19],
                            scan.get("scan_type", "N/A")[:8],
                            target,
                            detections
                        )
                    
                    yield table
                    
            except Exception as e:
                yield Static(f"[red]Error: {e}[/]")
        
        with Horizontal():
            yield Button("🔄 Refresh", id="btn-refresh", variant="primary")
            yield Button("⬅️ Back", id="btn-back")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-refresh":
            self.app.pop_screen()
            self.app.push_screen(HistoryScreen())
    
    def action_refresh(self) -> None:
        self.app.pop_screen()
        self.app.push_screen(HistoryScreen())


class ScanScreen(Screen):
    """Scan operation screen."""
    
    def __init__(self, scan_type: str = "file"):
        super().__init__()
        self.scan_type = scan_type
        
    CSS = """
    ScanScreen {
        align: center top;
        padding: 2;
    }
    
    .title {
        text-style: bold;
        text-align: center;
        width: 100%;
        padding: 1 0;
    }
    
    ScanScreen Input {
        width: 80;
        margin: 1 0;
    }
    
    ScanScreen Button {
        width: 30;
        margin: 1 0;
    }
    
    #scan-status {
        width: 100%;
        padding: 1 0;
    }
    """
        
    def compose(self) -> ComposeResult:
        yield Static(f"Scan {self.scan_type.title()}", classes="title")
        
        if self.scan_type == "file":
            yield Input(placeholder="File path...", id="file-path")
            yield Button("📁 Browse Files", id="btn-browse-file")
        elif self.scan_type == "directory":
            yield Input(placeholder="Directory path...", id="dir-path")
            yield Button("📂 Browse Folders", id="btn-browse-dir")
        elif self.scan_type == "url":
            yield Input(placeholder="https://example.com", id="url-input")
            
        yield Button("🚀 Start Scan", id="btn-start-scan", variant="success")
        yield Button("⬅️ Back", id="btn-back")
        yield Static("", id="scan-status")
        yield ProgressBar(id="scan-progress", show_eta=False)
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-browse-file":
            self._browse_file()
        elif event.button.id == "btn-browse-dir":
            self._browse_directory()
        elif event.button.id == "btn-start-scan":
            self._start_scan()
    
    def _browse_file(self):
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            file_path = filedialog.askopenfilename(title="Select file")
            if file_path:
                self.query_one("#file-path", Input).value = file_path
                self.notify(f"Selected: {Path(file_path).name}")
            root.destroy()
        except Exception as e:
            self.notify(f"Error: {e}", severity="error")
    
    def _browse_directory(self):
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            dir_path = filedialog.askdirectory(title="Select directory")
            if dir_path:
                self.query_one("#dir-path", Input).value = dir_path
                self.notify(f"Selected: {Path(dir_path).name}")
            root.destroy()
        except Exception as e:
            self.notify(f"Error: {e}", severity="error")
            
    def _start_scan(self):
        try:
            if self.scan_type == "file":
                target = self.query_one("#file-path", Input).value
            elif self.scan_type == "directory":
                target = self.query_one("#dir-path", Input).value
            elif self.scan_type == "url":
                target = self.query_one("#url-input", Input).value
            
            if not target:
                self.query_one("#scan-status", Static).update("[red]Enter a target[/]")
                return
            
            self.query_one("#scan-status", Static).update("[yellow]Scanning...[/]")
            self.query_one("#scan-progress", ProgressBar).update(progress=30)
            
            from ..scanner.vt_client import VTClient
            from ..scanner.file_scanner import FileScanner
            from ..scanner.url_scanner import URLScanner
            
            vt_client = VTClient()
            result = None
            
            if self.scan_type == "file":
                scanner = FileScanner(vt_client)
                result = scanner.scan_file(Path(target))
            elif self.scan_type == "directory":
                scanner = FileScanner(vt_client)
                results = scanner.scan_directory(Path(target))
                result = results[0] if results else None
            elif self.scan_type == "url":
                scanner = URLScanner(vt_client)
                result = scanner.scan_url(target)
            
            self.query_one("#scan-progress", ProgressBar).update(progress=100)
            
            if result:
                self.query_one("#scan-status", Static).update(
                    f"[green]Complete: {result.positives}/{result.total}[/]"
                )
                self.app.add_scan_result(result.to_dict())
            else:
                self.query_one("#scan-status", Static).update(
                    "[orange]Already scanned recently[/]"
                )
                
        except ValueError as e:
            self.query_one("#scan-progress", ProgressBar).update(progress=0)
            self.query_one("#scan-status", Static).update(f"[red]API Error: {e}[/]")
        except Exception as e:
            self.query_one("#scan-progress", ProgressBar).update(progress=0)
            self.query_one("#scan-status", Static).update(f"[red]Error: {e}[/]")


class ResultsScreen(Screen):
    """Results display screen."""
    
    def __init__(self, results: list):
        super().__init__()
        self.results = results or []
        
    CSS = """
    ResultsScreen {
        align: center top;
        padding: 2;
    }
    
    .title {
        text-style: bold;
        text-align: center;
        width: 100%;
    }
    
    ResultsScreen DataTable {
        width: 100%;
        height: 20;
    }
    
    ResultsScreen Button {
        width: 20;
        margin: 1 2;
    }
    """
        
    def compose(self) -> ComposeResult:
        yield Static("Scan Results", classes="title")
        
        if not self.results:
            yield Static("[dim]No results yet[/]")
        else:
            table = DataTable(id="results-table")
            table.add_column("Date", width=19)
            table.add_column("Type", width=8)
            table.add_column("Target", width=40)
            table.add_column("Detections", width=12)
            
            for result in self.results:
                table.add_row(
                    result.get("timestamp", "N/A")[:19],
                    result.get("type", "N/A"),
                    result.get("target", "N/A")[:38],
                    f"{result.get('positives', 0)}/{result.get('total', 0)}"
                )
            yield table
            
        with Horizontal():
            yield Button("💾 Export", id="btn-export")
            yield Button("⬅️ Back", id="btn-back")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-export":
            from ..utils.export import ExportManager
            exporter = ExportManager()
            exporter.export(self.results, "json")
            self.notify("Exported to exports/")


class SettingsScreen(Screen):
    """Settings configuration screen."""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    CSS = """
    SettingsScreen {
        align: center top;
        padding: 2;
    }
    
    .title {
        text-style: bold;
        text-align: center;
        width: 100%;
    }
    
    SettingsScreen Input {
        width: 60;
        margin: 1 0;
    }
    
    SettingsScreen Button {
        width: 25;
        margin: 1 2;
    }
    """
        
    def compose(self) -> ComposeResult:
        yield Static("Settings", classes="title")
        yield Label("API Key (set in .env):")
        yield Input(placeholder="VT_API_KEY", id="api-key", password=True)
        yield Label("Scan Interval (minutes):")
        yield Input(value="60", id="scan-interval")
        
        with Horizontal():
            yield Button("💾 Save", id="btn-save", variant="success")
            yield Button("⬅️ Back", id="btn-back")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-save":
            self._save_settings()
            self.notify("Settings saved!")
            
    def _save_settings(self):
        pass
