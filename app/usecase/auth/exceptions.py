class UsernameRequired(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class UserAlreadyExist(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class IncorrectTypeData(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class DataValidationError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class UserNotFound(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class WrongPassword(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class UserNotAuthorized(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
