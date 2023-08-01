
from site_API.utils.site_api_handler import SiteApiInterface
from ..config_data.config import SiteSettings


site = SiteSettings()

site_api = SiteApiInterface()

if __name__ == "__main__":
    site_api()
