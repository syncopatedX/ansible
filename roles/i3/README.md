# Ansible Role: i3 Window Manager Setup

This role installs and configures the i3 window manager, i3status-rust, and various related tools and utilities on an Arch Linux-based system. It sets up configuration files from templates, allowing for customization through Ansible variables.

## Requirements

- **Operating System:** Assumed to be Arch Linux or an Arch-based distribution due to the use of AUR.

- **AUR Helper:** `paru` is used by default for installing AUR packages. Ensure `paru` (or the AUR helper specified in `aur: use:`) is installed and configured for the user running Ansible. The package installation task runs with `become: false`, so the executing user must have passwordless rights for `paru` or be ableto use it interactively if Ansible is run with TTY.

- **User Variables:** This role relies on certain user-specific variables being defined, typically through Ansible facts or other roles:

  - `user.name`: The username of the target user.

  - `user.group`: The primary group of the target user.

  - `user.home`: The home directory path of the target user (e.g., `/home/{{ user.name }}`).

  - `user.uid`: The user ID of the target user.

- **Python `python-i3ipc`:** While listed in `packages__i3`, ensure your Python environment for Ansible controller (if different from target) or target (for local actions if any) can satisfy dependencies if modules require it directly.

## Role Variables

This role uses variables to customize the i3 environment. Variables are primarily defined in `defaults/main.yml` and `vars/main.yml`. You can override these in your playbook or inventory.

### Package Management

- `packages__i3`

  - **Default Value (from `vars/main.yml`):**

        ```yaml
        - arandr
        - dex
        - dunst
        - i3-wm
        - i3status-rust
        - nitrogen-git
        - perl-anyevent-i3
        - picom
        - polybar
        - python-i3ipc
        - sxhkd
        - wmctrl
        - wmfocus
        - xob
        ```

  - **Description:** A list of packages to install for the i3 setup. This includes the window manager, status bar, notification daemon, compositor, and other utilities.

  - **Customization:** Modify this list to add, remove, or change packages. For example, you might replace `i3-wm` with `i3-gaps` or add other preferred applications.

### i3 Configuration (`i3` dictionary)

This dictionary, defined in `defaults/main.yml`, groups several i3-specific settings.

- `i3.home`

  - **Default Value:** `{{ lookup('env','HOME') }}/.config/i3` (resolves to the user's `~/.config/i3`)

  - **Description:** The base directory where i3 configuration files will be stored.

- `i3.autostart`

  - **Default Value:** `"default"`

  - **Description:** Intended to select a specific autostart configuration. Currently, the task that would use this (`autostart.j2` template) is commented out in `tasks/main.yml`. You can uncomment it and provide a corresponding `autostart.j2` template in `templates/home/.config/i3/` to manage applications that start with i3.

- `i3.assignments`

  - **Default Value:** `"default"`

  - **Description:** Intended to select a specific window assignment configuration. The task for `window_assignments.j2` is also currently commented out. If enabled, it would manage rules for assigning specific windows to workspaces.

- `i3.workspaces`

  - **Default Value:** `"default"`

  - **Description:** This variable could be used to switch between different workspace definition schemes if multiple `config.j2` templates or conditional logic for workspaces were implemented. The actual workspace definitions are managed by `__i3_workspaces`.

- `i3.keybindings`

  - **Default Value:** `"default"`

  - **Description:** Determines the set of keybindings to apply. The role uses this to template `templates/home/.config/i3/keybindings.j2`. You could potentially use this variable to switch between different keybinding template files if you create them.

- `i3.tray_output`

  - **Default Value:** `"primary"`

  - **Description:** Specifies the monitor output where the i3bar system tray should appear (e.g., "primary", "HDMI-1", "eDP-1"). This is used within the main i3 `config.j2` template.

### Workspace Definitions

- `__i3_workspaces`

  - **Default Value (from `defaults/main.yml`):**

        ```yaml
        __i3_workspaces:
          - workspace:
            id: 1
            name: " 1 "
          - workspace: { id: 2, name: " 2 " }
          # ... and so on for workspaces 3 through 9, and 0
          - workspace: { id: 0, name: " 0 " }
        ```

  - **Description:** A list of dictionaries defining i3 workspaces. Each item must have an `id` (the workspace number) and a `name` (how it appears in i3bar). This is used in `templates/home/.config/i3/config.j2` to generate workspace assignments and names.

  - **Customization:** Modify this list to change the number of workspaces, their IDs, or their display names.

### Directory Management

These variables control the creation of directories needed for i3 and related configurations.

- `i3_directory_default_mode`

  - **Default Value:** `"0750"`

  - **Description:** Default permissions for directories created by this role.

- `i3_directory_default_owner`

  - **Default Value:** `{{ user.name }}`

  - **Description:** Default owner for created directories.

- `i3_directory_default_group`

  - **Default Value:** `{{ user.group }}`

  - **Description:** Default group for created directories.

- `i3_directory_default_location`

  - **Default Value:** `{{ user.home }}` (e.g., `/home/{{ user.name }}`)

  - **Description:** The base path under which directories specified in `i3_directory_definitions` will be created.

- `i3_directory_default_recurse`

  - **Default Value:** `false`

  - **Description:** Default value for the `recurse` parameter when creating directories.

- `i3_directory_definitions`

  - **Default Value (from `defaults/main.yml`):**

        ```yaml
        i3_directory_definitions:
          - dest: ".config/i3"
          - dest: ".config/i3/modes"
          - dest: ".config/i3status-rust/themes"
        ```

  - **Description:** A list of directories to ensure exist. Paths are relative to `i3_directory_default_location`. Each item can be a string (path) or a dictionary specifying `dest`, `owner`, `group`, `mode`, `recurse` to override defaults for that specific entry.

  - **Customization:** Add new directories or modify existing ones as needed for your configuration.

### Terminal Emulators

- `terminal`

  - **Default Value:** `terminator`

  - **Description:** The primary terminal emulator to be launched by i3's default keybinding (usually Mod+Enter). This value is used in the `templates/home/.config/i3/keybindings.j2` template.

  - **Customization:** Change to your preferred terminal emulator (e.g., `alacritty`, `kitty`, `st`, `xfce4-terminal`).

- `terminal_alt`

  - **Default Value:** `urxvt`

  - **Description:** An alternative terminal emulator. Its usage depends on how it's incorporated into the i3 keybindings or scripts.

  - **Customization:** Change to another preferred terminal emulator.

### User Information (Expected as input)

- `user.name`: Username (e.g., `myuser`)

- `user.group`: User's primary group (e.g., `myuser` or `users`)

- `user.home`: User's home directory (e.g., `/home/myuser`)

- `user.uid`: User's numerical ID (e.g., `1000`)

These are typically provided by Ansible facts (`ansible_user_id` for name, `ansible_user_uid`, `ansible_user_gid`, `ansible_user_dir`) or can be set explicitly in your inventory or playbook. The role uses them for setting file ownership and paths.

## Tasks Overview

The role performs the following main actions:

1. **Install Packages:** Installs i3-wm and related packages listed in `packages__i3` using an AUR helper (default `paru`).

2. **Create Directories:** Ensures necessary configuration directories exist (e.g., `~/.config/i3`, `~/.config/i3status-rust/themes`) based on `i3_directory_definitions`.

3. **Set `.dmrc`:** Creates or updates `~/.dmrc` to set i3 as the default session for display managers like LightDM.

4. **Deploy i3status-rust Configuration:** Templates configuration files for i3status-rust:

    - `~/.config/i3status-rust/config.toml`

    - `~/.config/i3status-rust/themes/syncopated.toml`

5. **Deploy i3 Configuration:** Templates core i3 configuration files:

    - `~/.config/i3/config` (main configuration)

    - `~/.config/i3/modes/resize` (resize mode keybindings)

    - `~/.config/i3/keybindings` (general keybindings)

    - `~/.config/i3/appearance` (fonts, colors)

    - `~/.config/i3/window_behavior` (floating windows, focus behavior)

    - Note: `window_assignments` and `autostart` templates are present in the loop but commented out in the default `tasks/main.yml`.

6. **Update `/etc/environment`:** Copies a predefined `etc/environment` file to `/etc/environment`. This requires `become: true`.

## Handlers

- `Reload i3`: This handler is triggered when i3 configuration files are changed. It attempts to reload i3 in place using `i3-msg` -s /run/user/{{ `user.uid }}/i3/ipc-socket.* reload`.

## Dependencies

This role has no explicit Ansible Galaxy role dependencies listed in `meta/main.yml`. However, it implicitly depends on:

- A working AUR helper (e.g., `paru`).

- The target system being Arch Linux or compatible.

## Example Playbook

Here's an example of how to use this role in your playbook:

```yaml
- hosts: workstation
  vars:
    user:
      name: "your_username" # Replace with the actual username
      home: "/home/your_username" # Replace with the actual home directory
      uid: "1000" # Replace with the actual UID
      group: "your_username" # Replace with the actual group
    
    # Example: Customize the terminal
    terminal: "alacritty"
    
    # Example: Customize packages
    packages__i3:
      - i3-gaps # Using i3-gaps instead of i3-wm
      - rofi
      - dunst
      - i3status-rust
      - nitrogen-git
      - picom
      - python-i3ipc
      - sxhkd # If you want to manage hotkeys with sxhkd separately
      - lxappearance # For GTK theming
      - flameshot # For screenshots

  roles:
    - role: your_username.i3 # Or the path to the role if not in a standard location
      # If your role is named 'i3' and in a 'roles/' directory:
      # - role: i3 
```

## Customization

To customize the i3 setup:

1. **Override Variables:** The primary way to customize is by overriding the default variables in your Ansible inventory, group variables, host variables, or directly in your playbook (as shown in the example above).

2. **Modify Templates:** For more advanced changes beyond what variables allow, you can fork the role and modify the Jinja2 templates located in the `templates/` directory.

    - i3 main config: `templates/home/.config/i3/config.j2`

    - i3 keybindings: `templates/home/.config/i3/keybindings.j2`

    - i3 appearance: `templates/home/.config/i3/appearance.j2`

    - i3status-rust config: `templates/home/.config/i3status-rust/config.toml.j2`

3. **Add/Remove Tasks:** You can also fork the role and modify `tasks/main.yml` to add or remove steps in the setup process.

## License

MIT (or specify the license chosen in `meta/main.yml`)

## Author Information

This role was created by [Your Name/Organization].

(Update meta/main.yml with appropriate author details).
