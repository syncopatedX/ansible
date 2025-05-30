# Ansible Role - gnfzdz.network.wireguard

Install wireguard userspace utilities and create/configure wireguard networks using systemd-network

NOTE: Variables and data structure for this role are very likely to change in a future release

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_wireguard_vpns_auto` | A list of vpn configuration objects | list of dict | a list containing the contents of all variables matching `/^network_wireguard_vpn_.*$/`


A vpn configuration object supports the below fields

Variable | Description | Type | Required | Default
-------- | ----------- | -------- | --------
`device_name` | The name of the wireguard network device to create for this VPN | str | True | N/A
`address` | A static IPv4 address to assign this host within the network 
`private_key` | A private key unique to this host used for authentication/encryption of VPN traffic | True | N/A
`description` | An brief summary of the network's purpose used when displaying it | str | False | N/A
`port` | The port where wireguard will listen for incoming VPN traffic | int | False | 51820
`route_metric` | The route metric used to determine priority of traffic to this wireguard network device | int | 0
`activation_policy` | Manages the policy for how/when networkd will manage the VPN | str | False | up
`forward` | A flag controlling with ip forwarding/masquerading is allowed for traffic from this network | bool | False | False
`peers` | A list of peer configuration objects | list of dict | True | []


A peer configuration object supports the below fields

Variable | Description | Type | Required | Default
-------- | ----------- | -------- | --------
`public_key` | The public key used for authentication/encryption of VPN traffic | True | N/A
`allowed_ips` | A list of ip addresses (with CIDR masks) specifiying the allowed source/destination of traffic to/from this peer | list of str | False | []
`endpoint` | An ip/hostname and port where the peer is listening for vpn traffic. If not initially set, it will be saved after a connection is received from the peer. | False | N/A
