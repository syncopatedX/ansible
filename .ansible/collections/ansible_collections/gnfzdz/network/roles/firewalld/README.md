# Ansible Role - gnfzdz.network.firewalld

Install, configure and enable firewalld and create/configure firewalld zones

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_firewalld_service_enabled` | A flag controlling whether firewalld should be currently started and started automatically on reboot | bool | True
`network_firewalld_service_packages` | A list of packages to install for Firewalld support | list of str | A distribution specific list of packages
`network_firewalld_zones_auto` | A list of zone configuration objects | list of dict | a list containing the contents of all variables matching `/^network_firewalld_zone_.*$/`

Each zone configuration object may have the below fields

Variable | Description | Type | Required
-------- | ----------- | -------- | --------
`name` | The name of the zone | str | Yes
`target` | The default target for incoming traffic that doesn't match another rule Should be one of 'ACCEPT', '%%REJECT%%', 'DROP' or 'default' | str | No
`forward` | Enables intrazone forwarding of traffic between interfaces | bool | No
`masquerade` | Enables masquerading | bool | No
`description` | Provides an explanation for the use case and behavior of the zone | str | No

## Examples
-------

### Main entrypoint to install/configure firewalld and 1 zone
-------

```yaml
vars:
  network_firewalld_zone_vpn:
    name: vpn
    target: default
    forward: True
    masquerade: True
    description: "Traffic within wireguard VPN"

tasks:
    - ansible.builtin.import_role:
        name: "gnfzdz.network.firewalld"

```

### Zone entrypoint to configure a single zone
-------
```yaml
- ansible.builtin.import_role:
    name: "gnfzdz.network.firewalld"
    tasks_from: "zone"
  vars:
    zone:
        name: "scratch"
        target: "default"
        forward: False
        masquerade: False
        description: "Zone for temporary local development resources"
```

### Gui entrypoint to add supporting functionality
-------
```yaml
- ansible.builtin.import_role:
    name: "gnfzdz.network.firewalld"
    tasks_from: "gui"
```
