from http import HTTPStatus
from flask import g, request
from app.helpers.utils import json_abort, safe_get_env_var
import jwt
from app.authentication.entities.user import User, UserSchema
from mongoengine import DoesNotExist


def verify_authentication():
    """Verify the user by Authorization Bearer token

    Returns:
      A session vairbale in flask.g containing the id of the current user
    Raises:
      HTTP 401 Unauthorized, containing a message of the reason
    """
    try:
        bearer = request.headers.get('Authorization')
        auth_token = bearer.split()[1]
    except:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "Invalid Token"
        })

    # Decode JWT Token
    secret_key = safe_get_env_var("SECRET_KEY")
    try:
        payload = jwt.decode(auth_token, secret_key, algorithms=["HS256"])
    except jwt.InvalidSignatureError:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "Invalid Token"
        })
    except jwt.ExpiredSignatureError:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "Invalid Token"
        })
    except jwt.DecodeError:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "Invalid Token"
        })

    # Verify existence of user
    try:
        User.objects(id=payload['user_id']).get()
    except DoesNotExist:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "Invalid Token"
        })

    g.user = payload['user_id']
