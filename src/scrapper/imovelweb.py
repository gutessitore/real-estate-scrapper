from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from src.utils.utils import *


driver = init_driver()
site = "https://www.google.com/"
address = "R. Monte Alegre"
driver.get(site)

