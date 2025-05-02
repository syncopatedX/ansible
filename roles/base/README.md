# Role Name: base

## Description

This role performs essential base system configuration tasks, primarily targeting Arch Linux systems. It handles:

* **User Setup:** Creates a primary user based on environment variables or specified parameters, configures groups, home directory, shell, and sudo access.
* **Package Management:** Installs a comprehensive set of base packages (utilities, development tools, libraries, etc.) using the default package manager. It also configures `reflector` for optimizing mirror lists and sets up GPG keyservers. Includes tasks for `paru` (AUR helper).
* **Repository Configuration:** Manages system repositories (details inferred from `repos.yml`).
* **System Services:** Configures `sudo`, `updatedb`, and potentially `rc.local`.
* **Theme Configuration:** Sets the Zsh theme.

## Requirements

* **Ansible:** Version 2.1 or higher.
* **Operating System:** Assumed to be Arch Linux or a derivative (due to `pacman`, `reflector`, `paru`).
* **Privileges:** Requires root privileges to install packages and modify system configuration.

## Role Variables

### User Configuration (`defaults/main.yml`)

These variables control the primary user setup. Defaults are often derived from the environment running Ansible.

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `user.name` | Username | `{{ lookup('env','USER') }}` |
| `user.group` | Primary group | `{{ lookup('env','USER') }}` |
| `user.uid` | User ID | `1000` |
| `user.gid` | Group ID | `1000` |
| `user.home` | Home directory path | `{{ lookup('env','HOME') }}` |
| `user.shell` | Default shell | `{{ lookup('env','SHELL') }}` |
| `user.secondary_groups` | Comma-separated list of secondary groups | `"video,audio,input"` |
| `user.realname` | User's real name | `""` |
| `user.sudoers` | Grant sudo privileges if `true` | `true` |
| `user.workspace` | Path to user's workspace | `""` |
| `user.email` | User's email address | `""` |
| `user.gpg` | User's GPG key ID | `""` |
| `use_etc_skel` | Whether to use `/etc/skel` when creating the user's home directory | `false` |
| `zsh_theme` | The Zsh theme to apply | `strug` |

### Package Configuration (`vars/main.yml`)

These variables control package installation and related settings.

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `packages__reflector_args` | Arguments passed to the `reflector` command for mirror list generation | ```--latest 200 --sort rate --protocol http --protocol https --threads {{ ansible_facts.processor_vcpus }} --save /etc/pacman.d/mirrorlist``` |
| `packages__gpg_keyserver` | The GPG keyserver to use | `keyserver.ubuntu.com` |
| `packages__gpg_conf` | Configuration content for GPG | ```keyserver {{ packages__gpg_keyserver }}``` |
| `packages__base` | A list of essential packages to be installed by the role | See `vars/main.yml` for the complete default list |

## Dependencies

None.

## Example Playbook

```yaml
- hosts: arch_servers
  become: yes
  roles:
    - role: base
      vars:
        user:
          name: johndoe
          group: users
          uid: 1001
          gid: 100
          realname: "John Doe"
          email: "john.doe@example.com"
          secondary_groups: "wheel,video,audio,storage"
        zsh_theme: agnoster
```

## License

BSD

## Author Information

An optional section for the role authors to include contact information, or a website.
