import logging

from pyroute2 import IPRoute, NetlinkError

logger = logging.getLogger()


def ip_route_add(ifname, ip_list, gw_ipv4):
    ip_route = IPRoute()
    devices = ip_route.link_lookup(ifname=ifname)
    dev = devices[0]
    for ip in ip_list:
        try:
            ip_route.route('add', dst=ip, gateway=gw_ipv4, oif=dev)
        except NetlinkError as error:
            if error.code != 17:
                raise
            logger.info(f"[WG_CONF] add route failed [{ip}] - already exists")


def ip_route_del(ifname, ip_list, scope=None):
    ip_route = IPRoute()
    devices = ip_route.link_lookup(ifname=ifname)
    dev = devices[0]
    for ip in ip_list:
        try:
            ip_route.route('del', dst=ip, oif=dev, scope=scope)
        except NetlinkError as error:
            if error.code != 17:
                raise
            logger.info(f"[WG_CONF] del route failed [{ip}] - does not exist")


def create_rule(internal_ip, rt_table_id):
    ip_route = IPRoute()
    ip_route.flush_rules(table=rt_table_id)
    ip_route.flush_routes(table=rt_table_id)
    ip_route.rule('add', src=internal_ip, table=rt_table_id)
