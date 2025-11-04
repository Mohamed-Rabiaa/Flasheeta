#!/usr/bin/python3
"""
API Error Handlers
Provides consistent error responses across all API endpoints
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException
from app.exceptions import APIException
import logging

# Configure logging
logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """
    Register error handlers with the Flask application
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        """Handle custom API exceptions"""
        logger.warning(f"API Exception: {error.message}", extra={
            'status_code': error.status_code,
            'payload': error.payload
        })
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """Handle ValueError exceptions from services"""
        logger.warning(f"ValueError: {str(error)}")
        response = jsonify({
            'error': str(error),
            'status_code': 400
        })
        response.status_code = 400
        return response
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 Not Found errors"""
        # Only return JSON for API routes
        from flask import request
        if request.path.startswith('/api/'):
            logger.info(f"404 Not Found: {request.path}")
            response = jsonify({
                'error': 'Resource not found',
                'status_code': 404,
                'path': request.path
            })
            response.status_code = 404
            return response
        # Let Flask handle non-API 404s normally
        return error
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handle 401 Unauthorized errors"""
        from flask import request
        if request.path.startswith('/api/'):
            logger.warning(f"401 Unauthorized: {request.path}")
            response = jsonify({
                'error': 'Unauthorized access',
                'status_code': 401,
                'message': 'Please log in to access this resource'
            })
            response.status_code = 401
            return response
        return error
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handle 403 Forbidden errors"""
        from flask import request
        if request.path.startswith('/api/'):
            logger.warning(f"403 Forbidden: {request.path}")
            response = jsonify({
                'error': 'Forbidden',
                'status_code': 403,
                'message': 'You do not have permission to access this resource'
            })
            response.status_code = 403
            return response
        return error
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 Method Not Allowed errors"""
        from flask import request
        if request.path.startswith('/api/'):
            logger.warning(f"405 Method Not Allowed: {request.method} {request.path}")
            response = jsonify({
                'error': 'Method not allowed',
                'status_code': 405,
                'method': request.method,
                'path': request.path
            })
            response.status_code = 405
            return response
        return error
    
    @app.errorhandler(422)
    def handle_unprocessable_entity(error):
        """Handle 422 Unprocessable Entity errors"""
        from flask import request
        if request.path.startswith('/api/'):
            logger.warning(f"422 Unprocessable Entity: {request.path}")
            response = jsonify({
                'error': 'Unprocessable entity',
                'status_code': 422,
                'message': 'The request was well-formed but contains invalid data'
            })
            response.status_code = 422
            return response
        return error
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 Internal Server Error"""
        from flask import request
        if request.path.startswith('/api/'):
            logger.error(f"500 Internal Server Error: {request.path}", exc_info=True)
            response = jsonify({
                'error': 'Internal server error',
                'status_code': 500,
                'message': 'An unexpected error occurred. Please try again later.'
            })
            response.status_code = 500
            return response
        return error
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle any unexpected exceptions"""
        from flask import request
        
        # If it's an HTTPException, let it be handled by its specific handler
        if isinstance(error, HTTPException):
            return error
        
        # For API routes, return JSON error
        if request.path.startswith('/api/'):
            logger.error(f"Unexpected error: {str(error)}", exc_info=True)
            response = jsonify({
                'error': 'An unexpected error occurred',
                'status_code': 500,
                'message': str(error) if app.debug else 'Please try again later.'
            })
            response.status_code = 500
            return response
        
        # For non-API routes, re-raise to let Flask handle it
        raise error
