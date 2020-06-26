from platform_agent.cmd.lsmod import module_loaded
from platform_agent.cmd.wg_info import WireGuardRead


def get_peer_info(ifname, wg):
    results = {}
    if module_loaded('wireguard'):
        ss = wg.info(ifname)
        wg_info = dict(ss[0]['attrs'])
        peers = wg_info.get('WGDEVICE_A_PEERS', [])
        for peer in peers:
            peer = dict(peer['attrs'])
            results[peer['WGPEER_A_PUBLIC_KEY'].decode('utf-8')] = [allowed_ip['addr'] for allowed_ip in
                                                                    peer['WGPEER_A_ALLOWEDIPS']]
    else:
        wg = WireGuardRead()
        iface = wg.wg_info(ifname)[0]
        for peer in iface['peers']:
            results[peer['peer']] = peer['allowed_ips']
    return results