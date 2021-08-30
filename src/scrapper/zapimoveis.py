from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from src.utils.utils import *

driver = init_driver()
site = "https://www.zapimoveis.com.br/"
address = "R. Monte Alegre"

def rent_or_buy():
    rent = driver.find_element_by_xpath("""/html/body/main/section/section[1]/div/section/form/div/div[1]/div[1]/div/button[2]""")
    rent.click()

def send_address(address):
    type_in = driver.find_element_by_xpath("""//*[@id="app"]/section/section[1]/div/section/form/div/div[2]/div/div/div/input""")
    type_in.click()
    type_in.send_keys(address)
    try:
        WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="app"]/section/section[1]/div/section/form/div/div[2]/div/div/ul"""))
        )
        type_in.send_keys(Keys.RETURN)
    except:
        print("There's something wrong fam. Try again")

def click_search():
    search_btn = driver.find_element_by_xpath("""//*[@id="app"]/section/section[1]/div/section/form/div/div[2]/button""")
    search_btn.click()

def get_info():
    try:
        WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, """/html/body/main/section/div[2]/div[3]/section/div/div[1]/div[1]/div[2]"""))
        )
        for i in range(1,25):
            values = driver.find_element_by_xpath(f"/html/body/main/section/div[2]/div[3]/section/div/div[{i}]/div[1]/div[2]").text
            print(values)
    except:
        print("Where the hell is it fam?")
    #page_numbers = driver.find_elements_by_class_name("pagination__item pagination__page link link-primary link--regular")
    #page_one = driver.find_elements_by_class_name("pagination__item pagination__page link link-primary link--regular pagination__active js-active-page")

def get_more_info():
    more_info = driver.find_elements_by_class_name("feature__container simple-card__amenities")
    print(more_info)










driver.get(site)
rent_or_buy()
send_address(address)
click_search()
get_info()


#output_filename = build_output_filename(site, address)
#save_raw_data(output_json, output_filename)