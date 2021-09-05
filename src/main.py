from selenium.webdriver.chrome.options import Options
from src.scrapper.trovit import get_trovit_data
from src.scrapper.olx import get_olx_data
from utils.utils import save_raw_data

address = "rua monte alegre"

chrome_options = Options()
# chrome_options.add_argument("--headless")

trovit_data = get_trovit_data(address, chrome_options)
olx_data = get_olx_data(address, chrome_options)

save_raw_data(trovit_data, "trovit-santo_amaro.json")
save_raw_data(olx_data, "olx-santo_amaro.json")
