def format_networks_result(networks):
    result = []
    for network in networks:
        subnets = []
        for subnet in network['IPAM']['Config']:
            subnets.append(subnet['Subnet'])
        if subnets:
            result.append(
                {
                    'docker_network_id': network['Id'],
                    'docker_network_name': network.get('Name'),
                    'docker_network_subnets': subnets

                }
            )
    return result
