"""
Main TUI Application class using Textual framework.
"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Static

from .screens import MainScreen, ScanScreen, ResultsScreen, SettingsScreen
from ..utils.config import Config


class VTScannerApp(App):
    """Main VirusTotal TUI Scanner Application."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .container {
        width: 100%;
        height: 100%;
    }
    
    .menu-button {
        width: 100%;
        margin: 1 0;
    }
    
    .title {
        text-align: center;
        padding: 2;
    }
    
    .subtitle {
        text-align: center;
        color: $text-muted;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("d", "toggle_dark", "Toggle Dark Mode", show=True),
        Binding("1", "go_main", "Main", show=False),
        Binding("2", "go_scan", "Scan", show=False),
        Binding("3", "go_results", "Results", show=False),
    ]
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.scan_results = []
        self.dark = True
        
    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header(show_clock=True)
        yield Container(
            MainScreen(id="main-screen"),
            id="main-container"
        )
        yield Footer()
        
    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.title = "VT TUI Scanner v1.0.0"
        self.sub_title = "VirusTotal Community Scanner"
        
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()
        
    def action_toggle_dark(self) -> None:
        """Toggle dark/light mode."""
        self.dark = not self.dark
        
    def action_go_main(self) -> None:
        """Navigate to main screen."""
        self.push_screen(MainScreen())
        
    def action_go_scan(self) -> None:
        """Navigate to scan screen."""
        self.push_screen(ScanScreen())
        
    def action_go_results(self) -> None:
        """Navigate to results screen."""
        self.push_screen(ResultsScreen(self.scan_results))
        
    def add_scan_result(self, result: dict) -> None:
        """Add a scan result to the results list."""
        self.scan_results.append(result)
        
    def get_scan_results(self) -> list:
        """Get all scan results."""
        return self.scan_results
