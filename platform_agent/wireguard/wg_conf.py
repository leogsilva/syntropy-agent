from pyroute2 import IPDB, WireGuard


class WgConfException(Exception):
    pass


class WgConf():

    def __init__(self):
        self.wg = WireGuard()

    def create_interface(self, ifname, internal_ip, listen_port):
        with IPDB() as ip:
            wg1 = ip.create(kind='wireguard', ifname=ifname)

            wg1.add_ip(internal_ip)
            wg1.up()
            wg1.commit()

        self.wg.set(ifname, private_key='RCdhcHJlc0JpY2hlLEplU2VyYWlzTGFQbHVzQm9ubmU=', fwmark=0x1337, listen_port=listen_port)

    def add_peer(self, ifname, public_key, allowed_ips, endpoint_addr, endpoint_port):
        peer = {'public_key': public_key,
                'endpoint_addr': endpoint_addr,
                'endpoint_port': endpoint_port,
                'persistent_keepalive': 15,
                'allowed_ips': allowed_ips}
        self.wg.set(ifname, peer=peer)

    def remove_peer(self, ifname, public_key):
        peer = {
            'public_key': public_key,
            'remove': True
            }
        self.wg.set(ifname, peer=peer)

    def remove_interface(self, ifname):
        with IPDB() as ipdb:
            if ifname not in ipdb.interfaces:
                raise WgConfException(f'[{ifname}] does not exist')
            with ipdb.interfaces[ifname] as i:
                i.remove()
