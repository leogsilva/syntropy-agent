from prometheus_client import start_http_server, Metric, REGISTRY
from platform_agent.network.network_info import BWDataCollect
from platform_agent.wireguard.wg_conf import WgConf

import time
import socket
import os
import threading


class JsonCollector(object):
    def __init__(self, interval=10):
        self.interval = interval

    def collect(self):
        # Fetch the JSON
        for iface in WgConf.get_wg_interfaces():
            print(iface)
            result = BWDataCollect.get_iface_info_set(iface, self.interval)
            del result['iface']
            metric = Metric(f'interface_info_{iface}',
                            'interface_information', 'summary')
            for k, v in result.items():
                print(k, v)
                metric.add_sample(f'interface_information_{k}',
                                  value=str(v),
                                  labels={'hostname': os.environ.get('NOIA_AGENT_NAME', socket.gethostname()),
                                          'interval': str(self.interval)})
            yield metric


class NetworExporter(threading.Thread):

    def __init__(self, ws_client, port=18001):
        super().__init__()
        self.ws_client = ws_client
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
