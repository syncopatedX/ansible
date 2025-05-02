# 🤖 Ansible Workstation Archlinux 🚀

This Ansible playbook automates the configuration of a development-focused workstation, primarily targeting Arch Linux 🐧 and its derivatives. It leverages Ansible roles for modularity and maintainability, setting up everything from base system utilities to a complete development environment. It supports both standard `ansible-playbook` execution and `ansible-pull` for agent-based configuration management.

## ✨ Features

This playbook provides a comprehensive workstation setup, including:

* **🔧 Base System:**
  * Package manager configuration (pacman, paru via custom `aur` module).
  * Repository setup (`archaudio`, `chaotic-aur`).
  * Essential system utilities (`mlocate`, `reflector`).
  * Mirrorlist update automation.
  * User account creation and sudo configuration.
  * `rc.local` compatibility setup.
* **🐚 Shell Environment:**
  * Shell customization (zsh, oh-my-zsh, aliases, functions).
  * Terminal emulator setup (kitty).
  * File manager configuration (ranger with devicons).
* **📦 Containerization & Virtualization:**
  * Docker installation and configuration (including optional NVIDIA support).
  * Libvirt installation and configuration (with optional Vagrant support).
* **🖥️ Desktop Environment (X11):**
  * Xorg server, drivers, and utilities.
  * i3 window manager setup (including i3status-rust, rofi).
  * Picom compositor configuration.
  * Dunst notification daemon setup.
  * sxhkd (Simple X Hotkey Daemon).
  * XDG Base Directory Specification compliance and user directories.
  * GRUB theme and configuration.
  * Font installation.
  * Optional LightDM setup (currently minimal).
* **🛠️ Development Tools:**
  * Ruby environment setup (system gems, optional RVM).
  * Go language environment setup.
  * Fabric (AI scripting tool) setup.
  * Custom tools installation (`code-packager`, `whisper-stream` via `tools` role).
* **⌨️ Input Device Management:**
  * `input-remapper` installation and configuration.
* **🌐 Networking & Services:**
  * `systemd-networkd` and `systemd-resolved` for network configuration.
  * `firewalld` setup.
  * OpenSSH server/client configuration (`ssh` role).
  * NTP (Time Synchronization) via `systemd-timesyncd` (`ntp` role).
  * NFS server setup (optional, via `nas` role).
  * Samba server setup (optional, via `nas` role).
* **📄 Homepage:**
  * Sets a simple static HTML homepage with configurable links.
* **🔊 Media:**
  * Configuration for media applications (e.g., Musikcube).

## ✅ Requirements

* **Ansible:** Version 2.9 or higher recommended.
* **Target Host:** An Arch Linux-based distribution. While some tasks might work elsewhere, the playbook is primarily tested and designed for Arch.
* **SSH Access:** Required for standard `ansible-playbook` execution.
* **Root/Sudo Privileges:** The playbook needs root or sudo privileges to install packages and modify system configurations. An `aur_builder` user is recommended for AUR operations.
* **Git:** Required on the target host for `ansible-pull`.

## ⚙️ Installation

1. **Clone the Repository (for Controller Machine):**
   If running `ansible-playbook` from a separate controller:

    ```bash
    # Replace with your repository URL if forked
    git clone https://github.com/your-username/syncopated-ansible.git
    cd syncopated-ansible
    ```

2. **(Optional) Install Ansible Roles via Galaxy:**
    If the playbook utilized external roles defined in `requirements.yml` (not currently present), you would run:

    ```bash
    # ansible-galaxy install -r requirements.yml
    ```

## 🚀 Usage

Choose the method that best suits your needs.

### Method 1: Ansible Pull (Recommended for Initial Setup & Agent-based Management)

This method runs directly on the target machine, pulling the configuration from the Git repository. It's ideal for bootstrapping new machines or for hosts managing their own configuration.

1. **Bootstrap Script (Easiest Initial Setup):**
    Run this command on the *target machine*:

    ```bash
    # Replace with the actual raw URL to your bootstrap script
    curl -sSL https://raw.githubusercontent.com/your-username/syncopated-ansible/main/scripts/bin/bootstrap-ansible-pull.sh | bash
    ```

    This script installs prerequisites (git, ansible), clones the repository, and runs `ansible-pull` using the `main.yml` playbook, targeting `localhost`.

2. **Manual `ansible-pull` Execution:**
    Run this command on the *target machine*:

    ```bash
    # Replace with your repository URL
    # Ensure git and ansible are installed first: sudo pacman -S --needed git ansible-core
    sudo ansible-pull -U https://github.com/your-username/syncopated-ansible.git main.yml
    ```

    * `ansible-pull` clones/updates the repository locally (typically to `/var/lib/ansible/local/`) and then runs the specified playbook (`main.yml`) against `localhost`.

3. **Customizing `ansible-pull`:**
    Pass extra variables (`-e`) or tags (`--tags`, `--skip-tags`) to customize the pull:

    ```bash
    # Example overriding user details (if playbook logic supports it)
    sudo ansible-pull -U https://github.com/your-username/syncopated-ansible.git main.yml \
      -e "user_name=myuser" \
      -e "user_home=/home/myuser" \
      -e "user_shell=/bin/zsh"

    # Example skipping docker and libvirt roles using tags
    sudo ansible-pull -U https://github.com/your-username/syncopated-ansible.git main.yml --skip-tags "docker,libvirt"

    # Example running only base and shell setup
    sudo ansible-pull -U https://github.com/your-username/syncopated-ansible.git main.yml --tags "base,shell"
    ```

### Method 2: Standard Ansible Playbook Execution (Controller-based)

This is the traditional method where you run `ansible-playbook` from a controller machine targeting one or more remote hosts.

1. **Create/Edit Inventory:**
    Define your target host(s) in an inventory file (e.g., `inventory/inventory.ini`).

    *Example `inventory/inventory.ini`:*

    ```ini
    [all:vars]
    ansible_user="{{ lookup('env', 'USER') }}" # Uses environment variable USER
    ansible_connection=ssh
    # Define other global variables from inventory/group_vars/all/*.yml if needed

    [workstations]
    lapbot ansible_host=192.168.1.101 # Example workstation
    soundbot ansible_connection=local # Example running locally

    [servers]
    crambot ansible_host=192.168.1.102 # Example server

    # Define groups as needed
    [dev:children]
    workstations

    [virt:children]
    servers
    ```

    * **Note:** Define host-specific variables in `inventory/host_vars/<hostname>.yml` and group variables in `inventory/group_vars/<groupname>.yml` or `inventory/group_vars/all/`.

2. **Run the Playbook:**
    Execute the desired playbook (`main.yml` for pull-compatible setup, `playbooks/full.yml` for a potentially more comprehensive run) using the inventory file.

    ```bash
    # Run the full playbook with sudo (-b)
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b

    # Run the main (pull-focused) playbook, specifying user (-u) and sudo (-b)
    ansible-playbook -i inventory/inventory.ini main.yml -b -u your_remote_username

    # Target a specific host or group (--limit)
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --limit lapbot
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --limit workstations
    ```

3. **Dry Run (Check Mode):**
    Simulate the playbook run without making actual changes.

    ```bash
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --check
    ```

## 🎨 Customization

Tailor the playbook using Ansible variables.

* **Locations (Order of Precedence - High to Low):**
  1. Command Line (`-e "var=value"`)
  2. Host Variables (`inventory/host_vars/<hostname>.yml`)
  3. Group Variables (`inventory/group_vars/<groupname>.yml`)
  4. Global Group Variables (`inventory/group_vars/all/*.yml`)
  5. Role Defaults (`roles/<rolename>/defaults/main.yml`)
* **Key Variables (Examples - Check role defaults/vars for specifics):**
  * `user_name`, `user_group`, `user_uid`, `user_home`, `user_shell`: Define primary user details (often used by `base` and `shell` roles).
  * `user_sudoer`: `true`/`false` to grant passwordless sudo via `base` role.
  * `use_docker`: `true`/`false` to enable/disable Docker role.
  * `use_libvirt`: `true`/`false` to enable/disable Libvirt role.
  * `use_vagrant`: `true`/`false` to enable/disable Vagrant (requires `use_libvirt=true`).
  * `docker_nvidia_support`: `true`/`false` to enable Docker NVIDIA support.
  * `rvm_install`: `true`/`false` to enable/disable RVM installation in `ruby` role.
  * `zsh_theme`: Set the desired Oh My Zsh theme in `shell` role.
  * `packages_*`: Variables within roles defining package lists (e.g., `base_packages`, `x_packages`).
  * `colors_*`: Variables defining color schemes (e.g., `colors_base00`, see `inventory/group_vars/all/colors.yml`).
  * `theme_*`: Variables defining theme elements (see `inventory/group_vars/all/theme.yml`).
  * `i3_*`: Dictionaries/variables for i3 settings within the `i3` role.
  * `x_*`: Dictionaries/variables for X11 settings within the `x` role.
  * `homepage_*`: Variables defining links for the static homepage.
  * `networkd_*`: Variables for configuring `systemd-networkd` interfaces, networks, netdevs, mounts (see `systemd-networkd` role).
* **Example (Command Line Override):**

    ```bash
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b -e "use_docker=false" -e "user_name=newuser"
    ```

## 🏷️ Using Tags

Run specific parts of the playbook using tags defined in playbooks (`main.yml`, `playbooks/full.yml`) and role tasks.

* **Run Only Specific Tags:**

    ```bash
    # Run only base setup and shell configuration tasks
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "base,shell"

    # Run only systemd-networkd and firewalld tasks
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "systemd-networkd,firewalld"
    ```

* **Skip Specific Tags:**

    ```bash
    # Run everything EXCEPT docker and libvirt
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --skip-tags "docker,libvirt"
    ```

* **List Available Tags:**

    ```bash
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml --list-tags
    # Or for the pull playbook:
    ansible-playbook -i inventory/inventory.ini main.yml --list-tags
    ```

## 🧩 Roles Overview

The playbook is organized into modular roles found in the `roles/` directory:

* `base`: Core system setup, package management (pacman/paru), repositories, base packages, user creation, sudoers, `rc.local`.
* `desktop`: General desktop environment components (potentially shared across WMs/DEs - check tasks).
* `docker`: Docker Engine & Docker Compose installation and configuration.
* `fabric`: Fabric AI tool setup.
* `firewalld`: Firewall configuration using firewalld.
* `fonts`: Font installation.
* `grub`: GRUB bootloader theme and configuration tweaks.
* `homepage`: Simple static HTML homepage setup.
* `i3`: i3 Window Manager, i3status-rust, Rofi configuration.
* `input-remapper`: Input device mapping tool setup.
* `libvirt`: Libvirt virtualization stack & optional Vagrant integration.
* `lightdm`: LightDM Display Manager setup (currently minimal).
* `media`: Media-related configurations (e.g., Musikcube).
* `nas`: NFS & Samba server configuration.
* `ntp`: Time synchronization using `systemd-timesyncd`.
* `ruby`: Ruby environment setup (System gems, optional RVM).
* `shell`: Zsh, Oh My Zsh, aliases, functions, kitty, ranger configuration.
* `ssh`: OpenSSH server/client configuration and hardening.
* `systemd-networkd`: Network configuration using `systemd-networkd` and `systemd-resolved`. Includes handling of network, netdev, link, and mount units.
* `tools`: Installation of custom scripts/tools like `code-packager`, `whisper-stream`.
* `x`: X11 server, drivers, core X utilities, Picom, Dunst, sxhkd, XDG configuration.

*(Refer to individual `roles/<role_name>/README.md` or `roles/<role_name>/tasks/main.yml` for specifics)*

## 🤔 Troubleshooting

* **SSH Issues:** Ensure SSH connectivity (for `ansible-playbook`), correct user, and authentication. Check firewall rules (`firewalld` role, `ssh` role).
* **Package Errors:** Check Ansible output for `pacman`/`paru` errors. Verify internet access and repository reachability. Ensure `aur_builder` user (if used) has necessary permissions.
* **`ansible-pull` Failures:** Check permissions for cloning/writing in `/var/lib/ansible/local/` (or configured path). Ensure `git` and `ansible-core` are installed on the target. Check the repository URL and branch.
* **Networking Issues:** Verify configurations applied by the `systemd-networkd` role. Use `networkctl` and `resolvectl` on the target host for diagnostics. Check `firewalld` status and rules.
* **Idempotency Problems:** Review task `when` conditions and checks for existing states.
* **Check Mode:** Use `ansible-playbook --check` to preview changes. Note that `--check` mode might not perfectly simulate all state changes, especially with shell commands or complex services.
* **Variable Issues:** Use `-v`, `-vv`, or `-vvv` for verbose output. Check variable precedence and definitions in inventory, group/host vars, and role defaults. Verify `ansible.cfg` settings like `error_on_undefined_vars`.

## 🤝 Contributing

Contributions are welcome! Please fork the repository, create a feature branch, make your changes following Ansible best practices, test thoroughly (using Vagrant, VMs, or dedicated hardware), and submit a pull request with a clear description of the changes.

## 📜 License

This project is likely licensed under the MIT License. Please refer to the `LICENSE` file in the repository root for details.
