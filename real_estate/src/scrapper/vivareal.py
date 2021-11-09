from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from real_estate.src.utils.utils import init_driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import re


MAX_DELAY = 10
# driver = init_driver()
SITE = "https://www.vivareal.com.br/"
address = "R. Monte Alegre"
# driver.get(site)


def accept_cookies(driver: Chrome):
    try:
        element = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, """//*[@id="cookie-notifier-cta"]"""))
        )
    except:
        pass
    else:
        element.click()


def select_rent_option(driver: Chrome, renting=True):
    search_type = driver.find_element_by_xpath(
        """//*[@id="js-site-main"]/section[1]/div/div/form[1]/div[1]/div/div/div[1]/select""")
    search_type.click()
    if renting:
        driver.find_element_by_xpath("""//select[@class="js-select-business"]/option[@value="rent"]""").click()
    else:
        driver.find_element_by_xpath("""//select[@class="js-select-business"]/option[@value="sale"]""").click()


def wait_for_addresses(driver: Chrome, address_label):
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located(
                (By.XPATH, """//*[@id="js-site-main"]/section[1]/div/div/form[1]/div[2]/div/div/div/div/div/*[1]"""))
        )
    except NoSuchElementException:
        raise ReferenceError("Could found any real address with this address")
    else:
        address_label.send_keys(Keys.RETURN)


def send_address(driver: Chrome, address: str):
    address_label = driver.find_element_by_xpath("""//*[@id="filter-location-search-input"]""")
    address_label.clear()
    address_label.send_keys(address)
    wait_for_addresses(driver, address_label)


def collect_real_state_raw_data(driver: Chrome) -> list:
    """
    Find each announcement element inside the page by it's xpath
    :param driver: Selenium driver
    :return: list of WebDriverElements
    """
    cards_xpath = "//*[@data-type='property']"
    element_present = ec.presence_of_element_located((By.XPATH, cards_xpath))
    WebDriverWait(driver, MAX_DELAY).until(element_present)

    return driver.find_elements_by_xpath(cards_xpath)


def collect_elements_data(elements: list, driver) -> list:
    data = list()

    for element in elements:
        driver.execute_script("arguments[0].scrollIntoView()", element)  # Scroll to element
        id = element.get_attribute("id")
        element_data = dict()
        raw_renting = element.find_element_by_xpath(""".//section[@class="property-card__values  "]/div/p""").text
        element_data["preço"] = int("".join(re.findall(r"\d+", raw_renting)))
        try:
            raw_condo_fee = element.find_element_by_xpath(""".//section[@class="property-card__values  "]/footer""").text
        except NoSuchElementException:
            element_data["valor_de_condominio"] = 0
        else:
            element_data["valor_de_condominio"] = int("".join(re.findall(r"\d+", raw_condo_fee)))
        element_data["área"] = int(element.find_element_by_xpath(""".//li[@class="property-card__detail-item property-card__detail-area"]/span[1]""").text)
        try:
            element_data["vagas"] = int(element.find_element_by_xpath(""".//li[@class="property-card__detail-item property-card__detail-garage js-property-detail-garages"]/span[1]""").text)
        except ValueError:
            element_data["vagas"] = 0
        element_data["quartos"] = int(element.find_element_by_xpath(""".//li[@class="property-card__detail-item property-card__detail-room js-property-detail-rooms"]/span[1]""").text)
        element_data["banheiros"] = int(element.find_element_by_xpath(""".//li[@class="property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom"]/span[1]""").text)
        element_data["endereço"] = element.find_element_by_xpath(""".//*[@class="property-card__address"]""").text
        element_data["texto"] = element.find_element_by_xpath(""".//*[@class="property-card__header"]""").text
        element_data["link"] = f"https://www.vivareal.com.br/imovel/{id}"
        element_data["img1"] = element.find_element_by_class_name("carousel__image").get_attribute("src")
        element_data["site"] = "vivareal"

        data.append(element_data)
    return data


def get_vivareal_data(address: str, driver_options: Options = None) -> list:
    """
    Scrapes vivareal site and build a array of maps in the following format:

    [
        {
            "preço": int,
            "valor_de_condominio": int,
            "banheiros": int,
            "quartos": int,
            "área": int,
            "vagas": int,
            "endereço": str
            "texto": str
        },
        ...
    ]


    :param address: Address to search for
    :param driver_options: driver options
    :return: json like string
    """
    # Initialize browser
    chrome = init_driver(driver_options)
    chrome.get(SITE)

    # Collect  data
    try:
        accept_cookies(chrome)
        select_rent_option(chrome)
        send_address(chrome, address)
        real_state_elements = collect_real_state_raw_data(chrome)
        real_state_parsed_data = collect_elements_data(real_state_elements, chrome)

    except Exception as e:
        print(e)
        real_state_parsed_data = None

    finally:
        chrome.close()

    return real_state_parsed_data

if __name__ == "__main__":
    import time
    start_time = time.time()
    data = get_vivareal_data("Perdizes, SP")
    print(f"Running time: {(time.time()-start_time):.2f} seconds.")
    print(json.dumps(data, indent=4))
