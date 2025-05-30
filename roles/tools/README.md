# Ansible Role: Tools

## Role Description

This Ansible role is designed to install a collection of command-line tools onto a target system. Currently, it supports the installation of:

1. **`code-packager`**: A utility cloned from [yohasebe/code-packager](https://github.com/yohasebe/code-packager "null"). It provides scripts (`code-packager` and `code-unpackager`) for packaging and unpackaging code, which are installed into the user's `~/.local/bin` directory.

2. **`whisper-stream`**: A tool cloned from [b08x/whisper-stream](https://github.com/b08x/whisper-stream "null"). The `whisper-stream` script is installed into the user's `~/.local/bin` directory.

The role handles cloning the respective Git repositories and placing the executable scripts into a standardized user-specific binary location.

## Requirements

### System Requirements

- **Operating System**: This role is primarily designed for Arch Linux or Arch-based distributions due to its use of the `aur` module for installing dependencies.

- **AUR Helper**: An AUR (Arch User Repository) helper (e.g., `paru`, `yay`) must be installed and configured on the target system for the user executing the playbook. The role attempts to use `paru` for `code-packager` dependencies and `auto` (which might pick `yay` or another helper) for `whisper-stream` dependencies.

- **Git**: The `git` command-line tool must be installed to clone the necessary repositories.

- **User `PATH`**: For the installed tools to be executable directly from the command line, the `~/.local/bin` directory should be included in the user's `PATH` environment variable.

### Ansible Requirements

- **Ansible Version**: `min_ansible_version: 2.1` (as specified in `meta/main.yml`).

- **Collections**: No specific collections are explicitly required beyond standard Ansible built-in modules, but the `community.general.aur` module (or a similar one providing `aur`) is implicitly needed. If not using a full Ansible installation, ensure the collection providing the `aur` module is available.

## Role Variables

The primary way to customize this role is by defining the `user` variable. The task files (`code-packager.yml`, `whisper-stream.yml`) expect this variable to have the following attributes:

- **`user.name`**: The username of the target user for whom the tools will be installed.

  - Example: `john_doe`

- **`user.group`**: The primary group of the target user.

  - Example: `users`

- **`user.home`**: The absolute path to the home directory of the target user. This is used to construct paths like `{{ user.home }}/.local/bin`.

  - Example: `/home/john_doe`

### Defaults

Currently, there are no default values set for these variables in `defaults/main.yml`. You **must** define the `user` variable when using this role.

File: `defaults/main.yml`

```yaml
# defaults file for tools
# No defaults are currently set.
# The 'user' variable must be defined by the user.
# Example structure:
# user:
#   name: your_username
#   group: your_usergroup
#   home: /home/your_username
```

### Vars

No variables are pre-defined in `vars/main.yml`.

File: `vars/main.yml`

```yaml
# vars file for tools
# No variables are pre-defined here.
```

## Dependencies

This role does not have any explicit Ansible role dependencies listed in `meta/main.yml`.

However, it has software dependencies for the tools it installs:

- **For `code-packager`**:

  - `jq`

- **For `whisper-stream`**:

  - `alsa-utils`

  - `curl`

  - `jq`

  - `sox`

  - `xclip`

  - `xsel`

These dependencies are installed using the `aur` Ansible module.

## Tasks

The role is structured with a main task file that imports tool-specific task files.

### `tasks/main.yml`

This file includes tasks for each tool based on tags:

```yaml
---
# tasks file for tools

- ansible.builtin.import_tasks:
    file: code-packager.yml
  tags: ["code-packager"]

- ansible.builtin.import_tasks:
    file: whisper-stream.yml
  tags: ["whisper-stream"]
```

You can run tasks for a specific tool by using its tag (e.g., `--tags "code-packager"`).

### `tasks/code-packager.yml`

1. **Install Dependencies**: Installs `jq` using the `aur` module (with `paru`).

2. **Clone Repository**: Clones `https://github.com/yohasebe/code-packager.git` into `/tmp/code-packager`.

3. **Move Scripts**:

    - Creates `{{ user.home }}/.local/bin` if it doesn't exist.

    - Makes `code-packager` and `code-unpackager` scripts executable.

    - Changes ownership of the scripts to `{{ user.name }}:{{ user.group }}`.

    - Moves the scripts to `{{ user.home }}/.local/bin/`.

4. **Remove Temp Folder**: Deletes `/tmp/code-packager`.

### `tasks/whisper-stream.yml`

1. **Install Dependencies**: Installs `alsa-utils`, `curl`, `jq`, `sox`, `xclip`, `xsel` using the `aur` module (with `use: auto`).

2. **Clone Repository**: Clones `https://github.com/b08x/whisper-stream.git` into `/tmp/whisper-stream`.

3. **Move Script**:

    - Creates `{{ user.home }}/.local/bin` if it doesn't exist.

    - Makes the `whisper-stream` script executable.

    - Changes ownership of the script to `{{ user.name }}:{{ user.group }}`.

    - Moves the script to `{{ user.home }}/.local/bin/whisper-stream`.

4. **Remove Temp Folder**: Deletes `/tmp/whisper-stream`.

## Customization

1. User Definition (Mandatory):

    Define the user variable in your playbook or inventory to specify the target user's details.

    ```yaml
    user:
      name: myuser
      group: mygroup
      home: /home/myuser
    ```

2. Targeting Specific Tools:

    Use Ansible tags to install only selected tools.

    - To install only `code-packager`: `ansible-playbook your_playbook.yml --tags "code-packager"`

    - To install only `whisper-stream`: `ansible-playbook your_playbook.yml --tags "whisper-stream"`

3. **AUR Helper Choice**:

    - For `code-packager`, the role explicitly tries to use `paru`. If you use a different AUR helper primarily, you might need to adjust `tasks/code-packager.yml`.

    - For `whisper-stream`, `use: auto` is specified for the `aur` module, which should automatically detect a common AUR helper.

4. Installation Path:

    The tools are hardcoded to be installed in {{ user.home }}/.local/bin/. If you need a different installation path, you will need to modify the ansible.builtin.shell tasks in tasks/code-packager.yml and tasks/whisper-stream.yml.

## Example Playbook

Here's an example of how to use this role in a playbook:

```yaml
---
- hosts: arch_desktops
  become: no # The role itself handles privileges for AUR tasks via 'become: false'
             # assuming the AUR helper is configured for the user.
             # If not, you might need 'become: yes' at the play level and adjust the role.
  vars:
    user:
      name: "jane_doe"
      group: "users"
      home: "/home/jane_doe"
  roles:
    - role: tools # Or your_galaxy_username.tools if published
      # To install only specific tools, use tags in the command line
      # or define tags at the role inclusion level:
      # tags:
      #   - code-packager
```

To run this playbook for all tools:

```yaml
ansible-playbook my_playbook.yml
```

To run this playbook for only `whisper-stream`:

```yaml
ansible-playbook my_playbook.yml --tags "whisper-stream"
```

## License

The `meta/main.yml` file suggests a license (e.g., GPL-2.0-or-later, MIT). Please update it with your chosen license. The template mentions:

```yaml
license: license (GPL-2.0-or-later, MIT, etc)
```

The original `README.md` template mentioned BSD.

## Author Information

(Optional) An optional section for the role authors to include contact information, or a website.
