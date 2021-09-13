from database.firebase_manager import get_firebase_data, upload_json_to_firebase, _connect_to_firebase
from postprocess.coordinates import add_lat_lon_to_json
from utils.utils import get_repo_absolute_path
from collector import scrape_sites
import os


def connect_to_firebase(repo_path: str) -> None:
    api_key = os.path.join(repo_path, "src", "database", "real-estate-scrapper-firebase.json")
    database_url = "https://real-estate-scrapper-2ac0c-default-rtdb.firebaseio.com/"
    _connect_to_firebase(api_key, database_url)


def collect_data(address: str):
    repo_path = get_repo_absolute_path()
    connect_to_firebase(repo_path)
    firebase_data = get_firebase_data(address)

    if data_in_firebase(firebase_data):
        json_path = os.path.join(repo_path, "data", "processed", "data.json")

        scrapped_data = scrape_sites(address)
        add_lat_lon_to_json(scrapped_data)
        upload_json_to_firebase(json_path, address)

        data = scrapped_data
    else:
        data = firebase_data

    return data


def data_in_firebase(data):
    return data is None


address = "Rua Monte Alegre, Perdizes, SP"
data = collect_data(address)
print(data)
