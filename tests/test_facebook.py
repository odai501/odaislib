"""
اختبارات دوال فيسبوك (باستخدام mock)
"""
import pytest
from unittest.mock import patch, MagicMock
from odaislib import facebook

def test_facebook_basic_structure():
    """اختبار أن دالة basic تعيد قاموساً بالمفاتيح المتوقعة"""
    # نمرر بيانات وهمية، ويجب أن تتعامل مع الاستثناء
    result = facebook.basic("test@example.com", "wrongpass")
    assert isinstance(result, dict)
    assert "status" in result
    assert "user" in result
    assert "password" in result

@patch('odaislib.requests.get')
@patch('odaislib.requests.Session')
def test_facebook_basic_success(mock_session, mock_get, mock_response):
    """اختبار نجاح تسجيل الدخول إلى فيسبوك (محاكاة)"""
    # تجهيز mock
    mock_response_obj = MagicMock()
    mock_response_obj.text = '<script>privacy_mutation_token = "test_token"</script>'
    mock_response_obj.cookies = {'fr': 'test_fr'}
    mock_get.return_value = mock_response_obj

    mock_session_instance = MagicMock()
    mock_session_instance.get.return_value.text = '"LSD",[],{"token":"test_lsd"}'
    mock_session_instance.post.return_value.text = '{"ACCOUNT_ID":"123","USER_ID":"456","USERNAME":"test_user"}'
    mock_session.return_value = mock_session_instance

    # تنفيذ الاختبار
    result = facebook.basic("test@example.com", "password")
    assert result["status"] == "success"
    assert result["account_id"] == "123"
    assert result["username"] == "test_user"

def test_extract_cookies():
    """اختبار استخراج الكوكيز من النص"""
    from odaislib import extract_cookies
    text = '{"session_cookies":[{"name":"c_user","value":"123"},{"name":"xs","value":"abc"}]}'
    result = extract_cookies(text)
    assert "c_user=123" in result
    assert "xs=abc" in result