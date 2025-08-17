class DatabaseError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)

class RecordAlreadyExist(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
