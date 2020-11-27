# Manual
You can install NOIA using pip. If you don't have pip installed, you can download it from here.
Pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes. https://pypi.org/project/pip/
#### 1. Install NOIA agent
`pip3 install platform-agent`
#### 2. Create/Edit /etc/systemd/system/noia-agent.service.d/10-vars.conf file 
##### NOIA_API_KEY (Required)
```ini
[Service]

# Required parameters

Environment=NOIA_API_KEY=YOUR_API_KEY

# Optional parameters

Environment=NOIA_CONTROLLER_URL=controller-prod-platform-agents.noia.network
Environment=NOIA_ALLOWED_IPS=[{"10.0.44.0/24":"oracle_vpc"},{"192.168.111.2/32":"internal"}]

# If using docker , NOIA_NETWORK_API=docker would allow agent to access docker networks for information.

Environment=NOIA_NETWORK_API=none

Environment=NOIA_AGENT_NAME=Azure EU gateway

# Select one of providers from the list - https://noia-network.readme.io/docs/start-noia-agent#section-variables

Environment=NOIA_PROVIDER=1

Environment=NOIA_LAT=40.14
Environment=NOIA_LON=-74.21

Environment=NOIA_SERVICES_STATUS=false
```
### Create Systemd service

```ini
[Unit]
Description=NOIA Platform Agent
After=multi-user.target

[Service]
Type=simple
Restart=always
RestartSec=1
ExecStart=/usr/local/bin/noia_agent run

[Install]
WantedBy=multi-user.target

```
