import docker


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


def format_container_result(containers):
    docker_client = docker.from_env()
    networks = docker_client.networks()
    conts = {}
    for network in networks:
        for k, v in network['Containers'].items():
            if conts.get(k) and conts[k].get('IPv4Address') and conts[k]['IPv4Address'] != v['IPv4Address']:
                conts[k]['IPv4Address'].extend(v['IPv4Address'])
                conts[k]['network_names'].extend(network['Name'])
                continue
            conts[k] = v
            conts[k]['IPv4Address'] = [conts[k].get('IPv4Address')]
            conts[k]['network_names'] = [network.get('Name')]
    result = []
    for container in containers:

        ports = {'udp': [], 'tcp': []}
        for port in container.get('Ports', []):
            private_port = port.get('PrivatePort')
            public_port = port.get('PublicPort')
            type = port.get('Type')
            if not type:
                continue
            if private_port:
                ports[type].append(private_port)
            if public_port:
                ports[type].append(public_port)
        container_info = conts.get(container['Id'])
        if container_info:
            result.append(
                {
                    'agent_container_id': container['Id'],
                    'agent_container_name': container_info.get('Name'),
                    'agent_container_ips': container_info.get('IPv4Address'),
                    'agent_container_networks': container_info.get('network_names'),
                    'agent_container_ports': ports,
                    'agent_container_state': container.get('State'),
                    'agent_container_uptime': container.get('Status'),
                }
            )
    return result
