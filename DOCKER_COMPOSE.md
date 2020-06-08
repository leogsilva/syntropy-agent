# Docker-Compose
```yaml
version: '2'
services:
  portainer:
    image: portainer/portainer
    command: -H unix:///var/run/docker.sock
    restart: always
    networks:
      - noia
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
  noia-agent:
    image: noia/agent
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - NOIA_API_KEY=yuor api key
      - NOIA_NETWORK_API=docker
    restart: always
    network_mode: "host"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
networks:
    noia:
        ipam:
            config:
                  # Select non overlapping subnet
                - subnet: 192.168.150.0/24
volumes:
  portainer_data:
```
#### Tags (Optional)
categorize your end-points. #You can use more than one tag.
e.g. eu-group,fr-group
```yaml
    environment:
      - NOIA_TAGS=Tag1,Tag2
```