from src.database.firebase_manager import get_firebase_data, upload_json_to_firebase, connect_to_firebase
from src.postprocess.coordinates import add_lat_lon_to_json
from src.collector import scrape_sites


def collect_data(address: str):
    connect_to_firebase()
    firebase_data = get_firebase_data(address)

    if data_in_firebase(firebase_data):
        # json_path = os.path.join(repo_path, "data", "processed", "data.json")

        scrapped_data = scrape_sites(address)
        data_with_lat_lon = add_lat_lon_to_json(scrapped_data, address)
        upload_json_to_firebase(data_with_lat_lon, address)

        data = data_with_lat_lon
    else:
        data = firebase_data

    return data


def data_in_firebase(data):
    return data is None


if __name__ == "__main__":
    import json
    address = "Rua Monte Alegre"
    data = collect_data(address)
    print(json.dumps(data, indent=4))
