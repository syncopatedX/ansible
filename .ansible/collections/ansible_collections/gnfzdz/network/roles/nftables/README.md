# Ansible Role - gnfzdz.network.nftables

Install nftables user space utilities and iptables compatability

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_nftables_packages` | A list of packages to install for nftables userspace support | list of str | A distribution specific list of packages
`network_nftables_service_enabled` | A flag controlling whether nftables rules should be loaded automatically on system start. | bool | True
