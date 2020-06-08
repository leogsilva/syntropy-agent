import threading
import time
import logging
import pyroute2
import ipaddress

from icmplib import multiping

from pyroute2 import WireGuard

from platform_agent.cmd.lsmod import module_loaded
from platform_agent.routes import ip_route_del, ip_route_add

logger = logging.getLogger()


def get_peer_info(ifname, wg):

    results = {}
    ss = wg.info(ifname)
    wg_info = dict(ss[0]['attrs'])
    peers = wg_info.get('WGDEVICE_A_PEERS', [])
    for peer in peers:
        peer = dict(peer['attrs'])
        results[peer['WGPEER_A_PUBLIC_KEY'].decode('utf-8')] = [allowed_ip['addr'] for allowed_ip in
                                                                peer['WGPEER_A_ALLOWEDIPS']]
    return results


def get_routing_info(wg):
    with pyroute2.IPDB() as ipdb:
        routing_info = {}
        peers_internal_ips = []
        res = {k: v for k, v in ipdb.by_name.items() if v.get('kind') == 'wireguard'}
        for ifname in res.keys():
            if not res[ifname].get('ipaddr'):
                continue
            internal_ip = f"{res[ifname]['ipaddr'][0]['address']}/{res[ifname]['ipaddr'][0]['prefixlen']}"
            peers = get_peer_info(ifname, wg)
            for peer in peers.keys():
                peer_internal_ip = next(
                    (
                        ip for ip in peers[peer]
                        if ipaddress.ip_address(ip.split('/')[0]) in ipaddress.ip_network(internal_ip, False)
                    ),
                    None
                )
                if not peer_internal_ip:
                    continue
                peers_internal_ips.append(peer_internal_ip)
                peers[peer].remove(peer_internal_ip)
                for allowed_ip in peers[peer]:
                    if not routing_info.get(allowed_ip):
                        routing_info[allowed_ip] = {'ifaces': {}}
                    routing_info[allowed_ip]['ifaces'][ifname] = peer_internal_ip
        return routing_info, peers_internal_ips


def get_interface_internal_ip(ifname):
    with pyroute2.IPDB() as ipdb:
        internal_ip = f"{ipdb.interfaces[ifname]['ipaddr'][0]['address']}"
        return internal_ip


def ping_internal_ips(ips):
    result = {}
    ping_res = multiping(ips, count=4, interval=0.5)
    for res in ping_res:
        result[res.address] = {
            "latency_ms": res.avg_rtt if res.is_alive else 10000,
            "packet_loss": res.packet_loss if res.is_alive else 1
        }
    return result


def get_fastest_routes(wg):
    result = {}
    routing_info, peers_internal_ips = get_routing_info(wg)
    ping_results = ping_internal_ips(peers_internal_ips)
    for dest, routes in routing_info.items():
        best_route = None
        best_ping = 9999
        for iface, internal_ip in routes['ifaces'].items():
            if ping_results[internal_ip]['latency_ms'] < best_ping:
                best_route = {'iface': iface, 'gw': internal_ip}
                best_ping = ping_results[internal_ip]['latency_ms']
        result[dest] = best_route
    return result


class Rerouting(threading.Thread):

    def __init__(self, interval=1):
        super().__init__()
        self.interval = interval
        self.wg = WireGuard()
        self.stop_rerouting = threading.Event()
        self.daemon = True

    def run(self):
        if not module_loaded('wireguard'):
            return
        while not self.stop_rerouting.is_set():
            previous_routes = {}
            new_routes = get_fastest_routes(self.wg)
            for dest, best_route in new_routes.items():
                if not best_route and previous_routes.get(dest) == best_route:
                    continue
                # Do rerouting logic with best_route
                logger.info(f"Rerouting {dest} via {best_route}")
                ip_route_del(ifname=best_route['iface'], ip_list=[dest])
                ip_route_add(
                    ifname=best_route['iface'], ip_list=[dest], gw_ipv4=get_interface_internal_ip(best_route['iface'])
                )
            time.sleep(int(self.interval))

    def join(self, timeout=None):
        self.stop_rerouting.set()
        super().join(timeout)
