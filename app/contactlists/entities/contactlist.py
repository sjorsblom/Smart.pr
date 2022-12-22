from flask_mongoengine import Document
from marshmallow import Schema, fields
from mongoengine import StringField, ReferenceField, ListField
from app.users.entities.user import User, UserSchema
from app.contacts.entities.contact import Contact, ContactSchema

##########################################
# Documents
##########################################

class ContactList(Document):
    user = ReferenceField(User)
    name =  StringField()
    description =  StringField()
    contacts =  ListField(ReferenceField(Contact))
 
##########################################
# Schemas
##########################################

class ContactListSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema())
    name = fields.Str()
    description = fields.Str()
    contacts = fields.List(fields.Nested(ContactSchema()))
