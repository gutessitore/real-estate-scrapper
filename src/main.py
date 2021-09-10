from database.firebase_manager import get_firebase_data
from database.firebase_manager import upload_json
from utils.utils import get_repo_absolute_path
from collector import scrape_sites
import time
import os

address = "Rua Monte Alegre, Perdizes, SP"
repo_path = get_repo_absolute_path()
api_key = os.path.join(repo_path, "src", "database", "real-estate-scrapper-firebase.json")
database_url = "https://real-estate-scrapper-2ac0c-default-rtdb.firebaseio.com/"


firebase_data = get_firebase_data(api_key, database_url, address)

start_time = time.time()
if firebase_data is None:
    scrape_sites(address)
    json_path = os.path.join(repo_path, "data", "processed", "data.json")
    upload_json(api_key, database_url, json_path, address)

else:
    print(firebase_data)

total_time = time.time() - start_time
print(f"Execution time: {total_time:.3f} secs")

