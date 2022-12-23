from flask import Blueprint, request, g
from app.contactlists.entities.contactlist import ContactList, ContactListSchema
from app.contacts.entities.contact import Contact, ContactSchema
from http import HTTPStatus
from app.authentication.decorators import require_login
from mongoengine import DoesNotExist
from app.helpers.utils import json_abort

bp_list = Blueprint('api-contactlists', __name__,
                    url_prefix='/api/contactlists')


@bp_list.route('/', methods=['POST'])
@require_login
def create_contactlist():
    json_data = request.get_json()

    cleaned_data = ContactListSchema().load(
        user=g.user,
        name=json_data['name'],
        description=json_data['description']
    )

    contactlist = ContactList(cleaned_data).save()
    return ContactListSchema().dumps(contactlist), HTTPStatus.CREATED


@bp_list.route('/', methods=['GET'])
@require_login
def get_contactlists():
    contactlists = ContactList.objects(user=g.user)
    return ContactListSchema().dumps(contactlists, many=True), HTTPStatus.OK


@bp_list.route('/<contactlist_id>', methods=['GET'])
@require_login
def get_contactlist(contactlist_id):
    try:
        contactlist = ContactList.objects(pk=contactlist_id, user=g.user).get()
    except DoesNotExist:
        json_abort(HTTPStatus.NOT_FOUND, {
            "error": "Not Found"
        })
    return ContactListSchema().dumps(contactlist), HTTPStatus.OK


@bp_list.route('/<contactlist_id>', methods=['DELETE'])
@require_login
def delete_contactlist(contactlist_id):
    ContactList.objects(pk=contactlist_id, user=g.user).delete()
    return "Contactlist successfully deleted!", HTTPStatus.OK


@bp_list.route('/<contactlist_id>/contacts', methods=['GET'])
def get_contacts_from_contactlist(contactlist_id):
    try:
        contactlist = ContactList.objects(pk=contactlist_id, user=g.user).get()
    except DoesNotExist:
        json_abort(HTTPStatus.NOT_FOUND, {
            "error": "Not Found"
        })
    contacts = contactlist.contacts
    name = request.args.get('name', default=None, type=str)
    if name:
        list(filter(lambda contact: contact['name'] in name, contacts))
    return ContactSchema().dumps(contacts, many=True), HTTPStatus.OK


@bp_list.route('/<contactlist_id>/contacts/<contact_id>', methods=['POST'])
def add_contact_to_contactlist(contactlist_id, contact_id):
    try:
        contact = Contact.objects(pk=contact_id, user=g.user).get()
    except DoesNotExist:
        json_abort(HTTPStatus.NOT_FOUND, {
            "error": "Contact Not Found"
        })
    try:
        contactlist = ContactList.objects(pk=contactlist_id, user=g.user).get()
    except DoesNotExist:
        json_abort(HTTPStatus.NOT_FOUND, {
            "error": "ContactList Not Found"
        })
    contactlist.update(add_to_set__contacts=contact)
    return ContactListSchema().dumps(contactlist), HTTPStatus.OK


@bp_list.route('/<contactlist_id>/contacts/<contact_id>', methods=['DELETE'])
def remove_contact_from_contactlist(contactlist_id, contact_id):
    try:
        contact = Contact.objects(pk=contact_id, user=g.user).get()
    except DoesNotExist:
        json_abort(HTTPStatus.NOT_FOUND, {
            "error": "Contact Not Found"
        })
    try:
        contactlist = ContactList.objects(pk=contactlist_id, user=g.user).get()
    except DoesNotExist:
        json_abort(HTTPStatus.NOT_FOUND, {
            "error": "ContactList Not Found"
        })
    contactlist.update(pull__contacts=contact)
    return ContactListSchema().dumps(contactlist), HTTPStatus.OK
