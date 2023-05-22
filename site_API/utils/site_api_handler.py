import requests
from typing import Dict
import urllib.parse


def _make_response(method: str, url: str, headers: Dict, params: Dict, timeout: int):
    if method == 'get':

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
        return response
    return status_code


def _find_location(base_url: str, location:str, headers: Dict, timeout:int, func=_make_response):
    url = urllib.parse.urljoin(base_url, "location/v3/search/", True)
    querystring = {"q": location, "locale": "en_US", "langid":"1033", "siteid":"30000001"}
    response = func("get", url, headers, querystring, timeout)
    return response

"""url = "https://hotels4.p.rapidapi.com/locations/v3/search"

querystring = {"q":"new york","locale":"en_US","langid":"1033","siteid":"300000001"}

headers = {
	"X-RapidAPI-Key": "6741070c10mshc69db9dd5f323c3p1a91c5jsnaddb2d72834a",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)"""
def _hotels_list(base_url: str, headers: Dict, params: Dict, timeout: int, func=_make_response)
    url = urllib.parse.urljoin(base_url, "properties/v2/list", True)
    headers["content-type"] = "application/json"
    payload =

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





def _get_math_fact(method: str, url: str, headers: Dict, params: Dict, number: int,
                   timeout: int, func=_make_response):
    url = f"{url}/{number}/math"
    response = func(method, url, headers=headers, params=params, timeout=timeout)

    return response


class SiteApiInterface:

    @staticmethod
    def find_location():
        return _find_location

    @staticmethod
    def get_math_fact():
        return _get_math_fact


if __name__ == "__main__":
    _make_response()
    _get_math_fact()
    _get_location_search()
    SiteApiInterface()
