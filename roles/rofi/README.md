# Ansible Role: Rofi

This role installs and configures Rofi, a window switcher, application launcher, and dmenu replacement. It supports installation for both X11 (with i3) and Wayland (with Sway) environments and deploys a predefined set of configuration files, themes, and scripts.

## Requirements

- **Ansible:** Version 2.1 or higher.

- **Operating System:** Primarily designed for Arch Linux or derivatives that use `pacman` and the AUR.

- **AUR Helper:** `paru` is used for installing AUR packages. Ensure it is installed and accessible by the user Ansible connects as (for AUR tasks, `become: false` is used).

- **User Variables:** The role expects a `user` object to be defined with details about the target user for whom Rofi will be configured.

- **Window Manager Variable:** The `window_manager` variable must be set to either `i3` or `sway` to determine the correct Rofi package to install.

## Role Variables

The role uses several variables to customize the installation and configuration. Key variables are defined in `defaults/main.yml` and can be overridden in your playbook or inventory.

### Required Variables

- `window_manager`:

  - Description: Specifies the window manager environment. This determines whether to install `rofi` (for X11) or `rofi-wayland`.

  - Accepted Values: `"i3"`, `"sway"`

  - Example: `window_manager: "i3"`

- `user`:

  - Description: An object containing information about the user for whom Rofi is being configured. This is used for setting file ownership and paths.

  - Structure:

    - `name`: (String) The username (e.g., `"johndoe"`).

    - `group`: (String) The user's primary group (e.g., `"users"`).

    - `home`: (String) The absolute path to the user's home directory (e.g., `"/home/johndoe"`).

  - Example:

        ```yaml
        user:
          name: "myuser"
          group: "mygroup"
          home: "/home/myuser"
        ```

### Optional Directory Configuration Variables

These variables control how Rofi's configuration directories are created under `{{ user.home }}/.config/rofi`.

- `rofi_directory_default_location`:

  - Description: The base location where Rofi's configuration directories will be created.

  - Default: `{{ user.home }}` (effectively making the path `{{ user.home }}/.config/rofi/...`)

- `rofi_directory_default_mode`:

  - Description: Default file system permissions for the created Rofi directories.

  - Default: `"0750"`

- `rofi_directory_default_owner`:

  - Description: Default owner for the created Rofi directories.

  - Default: `{{ user.name }}`

- `rofi_directory_default_group`:

  - Description: Default group for the created Rofi directories.

  - Default: `{{ user.group }}`

- `rofi_directory_default_recurse`:

  - Description: Default value for the `recurse` parameter when creating directories.

  - Default: `false`

- `rofi_directory_definitions`:

  - Description: A list of dictionaries defining the Rofi-related directories to be created within `{{ rofi_directory_default_location }}`. You can override or extend this list to manage custom directory structures.

  - Default:

        ```yaml
        rofi_directory_definitions:
          - dest: ".config/rofi"
          - dest: ".config/rofi/colors"
          - dest: ".config/rofi/images"
          - dest: ".config/rofi/launchers"
          - dest: ".config/rofi/launchers/type-1"
          - dest: ".config/rofi/launchers/type-1/shared"
          - dest: ".config/rofi/launchers/type-4"
          - dest: ".config/rofi/launchers/type-4/shared"
          - dest: ".config/rofi/powermenu"
          - dest: ".config/rofi/scripts"
        ```

  - Each item in the list can also have `owner`, `group`, `mode`, and `recurse` attributes to override the defaults for that specific directory.

## Customization

1. **Set Required Variables:** Ensure you define `window_manager` and the `user` object in your playbook or inventory.

2. **Override Default Variables:** Change any of the `rofi_directory_default_*` variables or the `rofi_directory_definitions` list to alter where and how Rofi's configuration directories are created.

3. **Modify Rofi Configuration Templates:** This role deploys a specific set of Rofi themes and scripts from its `templates/home/.config/rofi/` directory. To change Rofi's appearance (colors, fonts, layouts) or script behavior:

    - **Option** 1 (Recommended **for minor changes):** Fork this role and modify the template files (`.j2` files) within the role's `templates` directory directly.

    - **Option 2 (For complete theme overhaul):** You can modify the `tasks/main.yml` file in your forked role to point to your own set of template files or use a different mechanism to deploy your Rofi configurations.

## Dependencies

This role has no explicit Ansible Galaxy dependencies listed in `meta/main.yml`. However, it relies on:

- `paru` for AUR package installation.

- The `aur` Ansible module (implicitly, often part of `community.general` or installable separately).

- The `community.general.pacman` Ansible module.

## Example Playbook

Here's an example of how to use this role in your Ansible playbook:

```yaml
- hosts: myarchworkstation
  become: true # General become for system tasks, but AUR tasks in the role use become: false
  vars:
    window_manager: "i3" # or "sway"
    user:
      name: "archuser"
      group: "archuser"
      home: "/home/archuser"
    # Optionally override other defaults:
    # rofi_directory_default_mode: "0755"
  roles:
    - role: your_ansible_username.rofi # Or the path to the role if stored locally
      # Example of tagging if you only want to run certain parts:
      # tags: packages
      # tags: menus
```

## Tasks Overview

The role performs the following main actions:

1. **Package Installation (`packages` tag):**

    - If `window_manager` is `i3`, installs `rofi` from AUR using `paru`.

    - If `window_manager` is `sway`, removes any existing `rofi` package and installs `rofi-wayland` from AUR using `paru`.

2. **Directory Creation:**

    - Ensures that the necessary Rofi configuration directories (defined by `rofi_directory_definitions`) exist under `{{ user.home }}/.config/rofi`.

3. **Template Synchronization (`menus` tag):**

    - Copies Rofi configuration files (`config.rasi`), themes (`*.rasi`), and utility scripts (`*.sh`) from the role's `templates` directory to `{{ user.home }}/.config/rofi/`.

## License

BSD (Placeholder, update with your chosen license if different. The original `meta/main.yml` suggested GPL-2.0-or-later, MIT, etc.)

## Author Information

This role was created by [Your Name/Organization Here].

(You can add contact information or a website if desired).
