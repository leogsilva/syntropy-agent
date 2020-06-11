#!/bin/bash
yum update -y
yum install python3-pip -y
pip3 install platform-agent
yum install https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm -y
yum --enablerepo=elrepo-kernel install kernel-ml -y
grub2-mkconfig -o /boot/grub2/grub.cfg
grub2-set-default 0
echo wireguard >> /etc/modules-load.d/wireguard.conf
curl https://bitbucket.org/noianetwork-team/platform-agent/raw/master/systemd/noia-agent.service \
-o /etc/systemd/system/noia-agent.service
mkdir /etc/systemd/system/noia-agent.service.d/
echo NOIA_API_KEY=change_me >> /etc/systemd/system/noia-agent.service.d/10-vars.conf
systemctl daemon-reload
systemctl enable noia-agent
firewall-cmd --permanent --zone=public --add-port=1024-65535/udp
reboot
