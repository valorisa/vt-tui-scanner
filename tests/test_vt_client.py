"""
Tests for VTClient module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

from src.scanner.vt_client import VTClient, RateLimitExceeded


class TestVTClient:
    """Test cases for VTClient."""
    
    @pytest.fixture
    def mock_api_key(self):
        """Mock API key for tests."""
        with patch.dict("os.environ", {"VT_API_KEY": "test_api_key_123"}):
            yield
            
    @pytest.fixture
    def vt_client(self, mock_api_key):
        """Create VTClient instance for tests."""
        return VTClient()
        
    def test_init_with_api_key(self, mock_api_key):
        """Test client initialization."""
        client = VTClient()
        assert client.api_key == "test_api_key_123"
        
    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError):
                VTClient()
                
    @patch("src.scanner.vt_client.requests.Session")
    def test_get_file_report(self, mock_session, vt_client):
        """Test file report retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "attributes": {
                    "last_analysis_stats": {"malicious": 0, "suspicious": 0}
                }
            }
        }
        mock_session.return_value.get.return_value = mock_response
        
        result = vt_client.get_file_report("test_hash")
        
        assert "data" in result
        mock_session.return_value.get.assert_called_once()
        
    @patch("src.scanner.vt_client.requests.Session")
    def test_get_file_report_429(self, mock_session, vt_client):
        """Test rate limit handling."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        
        mock_session.return_value.get.return_value = mock_response
        
        with pytest.raises(RateLimitExceeded):
            vt_client.get_file_report("test_hash")
            
    @patch("src.scanner.vt_client.requests.Session")
    def test_get_file_report_401(self, mock_session, vt_client):
        """Test invalid API key handling."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        
        mock_session.return_value.get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Invalid API key"):
            vt_client.get_file_report("test_hash")
            
    def test_calculate_file_hash(self, vt_client, tmp_path):
        """Test file hash calculation."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        hashes = vt_client.calculate_file_hash(str(test_file))
        
        assert "md5" in hashes
        assert "sha1" in hashes
        assert "sha256" in hashes
        assert len(hashes["md5"]) == 32
        assert len(hashes["sha256"]) == 64
