from real_estate.src.utils.utils import get_regex_group_from_pattern, init_driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import warnings
import json


MAX_DELAY = 10
SITE = "https://imoveis.trovit.com.br/"


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
    """
    Find each announcement element inside the page by it's class name
    :param driver: Selenium driver
    :return: list of WebDriverElements
    """
    card_xpath = "snippet js-item"

    element_present = EC.presence_of_element_located((By.XPATH, f"//*[@class='{card_xpath}']"))
    WebDriverWait(driver, MAX_DELAY).until(element_present)

    return driver.find_elements_by_xpath(f"//*[@class='{card_xpath}']")


def announcement_parser(text: str) -> dict:
    bathroom_text_pattern = r"(\d) Ban."
    bedroom_text_pattern = r"(\d) Cama/s"
    area_text_pattern = r"(\d+) m²"
    price_text_pattern = r"^R\$([\d{1,3}\.?]+)[,\d{2}]?"

    real_state_dict = {
        "preço": get_regex_group_from_pattern(text, price_text_pattern),
        "banheiros": get_regex_group_from_pattern(text, bathroom_text_pattern),
        "quartos": get_regex_group_from_pattern(text, bedroom_text_pattern),
        "área": get_regex_group_from_pattern(text, area_text_pattern),
        "texto": text

    }

    return real_state_dict


def collect_elements_data(elements: list) -> list:
    data = list()
    for element in elements:
        element_text = element.find_element_by_xpath(".//*[@class='snippet-content-main']").text
        element_data = announcement_parser(element_text)
        element_data["endereço"] = element.find_element_by_class_name("address").text
        element_data["site"] = "trovit"
        element_data["link"] = element.find_element_by_xpath(".//*[@class='snippet-content-main']/..").get_attribute("href")
        element_data['img1'] = element.find_element_by_xpath(".//img").get_attribute("src")
        data.append(element_data)
    return data


def get_trovit_data(address: str, driver_options: Options = None) -> list:
    """
    Scrapes trovit site and build a array of maps in the following format:

    [
        {
            "preço": int,
            "banheiros": int,
            "quartos": int,
            "área": int,
            "texto": str
            "endereço": str
            "site": str
        },
        ...
    ]


    :param address: Address to search for
    :param driver_options: driver options
    :return: json like list
    """
    # Initialize browser
    chrome = init_driver(driver_options)
    chrome.get(SITE)

    # Collect  data
    try:
        select_rent_option(chrome)
        search_for_address(chrome, address)
        real_state_elements = collect_real_state_raw_data(chrome)
        real_state_parsed_data = collect_elements_data(real_state_elements)

    except Exception as e:
        warnings.warn(e)
        real_state_parsed_data = None

    finally:
        chrome.quit()

    return real_state_parsed_data


if __name__ == "__main__":
    import time
    start_time = time.time()
    data = get_trovit_data("Perdizes, SP")
    print(f"Running time: {(time.time()-start_time):.2f} seconds.")
    print(json.dumps(data, indent=4))
