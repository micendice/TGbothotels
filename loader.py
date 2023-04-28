from aiogram import Bot, Dispatcher, executor, types
from pydantic import SecretStr
import os
from dotenv import load_dotenv
load_dotenv()
tgbot_tkn: SecretStr = os.getenv("BOT_TOKEN", None)
bot = Bot(token=tgbot_tkn)
dp = Dispatcher(bot)

