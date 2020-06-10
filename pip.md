# Manual
You can install NOIA using pip. If you don’t have pip installed, you can download it from here.
Pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes. https://pypi.org/project/pip/
#### 1. Install NOIA agent
`pip3 install platform-agent`
#### 2. Create/Edit /etc/noia-agent/config.ini file 
##### Add API Key and NOIA API url (Required)
```ini
[SECRETS]
api_key = z99CuiZnMhe2qtz4LLX43Gbho5Zu9G8oAoWRY68WdMTVB9GzuMY2HNn667A752EA
```
##### List of Networks to join (Optional)
If `network_ids = 0` or not present the Agent will not join any network when deployed
```ini
[CONFIG]
network_ids = Lpy3zq2ehdVZehZvoRFur4tV,U7FrPST7bV6NQGyBdhHyiebg
```
##### Metadata (Optional)
```ini
[INFO]
NOIA_NETWORK_API = docker
name = Azure EU gateway 
country = Germany 
city = Frankfurt 

#Select one of the categories from the list or default will be assigned 
# 'zIoT', 'Server','none' 
category = IoT 

#Select one of providers from the list or default will be assigned 
#'AWS', 'DigtialOcean', 'Microsoft Azure', 'Rackspace', 'Alibaba Cloud', 
#'Google Cloud Platform', 'Oracle Cloud', 'VMware', 'IBM Cloud', 'Vultr'. 

provider = Microsoft Azure 
lat = 40.14 
lon = -74.21
```
##### Tags (Optional)
categorize your end-points. #You can use more than one tag.  e.g. eu-group,fr-group
```ini
[INFO]
tags = Tag1,Tag2
```
#### Start a NOIA Agent
`/usr/local/bin/noia_agent run` or `noia_agent run`
You can install NOIA using pip. If you don’t have pip installed, you can download it from here.


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
