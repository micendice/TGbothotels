
from site_API.utils.site_api_handler import SiteApiInterface
from ..config_data.config import SiteSettings

site = SiteSettings()

headers = {
	"X-RapidAPI-Key": site.api_key.get_secret_value(),
	"X-RapidAPI-Host": site.host_api
    }

base_url = "https://" + site.host_api


site_api = SiteApiInterface()

if __name__== "__main__":
    site_api()
