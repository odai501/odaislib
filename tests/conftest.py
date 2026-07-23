"""
إعدادات مشتركة لجميع اختبارات pytest
"""
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_response():
    """توفير كائن استجابة وهمي للاختبارات"""
    def _mock_response(status=200, json_data=None, text="", cookies=None):
        mock = MagicMock()
        mock.status_code = status
        mock.json.return_value = json_data or {}
        mock.text = text
        mock.cookies = cookies or {}
        return mock
    return _mock_response