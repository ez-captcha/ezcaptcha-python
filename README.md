[English](README.md) | [中文版](README_zh.md)
## English
EzCaptcha SDK for python
### Install
```
pip install ezcaptcha
```
### Usage
Sample: 
```python
from ezcaptcha import EzCaptcha

# Recaptcha
ez = EzCaptcha(client_key="yourapiKey")
solution = ez.solve({
    "websiteURL": "https://www.google.com/recaptcha/api2/demo",
    "websiteKey": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "type": ez.AllTaskType.RecaptchaV2TaskProxyless,  # or use str "RecaptchaV2TaskProxyless"
    "isInvisible": False
}, print_log=True)
if solution.get("errorId") == 0:
    print(solution.get("token"))
else:
    print(solution.get("errorDesc"))

# Funcaptcha
solution = ez.solve({
  "websiteURL": "https://iframe.arkoselabs.com",
  "websiteKey": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
  "type": ez.AllTaskType.FuncaptchaTaskProxyless,  # or use str "FuncaptchaTaskProxyless"
}, print_log=True)
```

Specify the language of log output and prompts, support "en" and "zh", default "en"
```python
from ezcaptcha import EzCaptcha

ez = EzCaptcha(client_key="yourapiKey", lang="zh")
...
```
Enable log printing function
```python
from ezcaptcha import EzCaptcha

ez = EzCaptcha(client_key="yourapiKey")
solution = ez.solve({
    "websiteURL": "https://www.google.com/recaptcha/api2/demo",
    "websiteKey": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "type": "RecaptchaV2TaskProxyless",
    "isInvisible": False,
}, print_log=True)
```

Specific waiting_interval(default 3s) and waiting_timeout(default 120s)
```python
from ezcaptcha import EzCaptcha

ez = EzCaptcha(client_key="yourapiKey")
solution = ez.solve({
    "websiteURL": "https://www.google.com/recaptcha/api2/demo",
    "websiteKey": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "type": "RecaptchaV2TaskProxyless",
    "isInvisible": False,
}, waiting_interval=1, waiting_timeout=90, print_log=True)
```
