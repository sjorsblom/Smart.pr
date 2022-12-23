from http import HTTPStatus
from flask import Blueprint, request, g
from app.contacts.entities.contact import Contact, ContactSchema
from app.authentication.entities.user import User
from app.authentication.decorators import require_login
from mongoengine import DoesNotExist
from app.helpers.utils import json_abort


bp_contacts = Blueprint('api-contacts', __name__, url_prefix='/api/contacts')


@bp_contacts.route('/', methods=['POST'])
@require_login
def create_contact():
    json_data = request.get_json()

    # TODO add data cleaning / verification

    contact = Contact(
        user=User.objects(pk=g.user).get(),
        name=json_data['name'],
        number=json_data['number'],
        email=json_data['email']
    ).save()

    return ContactSchema().dumps(contact), HTTPStatus.CREATED


@bp_contacts.route('/', methods=['GET'])
@require_login
def get_contacts():
    contacts = Contact.objects(user=g.user)
    return ContactSchema().dumps(contacts, many=True), HTTPStatus.OK


@bp_contacts.route('/<contact_id>', methods=['GET'])
@require_login
def get_contact(contact_id):
    try:
        contact = Contact.objects(pk=contact_id, user=g.user).get()
    except DoesNotExist:
        json_abort(HTTPStatus.NOT_FOUND, {
            "error": "Not Found"
        })
    return ContactSchema().dumps(contact), HTTPStatus.OK


@bp_contacts.route('/<contact_id>', methods=['DELETE'])
@require_login
def delete_contact(contact_id):
    Contact.objects(pk=contact_id, user=g.user).delete()
    return "Contact successfully deleted!", HTTPStatus.OK
