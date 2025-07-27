# Ansible Role: x

## Description

This role configures an X Window System environment on Arch Linux-based systems. It handles the installation of the Xorg server, essential X11 utilities, and common desktop environment components like a hotkey daemon (SXHKD), a compositor (Picom), and a notification daemon (Dunst). It also sets up XDG base directories and user-specific X server configuration files.

## Requirements

- **Operating System:** Arch Linux or an Arch-based distribution.

- **AUR Helper:** `paru` is used for installing AUR packages. It must be installed and configured on the target system for tasks that run with `become: false`.

- **User Account:** The role assumes a non-root user account (specified via the `user` variable) exists on the target system, for whom the X environment will be configured.

## Role Variables

This role uses several variables to customize the X environment setup. Some are defined in `defaults/main.yml` (lowest precedence, easily overridden), some in `vars/main.yml` (higher precedence, typically for role internal logic or important defaults), and some are expected to be passed in during playbook execution.

### User Configuration (Expected Variables)

These variables **must be defined** in your playbook or inventory to specify the user for whom the X environment is being configured.

- `user`: A dictionary containing user-specific information.

  - `user.name`: (String) The username of the target user (e.g., `john_doe`).

  - `user.home`: (String) The absolute path to the user's home directory (e.g., `/home/{{ user.name }}`).

  - `user.group`: (String) The primary group of the user (e.g., `john_doe`).

  - `user.uid`: (String or Integer) The UID of the user. This is used, for example, when setting up the `xdg-user-dirs-update.service`.

    **Example:**

    ```yaml
    user:
      name: myuser
      home: /home/myuser
      group: myuser
      uid: 1000
    ```

### Package Management

- `packages__x11`: (List of strings)

  - **Defined in:** `vars/main.yml`

  - **Purpose:** Specifies the list of Xorg server components, X11 utilities, fonts, and related packages (like Dunst, Picom) to be installed.

  - **Default:** A comprehensive list is provided in `vars/main.yml`.

  - **Customization:** While variables in `vars/main.yml` have high precedence, you can override this list by passing `packages__x11` as an extra variable (`-e`) or directly in your playbook with higher precedence. However, for minor modifications, it's often better to fork the role or manage additional packages outside this specific list.

    _(Note:_ `defaults/main.yml` contains a similar variable `xorg__packages`, but the role tasks _currently use `packages__x11` from `vars/main.yml` for package installation.)_

### X Configuration Defaults

- `x`: (Dictionary)

  - **Defined in:** `defaults/main.yml`

  - `x.autostart`: (String)

    - **Default:** `"default"`

    - **Purpose:** This variable is intended to control autostart behavior within the X session. Its specific effect depends on how it's used within the Jinja2 template files (e.g., `home/.xinitrc.j2`, `home/.xprofile.j2`). You would need to inspect these template files to see how `"default"` or other values influence the startup applications or scripts.

    - **Customization:** Override in your playbook or inventory:

            ```yaml
            x:
              autostart: "minimal" # Or any other value your templates support
            ```

### Optional Behavior Flags

- `disable_vblank`: (Boolean)

  - **Defined in:** Not defined by default (task skipped).

  - **Purpose:** If set to `true`, the role will create a `~/.drirc` file to disable VBlank. This can sometimes help with screen tearing or improve performance for certain graphics drivers/applications.

  - **Default:** Undefined (task to create `.drirc` is skipped).

  - **Customization:** Set to `true` to enable:

  ```yaml
  disable_vblank: true
  ```

- `debug_vars`: (Boolean)

  - **Defined in:** Not defined by default (task skipped).

  - **Purpose:** If set to `true`, the role will output the content of the `x` variable during execution. This is useful for debugging purposes.

  - **Default:** Undefined.

  - **Customization:** Set to `true` to enable:

  ```yaml
  debug_vars: true
  ```

### Configuration Templates

The role uses Jinja2 templates to create user-specific configuration files. The behavior of the X environment is heavily influenced by these templates. You can customize them by modifying the `.j2` files within the role's `templates/` directory or by providing your own templates.

**Key templated files:**

- `{{ user.home }}/.xprofile` (from `home/.xprofile.j2`)

- `{{ user.home }}/.xserverrc` (from `home/.xserverrc.j2`)

- `{{ user.home }}/.Xresources` (from `home/.Xresources.j2`)

- `{{ user.home }}/.xinitrc` (from `home/.xinitrc.j2`) - _Executable, crucial for starting window managers/desktop environments._

- `{{ user.home }}/.config/sxhkd/sxhkdrc` (from `home/.config/sxhkd/sxhkdrc.j2`) - _SXHKD hotkey definitions._

- `{{ user.home }}/.config/picom.conf` (from `home/.config/picom.conf.j2`) - _Picom compositor settings._

- `{{ user.home }}/.config/dunst/dunstrc` (from `home/.config/dunst/dunstrc.j2`) - _Dunst notification settings._

System-wide configuration:

- `/usr/lib/environment.d/50-xdg-environment.conf` - _Sets XDG environment variables._

- `/etc/xdg/user-dirs.defaults` - _Defines default XDG user directories._

## Tasks Overview

The role performs the following main actions:

1. **Installs Xorg Packages:** Installs the Xorg server, drivers, fonts, and utilities defined in the `packages__x11` variable using `paru`.

2. **Configures X Server Files:**

    - Templates user-specific X configuration files: `.xprofile`, `.xserverrc`, `.Xresources`, and `.xinitrc`.

    - Optionally creates a `.drirc` file to disable VBlank if `disable_vblank` is true.

3. **Sets up SXHKD (Simple X Hotkey Daemon):**

    - Installs SXHKD.

    - Copies a `reload-sxhkd.sh` helper script to `~/.local/bin/`.

    - Templates the SXHKD configuration file (`sxhkdrc`).

4. **Sets up Picom (Compositor):**

    - Templates the Picom configuration file (`picom.conf`).

5. **Sets up Dunst (Notification Daemon):**

    - Templates the Dunst configuration file (`dunstrc`).

6. **Configures XDG Directories:**

    - Installs `xdg-utils`.

    - Sets system-wide XDG environment variables.

    - Configures XDG user directory defaults and updates them using `xdg-user-dirs-update`.

    - Updates the desktop MIME database.

## Handlers

- `Reload sxhkd`: Triggered when the `sxhkdrc` configuration changes. It executes `reload-sxhkd.sh` to apply the new hotkey bindings without restarting the X session.

## Dependencies

This role has no external Ansible Galaxy role dependencies listed in `meta/main.yml`. However, it implicitly depends on:

- A working Arch Linux environment.

- `paru` AUR helper being installed and functional.

## Example Playbook

Here's a basic example of how to use the `x` role in a playbook:

```yaml
- hosts: arch_desktops
  become: true # Most tasks in the role run with become: false or manage user files,
               # but some XDG setup might need root for /etc files.
               # Adjust 'become' as needed based on your specific use case and permissions.
  vars:
    user:
      name: myuser
      home: /home/myuser
      group: myuser
      uid: 1000
    disable_vblank: true
    x:
      autostart: "custom_session" # Assuming your .xinitrc.j2 handles this
  roles:
    - role: x # Or your_username.x if sourced from Galaxy/custom path
```

**Explanation:**

- The playbook targets hosts in the `arch_desktops` group.

- It defines the mandatory `user` variable.

- It sets `disable_vblank` to `true`.

- It overrides the default `x.autostart` value.

- It includes the `x` role.

## Customization Notes

- **Window Manager/Desktop Environment:** This role sets up the X server and core utilities. You will need to install and configure a window manager (e.g., i3, bspwm, Openbox) or a desktop environment (e.g., XFCE, KDE) separately. The `.xinitrc` file is typically where you would launch your chosen window manager or session.

- **Keybindings (`sxhkdrc.j2`):** Customize your keyboard shortcuts by editing the `templates/home/.config/sxhkd/sxhkdrc.j2` file.

- **Compositor Effects (`picom.conf.j2`):** Adjust transparency, shadows, fading, and other visual effects by modifying `templates/home/.config/picom.conf.j2`.

- **Notifications (`dunstrc.j2`):** Configure the appearance and behavior of notifications in `templates/home/.config/dunst/dunstrc.j2`.

- **X Startup (`.xinitrc.j2`, `.xprofile.j2`):** These files control what applications and environment settings are loaded when X starts. Modify their respective `.j2` templates to suit your needs.

## License

As per `meta/main.yml`, the license should be specified (e.g., GPL-2.0-or-later, MIT, etc.). The template indicates: `license (GPL-2.0-or-later, MIT, etc)`. Please update this with the actual license.

## Author Information

An optional section for the role authors to include contact information or a website.
