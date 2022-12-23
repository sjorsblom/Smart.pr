from http import HTTPStatus
from flask import Blueprint, request, g
from app.contacts.entities.contact import Contact, ContactSchema
from app.authentication.decorators import require_login
from mongoengine import DoesNotExist
from app.helpers.utils import json_abort


bp_list = Blueprint('api-contacts', __name__, url_prefix='/api/contacts')


@bp_list.route('/', methods=['POST'])
@require_login
def create_contact():
    json_data = request.get_json()

    cleaned_data = ContactSchema().load(
        user=g.user,
        name=json_data['name'],
        number=json_data['number'],
        email=json_data['email']
    )

    contact = Contact(cleaned_data).save()
    return ContactSchema().dumps(contact), HTTPStatus.CREATED


@bp_list.route('/', methods=['GET'])
@require_login
def get_contacts():
    contacts = Contact.objects(user=g.user)
    return ContactSchema().dumps(contacts, many=True), HTTPStatus.OK


@bp_list.route('/<contact_id>', methods=['GET'])
@require_login
def get_contact(contact_id):
    try:
        contact = Contact.objects(pk=contact_id, user=g.user).get()
    except DoesNotExist:
        json_abort(HTTPStatus.NOT_FOUND, {
            "error": "Not Found"
        })
    return ContactSchema().dumps(contact), HTTPStatus.OK


@bp_list.route('/<contact_id>', methods=['DELETE'])
@require_login
def delete_contact(contact_id):
    Contact.objects(pk=contact_id, user=g.user).delete()
    return "Contact successfully deleted!", HTTPStatus.OK
