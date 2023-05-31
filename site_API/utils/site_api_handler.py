import requests
from typing import Dict
import urllib.parse
from ..settings import SiteSettings, url_loc_search, url_hotels_list, url_hotel_summary
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
        print(f'method: {method}\nurl: {url}\nheaders: {headers}\n params-(payload) : {params}\ntimeout: {timeout}')
        response = requests.request(
            method,
            url,
            json=params,
            headers=headers,
            timeout=timeout
        )

    status_code = response.status_code

    if 200 <= status_code <= 399:
        return response.text
    return status_code


def _find_location(location: str, base: str = base_url, headers: Dict = st_headers,
                   timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_loc_search , True)

    querystring = {"q": location, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    print(f'url: {str(url)}\nquerystring: {querystring}\n')
    response = func("get", url, headers, querystring, timeout)
    response_dict = json.loads(response)
    """print(response)"""
    print(response_dict['rc'], response_dict['rid'])

    if response_dict['rc'] == 'OK':
        gaiaId = response_dict["sr"][0]["gaiaId"]
        coordinates = response_dict["sr"][0]["coordinates"]
        result = gaiaId
        res1 = {"coordinates": {"latitude": coordinates["lat"], "longitude": coordinates["long"]}, "regionId": gaiaId},
    else:
        result = None

    return result

# Нет!  надо будет сортировать все отели по цене!!! пейлоад с большим количеством сделать, отсортировать как надо и взять первые несколько
def _hotels_list(payload: Dict, base: str = base_url, headers: Dict = st_headers,
                 timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_hotels_list, True)
    headers["content-type"] = "application/json"
    response = func("post", url, headers, payload, timeout)
    response_dict = json.loads(response)
    hotels_id_name = dict()
    properties_list = response_dict["data"]["propertySearch"]["properties"]

    for item in properties_list:
        hotels_id_name[item["id"]] = item["name"]
    return hotels_id_name


def _get_hotel_summary(payload: Dict, photo_num: int, base: str = base_url,
                    headers: Dict = st_header, timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_hotel_summary, True)
    headers["content-type"] = "application/json"
    response = func("post", url, headers, payload, timeout)
    response_dict = json.loads(response)
    hotel_details_dict = response_dict[""]

    short_descr = hotel_details_dict["data"]["propertyInfo"]["summary"]["tagline"]
    addressline = hotel_details_dict["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"]
    photo_urls = list()
    if photo_num > 0:
        for i_photo in range(photo_num):
            urlPhoto = hotel_details_dict["data"]["propertyInfo"]["propertyGallery"]["images"][i_photo]["image"]["url"]  # images - list of dicts
            photo_urls.append(urlPhoto)


def _get_price(payload, headers, params, timeout):
    pass

class SiteApiInterface:

    @staticmethod
    def find_location(location):
        return _find_location(location)

    @staticmethod
    def get_hotels_list(payload):
        return _hotels_list(payload)


site_api = SiteApiInterface()


if __name__ == "__main__":
    _make_response()
    _find_location()
    _hotels_list()
    SiteApiInterface()
