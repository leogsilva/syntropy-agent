import os
import logging
import socket
import requests

import docker
from platform_agent.docker_api.helpers import format_networks_result

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


def get_network_info():
    docker_client = docker.from_env()
    networks = docker_client.networks()
    network_info = format_networks_result(networks)
    return {
        "network_info": network_info
    }


def get_name():
    return {
        "agent_name": socket.gethostname()
    }


def get_tags():
    tags = os.environ.get('NOIA_TAGS')
    if tags:
        tags = os.environ.get('NOIA_TAGS').split(',')
    else:
        tags = []
    return {
        "agent_tags": tags
    }


def get_network_ids():
    network_ids = os.environ.get('NOIA_NETWORK_IDS')
    if network_ids:
        network_ids = os.environ.get('NOIA_NETWORK_IDS').split(',')
    else:
        network_ids = []
    return {
        "network_ids": network_ids
    }


def gather_initial_info():
    result = {}
    result.update(get_ip_addr())
    result.update(get_network_info())
    result.update(get_name())
    result.update(get_tags())
    result.update(get_network_ids())
    return result
