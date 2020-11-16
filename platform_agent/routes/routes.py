import logging

from pyroute2 import IPRoute, NetlinkError

logger = logging.getLogger()


class Routes:
    def __init__(self):
        self.ip_route = IPRoute()

    def ip_route_add(self, ifname, ip_list, gw_ipv4):
        devices = self.ip_route.link_lookup(ifname=ifname)
        dev = devices[0]
        statuses = []
        for ip in ip_list:
            msg = "OK"
            try:
                self.ip_route.route('add', dst=ip, gateway=gw_ipv4, oif=dev)
                status = "OK"
            except NetlinkError as error:
                if error.code != 17:
                    status = "ERROR"
                    msg = str(error)
                elif dict(self.ip_route.get_routes(dst=ip)[0]['attrs']).get('RTA_OIF') != dev:
                    logger.error(f"[WG_CONF] add route failed [{ip}] - already exists")
                    status = "ERROR"
                    msg = "OVERLAP"
                else:
                    status = "OK"
            statuses.append({"ip": ip, "status": status, "msg": msg})
        return statuses

    def ip_route_replace(self, ifname, ip_list, gw_ipv4):
        devices = self.ip_route.link_lookup(ifname=ifname)
        dev = devices[0]
        for ip in ip_list:
            try:
                self.ip_route.route('replace', dst=ip, gateway=gw_ipv4)
            except NetlinkError as error:
                if error.code != 17:
                    raise

    def ip_route_del(self, ifname, ip_list, scope=None):
        devices = self.ip_route.link_lookup(ifname=ifname)
        dev = devices[0]
        for ip in ip_list:
            try:
                self.ip_route.route('del', dst=ip, oif=dev, scope=scope)
            except NetlinkError as error:
                if error.code not in [17, 3]:
                    raise

    def create_rule(self, internal_ip, rt_table_id):
        self.ip_route.flush_rules(table=rt_table_id)
        self.ip_route.flush_routes(table=rt_table_id)
        self.ip_route.rule('add', src=internal_ip, table=rt_table_id)
