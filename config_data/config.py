import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("echo", "Реакция на непонятное"),
)
CUSTOM_COMMANDS = (
    ("highprice", "Поиск самых дорогих отелей"),
    ("lowprice", "Поиск самых дешевых отелей"),
    ("custom", "Поиск отелей по критерию"),
    ("history", "Вывод последних десяти запросов")
                   )

CITY_TEMPLATE = r'[a-z,A-Z,\s,-]'   # city name check
MAX_PHOTO_DISPLAYED: int = 5     # max number of displayed photo
MAX_HOTEL_DISPLAYED: int = 5     # max number of displayed hotels
SEARCH_INTERVAL: int = 90          # max days search depth
MAX_STAY: int = 30              # max stay duration
MAX_KID_AGE = 17

load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("RAPID_API_KEY", None)
    host_api: StrictStr = os.getenv("HOST_API", None)


rooms_payload = [{"adults": 2, "children": [{"age": 13}]}]
payload_hotels_list = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {"regionId": "2621"},
    "checkInDate": {
        "day": 10,
        "month": 10,
        "year": 2022
    },
    "checkOutDate": {
        "day": 15,
        "month": 10,
        "year": 2022
    },
    "rooms": rooms_payload,
    "resultsStartingIndex": 0,
    "resultsSize": 50,
    "sort": "PRICE_LOW_TO_HIGH",
    "filters": {"price": {
        "max": 150000,
        "min": 10
    }}
}
payload_hotel_details = {"currency": "USD", "eapid": 7, "locale": "en_US", "siteId": 300000001, "propertyId": "9209612"}
payload_summary = {"currency": "USD", "eapid": 1, "locale": "en_US", "siteId": 300000001, "propertyId": "9209612"}
payload_get_offer = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "propertyId": "9209612",
    "checkInDate": {
        "day": 6,
        "month": 10,
        "year": 2023
    },
    "checkOutDate": {
        "day": 9,
        "month": 10,
        "year": 2023
    },
    "destination": {
        "regionId": "6054439"
    },
    "rooms": rooms_payload
}


url_loc_search = "locations/v3/search"
url_hotels_list = "properties/v2/list"
url_hotel_details = "properties/v2/detail"
url_hotel_summary = "properties/v2/get-summary"
url_get_offer = "properties/v2/get-offers"

command_set = {
    "highprice": {
        "sort_command": "PRICE_HIGH_TO_LOW",
        "filters_command": {"price": {"max": 150000, "min": 10}},
        "russ_word": "самые дорогие отели"
    },
    "lowprice": {
        "sort_command": "PRICE_LOW_TO_HIGH",
        "filters_command": {"price": {"max": 500, "min": 5}},
        "russ_word": "самые дешевые отели"
    },
    "custom": {
        "sort_command": "PRICE_LOW_TO_HIGH",
        "filters_command": {"price": {"max": 150000, "min": 5}},
        "russ_word": "отели по критерию"
    }
}

sort_params = {
        "sort_price_rel": "PRICE_RELEVANT",
        "sort_guest_rating": "REVIEW",
        "sort_distance_from_dt": "DISTANCE",
        "sort_stars": "PROPERTY_CLASS",
        "sort_recommended": "RECOMMENDED",
        "sort_high": "PRICE_HIGH_TO_LOW",
        "sort_low": "PRICE_LOW_TO_HIGH"
}
