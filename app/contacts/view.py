from flask import Blueprint, request

bp_list = Blueprint('api-contacts' , __name__, url_prefix='/api/contacts')


@bp_list.route('/', methods=['POST'])
def create_contact():
    return


@bp_list.route('/', methods=['GET'])
def get_contacts():
    return
    

@bp_list.route('/<contact_id>', methods=['GET'])
def get_contact(contact_id):
    return


@bp_list.route('/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    return
