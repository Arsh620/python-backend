from fastapi import status
from typing import Any, Optional

def success_response(data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK):
    return {
        "success": True,
        "message": message,
        "data": data,
        "status_code": status_code
    }

def error_response(message: str = "Error", status_code: int = status.HTTP_400_BAD_REQUEST, errors: Optional[Any] = None):
    return {
        "success": False,
        "message": message,
        "errors": errors,
        "status_code": status_code
    }