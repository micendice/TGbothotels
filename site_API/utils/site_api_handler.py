import requests
import json
import logging
import urllib.parse
import traceback
import sys

from typing import Dict

from config_data.config import SiteSettings, url_loc_search, url_hotels_list, url_hotel_summary, url_get_offer
from utils.logging import log, error_log

site = SiteSettings()

st_headers = {
	"X-RapidAPI-Key": site.api_key.get_secret_value(),
	"X-RapidAPI-Host": site.host_api[8:]                    #Cutting off https prefix
    }


base_url = site.host_api

logger_2 = logging.getLogger(__name__)
logger_2.setLevel(logging.INFO)

handler_2 = logging.FileHandler(f"{__name__}.log", mode="a", encoding="utf-8")
formatter_2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler_2.setFormatter(formatter_2)
logger_2.addHandler(handler_2)

logger_2.info(f"logger site_api_handler started")


def _make_response(method: str, url: str, headers: Dict, params: Dict, timeout: int):
    log.info(f"Make response func started")
    if method == 'get':
        logger_2.info(f"Creating request : method: {method}\nurl: {url}\n"
                      f"headers: {headers}\n params- (querystring): {params}\ntimeout: {timeout}")
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=timeout
        )
    elif method == "post":
        logger_2.info(f"Creating request :method: {method}\nurl: {url}\n"
                      f"headers: {headers}\n params-(payload) : {params}\ntimeout: {timeout}")
        response = requests.request(
            method,
            url,
            json=params,
            headers=headers,
            timeout=timeout
        )

    status_code = response.status_code
    logger_2.info(f"Requesting successful. Response is {status_code}")

    if status_code == 200:
        log.info(f"Make response func succeeded with result {status_code}")
        return response.text
    else:
        logger_2.info(f"Fail! Response is {status_code}")
        log.info(f"Make response func failed with result {status_code}")


def _find_location(location: str, base: str = base_url, headers: Dict = st_headers,
                   timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_loc_search, True)

    querystring = {"q": location, "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    response = func("get", url, headers, querystring, timeout)
    response_dict = json.loads(response)

    if response_dict['rc'] == 'OK':
        # obtain list with number of locations with 'CITY' and 'NEIGHBORHOOD' keys. THEn offer multiply choice to user
        # first - form list of dicts. second - in TG API core create message with reply markup of multiple choice
        potential_loc_list = []
        for item in response_dict["sr"]:
            pll_dict = {}
            if item["type"] == "CITY" or item["type"] == "NEIGHBORHOOD":
                pll_dict["gaiaId"] = item["gaiaId"]
                pll_dict["display_name"] = item["regionNames"]["displayName"]
                pll_dict["type"] = item["type"]
                potential_loc_list.append(pll_dict)

        """gaiaId = response_dict["sr"][0]["gaiaId"]"""
        logger_2.info(f"result of location search: {response_dict['rc']}, potential locations = {potential_loc_list}")
        #coordinates = response_dict["sr"][0]["coordinates"]
        result = potential_loc_list
        #res1 = {"coordinates": {"latitude": coordinates["lat"], "longitude": coordinates["long"]}, "regionId": gaiaId},
    else:
        result = None
        logger_2.info(f"result of location search is None: {result}")
    return result


def _hotels_list(payload: Dict, base: str = base_url, headers: Dict = st_headers,
                 timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_hotels_list, True)
    headers["content-type"] = "application/json"
    try:
        response = func("post", url, headers, payload, timeout)
    except:
        frame = traceback.extract_tb(sys.exc_info()[2])
        line_no = str(frame[0]).split()[4]
        error_log(line_no)

    if response:
        logger_2.info(f"response for hotels list request is not None: ")
    else:
        logger_2.info(f"response for hotels list request is None!!! ")

    response_dict = json.loads(response)
    hotels_id_info = dict()
    try:
        properties_list = response_dict["data"]["propertySearch"]["properties"]

    except:
        frame = traceback.extract_tb(sys.exc_info()[2])
        line_no = str(frame[0]).split()[4]
        error_log(line_no)

    for item in properties_list:
        hotels_id_info[item["id"]] = {"name": item["name"]}
    return hotels_id_info


def _hotel_summary(payload: Dict, num_photo: int, base: str = base_url,
                    headers: Dict = st_headers, timeout: int = 1000, func=_make_response):
    url = urllib.parse.urljoin(base, url_hotel_summary, True)
    headers["content-type"] = "application/json"
    response = func("post", url, headers, payload, timeout)
    try:
        response_dict = json.loads(response)
    except:
        frame = traceback.extract_tb(sys.exc_info()[2])
        line_no = str(frame[0]).split()[4]
        error_log(line_no)

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
        logger_2.info(f"price not available {result}")
    else:
        accomodation_price = \
            response_dict["data"]["propertyOffers"]["units"][0]["ratePlans"][0]["priceDetails"][0]["totalPriceMessage"]
        result = accomodation_price

    return result


class SiteApiInterface:

    @staticmethod
    def find_location(location):
        try:
            return _find_location(location)
        except:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_no = str(frame[0]).split()[4]
            error_log(line_no)


    @staticmethod
    def get_hotels_list(payload):
        try:
            return _hotels_list(payload)
        except:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_no = str(frame[0]).split()[4]
            error_log(line_no)

    @staticmethod
    def get_hotel_summary(payload, num_photo):
        try:
            return _hotel_summary(payload, num_photo)

        except:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_no = str(frame[0]).split()[4]
            error_log(line_no)

    @staticmethod
    def get_hotel_price(payload):
        try:
            return _hotel_price(payload)
        except:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_no = str(frame[0]).split()[4]
            error_log(line_no)


site_api = SiteApiInterface()


if __name__ == "__main__":
    _make_response()
    _find_location()
    _hotels_list()
    _hotel_summary()
    _hotel_price()
    SiteApiInterface()
