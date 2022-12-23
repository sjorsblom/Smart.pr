from os import getenv

from dotenv import load_dotenv
from flask import abort, jsonify


def json_abort(status_code, data=None):
    """Json abort function

    Args:
      status_code (int): http code of the abort protocol
      data (str): message for the abort
    """
    response = jsonify(data)
    response.status_code = status_code
    abort(response)


def safe_get_env_var(key):
    """Safely import enviroment values

    Args:
      key (str): key value of the enviroment variable
    """
    load_dotenv()
    try:
        return getenv(key)
    except KeyError:
        raise NameError(f"Missing {key} environment variable.")
