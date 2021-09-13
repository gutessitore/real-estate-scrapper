from geopy.geocoders import Nominatim
from tqdm import tqdm
from math import sqrt
import pandas as pd
import json

json_file = open("/home/gustavo/PycharmProjects/real-estate-scrapper/data/processed/data.json", )
data = json.load(json_file)


def add_lat_lon_to_json(data: dict, address: str):
    locator = Nominatim(user_agent="myGeocoder")
    original_location = locator.geocode(address)
    original_location_lat = original_location.latitude
    original_location_lon = original_location.longitude

    for real_estate_id in tqdm(data):
        real_estate = real_estate_id

        real_estate_address = ", ".join(real_estate.get("endereço").split(",")[:-1])
        real_estate_location = locator.geocode(real_estate_address)

        real_estate_lat, real_estate_lon = None, None
        distance = None
        if real_estate_location is not None:
            real_estate_lat = real_estate_location.latitude
            real_estate_lon = real_estate_location.longitude

            distance = calculate_abs_distance(
                original_location_lat, real_estate_lat,
                original_location_lon, real_estate_lon
            )

        real_estate["lat"] = real_estate_lat
        real_estate["lon"] = real_estate_lon
        real_estate["distance"] = distance

    df = pd.DataFrame(data)
    df.to_json("../data/processed/data.json", indent=1, orient="index")
    return data


def calculate_abs_distance(x1, y1, x2, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)
