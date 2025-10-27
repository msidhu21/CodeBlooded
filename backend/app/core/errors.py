from fastapi import HTTPException, status

class NotFound(HTTPException):
    def __init__(self, detail="Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class Conflict(HTTPException):
    def __init__(self, detail="Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class Forbidden(HTTPException):
    def __init__(self, detail="Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

