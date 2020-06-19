

def get_peer_info(ifname, wg):

    results = {}
    ss = wg.info(ifname)
    wg_info = dict(ss[0]['attrs'])
    peers = wg_info.get('WGDEVICE_A_PEERS', [])
    for peer in peers:
        peer = dict(peer['attrs'])
        results[peer['WGPEER_A_PUBLIC_KEY'].decode('utf-8')] = [allowed_ip['addr'] for allowed_ip in
                                                                peer['WGPEER_A_ALLOWEDIPS']]
    return results


