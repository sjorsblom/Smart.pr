from flask_mongoengine import Document
from marshmallow import Schema, fields, post_dump
from mongoengine import StringField
from app.helpers.utils import safe_get_env_var
from datetime import timedelta, datetime
import jwt


class User(Document):
    email = StringField(unique=True)
    password = StringField()


class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    password = fields.Str()

    @post_dump
    def post_dump(self, data, *args, **kwargs):
        secret_key = safe_get_env_var("SECRET_KEY")
        data['token'] = jwt.encode(
            {
                'user_id': data['id'],
                'exp': datetime.utcnow() + timedelta(minutes=60)
            },
            secret_key,
            "HS256"
        )
        return data
