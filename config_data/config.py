import os
from dotenv import load_dotenv, find_dotenv

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
    ("survey", "Опрос")
)
CUSTOM_COMMANDS = (
    ("highprice", "Вывод самых высоких значений"),
    ("lowprice", "Вывод самых низких значений"),
    ("custom", "Вывод диапазона значений"),
    ("history", "Вывод последних десяти запросов")
                   )

CITY_TEMPLATE = r'[a-z,A-Z,\s,-]'   # city name check
MAX_PHOTO_DISPLAYED: int = 5     # max number of displayed photo
MAX_HOTEL_DISPLAYED: int = 5     # max number of displayed hotels
SEARCH_INTERVAL: int = 180          # max days search depth
MAX_STAY: int = 60              # max stay duration

payload = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": { "regionId": "6054439" },
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
    "rooms": [
        {
            "adults": 2,
            "children": [{"age": 13}, {"age": 0}]
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 200,
    "sort": "PRICE_LOW_TO_HIGH",
    "filters": { "price": {
        "max": 150,
        "min": 100
    }}
}


"""
User info for States
1.Name
2.Age
3.Country
4.City
5.Phone number

"""
