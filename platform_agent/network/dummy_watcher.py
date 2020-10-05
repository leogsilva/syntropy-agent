import json
import logging
import threading
import time
import psutil

from platform_agent.lib.ctime import now
from pyroute2 import IPDB
logger = logging.getLogger()


class DummyNetworkWatcher(threading.Thread):

    def __init__(self, ws_client):
        super().__init__()
        self.ws_client = ws_client
        self.stop_network_watcher = threading.Event()
        with IPDB() as ipdb:
            self.ifaces = [k for k, v in ipdb.by_name.items() if any(
                substring in k for substring in ['noia_'])]
        self.daemon = True

    def run(self):
        result = []
        ex_result = []
        with IPDB() as ipdb:
            while not self.stop_network_watcher.is_set():
                udp = psutil.net_connections(kind='udp')
                udp_info = [{x.laddr.ip: x.laddr.port} for x in udp]
                tcp = psutil.net_connections(kind='tcp')
                tcp_info = [{x.laddr.ip: x.laddr.port} for x in tcp]
                for iface in self.ifaces:
                    intf = ipdb.interfaces[iface]
                    for k, v in dict(intf['ipaddr']).items():
                        udp_ports = [ip[k] for ip in udp_info if ip.get(k)]
                        tcp_ports = [ip[k] for ip in tcp_info if ip.get(k)]
                        result.append(
                            {
                                'agent_network_subnets': f"{k}/{v}",
                                'agent_network_iface': iface,
                                'agent_network_udp_ports': udp_ports,
                                'agent_network_tcp_ports': tcp_ports,
                            }
                        )
                if result != ex_result:
                    self.ws_client.send(json.dumps({
                        'id': "ID." + str(time.time()),
                        'executed_at': now(),
                        'type': 'DUMMY_NETWORK_INFO',
                        'data': result
                    }))
                    ex_result = result
            time.sleep(1)

    def join(self, timeout=None):
        self.stop_network_watcher.set()
        super().join(timeout)
