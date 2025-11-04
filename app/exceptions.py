#!/usr/bin/python3
"""
Custom Exception Classes for API Error Handling
"""


class APIException(Exception):
    """Base exception class for API errors"""
    
    def __init__(self, message, status_code=400, payload=None):
        """
        Initialize API exception
        
        Args:
            message: Error message
            status_code: HTTP status code (default 400)
            payload: Additional error data
        """
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """Convert exception to dictionary for JSON response"""
        error_dict = {
            'error': self.message,
            'status_code': self.status_code
        }
        if self.payload:
            error_dict['details'] = self.payload
        return error_dict


class ValidationError(APIException):
    """Exception raised for validation errors"""
    
    def __init__(self, message, payload=None):
        super().__init__(message, status_code=400, payload=payload)


class NotFoundError(APIException):
    """Exception raised when resource is not found"""
    
    def __init__(self, message="Resource not found", payload=None):
        super().__init__(message, status_code=404, payload=payload)


class UnauthorizedError(APIException):
    """Exception raised for unauthorized access"""
    
    def __init__(self, message="Unauthorized access", payload=None):
        super().__init__(message, status_code=401, payload=payload)


class ForbiddenError(APIException):
    """Exception raised for forbidden access"""
    
    def __init__(self, message="Forbidden", payload=None):
        super().__init__(message, status_code=403, payload=payload)


class ConflictError(APIException):
    """Exception raised for resource conflicts (e.g., duplicate entries)"""
    
    def __init__(self, message="Resource conflict", payload=None):
        super().__init__(message, status_code=409, payload=payload)


class ServerError(APIException):
    """Exception raised for internal server errors"""
    
    def __init__(self, message="Internal server error", payload=None):
        super().__init__(message, status_code=500, payload=payload)
