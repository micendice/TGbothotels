
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

"""url = "https://hotels4.p.rapidapi.com/locations/v3/search"

querystring = {"q":"new york","locale":"en_US","langid":"1033","siteid":"300000001"}

headers = {
	"X-RapidAPI-Key": "6741070c10mshc69db9dd5f323c3p1a91c5jsnaddb2d72834a",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)"""