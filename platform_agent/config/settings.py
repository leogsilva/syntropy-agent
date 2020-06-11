import ipaddress
import os
from pathlib import Path

import yaml

CONFIG_FILE = "/etc/noia-agent/config.yaml"


class ConfigException(Exception):
    pass


class Config:

    _data = None

    def __init__(self):

        agent_path = "/etc/noia-agent"
        agent_dir = Path(f"{agent_path}")
        if not agent_dir.is_dir():
            agent_dir.mkdir()
            agent_dir.chmod(0o700)

        if os.environ.get("NOIA_API_KEY"):
            return

        if os.environ.get('NOIA_USER_API') == 'DOCKER' and not os.environ.get('NOIA_DOCKER_URL'):
            raise ConfigException(f"For Docker API, you must provide NOIA_DOCKER_URL")

        config_file = Path(CONFIG_FILE)
        if not config_file.is_file():
            print(f"Config file was not found in {CONFIG_FILE}")
            raise ConfigException(f"Config file was not found in {CONFIG_FILE}")
        env_conf = self.get_config()
        if env_conf.get('name') and type(env_conf['name']) == str:
            os.environ[f"NOIA_AGENT_NAME"] = env_conf['name']
        for k, v in env_conf.get('connection', {}).items():
            if type(v) in [int, str]:
                os.environ[f"NOIA_{k.upper()}"] = str(v)

    @staticmethod
    def get_config():
        with open(CONFIG_FILE) as f:
            config_dict = yaml.safe_load(f)
            return config_dict

    @staticmethod
    def get_list_item(key: str):
        result = Config.get_config().get(key, [])
        if type(result) != list:
            result = []
        return result

    @staticmethod
    def get_valid_allowed_ips():
        allowed_ips = Config.get_config().get('allowed_ips', [])
        result = []
        for allowed_ip in allowed_ips:
            if allowed_ip.get('name') and allowed_ip.get('subnet'):
                try:
                    ip_network = ipaddress.ip_interface(allowed_ip['subnet'])
                except ValueError:
                    continue
                result.append(
                    {
                        'agent_network_name': allowed_ip['name'],
                        'agent_network_subnets': [ip_network.with_prefixlen]
                    }
                )
        return result
