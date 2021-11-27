from real_estate.src.scrapper.zapimoveis import get_zapimoveis_data
from real_estate.src.scrapper.vivareal import get_vivareal_data
from real_estate.src.scrapper.trovit import get_trovit_data
from selenium.webdriver.chrome.options import Options
from real_estate.src.utils.utils import save_raw_data
import concurrent.futures
import re


def scrape_sites(driver_path: str, address: str, save_local_csv=False):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    scrappers = {
        # "olx": {
        #     "function": get_olx_data,
        #     "address": address,
        #     "option": chrome_options
        # },
        "trovit": {
            "function": get_trovit_data,
            "address": address,
            "option": chrome_options,
            "driver_path": driver_path
        },
        "zapimoveis": {
            "function": get_zapimoveis_data,
            "address": address,
            "option": chrome_options,
            "driver_path": driver_path
        },
        "vivareal": {
            "function": get_vivareal_data,
            "address": address,
            "option": chrome_options,
            "driver_path": driver_path
        }
    }

    number_of_elements = len(scrappers.keys())
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_elements) as executor:
        data = list(
            executor.map(
                collect_data_from_site,
                scrappers.items()
            )
        )

    flattened_data = [item for sublist in data for item in sublist if item is not None]

    # df = pd.DataFrame(flattened_data)
    # df.to_json("../data/processed/data.json", orient="index", indent=1)
    #
    # if save_local_csv:
    #     df.to_csv("../data/processed/data.csv", index_label=False)

    return flattened_data


def collect_data_from_site(site_info: (str, dict)):
    site = site_info[0]
    site_dict = site_info[1]
    address = site_dict.get("address")
    chrome_options = site_dict.get("option")
    scrapper_function = site_dict.get("function")
    driver_path = site_dict.get("driver_path")
    scrapper_data = scrapper_function(driver_path, address, chrome_options)
    filename = f"{site}-{address}.json"
    save_raw_data(scrapper_data, filename)
    return scrapper_data
