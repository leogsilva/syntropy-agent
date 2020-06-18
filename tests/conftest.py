from pytest import fixture


@fixture
def CONFIG_INFO():
    return 'CONFIG_INFO'


@fixture
def request_id():
    return 'TEST_01'

@fixture
def wg_int_name():
    return 'p2p_agent'

@fixture
def config_info_int_check():
    return {'agent_id': 71, 'vpn': [
        {'args': {'ifname': 'p2p_15_g8y3', 'internal_ip': '10.69.0.22/31'}, 'fn': 'create_interface'},
        {'args': {'ifname': 'mesh_111_v2t6', 'internal_ip': '10.69.0.35/31'}, 'fn': 'create_interface'},
        {'args': {'ifname': 'gw_113_d5yg', 'internal_ip': '10.69.0.56/31'}, 'fn': 'create_interface'},
        {'args': {'ifname': 'mesh_112_wnyt', 'internal_ip': '10.69.0.48/31'}, 'fn': 'create_interface'}
    ]}
