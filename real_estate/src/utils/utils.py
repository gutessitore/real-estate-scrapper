from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from urllib.parse import urlparse
import platform
import json
import os
import re


def get_current_os() -> str:
    return platform.system()


def get_repo_absolute_path() -> str:
    absolute_path = os.getcwd()
    repo_directory_name = "real-estate-scrapper"
    letters_to_repo_name = absolute_path.index(repo_directory_name) + len(repo_directory_name)
    repo_path = absolute_path[:letters_to_repo_name]
    return repo_path


def get_driver_path() -> str:
    current_os = get_current_os()
    if current_os == "Linux":
        driver_path_suffix = "real_estate/src/drivers/linux/chromedriver"
    elif current_os == "Windows":
        driver_path_suffix = "real_estate/src/drivers/windows/chromedriver"
    else:
        raise ValueError("Could not find proper chromedriver for the OS")

    absolute_repo_path = get_repo_absolute_path()
    return os.path.join(absolute_repo_path, driver_path_suffix)


def init_driver(driver_path, driver_options: Options = None) -> Chrome:
    return Chrome(executable_path=driver_path, options=driver_options)


def get_site_name(url: str) -> str:
    hostname = urlparse(url).hostname
    hostname = hostname.replace("www.", "")
    hostname = hostname.replace(".com", "")
    return hostname


def clean_address(address: str) -> str:
    address = address.replace(" ", "_")
    address = address.replace(".", "")
    address = address.replace(",", "")
    return address


def build_output_filename(url: str, address: str) -> str:
    return get_site_name(url) + "-" + clean_address(address)


def save_raw_data(data: list or dict, filename: str) -> None:
    if ".json" not in filename:
        filename += ".json"

    # raw_data_directory_path = os.path.join(get_repo_absolute_path(), "real_estate", "data", "raw")
    # filename_path = os.path.join(raw_data_directory_path, filename)
    save_data(data, filename)


def save_data(data: list or dict, filename_path: str):
    with open(filename_path, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_regex_group_from_pattern(text: str, pattern: str) -> str:
    value = 0
    if (match := re.search(pattern, text, re.MULTILINE)) is not None:
        value = match.group(1)
    try:
        value = int(value)
    except ValueError:
        value = int(value.replace(".", ""))
    return value
