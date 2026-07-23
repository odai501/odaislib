"""
اختبارات فئة Proxy
"""
from odaislib import Proxy

def test_proxy_build_http():
    """اختبار بناء وكيل HTTP عادي"""
    proxy = Proxy.build("127.0.0.1:8080")
    assert proxy == {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def test_proxy_build_https():
    """اختبار بناء وكيل HTTPS"""
    proxy = Proxy.build("https://proxy.example.com:3128")
    assert proxy == {"http": "https://proxy.example.com:3128", "https": "https://proxy.example.com:3128"}

def test_proxy_build_with_auth():
    """اختبار بناء وكيل مع مصادقة"""
    proxy = Proxy.build("http://user:pass@proxy.com:8080")
    assert proxy == {"http": "http://user:pass@proxy.com:8080", "https": "http://user:pass@proxy.com:8080"}

def test_proxy_build_socks():
    """اختبار بناء وكيل SOCKS"""
    proxy = Proxy.build("socks5://127.0.0.1:1080")
    assert proxy == {"http": "socks5://127.0.0.1:1080", "https": "socks5://127.0.0.1:1080"}

def test_proxy_build_invalid():
    """اختبار بناء وكيل غير صالح"""
    assert Proxy.build("invalid") is None
    assert Proxy.build("") is None
    assert Proxy.build(None) is None

def test_proxy_build_list():
    """اختبار تمرير قائمة من الوكسيات"""
    proxies = ["127.0.0.1:8080", "invalid", "proxy.com:3128"]
    proxy = Proxy.build(proxies)
    assert proxy == {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def test_proxy_raw():
    """اختبار استخراج الوكيل كـ string"""
    raw = Proxy.raw("127.0.0.1:8080")
    assert raw == "http://127.0.0.1:8080"
    assert Proxy.raw(None) is None