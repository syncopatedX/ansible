# Ansible Role: Desktop Environment Setup

This Ansible role is designed to automate the setup of a customized desktop environment on Linux systems. It handles the installation of specified desktop applications, fonts, themes, and Qt-related packages. Additionally, it can deploy and configure a collection of enhanced Nautilus file manager scripts.

## Requirements

- **Ansible:** Version 2.1 or higher.

- **Target System:** A Linux distribution. The package installation tasks (which would need to be implemented in `tasks/main.yml`) should be compatible with the target system's package manager (e.g., APT, DNF, Pacman).

- **Privileges:** Root or sudo privileges are required on the target machine to install packages and place files in system directories.

- **File Manager (for Nautilus Scripts):** If installing the Nautilus scripts, a compatible file manager (e.g., GNOME Files (Nautilus), Caja, Nemo, Dolphin, PCManFM-Qt, Thunar) should be present on the target system.

## Role Variables

The primary way to customize this role is by defining or overriding the `packages` dictionary and a few control variables. These variables are primarily defined in `vars/main.yml`.

### Package Lists

The `packages` variable is a dictionary containing lists of packages to be installed:

- **`packages.desktop`**:

  - **Description:** A list of general desktop applications and utilities.

  - **Default:** (See `vars/main.yml` for the extensive default list, including `ascii-image-converter`, `barrier`, `gedit`, `google-chrome`, `kitty`, `mpv`, `rofi`, `terminator`, `yt-dlp`, `zenity`, etc.)

  - **Customization:** You can override this list entirely or extend it in your playbook or inventory.

- **`packages.fonts`**:

  - **Description:** A list of font packages.

  - **Default:** (See `vars/main.yml`, includes `gnu-free-fonts`, `ttf-font-awesome`, `ttf-jetbrains-mono`, `ttf-hack-nerd`, etc.)

  - **Customization:** Override or extend this list as needed.

- **`packages.themes`**:

  - **Description:** A list of GTK themes and theme-related engine packages.

  - **Default:** (See `vars/main.yml`, includes `gtk-engines`, `gtk-engine-murrine`.)

  - **Customization:** Override or extend this list.

- **`packages.qt`**:

  - **Description:** A list of Qt-related packages, including libraries and tools.

  - **Default:** (See `vars/main.yml`, includes `kvantum-qt5`, `qt5-tools`, `qt6-base`, etc.)

  - **Customization:** Override or extend this list.

**Example of Overriding Package Lists:**

To add your own packages or replace the default lists, you can define the `packages` variable in your playbook:

```yaml
- hosts: my_desktops
  vars:
    packages:
      desktop:
        - geany
        - vlc
        - flameshot # Added application
      fonts:
        - ttf-cascadia-code
      # themes and qt will use defaults from vars/main.yml if not specified here
  roles:
    - { role: your_username.desktop } # Replace with your actual role name
```

To extend a list (Ansible 2.8+ for `combine` filter with `list_merge='append_rp'` or more complex logic for older versions):

```shell
# In your playbook or group_vars/all.yml
# This example assumes you want to add to the defaults defined in vars/main.yml
# Note: Direct extension of lists defined in vars/main.yml requires careful variable precedence management
# or loading them and then combining. A simpler approach for users is often to redefine the list.

# A more robust way if you want to truly extend the defaults from vars/main.yml
# would be to load them first if Ansible's default merging isn't sufficient.
# However, users typically just redefine the parts they want to change.
```

A common practice is to define the complete list you desire for a specific group or host if the defaults are not suitable.

### Nautilus Scripts Variables

These variables control the installation and configuration of the custom Nautilus scripts located in the `files/nautilus-scripts/` directory of the role.

- **`desktop_nautilus_scripts_install`**:

  - **Description:** A boolean value that determines whether to install the Nautilus scripts.

  - **Default:** `true`

  - **Customization:** Set to `false` to skip Nautilus script installation.

- **`desktop_nautilus_scripts_options`**:

  - **Description:** A comma-separated string of options to pass to the `install.sh` script for the Nautilus scripts. This allows customization of the script installation (e.g., installing dependencies, keyboard shortcuts). Refer to the `files/nautilus-scripts/README.md` and `files/nautilus-scripts/install.sh` for available options.

  - **Default:** `"dependencies,shortcuts,reload"` (This is a suggested default; you might want to set it in `defaults/main.yml`)

  - **Example Options:**

    - `dependencies`: Install basic dependencies for the scripts.

    - `shortcuts`: Install keyboard shortcuts.

    - `reload`: Close the file manager to reload its configuration.

    - `categories`: Choose script categories to install.

    - `preserve`: Preserve previous scripts.

  - **Customization:** Modify this string to change the installation behavior of the Nautilus scripts. For example, `"dependencies,shortcuts"` to install dependencies and shortcuts but not reload the file manager automatically.

## Nautilus Scripts Integration

This role includes a collection of powerful Nautilus scripts (compatible with Nautilus, Caja, Nemo, and other file managers) found in the `files/nautilus-scripts/` directory. These scripts enhance file manager functionality with intuitive right-click actions.

**Key features of these scripts (as per their README):**

- Parallel task execution

- Progress dialogs and task interruption

- Dependency management and status notifications

- Remote file support

- Non-destructive output

- Keyboard shortcuts

- And much more.

The installation is managed by the `files/nautilus-scripts/install.sh` script. This Ansible role will typically:

1. Copy the `files/nautilus-scripts/` directory to a temporary location on the target machine.

2. Execute the `install.sh` script with options specified by the `desktop_nautilus_scripts_options` variable.

Refer to `files/nautilus-scripts/README.md` for detailed information about the scripts themselves.

## Dependencies

This role currently has no external Ansible role dependencies listed in `meta/main.yml`.

## Example Playbook

Here's how you might use this role in your Ansible playbook:

```yaml
- hosts: all
  become: yes # Most tasks will require root privileges

  vars:
    # Example: Customize packages for the 'desktop' group
    packages:
      desktop:
        - firefox
        - thunderbird
        - gimp
        - inkscape
        - libreoffice-fresh
        - htop
        - git
      fonts:
        - ttf-fira-code
        - noto-fonts
      themes:
        - arc-gtk-theme
    
    # Example: Customize Nautilus script installation
    desktop_nautilus_scripts_install: true
    desktop_nautilus_scripts_options: "dependencies,shortcuts" # Don't reload file manager

  roles:
    - { role: your_username.desktop } # Replace with your actual role name/path
```

**To use only the default package lists and Nautilus script settings:**

```yaml
- hosts: all
  become: yes
  roles:
    - { role: your_username.desktop } # Replace with your actual role name/path
```

## Task Implementation Note

The `tasks/main.yml` file for this role would need to contain the Ansible tasks to perform the following actions:

1. **Package Installation:** Iterate through the lists in the `packages` variable (`packages.desktop`, `packages.fonts`, `packages.themes`, `packages.qt`) and install them using the appropriate Ansible package module (e.g., `ansible.builtin.package`, `ansible.builtin.apt`, `ansible.builtin.dnf`, `community.general.pacman`).

2. **Nautilus Scripts Installation:**

    - Check the `desktop_nautilus_scripts_install` variable.

    - If true, copy the `files/nautilus-scripts` directory to the target machine.

    - Execute the `install.sh` script from the copied directory, passing the `desktop_nautilus_scripts_options`.

    - Ensure the `install.sh` script is executable.

An example snippet for `tasks/main.yml` for package installation (Debian/Ubuntu focused):

```yaml
# tasks/main.yml (Partial Example)
---
- name: Update apt cache
  ansible.builtin.apt:
    update_cache: yes
  when: ansible_os_family == "Debian"
  changed_when: false

- name: Install desktop packages
  ansible.builtin.package:
    name: "{{ packages.desktop }}"
    state: present
  when: packages.desktop is defined and packages.desktop | length > 0

- name: Install font packages
  ansible.builtin.package:
    name: "{{ packages.fonts }}"
    state: present
  when: packages.fonts is defined and packages.fonts | length > 0

# ... similar tasks for themes and qt packages ...

- name: Ensure Nautilus scripts directory exists on target for copying
  ansible.builtin.file:
    path: "/tmp/nautilus-scripts-{{ ansible_date_time.epoch }}"
    state: directory
    mode: '0755'
  when: desktop_nautilus_scripts_install | default(true)
  register: nautilus_scripts_tmp_dir

- name: Copy Nautilus scripts to target
  ansible.builtin.copy:
    src: files/nautilus-scripts/
    dest: "{{ nautilus_scripts_tmp_dir.path }}"
    mode: '0755' # Ensure scripts within are executable if needed by install.sh
  when: desktop_nautilus_scripts_install | default(true)

- name: Install Nautilus scripts
  ansible.builtin.command:
    cmd: "bash install.sh {{ desktop_nautilus_scripts_options | default('dependencies,shortcuts,reload') }}"
    chdir: "{{ nautilus_scripts_tmp_dir.path }}/nautilus-scripts" # Adjust if copy places it directly
  when: desktop_nautilus_scripts_install | default(true)
  changed_when: true # Assume install.sh makes changes

- name: Clean up copied Nautilus scripts directory
  ansible.builtin.file:
    path: "{{ nautilus_scripts_tmp_dir.path }}"
    state: absent
  when: desktop_nautilus_scripts_install | default(true) and nautilus_scripts_tmp_dir.path is defined
```

You would need to adapt the package management and script execution logic to be robust and potentially cross-distribution compatible if required.

## License

(Specify your license here, e.g., MIT, BSD, GPL-2.0-or-later. The `meta/main.yml` suggests `license (GPL-2.0-or-later, MIT, etc)`)

## Author Information

(Provide your name, contact, or website here.)
