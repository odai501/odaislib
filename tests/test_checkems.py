"""
اختبارات دوال التحقق من البريد الإلكتروني
"""
import pytest
from unittest.mock import patch
from odaislib import checkems

def test_gmail_invalid_format():
    """اختبار صيغة إيميل غير صالحة"""
    result = checkems.gmail("invalid_email")
    assert "status" in result

@patch('odaislib.checkems.requests.post')
def test_gmail_available(mock_post, mock_response):
    """اختبار إيميل متاح"""
    mock_post.return_value = mock_response(text='"gf.uar",1')
    result = checkems.gmail("newuser")
    assert result["status"] == "available"

@patch('odaislib.checkems.requests.post')
def test_gmail_taken(mock_post, mock_response):
    """اختبار إيميل مستخدم"""
    mock_post.return_value = mock_response(text='"gf.uar",2')
    result = checkems.gmail("existinguser")
    assert result["status"] == "taken"

def test_yahoo_structure():
    """اختبار هيكل دالة yahoo"""
    result = checkems.yahoo("testuser")
    assert isinstance(result, dict)
    assert "status" in result