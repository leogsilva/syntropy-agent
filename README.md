[TOC]

---

#### [Latest NOIA Agent Docs](https://docs.noia.network/docs/start-noia-agent) 
- https://docs.noia.network/docs/start-noia-agent
#### Prerequisites

* Wireguard kernel module is installed and loaded:
```bash
lsmod | grep wireguard
```

* Optional:  Docker is installed and running: 
```sh
docker system info
```
---
#### Limitations

* Docker network subnets can't overlap.
* 10.69.0.0/16 is used for internal Wireguard network

#### Steps
----
##### 1. Login to [https://platform.noia.network](https://platform.noia.network) 
---
##### 2. Create API key (Settings > API keys)

---

##### 3. Install NOIA Agent

Possible Docker Container versions:

Stable:  ```noia/agent:stable```

Development:  ```noia/agent:devel``` or ```noia/agent:latest```  


###### With Docker 

```bash
docker run --network="host" --restart=on-failure:10 \ 
--cap-add=NET_ADMIN --cap-add=SYS_MODULE \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
--device /dev/net/tun:/dev/net/tun \
--name=noia-agent \
-e NOIA_API_KEY='z99CuiZnMhe2qtz4LLX43Gbho5Zu9G8oAoWRY68WdMTVB9GzuMY2HNn667A752EA' \
-e NOIA_NETWORK_API='docker' \
-d noia/agent:stable
```
Check agent logs:

```docker logs noia-agent```

More information:     [https://docs.noia.network/docs/start-noia-agent#install-with-docker](https://docs.noia.network/docs/start-noia-agent#install-with-docker)

---


###### With Docker-compose


> With Portainer agent:

```bash
curl  https://gitlab.com/noia-public/platform_agent/-/raw/master/docker-compose/na-pa.yml \
-o docker-compose.yaml
```

> Without portainer agent:

```bash
curl  https://gitlab.com/noia-public/platform_agent/-/raw/master/docker-compose/noia-agent.yaml \
-o docker-compose.yaml
```

Edit ```docker-compose.yaml``` file and edit these environment variables:

```yaml
NOIA_API_KEY= your_api_key
```

Start containers:

```bash
docker-compose up -d
```

Check agent logs:
```bash
docker logs noia-agent
```

P.S. NOIA Agent will ignore the default docker network, you will  need to create a separate network with different subnets on different hosts. Also, subnet 10.69.0.0/16 is used by our agent.

More information:

[https://docs.noia.network/docs/start-noia-agent#install-as-docker-compose](https://docs.noia.network/docs/start-noia-agent#install-as-docker-compose)

---


###### With pip 

```bash
pip3 install platform-agent
```

Download systemd service file:

```bash
curl https://gitlab.com/noia-public/platform_agent/-/raw/master/systemd/noia-agent.service -o /etc/systemd/system/noia-agent.service
```

Create noia-agent directory:
```bash
mkdir /etc/systemd/system/noia-agent.service.d/
chmod -R 600 /etc/systemd/system/noia-agent.service.d/
```
Download settings file:
```bash
curl https://gitlab.com/noia-public/platform_agent/-/raw/master/systemd/10-vars.conf -o /etc/systemd/system/noia-agent.service.d/10-vars.conf
```

Edit settings file ```/etc/systemd/system/noia-agent.service.d/10-vars.conf``` and change these settings:

```ini
[Service]
# Required parameters
Environment=NOIA_API_KEY=YOUR_API_KEY
# Optional parameters
Environment=NOIA_CONTROLLER_URL=controller-prod-platform-agents.noia.network
Environment=NOIA_ALLOWED_IPS=[{"10.0.44.0/24":"oracle_vpc"},{"192.168.111.2/32":"internal"}]
#If using docker , NOIA_NETWORK_API=docker would allow agent to access docker networks for information.
Environment=NOIA_NETWORK_API=none
Environment="NOIA_AGENT_NAME=Azure EU gateway"

# Select one of providers from the list - https://noia-network.readme.io/docs/start-noia-agent#section-variables
Environment="NOIA_PROVIDER=1"

Environment=NOIA_LAT=40.14
Environment=NOIA_LON=-74.21
Environment=NOIA_TAGS=Tag1,Tag2
Environment=NOIA_SERVICES_STATUS=false
```

```bash
systemctl  daemon-reload
```

```bash
systemctl enable --now noia-agent
```

Check if service is running:
```bash
systemctl status noia-agent
```

More information: [https://docs.noia.network/docs/start-noia-agent#install-with-pip](https://docs.noia.network/docs/start-noia-agent#install-with-pip)

---