# Ansible Role: Login Configuration

## Description

This Ansible role configures the login mechanism on a target system. It can set up either:

1. **TTY Autologin**: Automatically logs in a specified user on TTY1. This is typically used for systems running a window manager like i3 directly without a graphical display manager.
2. **Greetd**: A minimal and flexible login manager, often used with Wayland compositors like Sway. This role will install and configure `greetd` along with styling for `wlogout`.

The choice between these two mechanisms is determined by the `window_manager` variable.

## Requirements

* **Ansible**: Version 2.1 or higher (as specified in `meta/main.yml`).
* **Target System**:
  * A Linux system with `systemd`.
  * If `window_manager` is set to `'sway'`, the `greetd` package and its dependencies should be available for installation by the system's package manager (this role does not handle package installation, only configuration).
  * If `window_manager` is set to `'i3'` and `autologin` is `true`, the `getty` service is expected to be available.

## Role Variables

The behavior of this role is controlled by the following variables:

### `window_manager`

* **Description**: Specifies the window manager in use, which dictates the login mechanism to configure.
* **Required**: Yes. This variable must be set by the user.
* **Type**: String
* **Possible Values**:
  * `'i3'`: Configures the system for TTY autologin. The tasks in `tasks/getty.yml` will be executed.
  * `'sway'`: Configures `greetd` as the login manager. The tasks in `tasks/greetd.yml` will be executed. This includes synchronizing configuration files from `files/etc/greetd/` to `/etc/greetd/` on the target machine and enabling the `greetd` service.
* **Default**: None.
* **Example**: `window_manager: "sway"`

### `autologin`

* **Description**: Enables or disables automatic login on TTY1. This variable is only effective when `window_manager` is set to `'i3'`.
* **Required**: No.
* **Type**: Boolean (represented as a string `'true'` or `'false'` in the current task, but ideally should be a boolean).
* **Default**: `'false'` (as per the `default('false')` filter in `tasks/getty.yml`). It's recommended to explicitly set this in your playbook or defaults.
* **Example**: `autologin: true`

### `autologin_user`

* **Description**: Specifies the username for automatic login on TTY1. This variable is crucial and **must be set** if `autologin` is `true` and `window_manager` is `'i3'`.
* **Required**: Yes, if `autologin` is `true` and `window_manager` is `'i3'`.
* **Type**: String
* **Default**: None.
* **Example**: `autologin_user: "myuser"`
* **Note**: This role expects a Jinja2 template named `autologin.conf.j2` to exist at `templates/etc/systemd/system/getty@tty1.service.d/autologin.conf.j2`. This template is responsible for using the `autologin_user` variable to configure the `getty` service. **This template file is not currently included in the role's `templates` directory and needs to be created.**
    An example `autologin.conf.j2` might look like this:

    ```ini
    # {{ ansible_managed }}
    [Service]
    ExecStart=
    ExecStart=-/sbin/agetty --autologin {{ autologin_user }} --noclear %I $TERM
    ```

### Greetd Configuration Files

When `window_manager` is set to `'sway'`, the role synchronizes files from its local `files/etc/greetd/` directory to `/etc/greetd/` on the target machine. This includes:

* `style.css`: Main CSS for `gtkgreet`.
* `wlogout.css`: CSS for the `wlogout` logout menu.

You can customize these files within the role before applying it, or manage them outside the role if more complex configuration is needed.

## Dependencies

This role has no external Ansible Galaxy dependencies listed in `meta/main.yml`.

## Example Playbook

Here are a few examples of how to use this role:

1. **Configure `greetd` for Sway:**

    ```yaml
    - hosts: sway_desktops
      vars:
        window_manager: "sway"
      roles:
        - role: your_username.login # Replace with the actual role name if on Galaxy
          # or path to the role if local:
          # role: path/to/login_role
    ```

2. **Configure TTY autologin for i3:**

    ```yaml
    - hosts: i3_machines
      vars:
        window_manager: "i3"
        autologin: true
        autologin_user: "john_doe"
      roles:
        - role: your_username.login
    ```

3. **Using defaults (if `autologin` defaults to `false` or is set in `defaults/main.yml`):**
    If you add `autologin: false` and a placeholder for `autologin_user` to `defaults/main.yml`, you could simplify the i3 case when autologin is not desired:

    ```yaml
    # In defaults/main.yml
    # autologin: false
    # autologin_user: "" # Or a placeholder like "no_autologin_user"

    # In your playbook
    - hosts: i3_machines
      vars:
        window_manager: "i3"
        # autologin and autologin_user will use defaults
      roles:
        - role: your_username.login
    ```

## Tasks Overview

* **`tasks/main.yml`**:
  * Imports `getty.yml` if `window_manager == 'i3'`.
  * Imports `greetd.yml` if `window_manager == 'sway'`.

* **`tasks/getty.yml`**:
  * If `autologin` is `true` (defaults to `false`):
    * Creates the directory `/etc/systemd/system/getty@tty1.service.d`.
    * Templates `autologin.conf.j2` to `/etc/systemd/system/getty@tty1.service.d/autologin.conf` to configure autologin for `autologin_user`. **(Requires `autologin.conf.j2` to be created in the role's `templates` directory)**.

* **`tasks/greetd.yml`**:
  * Synchronizes configuration files from the role's `files/etc/greetd/` directory to `/etc/greetd/` on the target.
  * Enables the `greetd` systemd service.

## License

As specified in `meta/main.yml` (e.g., GPL-2.0-or-later, MIT, etc.). The template currently says `license (GPL-2.0-or-later, MIT, etc)`. Please update this with a specific license.

## Author Information

This section can be updated with the author's contact information or website.
