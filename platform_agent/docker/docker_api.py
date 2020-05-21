import json
import logging
import threading
import time

import docker
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
        while not self.stop_network_watcher.is_set():
            networks = self.docker_client.networks()
            result = []
            for network in networks:
                subnets = []
                for subnet in network['IPAM']['Config']:
                    subnets.append(subnet['Subnet'])
                if subnets:
                    result.append(
                        {
                            'docker_network_id': network['Id'],
                            'docker_network_name': network.get('Name'),
                            'docker_network_subnets': subnets

                        }
                    )
            logger.info(f"[NETWORK_INFO] Sending networks {result}")
            self.ws_client.send(json.dumps({
                'id': "ID." + str(time.time()),
                'executed_at': now(),
                'type': 'NETWORK_INFO',
                'data': result
            }))
            time.sleep(int(self.interval))

    def join(self, timeout=None):
        self.stop_network_watcher.set()
        super().join(timeout)

    def format_networks(self, networks):
        pass
