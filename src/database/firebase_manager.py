from firebase_admin import App
from firebase_admin import db
import firebase_admin
import json


def _connect_to_firebase(api_key_path: str, database_url: str):
    cred_obj = firebase_admin.credentials.Certificate(api_key_path)
    firebase_admin.initialize_app(cred_obj, dict(databaseURL=database_url))


def upload_json_to_firebase(
        json_file_path: str, address: str,
        api_key_path: str = None, database_url: str = None, is_new=True):
    try:
        if api_key_path and database_url:
            _connect_to_firebase(api_key_path, database_url)
    except ValueError:
        pass
    ref = db.reference(address)

    with open(json_file_path, "r") as f:
        file_contents = json.load(f)
    if is_new:
        ref.set(file_contents)


def get_firebase_data(address: str, api_key_path: str = None, database_url: str = None):
    try:
        if api_key_path and database_url:
            _connect_to_firebase(api_key_path, database_url)
    except ValueError:
        pass
    ref = db.reference(address)
    return ref.get()

