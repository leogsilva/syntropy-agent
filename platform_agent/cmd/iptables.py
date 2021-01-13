import subprocess


def iptables_create_syntropy_chain():
    try:

        # Check if already exists, if not - create
        subprocess.run(['iptables', '-N', 'SYNTROPY_CHAIN'], stderr=subprocess.DEVNULL)
        subprocess.run(
            ['iptables', '-C', 'FORWARD', '-s', '0.0.0.0/0', '-d', '0.0.0.0/0', '-j', 'SYNTROPY_CHAIN'],
            check=True,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        subprocess.run(
            ['iptables', '-I', 'FORWARD', '-s', '0.0.0.0/0', '-d', '0.0.0.0/0', '-j', 'SYNTROPY_CHAIN'],
            stderr=subprocess.DEVNULL,
            check=False
        )


def add_iptable_rules(ips: list):
    for ip in ips:
        try:
            # Check if already exists, if not - create
            subprocess.run(
                ['iptables', '-C', 'SYNTROPY_CHAIN', '-p', 'all', '-s', ip, '-j', 'ACCEPT'],
                check=True,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            subprocess.run(
                ['iptables', '-A', 'SYNTROPY_CHAIN', '-p', 'all', '-s', ip, '-j', 'ACCEPT'],
                stderr=subprocess.DEVNULL
            )


def delete_iptable_rule(ips: list):
    for ip in ips:
        subprocess.run(
            ['iptables', '-D', 'FORWARD', '-p', 'all', '-s', ip, '-j', 'ACCEPT'],
            check=False,
            stderr=subprocess.DEVNULL
        )

