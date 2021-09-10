from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from src.utils.utils import *
import warnings


SITE = "https://www.zapimoveis.com.br/"


def rent_or_buy(driver, rent=True):
    if rent:
        rent_button = driver.find_element_by_xpath(
            """/html/body/main/section/section[1]/div/section/form/div/div[1]/div[1]/div/button[2]""")
        rent_button.click()


def send_address(driver, address):
    type_in = driver.find_element_by_xpath(
        """//*[@id="app"]/section/section[1]/div/section/form/div/div[2]/div/div/div/input""")
    type_in.click()
    type_in.send_keys(address)
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, """//*[@id="app"]/section/section[1]/div/section/form/div/div[2]/div/div/ul"""))
        )
        type_in.send_keys(Keys.RETURN)
    except:
        print("There's something wrong fam. Try again")


def click_search(driver):
    search_btn = driver.find_element_by_xpath(
        """//*[@id="app"]/section/section[1]/div/section/form/div/div[2]/button""")
    search_btn.click()


def get_elements(driver):
    elements = None
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, """/html/body/main/section/div[2]/div[3]/section/div/div[1]/div[1]/div[2]"""))
        )

        elements = driver.find_elements_by_class_name("simple-card__box")

    except:
        warnings.warn("Where the hell is it fam?")
    # page_numbers = driver.find_elements_by_class_name("pagination__item pagination__page link link-primary
    # link--regular") page_one = driver.find_elements_by_class_name("pagination__item pagination__page link
    # link-primary link--regular pagination__active js-active-page")

    return elements


def announcement_parser(method, arg, pattern=None):
    try:
        announcement_text = method(arg).text
        if pattern is not None:
            announcement_text = get_regex_group_from_pattern(announcement_text, pattern)
    except NoSuchElementException:
        announcement_text = 0

    return announcement_text


def get_announcement_data(elements: list) -> list:
    data = list()
    price_text_pattern = "^R\$\s([\d{1,3}\.?]+)"
    area_text_pattern = "(\d+) m²"
    number_pattern = "(\d+)"
    for element in elements:
        card_info = {
            "preço": announcement_parser(element.find_element_by_tag_name, "strong", price_text_pattern),
            "vagas": announcement_parser(element.find_element_by_class_name, "js-parking-spaces", number_pattern),
            "banheiros": announcement_parser(element.find_element_by_class_name, "js-bathrooms", number_pattern),
            "quartos": announcement_parser(element.find_element_by_class_name, "js-bedrooms", number_pattern),
            "área": announcement_parser(element.find_element_by_class_name, "js-areas", area_text_pattern),
            "texto": element.text,
            "site": "zapimoveis"
        }

        data.append(card_info)
    return data


def get_zapimoveis_data(address: str, driver_options: Options = None) -> list:

    chrome = init_driver(driver_options)
    # Set window size to collect all dynamic data
    chrome.set_window_size(2000, 1000)
    chrome.get(SITE)
    try:
        rent_or_buy(chrome)
        send_address(chrome, address)
        click_search(chrome)
        real_state_elements = get_elements(chrome)
        real_state_parsed_data = get_announcement_data(real_state_elements)
    except Exception as e:
        warnings.warn(e)
        real_state_parsed_data = None

    finally:
        chrome.quit()

    return real_state_parsed_data
