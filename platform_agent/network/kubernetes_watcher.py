import json
import logging
import threading
import time

from platform_agent.lib.ctime import now
from pyroute2 import IPDB
from kubernetes import client, config

logger = logging.getLogger()


class KubernetesConfigException(Exception):
    pass


class KubernetesNetworkWatcher(threading.Thread):

    def __init__(self, ws_client):
        super().__init__()
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException:
            try:
                config.load_kube_config()
            except config.config_exception.ConfigException:
                raise KubernetesConfigException("Couldn't find config")
        self.v1 = client.CoreV1Api()
        self.ws_client = ws_client
        self.stop_kubernetes_watcher = threading.Event()
        self.interval = 10

        with IPDB() as ipdb:
            self.ifaces = [k for k, v in ipdb.by_name.items() if any(
                substring in k for substring in ['noia_'])]
        self.daemon = True

    def run(self):
        ex_result = []
        while not self.stop_kubernetes_watcher.is_set():
            result = []
            ret = self.v1.list_pod_for_all_namespaces()

            for i in ret.items:
                if not i.metadata.labels.get('name'):
                    continue
                ports = {'udp': [], 'tcp': []}
                for container in i.spec.containers:
                    if not container.ports:
                        continue
                    ports['tcp'] = [port.container_port for port in container.ports if port.protocol == 'TCP']
                    ports['udp'] = [port.container_port for port in container.ports if port.protocol == 'UDP']
                result.append(
                    {
                        'agent_service_subnets': f"{i.status.pod_ip}/32",
                        'agent_service_name': i.metadata.labels['name'],
                        'agent_service_ports': ports,
                        'agent_service_uptime': i.status.start_time.isoformat(),
                    }
                )
            if result != ex_result:
                self.ws_client.send(json.dumps({
                    'id': "ID." + str(time.time()),
                    'executed_at': now(),
                    'type': 'KUBERNETES_SERVICE_INFO',
                    'data': result
                }))
                ex_result = result
            time.sleep(10)

    def join(self, timeout=None):
        self.stop_kubernetes_watcher.set()
        super().join(timeout)
