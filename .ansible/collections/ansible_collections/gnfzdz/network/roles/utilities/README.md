# Ansible Role - gnfzdz.network.utilities

Install various networking related utilities:
- iproute (ip, ss, bridge)
- ldns (drill)
- netcat
- curl
- wget

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_utilities_packages` | A list of network utility packages to install.  | list of str | distribution specific list of packages
