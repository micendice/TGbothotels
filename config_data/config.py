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

