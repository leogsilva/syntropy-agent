import json
import logging
import threading
import time

from pyroute2 import WireGuard

from platform_agent.lib.ctime import now

logger = logging.getLogger()

IFNAME = 'wg0-server'


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
            results = []
            ss = self.wg.info(IFNAME)
            wg_info = dict(ss[0]['attrs'])
            peers = wg_info['WGDEVICE_A_PEERS']['attrs']
            for peer in peers:
                peer_dict = dict(peer[1]['attrs'])
                results.append(
                    {
                        "last_handshake": peer_dict['WGPEER_A_LAST_HANDSHAKE_TIME'],
                        "keep_alive_intreval": peer_dict['WGPEER_A_PERSISTENT_KEEPALIVE_INTERVAL'],
                        "public_key": peer_dict['WGPEER_A_PUBLIC_KEY'],
                        "rx_bytes": peer_dict['WGPEER_A_RX_BYTES'],
                        "tx_bytes": peer_dict['WGPEER_A_TX_BYTES'],

                    }
                )
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
