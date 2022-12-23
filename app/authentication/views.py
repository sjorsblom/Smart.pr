from flask import Blueprint, request
from app.authentication.entities.user import User, UserSchema
from app.helpers.utils import json_abort
from http import HTTPStatus
from werkzeug.security import check_password_hash, generate_password_hash
from mongoengine import DoesNotExist
from app.helpers.utils import safe_get_env_var
from datetime import timedelta, datetime
import jwt


bp_authentication = Blueprint('api-authentication', __name__,
                              url_prefix='/api/authentication')


@bp_authentication.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()

    email = json_data['email']
    password = json_data['password']

    try:
        user = User.objects(email=email).get()
        if check_password_hash(user.password, password):
            # Add jwt token to be used during calls to other endpoints
            secret_key = safe_get_env_var("SECRET_KEY")
            user.token = jwt.encode(
                {
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(minutes=60)
                },
                secret_key,
                "HS256"
            )
            return UserSchema().dumps(user), HTTPStatus.OK
    except DoesNotExist:
        json_abort(HTTPStatus.UNAUTHORIZED, {
            "error": "Invalid Login",
            "error_description": "Email and password combination unknown!"
        })

    json_abort(HTTPStatus.UNAUTHORIZED, {
        "error": "Invalid Login",
        "error_description": "Email and password combination unknown!"
    })


@bp_authentication.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()

    email = json_data['email']
    password = json_data['password']

    user = User.objects(email=email).first()
    if user:
        json_abort(HTTPStatus.CONFLICT, {
            "error": "Email used",
            "error_description": "Email is already in use!"
        })

    user = User(
        email=email,
        password=generate_password_hash(password)
    ).save()

    return UserSchema().dumps(user), HTTPStatus.OK
