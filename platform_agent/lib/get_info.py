from pathlib import Path
from pyroute2 import IPRoute
import logging

logger = logging.getLogger()


def get_ipv4_gw():
    # Get ipv4 gateway, relevant only for aws servers
    ifaces = ['ens5', 'eth0']
    res = netifaces.interfaces()
    ifaces = set(res) & set(ifaces)
    if not ifaces:
        return {}
    ip = IPRoute()
    routes = ip.get_default_routes(table=254)
    if len(routes):
        attrs = routes[0].get('attrs')
        for attr in attrs:
            if 'RTA_GATEWAY' in attr:
                return {"server_gateway_ipv4": attr[1]}
    return {}


def get_ipv6_gw():
    # Get ipv6 gateway, relevant only for aws servers
    ifaces = ['ens5', 'eth0']
    res = netifaces.interfaces()
    ifaces = set(res) & set(ifaces)
    if ifaces:
        iface = ifaces.pop()
    else:
        logger.warning(f"[AWS only] Expected interfaces not found || {res}")
        return {}
    try:
        ip = sr1(IPv6(dst="ff02::2") / ICMPv6ND_RS(), iface=iface, retry=1, timeout=5)[IPv6].src
    except (OSError, TypeError):
        return {}
    return {"server_gateway_ipv6": ip}


def get_wg_publickey():
    try:
        public_key = Path('/etc/wireguard/publickey-server').read_text().strip()
        return {"server_public_key": public_key}
    except FileNotFoundError:
        return {}


def get_server_ifaces_names():
    # Get sr-iov created interfaces, relevant only for sr-iov servers
    try:
        from platform_agent.lib.vpp_api import NoiaVppClient
    except ModuleNotFoundError:
        return {"server_interfaces_names": []}
    vpp = NoiaVppClient()
    vpp.connect()
    ifaces = vpp.api_iface_dump()
    res = [iface['interface_name'] for iface in ifaces if iface['interface_dev_type'] == 'dpdk']
    vpp.disconnect()
    return {"server_interfaces_names": res}


def gather_initial_info():
    result = {}
    result.update(get_ipv4_gw())
    result.update(get_ipv6_gw())
    result.update(get_wg_publickey())
    result.update(get_server_ifaces_names())
    return result
