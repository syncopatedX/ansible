# Ansible Role - gnfzdz.network.iwd

Install and configure IWD (iNet Wireless Daemon) including option configuration of known networks and gui support components.

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_iwd_config` | A dict representing the contents of the iwd main configuration file. Top level keys represent ini sections, while the nested dicts key and values represent ini options and values respectively. See `man 5 iwd.config` for all available configuration options. | dict | { 'General': { 'EnableNetworkConfiguration': true, 'AddressRandomization': 'network', 'AddressRandomizationRange': 'full' } }
`network_iwd_enabled` | Flag deteterming whether the iwd service should be started and enabled | bool | true if a wireless device is present else false
`network_iwd_default_config` | The default value of `network_iwd_config`. Provided as a separate variable for use in cases where you simply want to extend the role defaults. | dict | See `network_iwd_config`
`network_iwd_default_network_security_type` | The default security type of the configured network. This value must be one of 'open', 'psk' or '8021x'. | str | 'psk'
`network_iwd_default_network_config` | The default configuration for an iwd network configured by the role. This is merged into the network specific configuration. See `man 5 iwd.network` for all available configuration options. | dict | { 'Settings': { 'AlwaysRandomizeAddress': True }}
`network_iwd_networks_auto` | A list of known network configurations to configure as part of role execution. | list of dict | a list containing the contents of all variables matching `/^network_iwd_network_.*$/`


An individual network configuration may contain the below fields

Variable | Description | Type | Required
-------- | ----------- | -------- | --------
`ssid` | The networks name/identifier | str | true
`security_type` | The network's security type. Should be one of 'open', 'psk' or '8021x' | str | false
`config` | A dict representing the contents of the network specific configuration file. Top level keys represent ini sections, while the nested dicts key and values represent ini options and values respectively. See `man 5 iwd.network` for all available configuration options. Note this dict is merged into `network_iwd_default_network_config` but with greater prescedence. | dict | false

## Examples
-------

### Main entrypoint to install/configure iwd and 3 known-networks
-------

```yaml
vars:
    network_iwd_enable: True
    network_iwd_config:
        General:
            EnableNetworkConfiguration: False
            AddressRandomization: 'network'
        Network:
            EnableIPv6: False
    network_iwd_network_home:
        ssid: 'home-sweet-home'
        config:
            IPv6:
                Enabled: True
    network_iwd_network_office:
        ssid: 'work-time'
        config:
            IPv6:
                Enabled: True
    network_iwd_network_cafe:
        ssid: 'coffee & donuts'
        security_type: 'open'
        config:
            Settings:
                AlwaysRandomizeAddress: True

tasks:
    - ansible.builtin.import_role:
        name: "gnfzdz.network.iwd"

```

### Network entrypoint to configure a single known network
-------
```yaml
- ansible.builtin.import_role:
    name: "gnfzdz.network.iwd"
    tasks_from: "network"
  vars:
    network: 
        ssid: 'home-sweet-home'
        config:
        IPv6:
            Enabled: True
```

### Gui entrypoint to add supporting functionality
-------
```yaml
- ansible.builtin.import_role:
    name: "gnfzdz.network.iwd"
    tasks_from: "gui"
```
