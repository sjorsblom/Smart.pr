from flask import Blueprint, request
from app.authentication.entities.user import User, UserSchema
from app.helpers.utils import json_abort
from http import HTTPStatus
from werkzeug.security import check_password_hash, generate_password_hash
from mongoengine import DoesNotExist


bp_list = Blueprint('api-authentication', __name__,
                    url_prefix='/api/authentication')


@bp_list.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()

    email = json_data['email']
    password = json_data['password']

    try:
        user = User.objects(email=email).get()
        if check_password_hash(user.password, password):
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


@bp_list.route('/register', methods=['POST'])
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
    )

    return UserSchema().dumps(user), HTTPStatus.OK
