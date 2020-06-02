import socket
import base64
import logging
import subprocess
from pathlib import Path

from pyroute2 import IPDB, WireGuard
from nacl.public import PrivateKey

from platform_agent.cmd.lsmod import module_loaded
from platform_agent.cmd.wg_show import get_wg_listen_port
from platform_agent.routes import ip_route_add, ip_route_del

logger = logging.getLogger()


class WgConfException(Exception):
    pass


class WgConf():

    def __init__(self):

        self.wg_kernel = module_loaded('wireguard')
        self.wg = WireGuard() if self.wg_kernel else WireguardGo()

    def get_wg_keys(self, ifname):
        private_key_path = f"/etc/wireguard/privatekey-{ifname}"
        public_key_path = f"/etc/wireguard/publickey-{ifname}"
        private_key = Path(private_key_path)
        public_key = Path(public_key_path)
        if not private_key.is_file() or not public_key.is_file():
            privKey = PrivateKey.generate()
            pubKey = base64.b64encode(bytes(privKey.public_key))
            privKey = base64.b64encode(bytes(privKey))
            base64_privKey = privKey.decode('ascii')
            base64_pubKey = pubKey.decode('ascii')
            private_key.write_text(base64_privKey)
            public_key.write_text(base64_pubKey)
        if self.wg_kernel:
            return public_key.read_text().strip(), private_key.read_text().strip()
        else:
            return public_key.read_text().strip(), private_key_path


    def next_free_port(self, port=1024, max_port=65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while port <= max_port:
            try:
                sock.bind(('', port))
                sock.close()
                return port
            except OSError:
                port += 1
        raise IOError('no free ports')

    def create_interface(self, ifname, internal_ip, listen_port=None):
        logger.info(f"[WG_CONF] - Creating interface {ifname}")
        public_key, private_key = self.get_wg_keys(ifname)

        with IPDB() as ip:
            if self.wg_kernel:
                wg1 = ip.create(kind='wireguard', ifname=ifname)
            else:
                self.wg.create_interface(ifname)
                wg1 = ip.interfaces[ifname]
            wg1.add_ip(internal_ip)
            wg1.up()
            wg1.commit()
        self.wg.set(
            ifname,
            private_key=private_key,
            listen_port=listen_port
        )

        listen_port = self.get_listening_port(ifname)

        return {
            "public_key": public_key,
            "listen_port": listen_port
        }

    def add_peer(self, ifname, public_key, allowed_ips, gw_ipv4, endpoint_ipv4=None, endpoint_port=None):
        peer = {'public_key': public_key,
                'endpoint_addr': endpoint_ipv4,
                'endpoint_port': endpoint_port,
                'persistent_keepalive': 15,
                'allowed_ips': allowed_ips}
        self.wg.set(ifname, peer=peer)
        ip_route_add(ifname, allowed_ips, gw_ipv4)
        return

    def remove_peer(self, ifname, public_key, allowed_ips):
        peer = {
            'public_key': public_key,
            'remove': True
            }

        self.wg.set(ifname, peer=peer)
        ip_route_del(ifname, allowed_ips)
        return

    def remove_interface(self, ifname):
        with IPDB() as ipdb:
            if ifname not in ipdb.interfaces:
                raise WgConfException(f'[{ifname}] does not exist')
            with ipdb.interfaces[ifname] as i:
                i.remove()
        return

    def get_listening_port(self, ifname):
        if self.wg_kernel:
            wg_info = dict(self.wg.info(ifname)[0]['attrs'])
            return wg_info['WGDEVICE_A_LISTEN_PORT']

        else:
            wg_info = self.wg.info(ifname)
            return wg_info['listen_port']


class WireguardGo():

    def set(self, ifname, peer=None, private_key=None, listen_port=None):
        full_cmd = f"wg set {ifname}".split(' ')
        if peer:
            allowed_ips_cmd = ""
            if not peer.get('remove'):
                for ip in peer.get('allowed_ips', []):
                    allowed_ips_cmd += f"allowed-ips {ip} "
                peer_cmd = f"peer {peer['public_key']} {allowed_ips_cmd}endpoint {peer['endpoint_addr']}:{peer['endpoint_port']}".split(' ')
            else:
                peer_cmd = f"peer {peer['public_key']} remove"
            full_cmd += peer_cmd
        if private_key:
            private_key_cmd = f"private-key {private_key}".split(' ')
            full_cmd += private_key_cmd
        if listen_port:
            listen_port_cmd = f"listen-port {listen_port}".split(' ')
            full_cmd += listen_port_cmd

        result_set = subprocess.run(full_cmd, encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        complete_output = result_set.stdout or result_set.stderr
        complete_output = complete_output or 'Success'
        logger.info(f"[Wireguard-go] - WG SET - {complete_output} , args {full_cmd}")
        return complete_output

    def create_interface(self, ifname):
        result_set = subprocess.run(['wireguard-go', ifname], encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        complete_output = result_set.stdout or result_set.stderr
        complete_output = complete_output or 'Success'
        return complete_output

    def info(self, ifname):
        return {
            "listen_port": get_wg_listen_port(ifname)
        }