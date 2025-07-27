"""
HTTP functions.
"""


# ----------------------------------------------------------------------------------------------------
# imports

import urllib3
import requests

from fetcher.lib.defs import ENCODING


# ----------------------------------------------------------------------------------------------------
# defines

SECURE = False


# ----------------------------------------------------------------------------------------------------
# module init code

# disable https warnings (only use known hosts and disable host verification)
if not SECURE:
    urllib3.disable_warnings()


# ----------------------------------------------------------------------------------------------------
# functions

def http_get(url: str, accept=None, authorization=None) -> str:
    """Send HTTP GET request."""

    # gen http request header
    headers = dict()

    if accept is not None:
        headers["Accept"] = accept
    if authorization is not None:
        headers["Authorization"] = authorization

    # send request and return response as text
    response = requests.get(url=url, headers=headers, verify=SECURE)
    response.encoding = ENCODING

    return response.text
