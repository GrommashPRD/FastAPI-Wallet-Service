class UserAlreadyHaveWallet(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class WalletNotFound(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class InsufficientFunds(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class DetalizationError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)


class WalletDontExist(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
