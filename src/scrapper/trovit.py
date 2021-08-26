from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from src.utils.utils import *
import json
import re

MAX_DELAY = 10


def select_rent_option(driver: Chrome) -> None:

    rent_or_sale_selector_xpath = "/html/body/div[3]/div[1]/div[3]/form/div/a[2]"
    element_present = EC.element_to_be_clickable((By.XPATH, rent_or_sale_selector_xpath))
    WebDriverWait(driver, MAX_DELAY).until(element_present).click()

    rent_button_text = "Aluguel"
    element_present = EC.element_to_be_clickable((By.LINK_TEXT, rent_button_text))
    WebDriverWait(driver, MAX_DELAY).until(element_present)
    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text(rent_button_text))


def search_for_address(driver: Chrome, address: str) -> None:
    search_bar_id = "what_d"
    driver.find_element_by_id(search_bar_id).send_keys(address, Keys.ENTER)


def collect_real_state_raw_data(driver: Chrome) -> list:
    delay = 10
    card_class_name = "snippet-content-main"

    element_present = EC.presence_of_element_located((By.CLASS_NAME, card_class_name))
    WebDriverWait(driver, delay).until(element_present)

    return driver.find_elements_by_class_name(card_class_name)


def announcement_parser(text: str) -> dict:
    bathroom_text_pattern = "(\d) Ban."
    bedroom_text_pattern = "(\d) Cama/s"
    area_text_pattern = "(\d+) m²"
    price_text_pattern = "^R\$([\d{1,3}\.?]+)[,\d{2}]?"

    real_state_dict = {
        "price": get_regex_group_from_pattern(text, price_text_pattern),
        "bathrooms": get_regex_group_from_pattern(text, bathroom_text_pattern),
        "bedrooms": get_regex_group_from_pattern(text, bedroom_text_pattern),
        "size": get_regex_group_from_pattern(text, area_text_pattern),
        "full_text": text
    }

    return real_state_dict


def get_regex_group_from_pattern(text: str, pattern: str) -> str:
    value = 0
    if (match := re.search(pattern, text, re.MULTILINE)) is not None:
        value = match.group(1)
    try:
        value = int(value)
    except ValueError:
        value = int(value.replace(".", ""))
    return value


def collect_elements_data(elements: list) -> list:
    data = list()
    for element in elements:
        element_text = element.text
        element_data = announcement_parser(element_text)
        element_data["address"] = element.find_element_by_class_name("address").text
        data.append(element_data)
    return data


options = Options()
options.add_argument("--headless")
chrome = init_driver()

site = "https://imoveis.trovit.com.br/"
address_to_search = "R. Monte Alegre"
chrome.get(site)

select_rent_option(chrome)
search_for_address(chrome, address_to_search)
real_state_elements = collect_real_state_raw_data(chrome)
real_state_parsed_data = collect_elements_data(real_state_elements)
print(json.dumps(real_state_parsed_data, indent=4))

chrome.quit()

