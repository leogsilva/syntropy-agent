import os
import logging
import requests

logger = logging.getLogger()


def get_ip_addr():
    resp = requests.get("https://ip.noia.network/")
    return {
        "external_ip": resp.json()
    }


def get_location():
    return {
        "location_lat": os.environ.get('NOIA_LAT'),
        "location_lon": os.environ.get('NOIA_LON'),
        "location_city": os.environ.get('NOIA_CITY')
    }


def gather_initial_info():
    result = {}
    result.update(get_ip_addr())
    return result
