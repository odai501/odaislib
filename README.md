# 📦 odaislib – مكتبة بايثون الاحترافية متعددة المهام

![PyPI version](https://img.shields.io/pypi/v/odaislib.svg)
![Python versions](https://img.shields.io/pypi/pyversions/odaislib.svg)
![License](https://img.shields.io/github/license/odai501/odaislib.svg)
![Downloads](https://img.shields.io/pypi/dm/odaislib.svg)
![GitHub stars](https://img.shields.io/github/stars/odai501/odaislib.svg)

**odaislib** هي مكتبة بايثون شاملة ومتقدمة، صُممت لتوفير أدوات قوية للتفاعل مع منصات التواصل الاجتماعي، والتحقق من البريد الإلكتروني، وأدوات مساعدة متنوعة، وكل ذلك في حزمة واحدة سهلة الاستخدام.

---

## ⚠️ تنبيه أخلاقي وقانوني

> **📢 هام**: هذه المكتبة مخصصة للأغراض التعليمية والبحثية فقط. استخدامها في:
> - اختراق الحسابات
> - انتهاك خصوصية الآخرين
> - تجاوز سياسات الخدمة (Terms of Service)
> - أي نشاط غير قانوني أو غير أخلاقي
>
> **يُعتبر غير قانوني ويعرّضك للمساءلة القانونية**. أنت المسؤول الوحيد عن أي استخدام للمكتبة. نحن ندعم الاستخدام المسؤول والأخلاقي للتكنولوجيا.

---

## ✨ المميزات الرئيسية

| المجال | المميزات |
| :--- | :--- |
| **🌐 فيسبوك (Facebook)** | تسجيل الدخول بـ 4 طرق مختلفة (basic, auth, mobile, blockslogin)، استخراج معلومات الحساب (الاسم، المعرف، الصورة)، استخراج جهات الاتصال، تاريخ الميلاد، البحث عن الحسابات (OSINT) |
| **📸 إنستغرام (Instagram)** | تسجيل الدخول، التحقق من اسم المستخدم، التحقق من البريد الإلكتروني، استخراج معلومات الملف الشخصي، استعادة كلمة المرور، تحديد تاريخ إنشاء الحساب من المعرف، البحث عن حسابات عشوائية |
| **💬 ثريدز (Threads)** | تسجيل الدخول، جلب معلومات الملف الشخصي (المتابعين، المنشورات، السيرة الذاتية) |
| **📧 التحقق من البريد الإلكتروني** | دعم متكامل لـ: **Gmail**، **Yahoo**، **Outlook**، **AOL**، **GMX**، **hi2.in** – مع تحديد الحالة (متاح/مستخدم) |
| **📬 أوتلوك (Outlook) المتقدم** | تسجيل الدخول، جلب الملف الشخصي (الاسم، الدولة، تاريخ الميلاد)، البحث عن كلمات مفتاحية في البريد |
| **🎮 ستيم (Steam)** | تسجيل الدخول، جلب معلومات الحساب (البريد الإلكتروني، الدولة، الرصيد، المستوى، سنوات العضوية) |
| **🧸 روبلوكس (Roblox)** | التحقق من توفر اسم المستخدم |
| **🎬 كيك (Kick)** | تسجيل الدخول، معلومات القناة، البث المباشر، غرفة الدردشة، المتابعين، المقاطع، لوحات المتصدرين، الاستطلاعات، متابعة/إلغاء متابعة القنوات، إرسال رسائل، البحث |
| **📱 تيليغرام (Telegram)** | التحقق من اسم المستخدم عبر Fragment |
| **🐙 جيت هاب (GitHub)** | معلومات المستخدم، قائمة المستودعات، المتابعين، من يتابعهم |
| **📌 بينتريست (Pinterest)** | جلب جميع المنشورات مع التفاصيل، تحميل الوسائط (صور/فيديو) |
| **🎫 ديسكورد (Discord)** | استخراج معلومات الدعوات (السيرفر، الأعضاء، المنشئ، تاريخ الانتهاء) |
| **🎮 بلودسترايك (Bloodstrike)** | تسجيل الدخول والتحقق من الحساب |
| **🛠 أدوات مساعدة** | **وكيل (Proxy)**: بناء وتحليل الوكسيات بمرونة، **ريكابتشا (reCAPTCHA)**: حل آلي V2/V3، **الطقس**: معلومات الطقس بناءً على الموقع، **معلومات الحزمة**: بيانات PyPI (التحميلات، المعلومات العامة)، **تحويل الملفات**: رفع الكود إلى Pastie، **البحث عن الاسم من رقم الهاتف**، **استعادة كلمة المرور** (Konami)، **تسجيل الدخول إلى Zefame و Damkom** |

---

## 📥 التثبيت

```bash
pip install odaislib
```

أو باستخدام Poetry:

```bash
poetry add odaislib
```

---

## 🚀 أمثلة الاستخدام

### 1️⃣ فئة Proxy – بناء الوكيل بسهولة

```python
from odaislib import Proxy

# وكيل HTTP عادي
proxy = Proxy.build("127.0.0.1:8080")
print(proxy)
# {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# وكيل مع مصادقة
proxy = Proxy.build("http://user:pass@proxy.com:3128")
print(proxy)

# وكيل SOCKS5
proxy = Proxy.build("socks5://127.0.0.1:1080")
print(proxy)

# استخراج الوكيل كـ string
raw = Proxy.raw("127.0.0.1:8080")
print(raw)  # http://127.0.0.1:8080
```

---

### 2️⃣ فيسبوك (Facebook)

#### تسجيل الدخول بطرق متعددة

```python
from odaislib import facebook

# الطريقة الأساسية
result = facebook.basic("email@example.com", "password")
print(result)
# {'status': 'success', 'account_id': '123456', 'username': 'user', ...}

# طريقة auth (via graph.facebook.com)
result = facebook.auth("email@example.com", "password")
print(result)
# {'status': 'success', 'uid': '123456', 'cookies': 'c_user=...; xs=...', ...}

# طريقة mobile (محاكاة الجوال)
result = facebook.mobile("email@example.com", "password")
print(result)

# طريقة blockslogin (محاكاة m.facebook.com)
fb = facebook()
result = fb.blockslogin("email@example.com", "password")
print(result)
```

#### استخراج معلومات الحساب (باستخدام الكوكيز)

```python
from odaislib import facebook

cookies = "c_user=123456; xs=abc123; datr=...; sb=..."

# معلومات الحساب الأساسية مع حسابات إنستغرام المرتبطة
info = facebook.account_info.info(cookies)
print(info)
# {'facebook_name': 'Odai', 'instagram_accounts': [{'username': '...'}]}

# جهات الاتصال (الإيميلات وأرقام الهواتف)
contacts = facebook.account_info.contact(cookies)
print(contacts)
# {'emails': ['user@example.com'], 'phones': ['+962...']}

# تاريخ الميلاد
birthday = facebook.account_info.birthday(cookies)
print(birthday)
# {'birthday': '2000-05-09'}

# البحث عن حساب (OSINT)
result = facebook.account_info.osint("username_or_id")
print(result)
```

---

### 3️⃣ إنستغرام (Instagram)

```python
from odaislib import instagram

# تسجيل الدخول
result = instagram.login("username", "password")
print(result)

# التحقق من اسم المستخدم
result = instagram.checkusername("username")
print(result)  # {'status': 'available'/'taken'}

# التحقق من البريد الإلكتروني
insta = instagram()
result = insta.checkemail("email@example.com")
print(result)

# معلومات حساب عام (عبر PeekViewer)
result = instagram.info("username")
print(result)
# {'id': '...', 'full_name': '...', 'followers': 1000, ...}

# تاريخ إنشاء الحساب من المعرف
result = instagram.date("1234567890")
print(result)  # {'date': 2020, ...}

# البحث عن حسابات عشوائية
result = instagram.search()
print(result)  # {'users': ['user1', 'user2', ...]}

# استعادة كلمة المرور (التحقق من وجود الحساب)
insta = instagram()
result = insta.reset("email@example.com")
print(result)
```

---

### 4️⃣ ثريدز (Threads)

```python
from odaislib import threads

# تسجيل الدخول
result = threads.login("username", "password")
print(result)

# معلومات الملف الشخصي
result = threads.info("username")
print(result)
# {'username': '...', 'name': '...', 'followers': 1000, 'bio': '...', 'posts': [...]}
```

---

### 5️⃣ التحقق من البريد الإلكتروني

```python
from odaislib import checkems

# Gmail
result = checkems.gmail("username")
print(result)  # {'status': 'available'/'taken'}

# Yahoo
result = checkems.yahoo("username")
print(result)

# Outlook
result = checkems.outlook("email@outlook.com")
print(result)

# AOL
result = checkems.aol("username@aol.com")
print(result)

# GMX
available, suggestions = checkems.gmx("username@gmx.com")
print(f"Available: {available}, Suggestions: {suggestions}")

# hi2.in
ch = checkems()
result = ch.hi2("username@hi2.in")
print(result)
```

---

### 6️⃣ أوتلوك المتقدم (Outlook)

```python
from odaislib import Outlook

out = Outlook()
result = out.login("email@outlook.com", "password", keyword="بحث")
print(result)
# {
#   'status': True,
#   'email': '...',
#   'profile': {'name': '...', 'country': '...', 'birth_date': '...'},
#   'keyword_result': {'found': True, 'count': 5}
# }
```

---

### 7️⃣ ستيم (Steam)

```python
from odaislib import steam

# تسجيل الدخول
status, data = steam.login("username", "password")
if status == "SUCCESS":
    session = data
    info = steam.info(session)
    print(info)
    # {'Email': '...', 'Country': '...', 'Balance': '...', 'Level': '...'}
else:
    print("Login failed:", data)
```

---

### 8️⃣ روبلوكس (Roblox)

```python
from odaislib import roblox

result = roblox.usernamecheck("username")
print(result)  # {'available': True/False}
```

---

### 9️⃣ تيليغرام (Telegram)

```python
from odaislib import telegram

result = telegram.checkusername("username")
print(result)
# {'status': True, 'username': 'username', 'state': 'available'/'for sell'/'on telegram'}
```

---

### 🔟 كيك (Kick)

```python
from odaislib import kick

k = kick.Kick()

# تسجيل الدخول
login_result = k.login("email@example.com", "password")
print(login_result)

# معلومات القناة
channel = k.channel_info("channel_slug")
print(channel)
# {
#   'channel': {'id': ..., 'slug': ..., 'followers': ...},
#   'user': {'username': ..., 'bio': ...},
#   'livestream': {'is_live': True, 'title': ..., 'viewers': ...}
# }

# البث المباشر
live = k.livestream("channel_slug")
print(live)

# غرفة الدردشة
chat = k.chatroom("channel_slug")
print(chat)

# المقاطع
clips = k.clips("channel_slug", cursor=0, limit=20)
print(clips)

# متابعة/إلغاء متابعة
k.follow("channel_slug")
k.unfollow("channel_slug")

# إرسال رسالة
k.send_message(chatroom_id, "Hello!")

# البحث
search = k.search("query")
print(search)
```

---

### 1️⃣1️⃣ جيت هاب (GitHub)

```python
from odaislib import github

# معلومات المستخدم
info = github.info("odai501")
print(info['data'])
# {'username': '...', 'name': '...', 'followers': ..., 'public_repos': ...}

# المستودعات
repos = github.repositoriesinfo("odai501")
print(repos['data'])

# المتابعين
followers = github.followersinfo("odai501")
print(followers['data'])

# من يتابعهم
following = github.followingsinfo("odai501")
print(following['data'])
```

---

### 1️⃣2️⃣ بينتريست (Pinterest)

```python
from odaislib import pinterest

# جلب المنشورات بدون تحميل
result = pinterest.info("username")
print(result)
# {
#   'user': {'name': '...', 'followers': ...},
#   'pins_count': 100,
#   'pins': [{'index': 1, 'type': 'image', 'description': '...', 'url': '...'}]
# }

# جلب وتحميل جميع الوسائط
result = pinterest.info("username", download=True)
# سيتم إنشاء مجلد downloads_username/ يحتوي على جميع الصور والفيديوهات
```

---

### 1️⃣3️⃣ ديسكورد (Discord)

```python
from odaislib import inviteinfo

result = inviteinfo("discord.gg/invite_code")
print(result)
# {
#   'server': {'name': '...', 'members': 1000, 'online': 200},
#   'inviter': {'username': '...', 'id': '...'},
#   'invite': {'code': '...', 'expires': '2025-01-01 00:00:00'}
# }
```

---

### 1️⃣4️⃣ بلودسترايك (Bloodstrike)

```python
from odaislib import bloodstrike

result = bloodstrike.login("username", "password")
print(result)  # {'status': 'success'/'not_found'/'bad password'}
```

---

### 1️⃣5️⃣ أدوات مساعدة إضافية

#### ريكابتشا (reCAPTCHA)

```python
from odaislib import recaptcha

r = recaptcha()

# V3
result = r.V3(siteUrl="https://example.com", siteKey="your_site_key")
print(result['token'])

# V2
result = r.V2(siteUrl="https://example.com", siteKey="your_site_key")
print(result['token'])
```

#### معلومات الطقس

```python
from odaislib import weatherinfo

weather = weatherinfo.info()
print(weather)
# {'city': 'Amman', 'forecast': [{'time': '01 AM', 'tempC': '15'}, ...]}
```

#### معلومات حزمة بايثون

```python
from odaislib import pipinfo

result = pipinfo.info("requests")
print(result)
# {'package': 'requests', 'total_downloads': 1000000, 'public info': {...}}
```

#### تحويل ملف بايثون إلى رابط (Pastie)

```python
from odaislib import file2link

result = file2link.convert("my_script.py")
print(result['paste_link'])  # رابط الملف
```

#### البحث عن الاسم من رقم الهاتف

```python
from odaislib import namefromphone

n = namefromphone()
names = n.get_name("123456789", "JO")  # JO = الأردن
print(names)
```

#### استعادة كلمة المرور (Konami)

```python
from odaislib import konami

k = konami()
result = k.reset("email@example.com")
print(result)  # {'status': 'success', 'message': 'reset link sent'}
```

#### تسجيل الدخول إلى Zefame

```python
from odaislib import zefame

result = zefame.login("username", "password")
print(result)  # {'status': 'success', 'balance': 10.5}
```

#### تسجيل الدخول إلى Damkom

```python
from odaislib import damkom

result = damkom.login("username", "password")
print(result)  # {'status': 'success', 'balance': '10.5'}
```

---

## 📦 المتطلبات (Dependencies)

يتم تثبيت هذه التبعيات تلقائياً عند تثبيت المكتبة:

```toml
requests >= 2.31.0
httpx >= 0.27.0
user-agent >= 0.1.10
beautifulsoup4 >= 4.12.3
pycryptodome >= 3.20.0
urllib3 >= 2.2.1
```

**تبعيات اختيارية (للوظائف المتقدمة)**:
- `cloudscraper` – لـ Kick (تجاوز Cloudflare)
- `curl_cffi` – بديل لـ Kick
- `faker` – لتوليد بيانات وهمية

---

## 👨‍💻 المطور

**Odai @K33K1**

- Telegram: [@K33K1](https://t.me/K33K1)
- GitHub: [@odai501](https://github.com/odai501)
- PyPI: [odaislib](https://pypi.org/project/odaislib/)

---

## 🤝 المساهمة (Contributing)

نرحب بمساهماتكم! إذا أردت المساعدة في تطوير المكتبة:

1. **استنساخ** (Fork) المستودع.
2. أنشئ **فرعاً** جديداً (`git checkout -b feature/amazing-feature`).
3. أجرِ التغييرات وأضف **اختبارات**.
4. تأكد من اجتياز الاختبارات (`pytest`).
5. ارفع التغييرات (`git push origin feature/amazing-feature`).
6. افتح **Pull Request** إلى فرع `main`.

### إرشادات التطوير

- استخدم **Black** لتنسيق الكود.
- استخدم **Flake8** أو **Ruff** للتحقق من الأسلوب.
- أضف **Docstrings** للدوال الجديدة.
- التزم بـ **Semantic Versioning** للإصدارات.

---

## 📄 الترخيص

هذا المشروع مرخص بموجب [MIT License](LICENSE).

---

## ⭐ الدعم

إذا أعجبتك المكتبة، لا تنسَ منحها **نجمة (⭐)** على GitHub! هذا يساعدني في الاستمرار في تطويرها.

---

**تم التطوير بكل ❤️ بواسطة Odai @K33K1**

---

*استخدم التكنولوجيا بحكمة ومسؤولية. 🔒*
