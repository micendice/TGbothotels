import os
from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("RAPID_API_KEY", None)
    host_api: StrictStr = os.getenv("HOST_API", None)

