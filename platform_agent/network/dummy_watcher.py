import json
import logging
import threading
import time

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
        while not self.stop_network_watcher.is_set():
            for iface in self.ifaces:
                with IPDB() as ipdb:
                    intf = ipdb.interfaces[iface]
                    for k, v in dict(intf['ipaddr']).items():
                        result.append(
                            {
                                'agent_network_subnets': f"{k}/{v}",
                                'agent_network_iface': iface,
                            }
                        )
                    logger.info(f"[DUMMY_NETWORK_INFO] Sending networks {result}")
                if result != ex_result:
                    self.ws_client.send(json.dumps({
                        'id': "ID." + str(time.time()),
                        'executed_at': now(),
                        'type': 'DUMMY_NETWORK_INFO',
                        'data': result
                    }))
            time.sleep(1)

    def join(self, timeout=None):
        self.stop_network_watcher.set()
        super().join(timeout)
