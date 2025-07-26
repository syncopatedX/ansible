# Ansible Role: Docker on Fedora

This Ansible role installs and configures Docker Engine on Fedora systems. It handles repository setup, Docker installation, and provides options for advanced daemon configuration and user management.

## Role Variables

The role utilizes several variables to customize its behavior, defined in `defaults/main.yml`.

- `docker_version`: Specifies a version of Docker CE to install (e.g., `"3:28.3.2-1.fc41"`). If empty, the latest version is installed.
- `docker_packages`: A list of core Docker packages to install.
- `docker_gpg_key_url`: URL for the Docker GPG key.
- `docker_service_name`: The name of the Docker systemd service (default: `docker.service`).
- `docker_service_enabled`: Whether to enable the Docker service on boot (default: `true`).
- `docker_users`: A list of users to add to the `docker` group. **Warning**: This grants root-equivalent privileges. Use with caution. Default is an empty list.
- `docker_daemon_config`: A dictionary of key-value pairs to configure `/etc/docker/daemon.json`.
- `docker_remove_conflicting_packages`: Whether to remove potentially conflicting packages like `podman-docker` (default: `true`).

## Dependencies

- Requires a Fedora target system.
- `dnf-plugins-core` is installed by the role.

## Example Playbook

Here's a basic example of how to use this role in a playbook:

```yaml
---
- hosts: fedora_servers
  become: true
  roles:
    - role: docker
      vars:
        # Example: Add 'devuser' to the docker group (use with caution)
        docker_users:
          - devuser

        # Example: Apply a hardened configuration to the daemon
        docker_daemon_config:
          log-driver: "journald"
          icc: false
          userns-remap: "default"
          live-restore: true
          no-new-privileges: true
```

## License

MIT

## Author Information

This role was created by B08X.