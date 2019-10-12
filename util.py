"""utils.py
util
"""
import json

def get_token(json_file):
    """get_token

    :param json_file:
    """
    token = json.load(open(json_file, 'r'))
    return token
