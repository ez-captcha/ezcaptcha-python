[English](README.md) | [中文版](README_zh.md)
# 中文版
EzCaptcha SDK for python
### 安装
```
pip install ezcaptcha
```
### 使用
示例: 
```python
from ezcaptcha import EzCaptcha

# Recaptcha
ez = EzCaptcha(client_key="yourapiKey")
solution = ez.solve({
    "websiteURL": "https://www.google.com/recaptcha/api2/demo",
    "websiteKey": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "type": ez.AllTaskType.RecaptchaV2TaskProxyless,  # 或使用字符串 "RecaptchaV2TaskProxyless"
    "isInvisible": False
})
if solution.get("errorId") == 0:
    print(solution.get("token"))
else:
    print(solution.get("errorDesc"))

# Funcaptcha
solution = ez.solve({
  "websiteURL": "https://iframe.arkoselabs.com",
  "websiteKey": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
  "type": ez.AllTaskType.FuncaptchaTaskProxyless,  # 或使用字符串 "FuncaptchaTaskProxyless"
})
```

指定日志输出及提示的语言，支持中文"zh"、英文"en"，默认为英文"en"
```python
from ezcaptcha import EzCaptcha

ez = EzCaptcha(client_key="yourapiKey", lang="zh")
...
```
开启日志打印功能
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

指定等待时间间隔 `waiting_interval`(默认为 3秒)，任务结果等待超时时间`waiting_timeout`(默认为120秒)
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

