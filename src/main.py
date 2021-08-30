from selenium.webdriver.chrome.options import Options
from src.scrapper.trovit import get_trovit_data
from utils.utils import save_raw_data

address = "avenida santo amaro"

chrome_options = Options()
chrome_options.add_argument("--headless")

trovit_data = get_trovit_data(address, chrome_options)

save_raw_data(trovit_data, "trovit-santo_amaro.json")