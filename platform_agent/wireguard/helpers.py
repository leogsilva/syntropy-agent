import datetime
import os

from platform_agent.cmd.wg_info import WireGuardRead


def get_peer_info(ifname, wg):
    results = {}
    if os.environ.get("NOIA_WIREGUARD"):
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


def get_peer_info_all(ifname, wg):
    results = []
    if os.environ.get("NOIA_WIREGUARD"):
        ss = wg.info(ifname)
        wg_info = dict(ss[0]['attrs'])
        peers = wg_info.get('WGDEVICE_A_PEERS', [])
        for peer in peers:
            peer_dict = dict(peer['attrs'])
            results.append({
                "public_key": peer_dict['WGPEER_A_PUBLIC_KEY'].decode('utf-8'),
                "last_handshake": datetime.datetime.strptime(peer_dict['WGPEER_A_LAST_HANDSHAKE_TIME']['latest handshake'],
                                                             "%a %b %d %H:%M:%S %Y").isoformat(),
                "keep_alive_interval": peer_dict['WGPEER_A_PERSISTENT_KEEPALIVE_INTERVAL'],
                "rx_bytes": peer_dict['WGPEER_A_RX_BYTES'],
                "tx_bytes": peer_dict['WGPEER_A_TX_BYTES'],
            })

    else:
        wg = WireGuardRead()
        iface = wg.wg_info(ifname)[0]
        for peer in iface['peers']:
            results.append({
                "public_key": peer['peer'],
                "last_handshake": datetime.datetime.now().isoformat() if peer['latest_handshake'] else None,
                "keep_alive_interval": peer['persistent_keepalive'],
            })
    return results