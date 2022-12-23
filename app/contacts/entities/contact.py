from flask_mongoengine import Document
from marshmallow import Schema, fields
from mongoengine import StringField, ReferenceField
from app.authentication.entities.user import User, UserSchema

##########################################
# Documents
##########################################


class Contact(Document):
    user = ReferenceField(User)
    name = StringField()
    number = StringField()
    email = StringField()

##########################################
# Schemas
##########################################


class ContactSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema())
    name = fields.Str()
    number = fields.Str()
    email = fields.Str()
