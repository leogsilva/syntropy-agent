# Docker-Compose
```yaml
version: '2'

services:
  portainer:
    image: portainer/agent
    restart: always
    networks:
      - noia
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/lib/docker/volumes:/var/lib/docker/volumes
  noia-agent:
    image: noia/agent:prod
    container_name: noia-agent
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - NOIA_API_KEY=my-random-api-key
      - NOIA_NETWORK_API=docker
    restart: always
    network_mode: "host"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    devices:
      - "/dev/net/tun:/dev/net/tun"
networks:
    noia:
        ipam:
            config:
                - subnet: 192.168.150.0/24

volumes:
  portainer_data:
```

##### You must select non overlapping subnet for network
```yaml
networks:
    noia:
        ipam:
            config:
                - subnet: 192.168.150.0/24  #  Replace your subnet here
```

##### Add API Key and NOIA API url (Required)
```yaml
environment:
  - NOIA_API_KEY=z99CuiZnMhe2qtz4LLX43Gbho5Zu9G8oAoWRY68WdMTVB9GzuMY2HNn667A752EA
  - NOIA_NETWORK_API=docker
```
##### List of Networks to join (Optional)
If `network_ids = 0` or not present the Agent will not join any network when deployed
```yaml
environment:
  - NOIA_NETWORK_IDS=Lpy3zq2ehdVZehZvoRFur4tV,U7FrPST7bV6NQGyBdhHyiebg
```
##### Metadata (Optional)
```yaml
environment:
  - NOIA_NETWORK_IDS=Lpy3zq2ehdVZehZvoRFur4tV,U7FrPST7bV6NQGyBdhHyiebg
  - NOIA_AGENT_NAME=Azure EU gateway 

# Select one of providers from the list - https://noia-network.readme.io/docs/start-noia-agent#section-variables
  - NOIA_PROVIDER=1
  - NOIA_LAT=40.14 
  - NOIA_LON=-74.21

  - NOIA_ALLOWED_IPS='[{"127.0.24.0/24""myvpc"},{"192.168.24.0/32":"vpc"}]'
  - NOIA_SERVICES_STATUS='false'

```
##### Tags (Optional)
categorize your end-points. #You can use more than one tag.
e.g. eu-group,fr-group
```yaml
environment:
  - NOIA_TAGS=Tag1,Tag2
```
