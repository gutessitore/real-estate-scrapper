from firebase_admin import db
import firebase_admin


def _connect_to_firebase(api_key: dict, database_url: str):
    if not firebase_admin._apps:
        cred_obj = firebase_admin.credentials.Certificate(api_key)
        firebase_admin.initialize_app(cred_obj, dict(databaseURL=database_url))


def connect_to_firebase() -> None:
    api_key = {}
    database_url = "https://real-estate-scrapper-2ac0c-default-rtdb.firebaseio.com/"
    _connect_to_firebase(api_key, database_url)


def upload_json_to_firebase(
        json_data: dict, address: str,
        api_key: dict = None, database_url: str = None, is_new=True):
    try:
        if api_key and database_url:
            _connect_to_firebase(api_key, database_url)
    except ValueError:
        pass
    ref = db.reference(address)

    # with open(json_file_path, "r") as f:
    #     file_contents = json.load(f)
    if is_new:
        ref.set(json_data)


def get_firebase_data(address: str, api_key: dict = None, database_url: str = None):
    try:
        if api_key and database_url:
            _connect_to_firebase(api_key, database_url)
    except ValueError:
        pass
    ref = db.reference(address)
    return ref.get()

