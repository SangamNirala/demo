from typing import Any, Optional
from fastapi.responses import JSONResponse

def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200
) -> JSONResponse:
    """Standard success response"""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )

def error_response(
    message: str = "Error occurred",
    errors: Optional[dict] = None,
    status_code: int = 400
) -> JSONResponse:
    """Standard error response"""
    content = {
        "success": False,
        "message": message
    }
    
    if errors:
        content["errors"] = errors
    
    return JSONResponse(
        status_code=status_code,
        content=content
    )

def paginated_response(
    items: list,
    total: int,
    page: int,
    page_size: int,
    message: str = "Success"
) -> JSONResponse:
    """Paginated response"""
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": {
                "items": items,
                "pagination": {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": (total + page_size - 1) // page_size
                }
            }
        }
    )
