"""
Tests for FileScanner module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.scanner.file_scanner import FileScanner
from src.models.scan_result import ScanResult


class TestFileScanner:
    """Test cases for FileScanner."""
    
    @pytest.fixture
    def mock_vt_client(self):
        """Create mock VT client."""
        client = Mock()
        
        # Return different hash based on file path for realistic testing
        def mock_calculate_hash(file_path):
            import hashlib
            return {"sha256": hashlib.md5(str(file_path).encode()).hexdigest()}
        
        client.calculate_file_hash.side_effect = mock_calculate_hash
        client.get_file_report.return_value = {
            "data": {
                "attributes": {
                    "last_analysis_stats": {"malicious": 0, "suspicious": 0}
                }
            }
        }
        return client
        
    @pytest.fixture
    def file_scanner(self, mock_vt_client, tmp_path):
        """Create FileScanner instance for tests."""
        history_file = tmp_path / "test_history.json"
        return FileScanner(mock_vt_client, str(history_file))
        
    def test_scan_file_not_found(self, file_scanner):
        """Test scanning non-existent file."""
        result = file_scanner.scan_file(Path("/nonexistent/file.txt"))
        assert result is None
        
    def test_scan_file_success(self, file_scanner, tmp_path):
        """Test successful file scan."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        result = file_scanner.scan_file(test_file)
        
        assert result is not None
        assert isinstance(result, ScanResult)
        assert result.scan_type == "file"
        
    def test_scan_file_already_scanned(self, file_scanner, tmp_path):
        """Test skipping already scanned file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        # First scan
        file_scanner.scan_file(test_file)
        
        # Second scan should return None (already scanned)
        result = file_scanner.scan_file(test_file)
        assert result is None
        
    def test_scan_directory(self, file_scanner, tmp_path):
        """Test directory scanning."""
        # Create test files
        for i in range(3):
            (tmp_path / f"file{i}.txt").write_text(f"content {i}")
            
        results = file_scanner.scan_directory(tmp_path)
        
        assert len(results) == 3
        
    def test_scan_directory_with_extension_filter(self, file_scanner, tmp_path):
        """Test directory scanning with extension filter."""
        (tmp_path / "file1.txt").write_text("text")
        (tmp_path / "file2.py").write_text("python")
        (tmp_path / "file3.txt").write_text("text")
        
        results = file_scanner.scan_directory(tmp_path, extensions=[".txt"])
        
        assert len(results) == 2
        
    def test_export_results(self, file_scanner, tmp_path):
        """Test result export."""
        results = [
            ScanResult(
                timestamp="2024-01-01T00:00:00",
                scan_type="file",
                target="test.txt",
                hash="abc123",
                positives=0,
                total=70,
                status="completed"
            )
        ]
        
        output_path = tmp_path / "export.json"
        exported = file_scanner.export_results(results, "json", output_path)
        
        assert exported.exists()
