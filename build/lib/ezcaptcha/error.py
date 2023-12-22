class BaseEzCaptchaException(Exception):
    def __init__(self, message):
        super().__init__(self)
        self._message = message

    def __str__(self):
        return f"{type(self).__name__}: {self._message}"

