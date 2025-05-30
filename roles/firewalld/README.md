# Ansible Role: firewalld

## Role Name

`firewalld`

## Description

This role manages the `firewalld` service on Linux systems. It ensures that `firewalld` is enabled and started, and it configures firewall rules to permit traffic for specified services and ports.

## Requirements

- `firewalld` must be installed on the target host(s). This role does not install `firewalld` itself but manages its configuration.

- The target host(s) must be using `systemd` as `firewalld` is managed as a `systemd` service by this role.

## Role Variables

The role uses the following variables, which can be found in `defaults/main.yml`:

### `rules`

This is a dictionary defining the firewall rules. Currently, it only contains one key:

- **`allowed`**: A list of ports and their protocols to be permanently enabled in `firewalld`.

  - **Default value** (from `defaults/main.yml`):

        ```yaml
        rules:
          allowed:
            - 1900/udp
            - 1935/tcp
            - 4000/tcp
            # ... (and many others)
            - 50924/udp
            - 55311/udp
        ```

  - **Purpose**: This list specifies custom ports that should be opened. Each item should be in the format `port/protocol` (e.g., `8080/tcp`, `53/udp`).

  - **Customization**: You can override this list in your playbook or inventory to specify exactly which ports you want to open. If you want to add to the default list, you'll need to redefine the entire list including the defaults you wish to keep.

### Implicitly Managed Services

The role also explicitly enables the following common services by default within the `tasks/main.yml` file:

- `ntp`

- `rsyncd`

- `ssh`

These are not controlled by the `rules.allowed` variable but are hardcoded in the tasks. If you need to change these, you would need to modify the `tasks/main.yml` file or manage them separately.

## Dependencies

This role has no external dependencies on other Ansible Galaxy roles.

## Handlers

The role includes the following handler:

- **`reload firewalld`**: This handler is triggered when any firewall rule (service or port) is changed. It executes `firewall-cmd --reload` to apply the changes without interrupting existing connections.

    _Defined in `handlers/main.yml`_:

    ```yaml
    - name: reload firewalld
      shell: "firewall-cmd --reload"
      ignore_errors: "{{ ansible_check_mode }}"
    ```

## Example Playbook

Here's an example of how to use this role in a playbook.

### Basic Usage (using defaults)

This will apply the default set of allowed ports and services.

```yaml
- hosts: all
  become: yes
  roles:
    - your_username.firewalld # Or simply 'firewalld' if in a local roles path
```

### Customizing Allowed Ports

This example overrides the default `rules.allowed` list to open only specific TCP ports and keeps the default SSH, NTP, and Rsyncd services.

```yaml
- hosts: webservers
  become: yes
  vars:
    rules:
      allowed:
        - 80/tcp   # HTTP
        - 443/tcp  # HTTPS
        - 8080/tcp # Custom web app
  roles:
    - your_username.firewalld # Or simply 'firewalld'
```

### Adding to Default Allowed Ports (Manual Merge)

If you want to keep the default ports and add your own, you would need to define the full list. Ansible doesn't automatically merge lists in this way for role defaults.

A more advanced way to merge would be to load the defaults explicitly using `include_vars` and then combine them, but for simplicity, redefining is often easier for this type of variable:

```yaml
- hosts: myservers
  become: yes
  vars:
    rules:
      allowed:
        # Default ports you want to keep
        - 1900/udp
        - 1935/tcp
        # ... (include other defaults as needed)
        # Your custom additions
        - 9000/tcp
        - 9001/udp
  roles:
    - your_username.firewalld # Or simply 'firewalld'
```

## Tasks Overview

The main tasks performed by this role (from `tasks/main.yml`) are:

1. **Enable and start firewalld**: Ensures the `firewalld` service is running and enabled at boot using the `ansible.builtin.systemd` module.

2. **Permit traffic to common services**: Uses the `ansible.posix.firewalld` module to enable `ntp`, `rsyncd`, and `ssh` services permanently. This task notifies the `reload firewalld` handler.

3. **Permit traffic to custom ports**: Iterates through the `rules.allowed` list and uses the `ansible.posix.firewalld` module to enable each specified port/protocol combination permanently. This task also notifies the `reload firewalld` handler.

## License

As specified in meta/main.yml. If not set, consider using a common open-source license like MIT or BSD-3-Clause.

(The meta/main.yml provided has: license: license (GPL-2.0-or-later, MIT, etc))

## Author Information

This role was created by [Your Name/Organization].

(The meta/main.yml provided has: author: your name, company: your company (optional))
