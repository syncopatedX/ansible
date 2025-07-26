# Ansible Role: Libvirt on Fedora

This role installs and configures a libvirt virtualization environment on Fedora systems.

## Features

- Installs the standard Fedora virtualization package group (`@virtualization`).
- Configures `/etc/libvirt/libvirtd.conf` for group-based access.
- Configures `/etc/qemu/bridge.conf`.
- Optionally disables `lvmetad` for better libvirt storage pool integration.
- Adds specified users to the `libvirt` group for passwordless management access.
- Ensures the `libvirtd` service is enabled and running.

## Role Variables

Variables are defined in `defaults/main.yml`.

- `libvirt_packages`: The list of packages to install. Defaults to `["@virtualization"]`.
- `libvirt_service`: The name of the libvirt service. Defaults to `libvirtd.service`.
- `libvirt_service_enabled`: Whether the service should be enabled. Defaults to `true`.
- `libvirt_users`: A list of users to add to the `libvirt` group. Defaults to `[]`.
- `libvirt_unix_sock_group`: The group for the libvirt UNIX socket. Defaults to `libvirt`.
- `libvirt_unix_sock_rw_perms`: Permissions for the read-write socket. Defaults to `0770`.
- `libvirt_auth_unix_rw`: Authentication method for the read-write socket. Defaults to `none`.
- `libvirt_configure_lvm`: Whether to disable `lvmetad`. Defaults to `true`.

## Example Playbook

```yaml
---
- hosts: virtualization_hosts
  become: true
  roles:
    - role: libvirt
      vars:
        libvirt_users:
          - your_user
```

## License

MIT

## Author Information

Created by B08X.