from geopy.geocoders import Nominatim
from tqdm import tqdm
import pandas as pd
import json

json_file = open("/home/gustavo/PycharmProjects/real-estate-scrapper/data/processed/data.json", )
data = json.load(json_file)


def add_lat_lon_to_json(data: dict):

    locator = Nominatim(user_agent="myGeocoder")
    for real_estate_id in tqdm(data):
        real_estate = data.get(real_estate_id)

        real_estate_address = real_estate.get("endereço")
        real_estate_location = locator.geocode(real_estate_address)

        real_estate_lat, real_estate_lon = None, None
        if real_estate_location is not None:
            real_estate_lat = real_estate_location.latitude
            real_estate_lon = real_estate_location.longitude

        real_estate["lat"] = real_estate_lat
        real_estate["lon"] = real_estate_lon

    df = pd.DataFrame(data)
    df.to_json("../data/processed/data.json", indent=1)

