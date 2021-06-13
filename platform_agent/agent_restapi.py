import json
import logging
import os
import traceback

import syntropy_sdk as sdk
from syntropy_sdk.exceptions import ApiException
from syntropy_sdk.utils import *

logger = logging.getLogger()


class AgentRestApi:

    def __init__(self, host, api_key):
        self.api_key = api_key
        self.host = host


    def login(self):
        config = sdk.Configuration()
        config.host = self.host
        config.api_key["Authorization"] = sdk.utils.login_with_access_token(self.host,self.api_key)
        self.api = sdk.ApiClient(config)
        self.platform_api = sdk.PlatformApi(self.api)     

    def get_network_info(self, agentId, netId):
        api_response = []
        try:
            self.login()
            api_response = WithRetry(self.platform_api.platform_network_info)(netId)
        except:
            traceback.print_exc()
            pass
        if len(api_response):
            data = api_response['data']
            logger.debug(f"[RESTAPI] api_response  = |{data}|")
            k = [ x['agent']['agent_tags'] for x in data['network_agents'] if x['agent_id'] == agentId]
            if len(k):
                flat_list = [item for sublist in k for item in sublist]
                logger.debug(f"[RESTAPI] found network info for {agentId}  = |{flat_list}|")
                submariner  = {}
                if len(flat_list):
                    for tag in flat_list:
                        if tag['agent_tag_name'].startswith('pod_cidr'):
                            submariner["pod_cidr"] = tag['agent_tag_name'].split(':')[1]
                        elif tag['agent_tag_name'].startswith('service_cidr'):
                            submariner["service_cidr"] = tag['agent_tag_name'].split(':')[1]
                        elif tag['agent_tag_name'].startswith('global_ip'):
                            submariner["global_ip"] =  tag['agent_tag_name'].split(':')[1]
                        submariner["type"] = tag['agent_tag_name']
                return submariner
        return {}

# >>> api_response = platform_api.platform_network_info(1400)
# >>> pprint(api_response)
# {'data': {'agent_connections': [{'agent_1': {'agent_id': 2687,
#                                              'agent_name': 'u2',
#                                              'agent_public_ipv4': '192.168.121.55',
#                                              'agent_type': 'Linux'},
#                                  'agent_1_id': 2687,
#                                  'agent_2': {'agent_id': 2688,
#                                              'agent_name': 'u3',
#                                              'agent_public_ipv4': '192.168.121.12',
#                                              'agent_type': 'Linux'},
#                                  'agent_2_id': 2688,
#                                  'agent_connection_id': 30502,
#                                  'agent_connection_status': 'CONNECTED',
#                                  'agent_connection_status_reason': None}],
#           'agent_groups': [],
#           'network': {'network_created_at': '2021-05-17T22:11:00.688',
#                       'network_id': 1400,
#                       'network_key': 'RQiLCrbb3fDfAYW7AjaGpJ3TdiooGjH8',
#                       'network_metadata': {'network_created_by': 'UI',
#                                            'network_updated_by': 'UI'},
#                       'network_name': 'test',
#                       'network_updated_at': '2021-06-09T00:09:40.326',
#                       'user_id': 1889},
#           'network_agents': [{'agent': {'agent_id': 2687,
#                                         'agent_is_online': True,
#                                         'agent_name': 'u2',
#                                         'agent_provider_id': None,
#                                         'agent_public_ipv4': '192.168.121.55',
#                                         'agent_tags': [{'agent_tag_id': 411,
#                                                         'agent_tag_name': 'pod_cidr:10.2.0.0/16'},
#                                                        {'agent_tag_id': 412,
#                                                         'agent_tag_name': 'service_cidr:100.2.0.0/16'},
#                                                        {'agent_tag_id': 413,
#                                                         'agent_tag_name': 'submariner'}],
#                                         'agent_type': 'Linux'},
#                               'agent_id': 2687,
#                               'network_agent_coord_x': 377.439358251301,
#                               'network_agent_coord_y': 494.7860624343625},
#                              {'agent': {'agent_id': 2688,
#                                         'agent_is_online': True,
#                                         'agent_name': 'u3',
#                                         'agent_provider_id': None,
#                                         'agent_public_ipv4': '192.168.121.12',
#                                         'agent_tags': [],
#                                         'agent_type': 'Linux'},
#                               'agent_id': 2688,
#                               'network_agent_coord_x': 1021.5238934549973,
#                               'network_agent_coord_y': 154.8509146843046}]}}
