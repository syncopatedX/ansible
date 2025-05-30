# Ansible Collection - gnfzdz.network

A collection of roles to support in setting up the system's networking primarily built around systemd-networkd.

## Roles


Name | Description
-------- | -----------
[gnfzdz.network.autoconfigure](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/all/README.md) | A meta role automatically applying all configuration within this collection
[gnfzdz.network.bluetooth](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/bluetooth/README.md) | Install/configure bluez and supporting utilities for bluetooth support
[gnfzdz.network.firewalld](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/firewalld/README.md) |   FirewallD installation and base configuration
[gnfzdz.network.iwd](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/iwd/README.md) |   Install and configure IWD (iNet Wireless Daemon)
[gnfzdz.network.systemd_networkd](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/systemd_networkd/README.md) |   Install, configure and enable systemd-networkd
[gnfzdz.network.systemd_networkd_dispatcher](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/systemd_networkd_dispatcher/README.md) |   Install, configure and enable systemd-networkd dispatcher
[gnfzdz.network.systemd_networkd_units](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/systemd_networkd_units/README.md) |   Create and configure systemd-network links, netdevs and networks
[gnfzdz.network.nftables](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/nftables/README.md) |   Install nftables user space utilities and iptables compatability
[gnfzdz.network.openssh](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/openssh/README.md) |   Install, configure and enable OpenSSH daemon
[gnfzdz.network.systemd_resolved](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/systemd_resolved/README.md) |   Install, configure and enable systemd-resolved
[gnfzdz.network.wireguard](https://gitlab.com/gnfzdz/gnfzdz.network/-/blob/main/roles/wireguard/README.md) |   Use systemd-network and wireguard to create and configure virtual private network(s)
