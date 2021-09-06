from selenium.webdriver.chrome.options import Options
from src.scrapper.zapimoveis import get_zapimoveis_data
from src.scrapper.vivareal import get_vivareal_data
from src.scrapper.trovit import get_trovit_data
from src.scrapper.olx import get_olx_data
from utils.utils import save_raw_data

address = "rua monte alegre"

chrome_options = Options()
chrome_options.add_argument("--headless")

scrappers = {
    "olx": {
        "function": get_olx_data,
    },
    "trovit": {
        "function": get_trovit_data
    },
    "zapimoveis": {
        "function": get_zapimoveis_data
    },
    "vivareal": {
        "function": get_vivareal_data
    }
}

for scrapper in scrappers.keys():
    print("_"*30)
    print(f"collecting data from {scrapper}")

    scrapper_function = scrappers[scrapper]["function"]
    scrapper_data = scrapper_function(address, chrome_options)

    filename = f"{scrapper}-{address}.json"
    print(f"saving data to {filename}")

    save_raw_data(scrapper_data, filename)
