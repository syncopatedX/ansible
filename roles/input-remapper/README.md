# Ansible Role: input-remapper

This role installs and configures `input-remapper`, a tool for remapping input device events (keyboard, mouse, etc.) on Linux. It handles the installation of `input-remapper-git` from the AUR, synchronizes user-defined presets, and enables the necessary systemd service.

## Requirements

- **Target System:** This role is designed for Arch Linux or Arch-based distributions.

- **AUR Helper:** `paru` must be installed and configured on the target system for installing `input-remapper-git`. The installation task runs with `become: false`, so `paru` should be usable by the remote Ansible user.

- **rsync:** The `rsync` utility must be installed on both the Ansible control node and the managed hosts for the preset synchronization task.

- **User Variables:** The role requires specific user-related variables to be defined (see Role Variables section).

## Role Variables

The following variables need to be defined by the user when applying this role. They are crucial for the correct synchronization of presets and setting file permissions.

- `user`: A dictionary containing user-specific information for the target system.

  - `name`: (Required) The username of the user for whom `input-remapper` presets will be configured.

    - Example: `jdoe`

  - `home`: (Required) The absolute path to the user's home directory on the target system.

    - Example: `/home/jdoe`

  - `group`: (Required) The primary group of the user on the target system.

    - Example: `jdoe` or `users`

**Example of defining `user` variable (e.g., in host_vars or group_vars):**

```yaml
user:
  name: myuser
  home: /home/myuser
  group: myuser
```

## Dependencies

This role has no external Ansible Galaxy role dependencies.

## Role Tasks

The role performs the following main tasks:

1. **Install input-remapper:**

    - Installs `input-remapper-git` from the Arch User Repository (AUR) using `paru`.

    - This task is tagged with `packages`.

    - It attempts to rescue with a debug message if the installation fails.

2. **Ensure input-remapper preset synchronization:**

    - Ensures the destination directory `{{ user.home }}/.config/input-remapper-2/presets/` exists with the correct ownership and permissions (`0755`).

    - Synchronizes presets from a source directory `home/.config/input-remapper/presets/` (relative to the playbook or role path on the control node) to the user's configuration directory on the target machine.

        - **Source Path Note:** You need to create a directory structure `home/.config/input-remapper/presets/` within your Ansible project (e.g., alongside your playbook or inside this role's directory if you intend to bundle default presets) and populate it with your desired `.json` preset files.

        - The `ansible.posix.synchronize` module is used with options to ensure checksums, update existing files, and set correct ownership (`{{ user.name }}:{{ user.group }}`).

    - It attempts to rescue with a debug message if synchronization fails.

3. **Enable input-remapper service:**

    - Enables the `input-remapper` systemd service to start on boot.

    - Errors are ignored during check mode (`ansible_check_mode`).

## Example Playbook

Here's an example of how to use this role in a playbook:

```yaml
---
- hosts: workstations
  become: true # Most tasks in a typical setup might need sudo, though specific tasks in this role override it.
  vars:
    user:
      name: johndoe
      home: /home/johndoe
      group: users
  roles:
    - role: your_username.input-remapper # Or the local path to the role if not from Galaxy
      tags:
        - input-remapper
```

**To run this playbook:**

1. Ensure you have a directory structure like `your_playbook_directory/home/.config/input-remapper/presets/` containing your preset files (e.g., `my_custom_keyboard.json`).

2. Execute the playbook: `ansible-playbook your_playbook.yml`

## Local Preset Source Structure

When using the preset synchronization feature, you should have your presets stored locally on the Ansible control machine. The `synchronize` task expects the source path to be `home/.config/input-remapper/presets/`.

For example, if your playbook `my_playbook.yml` is in `/ansible/playbooks/`, you should place your presets in `/ansible/playbooks/home/.config/input-remapper/presets/`.

```shell
/ansible/playbooks/
├── my_playbook.yml
├── home/
│   └── .config/
│       └── input-remapper/
│           └── presets/
│               ├── preset1.json
│               └── preset2.json
└── roles/
    └── your_username.input-remapper/  (or path to this role)
        ├── tasks/
        │   └── main.yml
        └── ... (other role files)
```

If you bundle the presets _within_ the role itself, the source path in `tasks/main.yml` (`src: home/.config/input-remapper/presets/`) would look for this directory structure _inside_ the `input-remapper` role directory.

## License

BSD (Based on the original template, please update `meta/main.yml` with the correct SPDX license identifier if different).

## Author Information

This role was created by [Your Name/Organization].

(Update meta/main.yml with actual author details).

## Development Notes

- **Handlers:** The `handlers/main.yml` file is currently empty. Handlers can be added if specific actions need to be triggered by `notify` directives in tasks (e.g., restarting a service only if its configuration changed).

- **Defaults/Vars:** The `defaults/main.yml` and `vars/main.yml` files are currently empty. Default values for variables could be provided in `defaults/main.yml` if applicable.

- **Testing:** A basic test playbook is provided in `tests/test.yml`.
