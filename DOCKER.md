# Docker
```docker run --network="host" --restart=on-failure:10 --cap-add=NET_ADMIN --cap-add=SYS_MODULE -v /var/run/docker.sock:/var/run/docker.sock:ro --device /dev/net/tun:/dev/net/tun --name=noia-agent -e NOIA_API_KEY='z99CuiZnMhe2qtz4LLX43Gbho5Zu9G8oAoWRY68WdMTVB9GzuMY2HNn667A752EA' -e NOIA_CONTROLLER_URL='app-controller-platform-agents.noia.network' -e NOIA_NETWORK_API='docker' -d noia/agent:prod```
#### Add API Key and NOIA API url (Required)
```ini
-e NOIA_API_KEY='z99CuiZnMhe2qtz4LLX43Gbho5Zu9G8oAoWRY68WdMTVB9GzuMY2HNn667A752EA'
```
#### List of networks to join. `network_ids = 0 `  (Optional)
`-e NETWORK_IDS='Lpy3zq2ehdVZehZvoRFur4tV,U7FrPST7bV6NQGyBdhHyiebg'`
#### Metadata (Optional)
```ini
-e NOIA_NETWORK_API='docker'
-e NOIA_AGENT_NAME='Azure EU gateway '

# Select one of providers from the list - https://noia-network.readme.io/docs/start-noia-agent#section-variables
-e NOIA_PROVIDER ='1

-e NOIA_LAT='40.14'
-e NOIA_LON='-74.21'

#You can manually add allowed ips
-e NOIA_ALLOWED_IPS='[{"127.0.24.0/24":"myvpc"},{"192.168.24.0/32":"vpc"}]'
-e NOIA_SERVICES_STATUS='false'
```
##### Tags (Optional)
categorize your end-points. #You can use more than one tag.  e.g. eu-group,fr-group
```ini
-e NOIA_TAGS='Tag1,Tag2'
```
