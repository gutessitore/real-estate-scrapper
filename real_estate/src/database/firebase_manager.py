from real_estate.src.utils.utils import get_repo_absolute_path
from firebase_admin import db
import firebase_admin
import os


def _connect_to_firebase(api_key_path: str, database_url: str):
    if not firebase_admin._apps:
        cred_obj = firebase_admin.credentials.Certificate(api_key_path)
        firebase_admin.initialize_app(cred_obj, dict(databaseURL=database_url))


def connect_to_firebase() -> None:
    repo_path = get_repo_absolute_path()
    api_key = os.path.join(repo_path, "real_estate", "src", "database", "real-estate-scrapper-firebase.json")
    database_url = "https://real-estate-scrapper-2ac0c-default-rtdb.firebaseio.com/"
    _connect_to_firebase(api_key, database_url)


def upload_json_to_firebase(
        json_data: dict, address: str,
        api_key_path: str = None, database_url: str = None, is_new=True):
    try:
        if api_key_path and database_url:
            _connect_to_firebase(api_key_path, database_url)
    except ValueError:
        pass
    ref = db.reference(address)

    # with open(json_file_path, "r") as f:
    #     file_contents = json.load(f)
    if is_new:
        ref.set(json_data)


def get_firebase_data(address: str, api_key_path: str = None, database_url: str = None):
    try:
        if api_key_path and database_url:
            _connect_to_firebase(api_key_path, database_url)
    except ValueError:
        pass
    ref = db.reference(address)
    return ref.get()

