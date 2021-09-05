import selenium
from src.utils.utils import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = init_driver()
site = "https://www.vivareal.com.br/"
address = "R. Monte Alegre"
driver.get(site)


def accept_cookies():
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="cookie-notifier-cta"]"""))
        )
    except:
        pass
    else:
        element.click()


def select_search_type(renting=True):
    search_type = driver.find_element_by_xpath(
        """//*[@id="js-site-main"]/section[1]/div/div/form[1]/div[1]/div/div/div[1]/select""")
    search_type.click()
    if renting:
        driver.find_element_by_xpath("""//select[@class="js-select-business"]/option[@value="rent"]""").click()
    else:
        driver.find_element_by_xpath("""//select[@class="js-select-business"]/option[@value="sale"]""").click()


def wait_for_addresses():
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, """//*[@id="js-site-main"]/section[1]/div/div/form[1]/div[2]/div/div/div/div/div/*[1]"""))
        )
    except selenium.common.exceptions.NoSuchElementException as e:
        print(e)

def send_address(address: str):
    address_label = driver.find_element_by_xpath("""//*[@id="filter-location-search-input"]""")
    address_label.clear()
    address_label.send_keys(address)
    wait_for_addresses()
    address_label.send_keys(Keys.RETURN)


accept_cookies()
select_search_type()
send_address(address)
# driver.close()

# output_json = [
#   {"valor": 123, "endereço": "abc", "vagas": 123, "valor_de_condominio": 123, "tamanho": 123, "quartos": 123, "banheiros": 123},
#   {"valor": 123, "endereço": "abc", "vagas": 123, "valor_de_condominio": 123, "tamanho": 123, "quartos": 123, "banheiros": 123}
# ]
#
# output_filename = build_output_filename(site, address)
# save_raw_data(output_json, output_filename)
