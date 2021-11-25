from real_estate.src.database.firebase_manager import get_firebase_data, upload_json_to_firebase, connect_to_firebase
from real_estate.src.postprocess.coordinates import add_lat_lon_to_json
from real_estate.src.collector import scrape_sites
import pandas as pd


class Collector:

    def __init__(self, address: str):
        self._address = address
        self._data = None

    def collect_data(self) -> None:
        connect_to_firebase()
        firebase_data = get_firebase_data(self._address)

        if not self._data_in_firebase(firebase_data):
            # json_path = os.path.join(repo_path, "data", "processed", "data.json")

            scrapped_data = scrape_sites(self._address)
            data_with_lat_lon = add_lat_lon_to_json(scrapped_data, self._address)
            upload_json_to_firebase(data_with_lat_lon, self._address)

            self._data = data_with_lat_lon
        else:
            self._data = firebase_data

    @staticmethod
    def _data_in_firebase(data):
        return data is not None

    @property
    def address(self):
        return self._address

    @property
    def data(self) -> pd.DataFrame:
        return pd.DataFrame(self._data)
