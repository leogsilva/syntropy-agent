import json
import logging
import threading
import time

import docker
from platform_agent.docker_api.helpers import format_networks_result
from platform_agent.lib.ctime import now

logger = logging.getLogger()


class DockerNetworkWatcher(threading.Thread):

    def __init__(self, ws_client, interval):
        super().__init__()
        self.ws_client = ws_client
        self.docker_client = docker.from_env()
        self.interval = interval
        self.stop_network_watcher = threading.Event()
        self.daemon = True
        threading.Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(int(self.interval))
            networks = self.docker_client.networks()
            result = format_networks_result(networks)
            logger.info(f"[NETWORK_INFO] Sending networks {result}")
            self.ws_client.send(json.dumps({
                'id': "ID." + str(time.time()),
                'executed_at': now(),
                'type': 'NETWORK_INFO',
                'data': result
            }))

    def join(self, timeout=None):
        self.stop_network_watcher.set()
        super().join(timeout)
