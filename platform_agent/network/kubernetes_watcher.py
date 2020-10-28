import json
import logging
import threading
import time
import os

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
            self.current_namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
        except config.config_exception.ConfigException:
            self.current_namespace = os.environ.get('NOIA_NAMESPACE', None)
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
            if not self.current_namespace:
                return
            ret = self.v1.list_namespaced_service(self.current_namespace)
            for i in ret.items:
                if not i.metadata.name:
                    continue
                ports = {'udp': [], 'tcp': []}
                if not i.spec.ports:
                    continue
                ports['tcp'] = [port.port for port in i.spec.ports if port.protocol == 'TCP']
                ports['udp'] = [port.port for port in i.spec.ports if port.protocol == 'UDP']
                result.append(
                    {
                        'agent_service_subnets': f"{i.spec.cluster_ip}/32",
                        'agent_service_name': i.metadata.name,
                        'agent_service_ports': ports,
                        'agent_service_uptime': i.metadata.creation_timestamp.isoformat(),
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