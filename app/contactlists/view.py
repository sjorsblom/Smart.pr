from flask import Blueprint, request

bp_list = Blueprint('api-contactlists' , __name__, url_prefix='/api/contactlists')


@bp_list.route('/', methods=['POST'])
def create_contactlist():
    return


@bp_list.route('/', methods=['GET'])
def get_contactlists():
    return
    

@bp_list.route('/<contactlist_id>', methods=['GET'])
def get_contactlist(contactlist_id):
    return


@bp_list.route('/<contactlist_id>', methods=['DELETE'])
def delete_contactlist(contactlist_id):
    return


@bp_list.route('/<contactlist_id>/contacts', methods=['GET'])
def get_contacts_from_contactlist(contactlist_id):
    return


@bp_list.route('/<contactlist_id>/contacts/<contact_id>', methods=['POST'])
def add_contact_to_contactlist(contactlist_id, contact_id):
    return


@bp_list.route('/<contactlist_id>/contacts/<contact_id>', methods=['DELETE'])
def remove_contact_from_contactlist(contactlist_id, contact_id):
    return



