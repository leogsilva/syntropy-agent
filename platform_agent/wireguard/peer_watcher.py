import json
import logging
import threading
import time

from pyroute2 import WireGuard

from platform_agent.lib.ctime import now
from platform_agent.wireguard import WgConf
from platform_agent.wireguard.helpers import get_peer_info_all

logger = logging.getLogger()


class WireguardPeerWatcher(threading.Thread):

    def __init__(self, client, interval):
        super().__init__()
        self.client = client
        self.interval = interval
        self.wg = WireGuard()
        self.stop_peer_watcher = threading.Event()
        self.daemon = True

    def run(self):
        while not self.stop_peer_watcher.is_set():
            results = {}
            for iface in WgConf.get_wg_interfaces():
                peers = get_peer_info_all(iface, self.wg)
                results[iface] = peers
                self.client.send(json.dumps({
                    'id': "UNKNOWN",
                    'executed_at': now(),
                    'type': 'WIREGUARD_PEERS',
                    'data': results
                }))
                time.sleep(int(self.interval))

    def join(self, timeout=None):
        self.stop_peer_watcher.set()
        super().join(timeout)
