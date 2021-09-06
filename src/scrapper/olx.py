from urllib.parse import quote
from src.utils.utils import *


def announcement_parser(text: str) -> dict:
    bedroom_text_pattern = "(\d)(\sou mais)? quartos?"
    area_text_pattern = "(\d+)m²"
    parking_slot = "(\d+)(\sou mais)? vagas?"

    real_state_dict = {
        "quartos": get_regex_group_from_pattern(text, bedroom_text_pattern),
        "área": get_regex_group_from_pattern(text, area_text_pattern),
        "vagas": get_regex_group_from_pattern(text, parking_slot),
        "texto": text
    }

    return real_state_dict


address = "rua monte alegre, SP"
address_query = quote(address)

url_with_query = f"https://www.olx.com.br/imoveis?q={address_query}"

driver = init_driver()
driver.get(url_with_query)

announcement_info_class = "sc-1j5op1p-0"
announcement_elements = driver.find_elements_by_class_name(announcement_info_class)
parsed_announcement_text = [announcement_parser(an.text) for an in announcement_elements]

print(json.dumps(parsed_announcement_text, indent=4))


driver.quit()
