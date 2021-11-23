from pycep_correios import get_address_from_cep, WebService, exceptions
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from tqdm import tqdm
from math import sqrt
import pandas as pd
import geopy.distance
import time
import json
import re





# json_file = open("/home/gustavo/PycharmProjects/real-estate-scrapper/data/processed/data.json", )
# data = json.load(json_file)


def add_lat_lon_to_json(data: list, address: str):
    """
    Given a list of announcements, navigate
    through each announcement aggregating the
    coordinates of its address and its distance
    from the main address .

    :param data: list of dicts, each dict is an announcement
    :param address: the searched address
    :return: the enhanced list of dicts
    """
    locator = Nominatim(user_agent="myGeocoder")
    original_location = locator.geocode(address, country_codes="br")
    original_location_lat = original_location.latitude
    original_location_lon = original_location.longitude
    box_radius = 0.03
    viewbox = ((original_location_lat + box_radius, original_location_lon + box_radius),
               (original_location_lat - box_radius, original_location_lon - box_radius))

    for real_estate in tqdm(data):
        time.sleep(0.75)
        real_estate_address = clean_address(real_estate.get("endereço"))

        real_estate_address = search_by_zipcode(real_estate_address)

        real_estate_location = locator.geocode(real_estate_address, country_codes="br", viewbox=viewbox)

        if real_estate_location is None:
            real_estate_address = improve_address(real_estate_address)
            real_estate_location = locator.geocode(real_estate_address, country_codes="br", viewbox=viewbox)

        real_estate_lat, real_estate_lon = None, None
        distance = None
        if real_estate_location is not None:
            real_estate_lat = real_estate_location.latitude
            real_estate_lon = real_estate_location.longitude

            distance = geopy.distance.distance(
                (original_location_lat, original_location_lon),
                (real_estate_lat, real_estate_lon)
            ).km

        real_estate["lat"] = real_estate_lat
        real_estate["lon"] = real_estate_lon
        real_estate["distância"] = distance

    # df = pd.DataFrame(data)
    # df.to_json("../data/processed/data.json", indent=1, orient="index")
    return data


def clean_address(address):
    split_address = address.split(",")
    clean = [part.replace("Estado de", "") for part in split_address]
    return ",".join(clean)


def calculate_abs_distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def search_by_zipcode(address):
    # If there is a zip code
    zip_pattern = r"\d{5}-?\d{3}"
    zip_code = re.search(zip_pattern, address)
    if zip_code:
        zip_code_string = zip_code.group(0)
        try:
            address = get_address_from_cep(zip_code_string, webservice=WebService.VIACEP)
        except exceptions.CEPNotFound:
            pass
        else:
            if address['bairro']:
                return create_parsed_dict(address)
            else:
                return address
    return address


def create_parsed_dict(address_dict: dict):
    uf_to_state = {"AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia", "CE": "Ceará",
                   "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás", "MA": "Maranhão",
                   "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba",
                   "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro",
                   "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima",
                   "SC": "Santa Catarina", "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins", }
    new_dict = dict()
    new_dict['street'] = address_dict['logradouro']
    new_dict['city'] = address_dict['cidade']
    new_dict['state'] = uf_to_state[address_dict['uf']]
    new_dict['postalcode'] = address_dict['cep']
    return new_dict


def improve_address(address):
    """
    Apply some methods to make the address
    clearer to the locator.
    :param address: a string
    :return: str with improved address
    """
    if isinstance(address, dict):
        return f"{address['street']}, {address['city']}"
    parsed_address = re.split(r" - |, ", address)
    for i in parsed_address:
        if not re.search(r"\d+", i):
            street = i
            break
    else:
        return None
    states = ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal", "Espírito Santo", "Goiás",
              "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná",
              "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia",
              "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"]
    for e in states:
        if e in address:
            return f"{street}, {e}"
    else:
        return None
