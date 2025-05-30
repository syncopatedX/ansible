
# Ansible Role: networkmanager

## Description

This role manages network configurations on compatible Linux systems using **NetworkManager**. It is designed to:

* Establish NetworkManager as the primary network configuration tool by disabling services like `systemd-networkd`.
* Configure various network interface types, including **ethernet**, **Wi-Fi**, and **bridge** interfaces.
* Set static IP addresses, DHCP configurations, DNS, and routing.
* Create `udev` rules for persistent network interface naming based on MAC addresses.
* Manage the `/etc/hosts` file.

The role is structured to allow detailed configuration of network interfaces through Ansible variables.

## Important Note on Current Role Structure

As of the current structure of the provided files:

* The main entry point for the role, `tasks/main.yml`, by default, only executes a debug task and the task for setting the `/etc/hosts` file.
* The core networking functionalities (disabling `systemd-networkd`, configuring NetworkManager, and setting up interfaces via `tasks/networkmanager.yml` and `tasks/interfaces.yml`) are **not automatically executed**.
* To enable the full functionality of this role, you will likely need to ensure that `tasks/networkmanager.yml` is included in the execution flow, for example, by uncommenting or adding an `import_tasks` or `include_tasks` directive for `networkmanager.yml` within `tasks/main.yml`.

Example modification to `tasks/main.yml`:

```yaml
---
# tasks/main.yml
- name: Networking Tasks
  debug:
    msg: "Starting networking tasks"

- import_tasks: networkmanager.yml
  tags: ['networkmanager']

- name: Set hosts files
  template:
    src: etc/hosts.j2
    dest: /etc/hosts
    owner: root
    group: root
    mode: '0644'
    backup: True
  when: etc_hosts is defined
  tags: ['dns']
````

## Requirements

* **Ansible**: Version 2.1 or higher.
* **Target System**: A systemd-based Linux distribution where NetworkManager is the desired network management tool.
* **Collections**: The `community.general` Ansible collection must be installed (`ansible-galaxy collection install community.general`) as the role uses the `community.general.nmcli` module.
* **Privileges**: Root or sufficient `sudo` privileges are required on the target hosts to manage network services, configurations, and udev rules.

## Role Variables

This role uses several variables to customize network configurations. The primary variables are:

### `network_interfaces`

A list of dictionaries, where each dictionary defines a network interface to be configured. This is the most critical variable for customizing network setups.

* **Type**: `list` of `dict`
* **Default**: `undefined` (The tasks in `interfaces.yml` will only run if this variable is defined).

**Structure of each item in `network_interfaces`:**

|   |   |   |   |   |
|---|---|---|---|---|
|**Parameter**|**Type**|**Required**|**Description**|**Example**|
|`ifname`|`string`|Yes|Target interface name.|`"eth0"`, `"wlan0"`, `"br0"`|
|`conn_name`|`string`|Yes|NetworkManager connection name. Often the same as `ifname`.|`"Wired connection 1"`, `"MyWiFi"`|
|`type`|`string`|Yes|Type of interface. Supported: `ethernet`, `wifi`, `bridge`.|`"ethernet"`|
|`mac`|`string`|No|MAC address. Used for udev rules and specific ethernet/wifi configurations.|`"00:11:22:AA:BB:CC"`|
|`method4`|`string`|No|IPv4 configuration method: `manual` (static), `auto` (DHCP), `disabled` (deactivates connection).|`"manual"`|
|`ip4`|`string`|No|IPv4 address and prefix (e.g., `192.168.1.10/24`). Required for `method4: manual`.|`"192.168.1.50/24"`|
|`gw4`|`string`|No|IPv4 gateway. Usually required for `method4: manual` unless it's an isolated network.|`"192.168.1.1"`|
|`dns4`|`list`|No|List of IPv4 DNS servers.|`["8.8.8.8", "1.1.1.1"]`|
|`dns4_search`|`list`|No|List of DNS search domains.|`["example.com", "internal.example.com"]`|
|`autoconnect`|`boolean`|No|Whether the connection should automatically connect. Defaults to `yes` via `nmcli`.|`yes`|
|`state`|`string`|No|State of the connection: `present` (default), `absent`.|`"present"`|
|`ssid`|`string`|Wifi|SSID for `type: wifi` connections.|`"MyHomeNetwork"`|
|`assigned_address`|`string`|Wifi|Cloned MAC address for `type: wifi`.|`"00:DE:AD:BE:EF:00"`|
|`bridge`|`string`|BridgeSlave|Master bridge interface name (e.g., `br0`) for `type: ethernet` interfaces acting as bridge slaves.|`"br0"`|

**Note on `udev` rules:** The role includes a task to set `udev` rules using the `etc/udev/rules.d/10-network.rules.j2` template. This task iterates through all items in `network_interfaces` to potentially pin interface names based on MAC addresses (`item.mac` and `item.ifname`).

### `etc_hosts`

Defines the content for the `/etc/hosts` file. The role uses the `etc/hosts.j2` template to generate this file. The exact structure required for `etc_hosts` depends on the content of this template (which is not provided in the input). Typically, it could be a multi-line string or a dictionary/list of host entries.

* **Type**: `string` or `dict`/`list` (depending on `etc/hosts.j2` template)
* **Default**: `undefined` (The task will only run if this variable is defined).
* **Example (as a string)**:YAML

    ```yaml
    etc_hosts: |
      127.0.0.1 localhost
      192.168.1.10 server1.example.com server1
      192.168.1.11 server2.example.com server2
    ```

### `packages` (from `defaults/main.yml`)

* **Type**: `list`
* **Default**: `["network-manager-applet"]`
* **Note**: Currently, no task within this role uses this variable to install these packages. You would need to add a package installation task if desired.

### `conn_check` (from `defaults/main.yml`)

Variables intended for NetworkManager's connectivity check.

* **Type**: `dict`
* **Default**:YAML

    ```yaml
    conn_check:
      uri: "http://pihole/admin"
      interval: 120
    ```

* **Parameters**:
  * `uri` (string): The URI that NetworkManager will check to determine connectivity.
  * `interval` (integer): The interval in seconds between connectivity checks.
* **Note**: The task `Ensure networkmanager connection check is enabled` in `tasks/networkmanager.yml` currently hardcodes the connectivity check configuration (`[connectivity]\nenabled=true`) into `/etc/NetworkManager/conf.d/20-connectivity.conf` and **does not utilize these `conn_check.uri` or `conn_check.interval` variables**.

## Tasks Overview

The role is organized into several task files:

* **`tasks/main.yml`**:

  * The default entry point for the role.
  * Currently includes a debug message and a task to configure `/etc/hosts` using the `etc/hosts.j2` template (if `etc_hosts` is defined).
  * **Crucially, the import of `networkmanager.yml` (which contains the main network setup logic) is commented out by default.**
* **`tasks/networkmanager.yml`**: (Must be invoked, e.g., from `tasks/main.yml`)

  * Disables the `systemd-networkd` service to prevent conflicts with NetworkManager.
  * Creates a configuration file (`/etc/NetworkManager/conf.d/20-connectivity.conf`) to enable NetworkManager's connectivity check (hardcoded to `enabled=true`).
  * Ensures the `NetworkManager` service is enabled and started.
  * Ensures the `NetworkManager-dispatcher.service` is enabled and started.
  * Includes `tasks/interfaces.yml` if the `network_interfaces` variable is defined.
* **`tasks/interfaces.yml`**: (Invoked by `tasks/networkmanager.yml`)

  * Prints host network variables (`item.ifname` from `network_interfaces`).
  * Sets `udev` rules for network interface naming using the `etc/udev/rules.d/10-network.rules.j2` template, iterating over `network_interfaces`.
  * Manages various types of NetworkManager connections using the `community.general.nmcli` module:
    * Adds Ethernet devices (static IP).
    * Adds Wi-Fi devices (static IP or DHCP).
    * Adds "audio subnet" devices (ethernet without a gateway).
    * Adds bridge devices.
    * Adds Ethernet devices as bridge slaves.
    * Deactivates specified Ethernet or Wi-Fi devices (`method4: disabled`).
  * Ensures the `NetworkManager` service is enabled and restarted after interface configurations.

## Handlers

The role defines the following handlers in `handlers/main.yml`:

* **`Refresh host facts`**: Triggers `ansible.builtin.setup` to refresh Ansible facts for the host.
* **`Reload udev rules`**: Executes `/sbin/udevadm control --reload-rules` to apply new udev rules. This can be notified by tasks that modify udev rules.

## Dependencies

* None listed in `meta/main.yml`.

## Example Playbook

YAML

```yaml
- hosts: all
  become: yes
  vars:
    network_interfaces:
      - ifname: "eth0"
        conn_name: "Wired connection eth0"
        type: "ethernet"
        method4: "manual"
        ip4: "192.168.1.100/24"
        gw4: "192.168.1.1"
        dns4: ["192.168.1.1", "8.8.8.8"]
        dns4_search: ["mydomain.local"]
        autoconnect: yes
        state: "present"
        mac: "00:1A:2B:3C:4D:5E" # Important for udev rule if matching by MAC

      - ifname: "wlan0"
        conn_name: "MyOfficeWiFi"
        type: "wifi"
        method4: "auto" # DHCP
        ssid: "OfficeNetworkSSID"
        autoconnect: yes
        state: "present"
        mac: "00:AA:BB:CC:DD:EE"

      - ifname: "eth1" # Interface to be deactivated
        conn_name: "eth1_disabled"
        type: "ethernet"
        method4: "disabled"
        state: "present" # Connection profile exists but is inactive
        mac: "00:11:22:33:44:55"

    etc_hosts: |
      127.0.0.1 localhost
      {{ ansible_default_ipv4.address | default('127.0.0.1') }} {{ ansible_fqdn | default(ansible_hostname) }} {{ ansible_hostname }}
      10.0.0.5 appserver.mydomain.local appserver
      10.0.0.6 dbserver.mydomain.local dbserver

  roles:
    - your_username.networkmanager # Or just 'networkmanager' if in a standard roles path
```

**Note**: Ensure that `tasks/main.yml` in the role is configured to call `tasks/networkmanager.yml` for the above playbook to apply full network configurations.

## How to Customize

1. **Modify `tasks/main.yml`**:

    * As highlighted in the "Important Note" section, ensure `tasks/networkmanager.yml` is included from `tasks/main.yml` to activate the core networking logic.
2. **Define `network_interfaces`**:

    * This is the primary way to customize network settings. Populate the `network_interfaces` list in your playbook vars, host vars, or group vars.
    * **Static Ethernet Example**:YAML

        ```yaml
        network_interfaces:
          - ifname: "eno1"
            conn_name: "Static Eno1"
            type: "ethernet"
            method4: "manual"
            ip4: "10.10.0.50/16"
            gw4: "10.10.0.1"
            dns4: ["10.10.0.1"]
            mac: "YOUR_ENO1_MAC_ADDRESS" # For udev rule
        ```

    * **DHCP WiFi Example**:YAML

        ```yaml
        network_interfaces:
          - ifname: "wlp2s0"
            conn_name: "Company Guest WiFi"
            type: "wifi"
            method4: "auto"
            ssid: "GuestWiFiSSID"
            mac: "YOUR_WLAN_MAC_ADDRESS" # For udev rule / identification
        ```

    * **Bridge Example**:YAML

        ```yaml
        network_interfaces:
          # Bridge Interface
          - ifname: "br0"
            conn_name: "Bridge br0"
            type: "bridge"
            method4: "manual"
            ip4: "192.168.5.1/24"
            # No gateway for the bridge itself if it's just a layer 2 bridge for VMs on the same subnet
          # Slave interface 1
          - ifname: "eth1"
            conn_name: "br0-slave-eth1"
            type: "ethernet" # This interface becomes part of the bridge
            bridge: "br0"    # Master bridge name
            method4: "manual" # Often manual with no IP, or settings inherited
            state: "present"
            mac: "YOUR_ETH1_MAC_ADDRESS"
        ```

3. **Define `etc_hosts`**:

    * Provide the desired content for `/etc/hosts` via the `etc_hosts` variable. The format depends on your `etc/hosts.j2` template.
4. **Customize Default Variables (Optional)**:

    * You can override variables from `defaults/main.yml` (like `packages` or `conn_check`) in your inventory or playbook, though be aware of the current implementation notes (e.g., `packages` not being installed, `conn_check` vars not used by the connectivity task).
5. **Templates**:

    * If you need to change how udev rules are generated or how `/etc/hosts` is formatted, you will need to modify the Jinja2 templates used by the role:
        * `templates/etc/udev/rules.d/10-network.rules.j2`
        * `templates/etc/hosts.j2`
    * (Note: The content of these templates was not provided, so their exact behavior is assumed based on typical usage.)

## License

BSD

## Author Information

your name (Update with actual author details)

(Based on meta/main.yml)
