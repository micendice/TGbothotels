import requests
from typing import Dict


def _make_response(method: str, url: str, headers: Dict, params: Dict, timeout: int, success=200):
    response = requests.request(
        method,
        url,
        headers=headers,
        params=params,
        timeout=timeout
    )
    status_code = response.status_code

    if status_code == success:
        return response
    return status_code


def _get_date_fact(method: str, url: str, headers: Dict, params: Dict, date_day: str, date_month: str,
                   timeout: int, func=_make_response
                   ):
    url = f"{url}/{date_month}/{date_day}/date"
    response = func(method, url, headers=headers, params=params, timeout=timeout)

    return response


def _get_math_fact(method: str, url: str, headers: Dict, params: Dict, number: int,
                   timeout: int, func=_make_response):
    url = f"{url}/{number}/math"
    response = func(method, url, headers=headers, params=params, timeout=timeout)

    return response


class SiteApiInterface:

    @staticmethod
    def get_date_fact():
        return _get_date_fact

    @staticmethod
    def get_math_fact():
        return _get_math_fact


if __name__ == "__main__":
    _make_response()
    _get_math_fact()
    _get_date_fact()
    SiteApiInterface()
