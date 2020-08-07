import time
import socket
import os
import threading

from prometheus_client import start_http_server, Metric, REGISTRY

from platform_agent.wireguard.helpers import merged_peer_info
from pyroute2 import WireGuard


class JsonCollector(object):
    def __init__(self, interval=10):
        self.interval = interval
        self.wg = WireGuard()

    def collect(self):
        # Fetch the JSON
        peer_info = merged_peer_info(self.wg)
        for iface in peer_info:
            metric = Metric(f"interface_info_{iface['iface']}",
                            'interface_information', 'summary')
            for peer in iface['peers']:
                for k, v in peer.items():
                    if k not in ['latency_ms', 'packet_loss', 'rx_bytes', 'tx_bytes']:
                        continue
                    metric.add_sample(f"iface_information_{k}",
                                      value=str(v),
                                      labels={
                                          'hostname': os.environ.get('NOIA_AGENT_NAME', socket.gethostname()),
                                           'ifname': iface['iface'], 'peer': peer['public_key'], 'internal_ip': peer['internal_ip']})
            yield metric


class NetworkExporter(threading.Thread):

    def __init__(self, port=18001):
        super().__init__()
        self.stop_network_exporter = threading.Event()
        self.exporter_port = port
        self.daemon = True

    def run(self):
        start_http_server(self.exporter_port)
        REGISTRY.register(JsonCollector())
        while self.stop_network_exporter.is_set(): time.sleep(1)

    def join(self, timeout=None):
        self.stop_network_exporter.set()
        super().join(timeout)
