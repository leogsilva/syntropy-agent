import logging
from platform_agent.lib.get_info import gather_initial_info
from platform_agent.wireguard import WgConfException, WgConf, WireguardPeerWatcher
from platform_agent.rerouting import Rerouting
from platform_agent.docker_api.docker_api import DockerNetworkWatcher

logger = logging.getLogger()


class AgentApi:

    def __init__(self, runner):
        self.runner = runner
        self.wg_peers = None
        self.wgconf = WgConf()
        self.network_watcher = DockerNetworkWatcher(self.runner).start()
        self.rerouting = Rerouting().start()

    def call(self, type, data, request_id):
        result = None
        try:
            if hasattr(self, type):
                logger.info(f"[AGENT_API] Calling agent api {data}")
                if not isinstance(data, (dict, list)):
                    logger.error('[AGENT_API] data should be "DICT" type')
                    result = {'error': "BAD REQUEST"}
                else:
                    fn = getattr(self, type)
                    result = fn(data, request_id=request_id)
        except AttributeError as error:
            logger.warning(error)
            result = {'error': str(error)}
        return result

    def GET_INFO(self, data, **kwargs):
        return gather_initial_info(**data)

    def WG_INFO(self, data, **kwargs):
        if self.wg_peers:
            self.wg_peers.join(timeout=1)
            self.wg_peers = None
        self.wg_peers = WireguardPeerWatcher(self.runner, **data)
        self.wg_peers.start()
        logger.debug(f"[WIREGUARD_PEERS] Enabled | {data}")

    def WG_CONF(self, data, **kwargs):
        try:
            fn = getattr(self.wgconf, data['fn'])
            return {
                'fn': data['fn'],
                'data': fn(**data['args']),
                "args": data['args']
            }
        except WgConfException as e:
            logger.error(f"[WG_CONF] failed. exception = {str(e)}, data = {data}")
            return {
                'error': {data['fn']: str(e), "args": data['args']}
            }
