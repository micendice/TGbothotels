import os
from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("RAPID_API_KEY", None)
    host_api: StrictStr = os.getenv("HOST_API", None)


rooms_payload = [{"adults": 2, "children": [{"age": 13}, {"age": 5}]}]
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

