import time
import json
import threading

from platform_agent.wireguard.wg_conf import WgConf
from platform_agent.lib.ctime import now


class BWDataCollect(threading.Thread):

    def __init__(self, client, interval=10):
        super().__init__()
        self.interval = interval
        self.client = client
        self.stop_BWDataCollect = threading.Event()
        self.daemon = True

    def get_int_info(self, t, iface):
        with open('/sys/class/net/' + iface + '/statistics/' + t, 'r') as f:
            data = f.read()
            return int(data)

    def run(self):
        while not self.stop_BWDataCollect.is_set():
            for iface in WgConf.get_wg_interfaces():
                tx_bytes = self.get_int_info('tx_bytes', iface)
                rx_bytes = self.get_int_info('rx_bytes', iface)

                tx_dropped = self.get_int_info('tx_dropped', iface)
                tx_errors = self.get_int_info('tx_errors', iface)
                tx_packets = self.get_int_info('tx_packets', iface)

                rx_dropped = self.get_int_info('rx_dropped', iface)
                rx_errors = self.get_int_info('rx_errors', iface)
                rx_packets = self.get_int_info('rx_packets', iface)

                time.sleep(self.interval)

                tx_bytes_after = self.get_int_info('tx_bytes', iface)
                rx_bytes_after = self.get_int_info('rx_bytes', iface)

                tx_dropped_after = self.get_int_info('tx_dropped', iface)
                tx_errors_after = self.get_int_info('tx_errors', iface)
                tx_packets_after = self.get_int_info('tx_packets', iface)

                rx_dropped_after = self.get_int_info('rx_dropped', iface)
                rx_errors_after = self.get_int_info('rx_errors', iface)
                rx_packets_after = self.get_int_info('rx_packets', iface)

                tx_speed_mbps = round((tx_bytes_after - tx_bytes) / 10000000.0, 4)
                rx_speed_mbps = round((rx_bytes_after - rx_bytes) / 10000000.0, 4)
                tx_dropped = (tx_dropped_after - tx_dropped)
                tx_errors = (tx_errors_after - tx_errors)
                tx_packets = (tx_packets_after - tx_packets)
                rx_dropped = (rx_dropped_after - rx_dropped)
                rx_errors = (rx_errors_after - rx_errors)
                rx_packets = (rx_packets_after - rx_packets)
                result = [{
                    'iface': iface,
                    'tx_speed_mbps': tx_speed_mbps,
                    'rx_speed_mbps': rx_speed_mbps,
                    'tx_dropped': tx_dropped,
                    'tx_errors': tx_errors,
                    'tx_packets': tx_packets,
                    'rx_dropped': rx_dropped,
                    'rx_errors': rx_errors,
                    'rx_packets': rx_packets,
                    'interval': self.interval,
                }]
                self.client.send(json.dumps({
                    'id': "UNKNOWN",
                    'executed_at': now(),
                    'type': 'BW_DATA',
                    'data': result
                }))
                time.sleep(int(self.interval))

    def join(self, timeout=None):
        self.stop_BWDataCollect.set()
        super().join(timeout)