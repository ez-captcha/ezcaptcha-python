import time
from enum import Enum
import requests
from ezcaptcha.error import BaseEzCaptchaException
from ezcaptcha.language import lang_dict


class EzCaptcha:
    class AllTaskType(Enum):
        FuncaptchaTaskProxyless = "FuncaptchaTaskProxyless"
        RecaptchaV2TaskProxyless = "RecaptchaV2TaskProxyless"
        RecaptchaV2TaskProxylessS9 = "RecaptchaV2TaskProxylessS9"
        RecaptchaV2STaskProxyless = "RecaptchaV2STaskProxyless"
        RecaptchaV2EnterpriseTaskProxyless = "RecaptchaV2EnterpriseTaskProxyless"
        RecaptchaV2SEnterpriseTaskProxyless = "RecaptchaV2SEnterpriseTaskProxyless"
        RecaptchaV3TaskProxyless = "RecaptchaV3TaskProxyless"
        RecaptchaV3TaskProxylessS9 = "RecaptchaV3TaskProxylessS9"
        RecaptchaV3EnterpriseTaskProxyless = "RecaptchaV3EnterpriseTaskProxyless"
        HcaptchaTaskProxyless = "HcaptchaTaskProxyless"
        AkamaiBMPTaskProxyless = "AkamaiBMPTaskProxyless"

    def __init__(self, client_key: str, lang: str = "en"):
        """
        Init EzCaptcha
        :param client_key: Account client key
        :param lang: language("en" or "zh")
        """
        self.client_key = client_key
        self._api_host = "https://api.ez-captcha.com"
        if lang not in ['en', 'zh']:
            raise BaseEzCaptchaException("Unsupported language")
        self.lang = lang

    def solve(self, task: dict, waiting_interval: int = 3, waiting_timeout: int = 120, print_log: bool = False):
        """
        start to solve captcha
        :param task: a dict contain task parameters
        :param waiting_interval: Time interval for requesting task results.
        :param waiting_timeout: Timeout for waiting for task results.
        :param print_log: Whether to print detailed logs.
        :return: Token
        """
        validate_result = self._task_validator(task)
        if isinstance(validate_result, BaseEzCaptchaException):
            raise validate_result
        if waiting_interval:
            assert isinstance(waiting_timeout, int)
        if waiting_timeout:
            assert isinstance(waiting_timeout, int)
        if isinstance(task['type'], self.AllTaskType):
            task['type'] = task['type'].value
        task_id = self.create_task(task, print_log)
        solution = self.get_task_result(task_id, task['type'], waiting_interval, waiting_timeout, print_log)
        return solution

    def create_task(self, task: dict, print_log: bool) -> str:
        url = f'{self._api_host}/createTask'
        data = {
            "clientKey": self.client_key,
            "task": task
        }
        try:
            result = requests.post(url, json=data, timeout=8)
            result = result.json()
            if print_log:
                print(f"[Log] {lang_dict['create_task_log_' + self.lang]} {result}")
            taskId = result.get('taskId')
            if taskId is not None:
                return taskId
            else:
                raise BaseEzCaptchaException(f"{lang_dict['null_task_id_log_' + self.lang]}: {result}")
        except Exception as e:
            raise e

    def get_task_result(self, task_id: str, task_type, waiting_interval: int, waiting_timeout: int, print_log: bool) -> dict:
        times = 0
        if 'funcaptcha' in task_type.lower():
            waiting_interval = 1
        while times < waiting_timeout:
            try:
                url = f'{self._api_host}/getTaskResult'

                data = {
                    "clientKey": self.client_key,
                    "taskId": task_id
                }
                result = requests.post(url, json=data, timeout=8).json()
                if print_log:
                    print(f"[Log] {lang_dict['get_task_result_log_' + self.lang]} {result}")
                solution = result.get('solution', {})
                if solution:
                    response = None
                    if 'recaptcha' in task_type.lower():
                        response = solution.get('gRecaptchaResponse')
                    elif 'funcaptcha' in task_type.lower() or 'hcaptcha' in task_type.lower():
                        response = solution.get("token")
                    if response:
                        print(f"{lang_dict['get_token_log_' + self.lang]} ", response)
                        solution = {"errorId": result.get("errorId"), "errorCode": result.get("errorCode"), "errorDesc": result.get("errorDesc"), "token": response}
                        return solution
                if result.get("errorId") != 0:
                    solution = {"errorId": result.get("errorId"), "errorCode": result.get("errorCode"),
                                "errorDesc": result.get("errorDesc"), "token": None}
                    return solution
            except Exception as e:
                if print_log:
                    print(f"[Exception] {str(e)}")
            times += waiting_interval
            time.sleep(waiting_interval)
            if print_log:
                print(f"[Log] {lang_dict['waiting_time_log_' + self.lang]} {times}/{waiting_timeout}s")
        solution = {"errorId": 1, "errorCode": "TIME_OUT",
                    "errorDesc": lang_dict['get_token_failed_log_' + self.lang], "token": None}
        return solution

    def _captcha_basic_check(self, params: dict):
        params_keys = params.keys()
        if "websiteURL" not in params_keys:
            return BaseEzCaptchaException(f"\033[33m{lang_dict['missing_websiteURL_log_' + self.lang]}\033[0m")
        if "websiteKey" not in params_keys:
            return BaseEzCaptchaException(f"\033[33m{lang_dict['missing_websiteKey_log_' + self.lang]}\033[0m")
        return None

    def _check_recaptcha(self, task: dict):
        basic_check = self._captcha_basic_check(task)
        if isinstance(basic_check, BaseEzCaptchaException):
            return basic_check
        if 'isInvisible' not in task:
            print(f"\033[33m{lang_dict['recaptcha_missing_isInvisible_log_' + self.lang]}\033[0m")
        task_type = task["type"]
        if task_type == self.AllTaskType.RecaptchaV2SEnterpriseTaskProxyless:
            if 's' not in task:
                return BaseEzCaptchaException(f"\033[33m{lang_dict['recaptcha_missing_s_log_' + self.lang]}\033[0m")
        if task_type == self.AllTaskType.RecaptchaV3TaskProxyless or task_type == self.AllTaskType.RecaptchaV3EnterpriseTaskProxyless or task_type == self.AllTaskType.RecaptchaV3TaskProxylessS9:
            if 'pageAction' not in task:
                print(f"\033[33m{lang_dict['recaptcha_missing_pageAction_log_' + self.lang]}\033[0m")
        return None

    def _check_hcaptcha(self, task: dict):
        basic_check = self._captcha_basic_check(task)
        if isinstance(basic_check, BaseEzCaptchaException):
            return basic_check
        return None

    def _check_funcaptcha(self, task: dict):
        basic_check = self._captcha_basic_check(task)
        if isinstance(basic_check, BaseEzCaptchaException):
            return basic_check
        return None

    def _print_all_task_type(self):
        list_types = [task.value for task in self.AllTaskType]
        return "\n".join(list_types)

    def _task_validator(self, task: dict):
        task_type = task["type"]
        if not isinstance(task_type, str):
            if not isinstance(task_type, self.AllTaskType):
                return BaseEzCaptchaException(f"{lang_dict['unsupport_type_log_' + self.lang]} {str(task_type)}" + lang_dict['support_type_log_' + self.lang] + self._print_all_task_type())
            if "Recaptcha" in task_type.name:
                return self._check_recaptcha(task)
            elif task_type == self.AllTaskType.FuncaptchaTaskProxyless:
                return self._check_funcaptcha(task)
            elif task_type == self.AllTaskType.HcaptchaTaskProxyless:
                return self._check_hcaptcha(task)
        else:
            if task_type.lower() not in [task.value.lower() for task in self.AllTaskType]:
                return BaseEzCaptchaException(f"{lang_dict['unsupport_type_log_' + self.lang]} {str(task_type)}" + lang_dict['support_type_log_' + self.lang] + self._print_all_task_type())
            if "recaptcha" in task_type.lower():
                return self._check_recaptcha(task)
            elif "funcaptcha" in task_type.lower():
                return self._check_funcaptcha(task)
            elif "hcaptcha" in task_type.lower():
                return self._check_hcaptcha(task)

