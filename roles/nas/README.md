# Ansible Role: NAS

This Ansible role automates the setup of Network Attached Storage (NAS) services, specifically NFS (Network File System) and Samba, on target Linux servers.

## Table of Contents

- [Ansible Role: NAS](#ansible-role-nas)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Role Variables](#role-variables)
    - [Service Activation](#service-activation)
    - [NFS Configuration](#nfs-configuration)
    - [Directory Ownership](#directory-ownership)
    - [Firewall Configuration (Reference)](#firewall-configuration-reference)
  - [Dependencies](#dependencies)
  - [Example Playbook](#example-playbook)
    - [Inventory Example](#inventory-example)
    - [Host Variables Example](#host-variables-example)
    - [Playbook Execution](#playbook-execution)
  - [Detailed Functionality](#detailed-functionality)
    - [NFS Setup (`nfs_host: true`)](#nfs-setup-nfs_host-true)
    - [Samba Setup (`samba_host: true`)](#samba-setup-samba_host-true)
  - [Customization](#customization)
    - [Defining NFS Shares](#defining-nfs-shares)
    - [NFS Export Options](#nfs-export-options)
    - [Samba Configuration](#samba-configuration)
    - [Firewall Ports](#firewall-ports)
    - [Ownership](#ownership)
  - [Templates Required](#templates-required)
  - [Use Cases \& Network Diagrams](#use-cases--network-diagrams)
    - [Use Case 1: Simple Home NFS Server](#use-case-1-simple-home-nfs-server)
    - [Use Case 2: Samba Server for Mixed Environment](#use-case-2-samba-server-for-mixed-environment)
    - [Use Case 3: Combined NFS and Samba Server](#use-case-3-combined-nfs-and-samba-server)
  - [Testing](#testing)
  - [License](#license)
  - [Author Information](#author-information)

## Requirements

- **Ansible:** Version 2.1 or higher.
- **Supported Operating Systems:**
  - Arch Linux and its derivatives (e.g., EndeavourOS)
  - Red Hat based distributions (e.g., Fedora)
  - Debian and its derivatives (e.g., MX Linux)
- **Python Libraries:**
  - `community.general.ufw` (for UFW management on Debian/MX systems)
  - `ansible.posix.firewalld` (for firewalld management on Arch/RedHat systems)

## Role Variables

### Service Activation

These variables control which NAS services are configured.

- `nfs_host`:
  - Description: Enables or disables the NFS server configuration.
  - Type: `boolean`
  - Default: `false`
  - Example: `nfs_host: true`

- `samba_host`:
  - Description: Enables or disables the Samba server configuration.
  - Type: `boolean`
  - Default: `false`
  - Example: `samba_host: true`

### NFS Configuration

These variables are used when `nfs_host` is `true`.

- `bind_share_exports`:
  - Description: Controls how NFS shares are exposed. If `true`, the role creates directories under `/srv/exports/` and uses bind mounts to link them to the actual data directories specified by `share.nfs.parent` and `share.nfs.exports`. This is the primary supported method.
  - Type: `boolean`
  - Default: `true`

- `share`:
  - Description: A dictionary defining the NFS shares. This should typically be defined in `host_vars` or `group_vars`.
  - Type: `dict`
  - Structure:
    - `nfs`:
      - `parent`: (string, required) The absolute path to the parent directory containing the directories to be exported (e.g., `"/mnt/data"`, `"{{ user.home }}"`).
      - `exports`: (list of strings, required) A list of subdirectory names within the `parent` directory that will be exported (e.g., `["documents", "photos"]`).
  - Example:

        ```yaml
        share:
          nfs:
            parent: "/storage/shares"
            exports:
              - "public"
              - "private_archive"
        ```

### Directory Ownership

These variables define the ownership for directories created by the role (primarily for NFS shares).

- `user`:
  - Description: A dictionary defining the user and group for shared directories.
  - Type: `dict`
  - Structure:
    - `name`: (string, required) Username for the owner.
    - `group`: (string, required) Group name for the owner.
  - Example:

        ```yaml
        user:
          name: "filesharer"
          group: "filesharers"
        ```

### Firewall Configuration (Reference)

The role attempts to configure firewall rules automatically. The following variable is available in defaults but note that the `nfs.yml` task currently uses a more extensive, hardcoded list of ports for `firewalld`.

- `firewall.nfs.ports`:
  - Description: Defines default ports for various NFS-related services. This variable serves as a reference, as the current `nfs.yml` task for `firewalld` uses a more comprehensive, hardcoded list. For `ufw`, specific ports are also hardcoded.
  - Type: `dict`
  - Default:

        ```yaml
        firewall:
          nfs:
            ports:
              lockd:
                tcp: 32803
                udp: 32769
              mountd: 892
              statd: 662
              rpc: 40418 # This is a general RPC port, specific services like status/nlm might use others
        ```

## Dependencies

None explicitly listed in `meta/main.yml`.

## Example Playbook

### Inventory Example

(`inventory.ini`)

```ini
[nas_servers]
mynas ansible_host=192.168.1.100

[all:vars]
ansible_user=your_ssh_user
```

### Host Variables Example

(`host_vars/mynas.yml`)

```yaml
nfs_host: true
samba_host: true # Set to false if Samba is not needed

user:
  name: "nasuser"
  group: "nasgroup"

share:
  nfs:
    parent: "/mnt/tank/shares" # Location of your actual data
    exports:
      - "documents"
      - "photos"
      - "media"

# bind_share_exports: true # Default, explicitly set if needed
```

### Playbook Execution

1. **Create a playbook file** (e.g., `nas_setup.yml`):

    ```yaml
    ---
    - hosts: nas_servers
      become: yes
      roles:
        - role: path/to/your/nas_role # Or just 'nas' if in standard roles_path
    ```

2. **Run the playbook:**

    ```bash
    ansible-playbook -i inventory.ini nas_setup.yml
    ```

    To run for a specific host from the example README:

    ```bash
    ansible-playbook -i inventory.ini nas_setup.yml --limit tinybot
    ```

    (Assuming `tinybot` is defined in your inventory and host_vars).

## Detailed Functionality

### NFS Setup (`nfs_host: true`)

When `nfs_host` is enabled, the role performs the following actions:

1. **Creates `nobody` User and Group:** Ensures `nobody` user and group (UID/GID 65534) exist for NFS.
2. **Installs NFS Configuration Files:**
    - Templates `/etc/idmapd.conf` from `templates/etc/idmapd.conf.j2`.
    - Templates `/etc/nfs.conf` from `templates/etc/nfs.conf.j2`.
3. **Enables and Starts NFS Services:** Ensures the following services are started and enabled:
    - `nfsv4-server` (or `nfs-server` as seen in demo)
    - `nfs-mountd`
    - `nfs-idmapd`
    - `rpcbind`
4. **Configures Firewall:**
    - **Archlinux/RedHat (firewalld):** Opens a comprehensive list of TCP/UDP ports necessary for NFSv4, including 111 (rpcbind), 2049 (nfs), and ports for mountd, statd, lockd, etc. It then reloads firewalld.
    - **Debian/MX (ufw):** Allows TCP traffic on ports 111, 662, 892, 2049, 32803 and UDP traffic on ports 111, 662, 892, 32769, 32803.
5. **Manages Share Directories (if `bind_share_exports: true`):**
    - Creates the main export directory: `/srv/exports` (owner/group as per `user.name`/`user.group`).
    - Ensures the source directories (`{{ share.nfs.parent }}/{{ item }}`) exist.
    - Creates target directories within `/srv/exports` (`/srv/exports/{{ item }}`).
    - Adds bind mount entries to `/etc/fstab` to map `{{ share.nfs.parent }}/{{ item }}` to `/srv/exports/{{ item }}`.
    - Reloads `systemd` if `/etc/fstab` was changed.
    - Mounts the defined bind mounts.
6. **Sets Up NFS Exports:**
    - Templates `/etc/exports` from `templates/etc/exports.j2`. This file defines which directories are exported and with what options (e.g., client access, permissions).
    - Reloads NFS exports using `exportfs -rv` if `/etc/exports` was changed.

### Samba Setup (`samba_host: true`)

When `samba_host` is enabled, the role performs:

1. **Creates User and Group:**
    - Ensures a group named `storage` (GID 1036) exists.
    - Ensures a user named `home` (part of `storage` group, shell `/sbin/nologin`) exists.
2. **Installs Samba Configuration:**
    - Copies `/etc/samba/smb.conf` from a source file located at `files/etc/samba/smb.conf` within the role. (The task uses `ansible.builtin.copy`, so the source should be in the role's `files` directory).
3. **Configures Firewall (firewalld):**
    - Permits traffic for the `samba` service permanently.
4. **Enables and Starts Samba Service:**
    - Ensures the `samba` service (often `smbd` and `nmbd`) is started and enabled.

## Customization

### Defining NFS Shares

Modify the `share.nfs.parent` and `share.nfs.exports` variables in your `host_vars` or `group_vars` to define the directories you want to share via NFS.

- `share.nfs.parent`: The base directory on your server where the original data for shares is located.
- `share.nfs.exports`: A list of subdirectories under `parent` that will become individual NFS shares.

### NFS Export Options

The specific options for how NFS shares are exported (e.g., read/write permissions, client restrictions, `sync`/`async`, `root_squash`/`no_root_squash`) are controlled by the content of the **`templates/etc/exports.j2`** file within the role. You will need to customize this Jinja2 template to match your security and access requirements.

Example line in `exports.j2`:

```jinja
{% for export_item in share.nfs.exports %}
/srv/exports/{{ export_item }}    *(rw,sync,no_subtree_check,no_root_squash)
{% endfor %}
```

*(This is a basic example; consult NFS documentation for detailed options.)*

### Samba Configuration

Samba's behavior is almost entirely dictated by its configuration file. To customize Samba shares, permissions, and other settings:

1. Modify the **`files/etc/samba/smb.conf`** file within this Ansible role structure before running the playbook.
2. This file will be copied to `/etc/samba/smb.conf` on the target server.

### Firewall Ports

- **NFS:** The role hardcodes a list of TCP/UDP ports for `firewalld` and `ufw` in `tasks/nfs.yml`. While `defaults/main.yml` contains a `firewall.nfs.ports` variable, it's not directly used by these tasks for the full port list. If you need to change these ports, you'll likely need to modify `tasks/nfs.yml`.
- **Samba:** The role enables the predefined `samba` service in `firewalld`, which typically includes ports 137/udp, 138/udp, 139/tcp, and 445/tcp.

### Ownership

Directory ownership for NFS shares created under `/srv/exports` (and potentially the source directories under `share.nfs.parent` if the role creates them) is set using the `user.name` and `user.group` variables.

## Templates Required

This role relies on several Jinja2 templates and files that must be present in the role's directory structure:

- `templates/etc/idmapd.conf.j2`: Configuration for NFS ID mapping.
- `templates/etc/nfs.conf.j2`: General NFS daemon configuration.
- `templates/etc/exports.j2`: **Crucial for defining NFS export paths and options.**
- `files/etc/samba/smb.conf`: The Samba configuration file. (Note: `samba.yml` uses `ansible.builtin.copy`, implying this should be in the `files` directory of the role. If it were a template, it would typically end in `.j2` and be in the `templates` directory).

Ensure these files are properly configured within your role before execution.

## Use Cases & Network Diagrams

These are conceptual diagrams. Actual network topology may vary.

### Use Case 1: Simple Home NFS Server

- **Description:** A server configured to provide NFS shares (e.g., 'Media', 'Backups', 'Documents') to Linux or macOS clients on a home network.
- **Diagram:**

    ```shell
    [Linux Client 1] ----LAN----> [NAS Server (Ansible Managed)] ----accesses---> [Storage on NAS]
         ^                      (NFS Enabled)
         |
    [macOS Client] ------LAN---->
    ```

### Use Case 2: Samba Server for Mixed Environment

- **Description:** The NAS server provides shares accessible via the SMB/CIFS protocol, primarily for Windows clients, but also compatible with Linux and macOS.
- **Diagram:**

    ```shell
    [Windows Client 1] ---LAN---> [NAS Server (Ansible Managed)] ----accesses---> [Storage on NAS]
                                 (Samba Enabled)
    [Windows Client 2] ---LAN--->      ^
                                       |
    [Linux/macOS Client] --LAN--------> (using SMB/CIFS)
    ```

### Use Case 3: Combined NFS and Samba Server

- **Description:** The server is configured to offer both NFS (for Unix-like clients) and Samba (for Windows and broader compatibility) shares, potentially sharing the same backend data.
- **Diagram:**

    ```shell
    [Linux Client (NFS)] ---LAN---> [NAS Server (Ansible Managed)] ----accesses---> [Storage on NAS]
                                    (NFS & Samba Enabled)
    [Windows Client (Samba)] -LAN->      ^         ^
                                         |         |
    [macOS Client (NFS/Samba)] LAN------>          |
                                                   |
    [Other device (Samba)] ----LAN----------------->
    ```

## Testing

A basic test playbook is provided in `tests/test.yml`. This can be used as a starting point for verifying the role's functionality in a controlled environment (e.g., with Vagrant or Docker).

```yaml
---
- hosts: localhost # Or your test target
  remote_user: root # Adjust as necessary
  roles:
    - nas # Assuming 'nas' is the role name
```

## License

Specify your license here (e.g., MIT, GPL-2.0-or-later). The `meta/main.yml` suggests options like BSD-3-Clause, MIT, GPL-2.0-or-later, etc.

Example: `license (GPL-2.0-or-later)`

## Author Information

Provide your author details here.
Example from `meta/main.yml`:

- Author: your name
- Company: your company (optional)
- Role Description: your role description
- Contact: <rwpannick@gmail.com> (from demo.md)
