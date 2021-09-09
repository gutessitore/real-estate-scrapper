from firebase_admin import App
from firebase_admin import db
import firebase_admin
import json


def connect_to_firebase(api_key_path: str, database_url: str) -> App:
    cred_obj = firebase_admin.credentials.Certificate(api_key_path)
    firebase_admin.initialize_app(cred_obj, dict(databaseURL=database_url))


def upload_json(api_key_path: str, database_url: str, json_file_path: str, address: str, is_new=True):
    try:
        connect_to_firebase(api_key_path, database_url)
    except ValueError:
        pass
    ref = db.reference(address)

    with open(json_file_path, "r") as f:
        file_contents = json.load(f)
    if is_new:
        ref.set(file_contents)


def get_firebase_data(api_key_path: str, database_url: str, address: str):
    try:
        connect_to_firebase(api_key_path, database_url)
    except ValueError:
        pass
    ref = db.reference(address)
    return ref.get()

