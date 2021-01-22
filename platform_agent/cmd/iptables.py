import subprocess
import os

def iptables_version():
    iptables_proc = subprocess.Popen(['iptables', '-L'], stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
    text = iptables_proc.stderr.read()
    if "Warning: iptables-legacy tables present, use iptables-legacy to see them" in str(text):
        os.environ['SYNTROPY_IPTABLES'] = 'iptables-nft'
    else:
        os.environ['SYNTROPY_IPTABLES'] = 'iptables'

def iptables_create_syntropy_chain():
    try:

        # Check if already exists, if not - create
        subprocess.run([os.environ.get('SYNTROPY_IPTABLES', 'iptables'), '-N', 'SYNTROPY_CHAIN'], stderr=subprocess.DEVNULL)
        subprocess.run(
            [os.environ.get('SYNTROPY_IPTABLES', 'iptables'), '-C', 'FORWARD', '-s', '0.0.0.0/0', '-d', '0.0.0.0/0', '-j', 'SYNTROPY_CHAIN'],
            check=True,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        subprocess.run(
            [os.environ.get('SYNTROPY_IPTABLES', 'iptables'), '-I', 'FORWARD', '-s', '0.0.0.0/0', '-d', '0.0.0.0/0', '-j', 'SYNTROPY_CHAIN'],
            stderr=subprocess.DEVNULL,
            check=False
        )


def add_iptable_rules(ips: list):
    for ip in ips:
        try:
            # Check if already exists, if not - create
            subprocess.run(
                [os.environ.get('SYNTROPY_IPTABLES', 'iptables'), '-C', 'SYNTROPY_CHAIN', '-p', 'all', '-s', ip, '-j', 'ACCEPT'],
                check=True,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            subprocess.run(
                [os.environ.get('SYNTROPY_IPTABLES', 'iptables'), '-A', 'SYNTROPY_CHAIN', '-p', 'all', '-s', ip, '-j', 'ACCEPT'],
                stderr=subprocess.DEVNULL
            )


def delete_iptable_rule(ips: list):
    for ip in ips:
        subprocess.run(
            [os.environ.get('SYNTROPY_IPTABLES', 'iptables'), '-D', 'FORWARD', '-p', 'all', '-s', ip, '-j', 'ACCEPT'],
            check=False,
            stderr=subprocess.DEVNULL
        )