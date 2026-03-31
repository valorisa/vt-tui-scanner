"""
Main entry point for VT TUI Scanner.

Supports both TUI interactive mode and headless automation mode.
"""

import argparse
import sys
from pathlib import Path

from textual.app import App

from .tui.app import VTScannerApp
from .utils.config import load_config, setup_environment
from .utils.logger import setup_logger


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="VT TUI Scanner - VirusTotal scanning tool with TUI interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vt-tui-scanner                    Launch TUI interface
  vt-tui-scanner --headless         Run in headless mode
  vt-tui-scanner --file malware.exe Scan a specific file
  vt-tui-scanner --url http://...   Scan a specific URL
  vt-tui-scanner --dir /path/scan   Scan a directory
        """
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (no TUI, for automation/CI)"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a file to scan"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="URL to scan"
    )
    parser.add_argument(
        "--dir",
        type=str,
        help="Directory to scan"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )
    parser.add_argument(
        "--export",
        type=str,
        choices=["json", "csv", "both"],
        help="Export results to specified format"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_arguments()
    
    # Setup environment and load configuration
    setup_environment()
    config = load_config(args.config)
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = setup_logger(log_level)
    logger.info("VT TUI Scanner starting...")
    
    try:
        if args.headless:
            # Headless mode for automation
            from .scanner.file_scanner import FileScanner
            from .scanner.url_scanner import URLScanner
            from .scanner.vt_client import VTClient
            
            vt_client = VTClient()
            
            if args.file:
                scanner = FileScanner(vt_client)
                result = scanner.scan_file(Path(args.file))
                print(f"Scan result: {result}")
                
            elif args.url:
                scanner = URLScanner(vt_client)
                result = scanner.scan_url(args.url)
                print(f"Scan result: {result}")
                
            elif args.dir:
                scanner = FileScanner(vt_client)
                results = scanner.scan_directory(Path(args.dir))
                print(f"Scanned {len(results)} files")
                
            else:
                logger.error("No scan target specified in headless mode")
                return 1
                
            # Export if requested
            if args.export and results:
                from .utils.export import ExportManager
                exporter = ExportManager()
                exporter.export(results, args.export)
                
            return 0
            
        else:
            # TUI mode
            app = VTScannerApp(config)
            app.run()
            return 0
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
