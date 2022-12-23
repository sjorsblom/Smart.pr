from flask_mongoengine import Document
from marshmallow import Schema, fields
from mongoengine import StringField


class User(Document):
    email = StringField(unique=True)
    password = StringField()


class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str()
