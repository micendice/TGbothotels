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


"""
User info for States
1.Name
2.Age
3.Country
4.City
5.Phone number

"""
