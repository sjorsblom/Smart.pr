from os import getenv

from dotenv import load_dotenv
from flask import abort, jsonify


def json_abort(status_code, data=None):
    response = jsonify(data)
    response.status_code = status_code
    abort(response)


def safe_get_env_var(key):
    load_dotenv()
    try:
        return getenv(key)
    except KeyError:
        raise NameError(f"Missing {key} environment variable.")
