from platform_agent.agent_api import AgentApi

import mock


@mock.patch('platform_agent.agent_api.WgConf.clear_interfaces')
@mock.patch('platform_agent.agent_api.WgConf.create_interface')
def test_config_info(patch_create_interface, patch_clear_interfaces, config_info_int_check, CONFIG_INFO, request_id):
    agent_api = AgentApi(mock.MagicMock(), prod_mode=False)
    agent_api.call(CONFIG_INFO, config_info_int_check, request_id)
    assert patch_clear_interfaces.called
    assert patch_create_interface.call_count == len(config_info_int_check['vpn'])
    assert patch_clear_interfaces.call_args[0][0] == config_info_int_check['vpn']
