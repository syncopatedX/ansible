# Ansible Role: Network

This role manages various aspects of network configuration on a Linux host. It supports setting up wireless connections, mDNS, network interfaces via NetworkManager or systemd-networkd, DNS resolution with systemd-resolved, and network-related systemd mount units.

## Description

The `network` role aims to provide a flexible way to configure networking components. It can:

- Install and configure `iwd` for wireless connectivity, including prompting for SSID and passphrase if not provided as variables.
- Install and configure Avahi for mDNS (Multicast DNS), allowing for easier host discovery on the local network.
- Configure network interfaces (Ethernet, WiFi, Bridges) using **NetworkManager**. This includes setting static or DHCP IP addresses, DNS, and udev rules for interface naming.
- Configure network interfaces, DNS, and mounts using **systemd-networkd** and **systemd-resolved**. This includes managing `.network`, `.netdev`, and mount unit files.
- Automatically detect wireless interfaces to conditionally apply wireless configurations.
- Handle the installation of necessary packages for the chosen network management tools (NetworkManager or systemd-networkd components).
- Manage service states (enable, start, stop, disable, mask) for relevant network daemons like `NetworkManager`, `systemd-networkd`, `systemd-resolved`, `iwd`, and `avahi-daemon`.

## Requirements

- Ansible 2.1 or higher.
- The target host should be a Linux system using systemd.
- If using AUR packages (like `iwgtk`), an AUR helper should be configured on the target Arch Linux machine, and the Ansible user should have permissions to use it (or `become: false` tasks need to be managed appropriately).

## Role Variables

The role uses several variables to customize the network configuration. Key variables are often defined in `defaults/main.yml` and can be overridden in your playbook or inventory.

| Variable                                   | Description                                                                                                                                                                                             | Primary File(s) / Context                                                                                                |
| :----------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------- |
| **General Variables** |                                                                                                                                                                                                         |                                                                                                                          |
| `packages__network`                        | A dictionary defining packages to install. Contains keys `networkd` (list of packages for `systemd-networkd` setup e.g., `android-tethering`, `iwd`) and `networkmanager` (list for `NetworkManager` e.g., `network-manager-applet`). | `network/defaults/main.yml`                                                              |
| `conn_check`                               | Configuration for NetworkManager's connectivity check. Includes `uri` (default: "<http://piholes/admin>") and `interval` (default: 120).                                    | `network/defaults/main.yml`                                                              |
| `ansible_service_mgr`                      | Specifies the service manager (default: "systemd").                                                                                                                     | `network/defaults/main.yml`                                                              |
| **systemd-networkd & systemd-resolved** | These variables are primarily used when `systemd_network_networks` is defined, triggering the systemd-networkd configuration tasks.                                        |                                                                                                                          |
| `systemd_network_confs`                    | A dictionary defining custom configurations for `systemd-networkd` (e.g., global settings in `/etc/systemd/networkd.conf.d/`). Each key becomes the filename (e.g., `key.conf`) and the value is the content. | `network/defaults/main.yml`, `network/tasks/networkd/main.yml` |
| `systemd_resolve_confs`                    | A dictionary defining custom configurations for `systemd-resolved` (e.g., `/etc/systemd/resolved.conf.d/`). Each key becomes the filename and the value is the content. | `network/defaults/main.yml`, `network/tasks/networkd/resolve.yml` |
| `systemd_network_netdevs`                  | A dictionary defining virtual network devices (`.netdev` files) for `systemd-networkd`. The key is the filename (e.g., `vlan.netdev`) and the value contains the netdev configuration. | `network/defaults/main.yml`, `network/tasks/networkd/main.yml` |
| `systemd_network_networks`                 | A dictionary defining network configurations (`.network` files) for `systemd-networkd`. The key is the filename (e.g., `ethernet.network`) and the value contains the network configuration. | `network/defaults/main.yml`, `network/tasks/networkd/main.yml`, `network/tasks/main.yml` |
| `systemd_network_copy_files`               | A list of dictionaries, each specifying `src` and `dest` to copy additional files for `systemd-networkd`.                                                         | `network/defaults/main.yml`, `network/tasks/networkd/main.yml` |
| `systemd_network_keep_existing_definitions`| Boolean, if `false` (default), a cleanup of unmanaged networkd config files is performed.                                                                            | `network/defaults/main.yml`, `network/tasks/networkd/main.yml` |
| `systemd_mounts`                           | A dictionary defining systemd mount units. The key is a descriptive name, and the value contains the mount unit configuration details, particularly `Mount.Where` which specifies the mount point. | `network/defaults/main.yml`, `network/tasks/networkd/mounts.yml`, `network/tasks/networkd/mount-unit.yml` |
| **NetworkManager Variables** | These variables are primarily used when `network_interfaces` is defined, triggering the NetworkManager configuration tasks.           |                                                                                                                          |
| `network_interfaces`                       | A list of dictionaries, each defining a network interface to be configured by NetworkManager. See example structure in "Example Playbook" section.      | `network/tasks/networkmanager/interfaces.yml`, `network/tasks/main.yml` |
| `network_interface_bridge`                 | A variable (e.g., boolean or dictionary) that triggers the NetworkManager bridge configuration tasks. If defined, interactive prompts may appear unless sub-variables are set. Sub-variables include: `old_bridge_name`, `bridge_name`, `bridge_slave`, `ipaddr`, `gateway`, `dns`, `search`, `reboot_confirmation_input`. | `network/tasks/networkmanager/main.yml`, `network/tasks/networkmanager/bridge.yml` |
| **iwd (Wireless) Variables** | Used when `has_wireless` is true (auto-detected).                                                                                                                              |                                                                                                                          |
| `wifi_ssid`                                | The SSID of the wireless network. If not provided, the role will pause and prompt for it.                                                                                       | `network/tasks/iwd.yml`                                                                      |
| `wifi_passphrase`                          | The passphrase for the wireless network. If not provided, the role will pause and prompt for it (echo off). Consider using Ansible Vault for this.                              | `network/tasks/iwd.yml`                                                                      |

### Tags

The role utilizes tags to allow for more granular execution:

- `iwd`, `wireless`: Tasks related to `iwd` and wireless setup.
- `avahi`, `dns`: Tasks related to Avahi mDNS setup. `dns` tag is also used for other DNS related tasks.
- `networkmanager`: Tasks related to NetworkManager configuration.
- `systemd-network`: Tasks related to `systemd-networkd` base configuration.
- `systemd-resolve`: Tasks related to `systemd-resolved` configuration.
- `systemd-mounts`: Tasks related to `systemd` mount units.
- `udev`: Tasks related to udev rule configuration for network interfaces.

## Dependencies

None explicitly listed in `meta/main.yml`. However, based on tasks:

- `community.general.nmcli` module is used for NetworkManager tasks.
- `community.general.pacman` module is used for installing `systemd-resolvconf` on Arch Linux.
- `aur` module (implicit, likely from a collection like `kewlfft.aur`) is used for `iwd` and `iwgtk` installation if `use: auto` is effective.

## Example Playbook / Use Case Scenarios

### 1. Basic Setup with NetworkManager (DHCP Ethernet, mDNS)

```yaml
- hosts: servers
  become: yes
  roles:
    - role: network
  vars:
    network_interfaces:
      - ifname: "eth0"
        conn_name: "Wired connection 1"
        mac: "YOUR_ETH0_MAC_ADDRESS" # Important for udev rule if used
        type: "ethernet"
        method4: "auto"
        autoconnect: true
        state: "present"
