def format_networks_result(networks):
    result = []
    for network in networks:
        if network.get('Name') == 'bridge':
            continue
        subnets = []
        for subnet in network['IPAM']['Config']:
            subnets.append(subnet['Subnet'])
        if subnets:
            result.append(
                {
                    'agent_network_id': network['Id'],
                    'agent_network_name': network.get('Name'),
                    'agent_network_subnets': subnets,
                }
            )
    return result
