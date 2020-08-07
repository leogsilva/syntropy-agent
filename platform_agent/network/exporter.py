import time
import socket
import os
import threading
import json

from prometheus_client import start_http_server, Metric, REGISTRY

from platform_agent.lib.ctime import now
from platform_agent.network.network_info import BWDataCollect
from platform_agent.wireguard.wg_conf import WgConf
from platform_agent.wireguard.helpers import merged_peer_info
from pyroute2 import WireGuard


class JsonCollector(object):
    def __init__(self, ws_client, interval=10):
        self.interval = interval
        self.ws_client = ws_client
        self.wg = WireGuard()

    def collect(self):
        # Fetch the JSON
        while True:
            peer_info = merged_peer_info(self.wg)
            self.ws_client.send_log(json.dumps({
                'id': "ID." + str(time.time()),
                'executed_at': now(),
                'type': 'IFACES_PEERS_BW_DATA',
                'data': peer_info
            }))
            for iface in peer_info:
                metric = Metric(f"interface_info_{iface['iface']}",
                                'interface_information', 'summary')
                for peer in iface['peers']:
                    for k, v in peer.items():
                        metric.add_sample(f"iface_information_{k}",
                                          value=str(v),
                                          labels={'hostname': os.environ.get('NOIA_AGENT_NAME', socket.gethostname()),
                                                  'ifname': iface['iface']})
                yield metric


class NetworkExporter(threading.Thread):

    def __init__(self, ws_client, port=18001):
        super().__init__()
        self.ws_client = ws_client
        self.stop_network_exporter = threading.Event()
        self.exporter_port = port
        self.daemon = True

    def run(self):
        start_http_server(self.exporter_port)
        REGISTRY.register(JsonCollector(self.ws_client))
        while self.stop_network_exporter.is_set(): time.sleep(1)

    def join(self, timeout=None):
        self.stop_network_exporter.set()
        super().join(timeout)
