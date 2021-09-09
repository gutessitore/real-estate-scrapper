from database.firebase_manager import get_firebase_data
from database.firebase_manager import upload_json
from utils.utils import get_repo_absolute_path
from collector import scrape_sites
import os

address = "avenida santo amaro"
repo_path = get_repo_absolute_path()
api_key = os.path.join(repo_path, "src", "database", "real-estate-scrapper-firebase.json")
database_url = "https://real-estate-scrapper-2ac0c-default-rtdb.firebaseio.com/"


firebase_data = get_firebase_data(api_key, database_url, address)

if firebase_data is None:
    print("data not found on database")
    scrape_sites(address)

    json_path = os.path.join(repo_path, "data", "processed", "data.json")
    print("uploading to database")
    upload_json(api_key, database_url, json_path, address)
    print("uploaded to database")
else:
    print(firebase_data)


