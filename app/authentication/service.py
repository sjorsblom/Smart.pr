from http import HTTPStatus
from flask import g, request
from app.helpers.utils import json_abort, safe_get_env_var
import jwt
from app.authentication.entities.user import User, UserSchema
from mongoengine import DoesNotExist


def verify_authentication():
    try:
        bearer = request.headers.get('Authorization')
        auth_token = bearer.split()[1]
    except:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "Invalid Token"
        })

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

    try:
        user = User.objects(id=payload['user_id']).get()
    except DoesNotExist:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "Invalid Token"
        })

    g.user = payload['user_id']
