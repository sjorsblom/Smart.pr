from app.authentication.service import verify_authentication
from flask_restful import wraps


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_authentication()
        return func(*args, **kwargs)
    return wrapper
