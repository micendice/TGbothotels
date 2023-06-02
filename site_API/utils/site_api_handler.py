import requests
from typing import Dict
import urllib.parse
from ..settings import SiteSettings, url_loc_search, url_hotels_list, url_hotel_summary, url_get_offer
import json
site = SiteSettings()

st_headers = {
	"X-RapidAPI-Key": site.api_key.get_secret_value(),
	"X-RapidAPI-Host": site.host_api
    }

base_url = "https://" + site.host_api

def _make_response(method: str, url: str, headers: Dict, params: Dict, timeout: int):
    if method == 'get':
        """print(f'method: {method}\nurl: {url}\nheaders: {headers}\n params- (querystring): {params}\ntimeout: {timeout}')"""
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=timeout
        )
    elif method == "post":
        """print(f'method: {method}\nurl: {url}\nheaders: {headers}\n params-(payload) : {params}\ntimeout: {timeout}')"""
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
    else:
        print(response)
    return status_code


def _find_location(location: str, base: str = base_url, headers: Dict = st_headers,
                   timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_loc_search , True)

    querystring = {"q": location, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    """print(f'url: {str(url)}\nquerystring: {querystring}\n')"""
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


def _hotels_list(payload: Dict, base: str = base_url, headers: Dict = st_headers,
                 timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_hotels_list, True)
    headers["content-type"] = "application/json"

    response = func("post", url, headers, payload, timeout)
    response_dict = json.loads(response)
    hotels_id_info = dict()
    properties_list = response_dict["data"]["propertySearch"]["properties"]

    for item in properties_list:
        hotels_id_info[item["id"]] = {"name": item["name"]}
    return hotels_id_info


def _hotel_summary(payload: Dict, num_photo: int, base: str = base_url,
                    headers: Dict = st_headers, timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_hotel_summary, True)
    headers["content-type"] = "application/json"
    response = func("post", url, headers, payload, timeout)
    response_dict = json.loads(response)

    short_descr = response_dict["data"]["propertyInfo"]["summary"]["tagline"]
    addressline = response_dict["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"]
    photo_urls = list()
    if num_photo > 0:
        for i_photo in range(num_photo):
            url_photo = response_dict["data"]["propertyInfo"]["propertyGallery"]["images"][i_photo]["image"]["url"]  # images - list of dicts
            photo_urls.append(url_photo)

    hotel_summary_dict = {"short_descr": short_descr, "addressline": addressline, "urlphoto": photo_urls}
    return hotel_summary_dict


def _hotel_price(payload: Dict, base: str = base_url,
                    headers: Dict = st_headers, timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_get_offer, True)
    headers["content-type"] = "application/json"
    response = func("post", url, headers, payload, timeout)
    response_dict = json.loads(response)
    error_message = response_dict["data"]["propertyOffers"]["errorMessage"]
    if error_message:
        result = response_dict["data"]["propertyOffers"]["errorMessage"]["title"]["text"]
        print(error_message)
    else:
        accomodation_price = dict()
        accomodation_price["total_price"] =\
            response_dict["data"]["propertyOffers"]["units"][0]["ratePlans"][0]["priceDetails"][0]["price"]["total"][
            "amount"]
        accomodation_price["totalPriceMessage"] =\
            response_dict["data"]["propertyOffers"]["units"][0]["ratePlans"][0]["priceDetails"][0]["totalPriceMessage"]
        print(accomodation_price)
        result = accomodation_price

    return result


class SiteApiInterface:

    @staticmethod
    def find_location(location):
        return _find_location(location)

    @staticmethod
    def get_hotels_list(payload):
        return _hotels_list(payload)

    @staticmethod
    def get_hotel_summary(payload, num_photo):
        return _hotel_summary(payload, num_photo)

    @staticmethod
    def get_hotel_price(payload):
        return _hotel_price(payload)


site_api = SiteApiInterface()


if __name__ == "__main__":
    _make_response()
    _find_location()
    _hotels_list()
    _hotel_summary()
    _hotel_price()
    SiteApiInterface()
