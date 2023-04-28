
from site_API.utils.site_api_handler import SiteApiInterface
from settings import SiteSettings

site = SiteSettings()

headers = {
	"X-RapidAPI-Key": site.api_key.get_secret_value(),
	"X-RapidAPI-Host": site.host_api
    }

url = "https://" + site.host_api

params = {"fragment":"true","json":"true"}

site_api = SiteApiInterface()

if __name__== "__main__":
    site_api()

