# Ansible Role - gnfzdz.network.systemd_networkd_units

Create and configure systemd-network links, netdevs and networks

## Variables
-------

### Main entrypoint variables

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_systemd_networkd_links_auto` | A list of link configuration objects | list of dict | a list containing the contents of all variables matching `/^network_networkd_link_.*$/`
`network_systemd_networkd_netdevs_auto` | A list of netdev configuration objects | list of dict | a list containing the contents of all variables matching `/^network_networkd_netdev_.*$/`
`network_systemd_networkd_networks_auto` | A list of networks configuration objects | list of dict | a list containing the contents of all variables matching `/^network_networkd_network_.*$/`


### Link/Netdev/Network configuration structure

All of link, netdev and network configuration objects have the below fields

Variable | Description | Type | Required |Default
-------- | ----------- | -------- | -------- | --------
`label` | A descriptive label used in the unit filename | str | True | N/A
`priority` | A numeric priority used as a prefix for the filename | int | False | 50
`ini` | A dict representing ini data to insert in the unit file | dict | True | N/A

### Ini configuration structure

Ini configuration data is a dict where top level keys correspond to section names. The value is either a dict in the case of a single section wit that name or an array of dict if the section is repeated. The keys of each section correspond to option names while the values are either a single literal value (string/int/boolean) or an array of literals if the option is repeated. Optionally, a single '#' key may be added to the section dict providing a leading comment.

```yaml

netdev:
    label: vpn
    priority: 99
    ini:
        NetDev:
            Name: "wg0"
            Kind: "wireguard"
        WireGuard:
            ListenPort: 51820
            PrivateKey: "{{ vault_wireguard_private_key }}"
        WireGuardPeer:
        - '#': 'peer1.example.org'
          PublicKey: "{{ vault_wireguard_peer1_public_key }}"
          AllowedIPs: "10.0.0.101/24"
        - '#': 'peer2.example.org'
          PublicKey: "{{ vault_wireguard_peer2_public_key }}"
          AllowedIPs: "10.0.0.102/24"
```


```ini
[NetDev]
Name=wg0
Kind=wireguard

[WireGuard]
ListenPort=51820
PrivateKey={{ vault_wireguard_private_key }}

# peer1.example.org
[WireGuardPeer]
PublicKey={{ vault_wireguard_peer1_public_key }}
AllowedIPs=10.0.0.101/24

# peer2.example.org
[WireGuardPeer]
PublicKey={{ vault_wireguard_peer2_public_key }}
AllowedIPs=10.0.0.102/24
```
