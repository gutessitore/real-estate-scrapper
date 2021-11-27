from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib.parse import quote
import concurrent.futures
import selenium
import warnings
import json

MAX_DELAY = 5


def announcement_parser(text: str) -> dict:
    bedroom_text_pattern = r"(\d)(\sou mais)? quartos?"
    area_text_pattern = r"(\d+)m²"
    parking_slot = r"(\d+)(\sou mais)? vagas?"
    price_text_pattern = r"R\$\s?([\d{1,3}\.?]+)"

    real_state_dict = {
        "quartos": get_regex_group_from_pattern(text, bedroom_text_pattern),
        "área": get_regex_group_from_pattern(text, area_text_pattern),
        "vagas": get_regex_group_from_pattern(text, parking_slot),
        "preço": get_regex_group_from_pattern(text, price_text_pattern)
    }

    return real_state_dict


def build_url_with_address(address: str, rent_only=True, apartment_only=True) -> str:
    url_safe_address = quote(address)
    base_url = "https://sp.olx.com.br/imoveis"

    if rent_only:
        base_url += "/aluguel"

    if apartment_only:
        base_url += "/apartamentos"

    return base_url + "q=" + url_safe_address


def get_announcement_elements(driver: Chrome) -> list:
    announcement_card_class = "sc-1fcmfeb-2"

    element_present = EC.presence_of_element_located((By.CLASS_NAME, announcement_card_class))
    WebDriverWait(driver, MAX_DELAY).until(element_present)

    return driver.find_elements_by_class_name(announcement_card_class)


def collect_element_data_by_class_name(element, class_name):
    try:
        return element.find_element_by_class_name(class_name).text
    except selenium.common.exceptions.NoSuchElementException:
        return "0"


def get_link(element):
    try:
        link = element.find_element_by_tag_name("a").get_attribute("href")
    except:
        link = None
    return link


def get_element_data(element):
    announcement_info_class = "sc-1j5op1p-0"
    announcement_address_class = "sc-7l84qu-1"
    announcement_price_class = "aoie8y-0"

    announcement_info = collect_element_data_by_class_name(element, announcement_info_class)
    announcement_address = collect_element_data_by_class_name(element, announcement_address_class)
    announcement_price = collect_element_data_by_class_name(element, announcement_price_class)

    announcement_data = announcement_parser(announcement_info + " " + announcement_price)
    announcement_data["endereço"] = re.sub(r" - DDD \d+", "", announcement_address)
    announcement_data["texto"] = element.text
    announcement_data["link"] = get_link(element)
    announcement_data["site"] = "olx"

    if announcement_data["link"] is None:
        return None
    return announcement_data


def get_announcement_data(elements: list) -> list:
    number_of_elements = len(elements)
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_elements) as executor:
        announcements_data = list(executor.map(get_element_data, elements))

    return announcements_data


def get_olx_data(driver_path: str, address: str, driver_options: Options = None) -> list:

    chrome = init_driver(driver_path, driver_options)
    chrome.set_window_size(2000, 1000)

    url_with_query = build_url_with_address(address)
    chrome.get(url_with_query)
    try:
        real_state_elements = get_announcement_elements(chrome)
        real_state_parsed_data = get_announcement_data(real_state_elements)
    except Exception as e:
        warnings.warn(e)
        real_state_parsed_data = None

    finally:
        chrome.quit()

    return real_state_parsed_data


if __name__ == "__main__":
    data = get_olx_data("Rua Monte Alegre, Perdizes, SP")
    print(json.dumps(data, indent=4))
