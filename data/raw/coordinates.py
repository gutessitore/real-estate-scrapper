from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="myGeocoder")
lacation = locator.geocode("São Paulo, Jardim Guaianazes")
lacation.point

