import requests
from typing import Dict
import urllib.parse
from ..settings import SiteSettings, payload, url_loc_search
import json
site = SiteSettings()

st_headers = {
	"X-RapidAPI-Key": site.api_key.get_secret_value(),
	"X-RapidAPI-Host": site.host_api
    }

base_url = "https://" + site.host_api

def _make_response(method: str, url: str, headers: Dict, params: Dict, timeout: int):
    if method == 'get':
        print(f'method: {method}\nurl: {url}\nheaders: {headers}\n params- (querystring): {params}\ntimeout: {timeout}')
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=timeout
        )
    elif method == "post":
        response = requests.request(
            method,
            url,
            json=headers,
            params=params,
            timeout=timeout
        )

    status_code = response.status_code

    if 200 <= status_code <= 399:
        return response.text
    return status_code


def _find_location(location: str, base: str = base_url, headers: Dict = st_headers, timeout: int = 1000, func=_make_response):
    print('Function _find_location called')
    url = urllib.parse.urljoin(base, url_loc_search , True)

    querystring = {"q": location, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    print(f'url: {str(url)}\nquerystring: {querystring}\n')
    response = func("get", url, headers, querystring, timeout)
    response_dict = json.loads(response)
    """print(response)"""
    print(response_dict['rc'], response_dict['rid'])

    if response_dict['rc'] == 'OK':
        result = response_dict['rid']
    else:
        result = None

    return result

"""url = "https://hotels4.p.rapidapi.com/locations/v3/search"

querystring = {"q":"new york","locale":"en_US","langid":"1033","siteid":"300000001"}

headers = {
	"X-RapidAPI-Key": "6741070c10mshc69db9dd5f323c3p1a91c5jsnaddb2d72834a",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)"""
def _hotels_list(params: Dict, base: str, headers: Dict, timeout: int, func=_make_response):
    url = urllib.parse.urljoin(base, "properties/v2/list", True)
    headers["content-type"] = "application/json"
    payload = " "

    response = func("post", url, headers, payload, timeout)

"""url = "https://hotels4.p.rapidapi.com/properties/v2/list"

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
			"children": [{ "age": 5 }, { "age": 7 }]
		}
	],
	"resultsStartingIndex": 0,
	"resultsSize": 200,
	"sort": "PRICE_LOW_TO_HIGH",
	"filters": { "price": {
			"max": 150,
			"min": 100
		} }
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "6741070c10mshc69db9dd5f323c3p1a91c5jsnaddb2d72834a",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)
"""


class SiteApiInterface:

    @staticmethod
    def find_location(location):
        return _find_location(location)

    @staticmethod
    def get_math_fact():
        return _hotels_list


site_api = SiteApiInterface()


if __name__ == "__main__":
    _make_response()
    _find_location()
    _hotels_list()
    SiteApiInterface()
