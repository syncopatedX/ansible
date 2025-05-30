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
* **🎵 Professional Audio:**
  * Configurable audio server selection (JACK, PulseAudio, PipeWire).
  * System tuning for low-latency audio performance.
  * Realtime privileges and CPU optimization for audio processing.
  * Audio normalization tools and utilities.

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

## 🧩 Roles Overview

The playbook is organized into modular roles found in the `roles/` directory:

| Role               | Description                                                                                                                            |
| :----------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| [audio](audio/)            | Professional Linux audio setup with configurable server selection (JACK, PulseAudio, PipeWire) via `use_jack` and `use_pipewire` variables. Includes comprehensive system tuning for low-latency performance, realtime privileges, CPU optimization, and audio normalization tools.                                                                         |
| [base](base/)             | Core system setup, package management (pacman/paru), repositories, base packages, user creation, sudoers, `rc.local`.                   |
| [desktop](desktop/)          | General desktop applications, fonts, and themes.                                                                                       |
| [docker](docker/)           | Docker Engine & Docker Compose installation and configuration (including optional NVIDIA support).                                       |
| `fabric`           | Fabric AI scripting tool setup and configuration.                                                                                      |
| [firewalld](firewalld)        | Firewall configuration using firewalld, opening necessary ports.                                                                       |
| [grub](grub/)             | GRUB bootloader configuration tweaks (kernel parameters, submenus, savedefault).                                                       |
| [homepage](homepage)         | Simple static HTML homepage setup.                                                                                                     |
| [i3](i3/)               | i3 Window Manager, i3status-rust, Rofi configuration.                                                                                  |
| [input-remapper](input-remapper/)   | Input device mapping tool setup.                                                                                                       |
| [libvirt](libvirt)          | Libvirt virtualization stack & optional Vagrant integration.                                                                           |
| `media`            | Media-related configurations (e.g., Musikcube).                                                                                        |
| [nas](nas/)              | NFS & Samba server configuration.                                                                                                      |
| [ntp](ntp/)              | Time synchronization using `systemd-timesyncd`.                                                                                        |
| [ruby](ruby/)             | Ruby environment setup (System gems, optional RVM).                                                                                    |
| [shell](shell)            | Zsh, Oh My Zsh, aliases, functions, kitty, ranger configuration.                                                                       |
| [ssh](ssh/)              | OpenSSH server/client configuration and hardening.                                                                                     |
| [sway](sway/)             | Tiling Window Manager for Wayland                                                                                    |
| [systemd-networkd](systemd-networkd) | Network configuration using `systemd-networkd` and `systemd-resolved`. Includes handling of network, netdev, link, and mount units. |
| [tools](tools/)            | Installation of custom scripts/tools like `code-packager`, `whisper-stream`.                                                           |
| [x](x/)                | X11 server, drivers, core X utilities, Picom, Dunst, sxhkd, XDG configuration.                                                         |

*(Refer to individual `roles/<role_name>/README.md` or `roles/<role_name>/tasks/main.yml` for specifics)*

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

### Variable Precedence (Highest to Lowest)

| Level | Location                                      | Description                                    |
| :---- | :-------------------------------------------- | :--------------------------------------------- |
| 1     | Command Line (`-e "var=value"`)               | Overrides all other variable definitions.      |
| 2     | Host Variables (`inventory/host_vars/*.yml`)  | Specific variables for a single host.          |
| 3     | Group Variables (`inventory/group_vars/*.yml`) | Variables applied to hosts within a group.     |
| 4     | Global Variables (`inventory/group_vars/all`) | Variables applied to all hosts in inventory. |
| 5     | Role Defaults (`roles/*/defaults/main.yml`)   | Default values defined within each role.       |

### Key Variables

The playbook's behavior can be customized through variables. Below are key variables organized by category with their file locations. For a complete list, check individual role `defaults/main.yml` or `vars/main.yml` files.

#### User Configuration

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `user_name`             | `base`, `shell`     | `roles/base/defaults/main.yml`              | Primary user's username for the system.                                                                 |
| `user_group`            | `base`, `shell`     | `roles/base/defaults/main.yml`              | Primary user's group name (defaults to same as username).                                               |
| `user_uid`              | `base`              | `roles/base/defaults/main.yml`              | Primary user's UID (numeric user identifier).                                                           |
| `user_home`             | `base`, `shell`     | `roles/base/defaults/main.yml`              | Full path to primary user's home directory (e.g., `/home/username`).                                    |
| `user_shell`            | `base`, `shell`     | `roles/base/defaults/main.yml`              | Primary user's default shell (e.g., `/bin/zsh`).                                                        |
| `user_sudoer`           | `base`              | `roles/base/defaults/main.yml`              | When `true`, grants passwordless sudo access to the primary user.                                       |

#### Virtualization & Containerization

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `use_docker`            | `docker`            | `roles/docker/defaults/main.yml`            | When `true`, enables Docker installation and configuration.                                             |
| `docker_nvidia_support` | `docker`            | `roles/docker/defaults/main.yml`            | When `true`, configures Docker with NVIDIA GPU support.                                                 |
| `use_libvirt`           | `libvirt`           | `roles/libvirt/defaults/main.yml`           | When `true`, enables libvirt virtualization stack installation.                                         |
| `use_vagrant`           | `libvirt`           | `roles/libvirt/defaults/main.yml`           | When `true`, installs Vagrant (requires `use_libvirt=true`).                                            |

#### Shell & Desktop Environment

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `zsh_theme`             | `shell`             | `roles/shell/defaults/main.yml`             | Specifies the Oh My Zsh theme to use.                                                                   |
| `i3_*`                  | `i3`                | `roles/i3/defaults/main.yml`                | Collection of variables for i3 window manager configuration.                                            |
| `x_*`                   | `x`                 | `roles/x/defaults/main.yml`                 | Variables controlling X11 environment settings.                                                         |

#### Development Environment

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `rvm_install`           | `ruby`              | `roles/ruby/defaults/main.yml`              | When `true`, installs Ruby Version Manager instead of system Ruby.                                      |

#### Networking

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `systemd_network_confs` | `systemd-networkd`  | `roles/systemd-networkd/defaults/main.yml`  | Configures `/etc/systemd/networkd.conf.d/*.conf` files.                                                |
| `systemd_resolve_confs` | `systemd-networkd`  | `roles/systemd-networkd/defaults/main.yml`  | Configures `/etc/systemd/resolved.conf.d/*.conf` files.                                                |
| `systemd_mounts`        | `systemd-networkd`  | `roles/systemd-networkd/defaults/main.yml`  | Configures `/etc/systemd/system/*.mount` files.                                                        |
| `systemd_network_netdevs` | `systemd-networkd` | `roles/systemd-networkd/defaults/main.yml` | Configures `/etc/systemd/network/*.netdev` files for virtual network interfaces.                      |
| `systemd_network_networks` | `systemd-networkd` | `roles/systemd-networkd/defaults/main.yml` | Configures `/etc/systemd/network/*.network` files for network interfaces.                            |
| `systemd_network_keep_existing_definitions` | `systemd-networkd` | `roles/systemd-networkd/defaults/main.yml` | When `false`, deletes existing network definitions and interfaces before applying new ones. |

#### Theming & Appearance

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `colors_*`              | Various (via `all`) | `inventory/group_vars/all/colors.yml`        | Color scheme definitions (e.g., `colors_base00`) defined in `inventory/group_vars/all/colors.yml`.      |
| `theme_*`               | Various (via `all`) | `inventory/group_vars/all/theme.yml`         | Theme element definitions defined in `inventory/group_vars/all/theme.yml`.                              |

#### Package Installation

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `packages_*`            | Various             | `roles/*/defaults/main.yml` (role-specific)  | Lists of packages to install (e.g., `base_packages`, `x_packages`).                                     |

#### Audio Configuration

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `use_jack`              | `audio`             | `roles/audio/defaults/main.yml`             | When `true`, configures JACK audio server for professional audio work.                                  |
| `use_pipewire`          | `audio`             | `roles/audio/defaults/main.yml`             | When `true`, configures PipeWire audio server (modern replacement for PulseAudio and JACK).             |
| `jack_control`          | `audio`             | `roles/audio/defaults/main.yml`             | Configuration settings for JACK server (device selection, etc).                                         |
| `additional_packages`   | `audio`             | `roles/audio/defaults/main.yml`             | List of additional audio-related packages to install.                                                   |

#### Web & Services

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `homepage_*`            | `homepage`          | `roles/homepage/defaults/main.yml`          | Variables defining links and appearance for the static homepage.                                        |

### Example Variable Customization

```yaml
# Example host_vars/myworkstation.yml
user_name: developer
user_home: /home/developer
user_shell: /bin/zsh
user_sudoer: true

use_docker: true
docker_nvidia_support: true
use_libvirt: true
use_vagrant: true

zsh_theme: robbyrussell

rvm_install: true

# Networking example
systemd_network_networks:
  20-wired:
    Match:
      Name: enp1s0
    Network:
      DHCP: yes
      DNS: 192.168.1.1
```

### Example (Command Line Override)

```bash
ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b -e "use_docker=false" -e "user_name=newuser"
```

### Example (Command Line Override)

```bash
ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b -e "use_docker=false" -e "user_name=newuser"
```

## 🏷️ Using Tags

Run specific parts of the playbook using tags defined in playbooks (`main.yml`, `playbooks/full.yml`) and role tasks.

### Available Tags

| Tag | Description |
| :--- | :--- |
| `aliases` | Configure shell aliases |
| `audio` | Configure professional audio setup (JACK, PulseAudio, PipeWire) |
| `base` | Core system setup tasks |
| `base_pkgs` | Install base system packages |
| `code-packager` | Install and configure code-packager tool |
| `docker` | Docker installation and configuration |
| `docker_pkgs` | Install Docker-related packages |
| `dunst` | Configure Dunst notification daemon |
| `env` | Set up environment variables |
| `fabric` | Install and configure Fabric AI scripting tool |
| `firewalld` | Configure firewall using firewalld |
| `folders` | Create and configure directories |
| `groups` | Manage system groups |
| `grub` | Configure GRUB bootloader |
| `grub_pkgs` | Install GRUB-related packages |
| `homepage` | Set up static HTML homepage |
| `i3` | Install and configure i3 window manager |
| `i3_config` | Configure i3 window manager settings |
| `input-remapper` | Set up input device mapping |
| `keybindings` | Configure keyboard shortcuts |
| `libvirt` | Install and configure libvirt virtualization |
| `makepkg` | Configure makepkg settings |
| `menus` | Configure application menus |
| `mirrors` | Update and optimize package mirrors |
| `nas` | Set up NAS-related services |
| `networkd` | Configure systemd-networkd |
| `nfs` | Set up NFS server/client |
| `ntp` | Configure time synchronization |
| `packages` | General package installation tasks |
| `paru` | Install and configure paru AUR helper |
| `picom` | Configure Picom compositor |
| `profile` | Set up user profile configurations |
| `repos` | Configure package repositories |
| `rofi` | Configure Rofi application launcher |
| `rsyncd` | Set up rsync daemon |
| `ruby` | Install and configure Ruby environment |
| `rvm` | Install and configure Ruby Version Manager |
| `samba` | Set up Samba file sharing |
| `setup` | General setup tasks |
| `shell` | Configure shell environment |
| `shell_pkgs` | Install shell-related packages |
| `ssh` | Configure SSH server/client |
| `sudo` | Configure sudo access |
| `sudoers` | Manage sudoers configuration |
| `sxhkd` | Configure Simple X Hotkey Daemon |
| `systemd-mounts` | Configure systemd mount units |
| `systemd-network` | Configure systemd network settings |
| `systemd-resolve` | Configure systemd-resolved |
| `tools` | Install and configure custom tools |
| `updatedb` | Configure and run updatedb for file indexing |
| `user` | Manage user accounts |
| `vagrant` | Install and configure Vagrant |
| `whisper-stream` | Install and configure whisper-stream tool |
| `x` | Configure X11 environment |
| `xdg` | Configure XDG Base Directory settings |
| `xprofile` | Configure X11 profile settings |
| `zprofile` | Configure Zsh profile |
| `zsh` | Install and configure Zsh shell |
| `zsh_functions` | Configure Zsh functions |

### Usage Examples

* **Run Only Specific Tags:**

    ```bash
    # Run only base setup and shell configuration tasks
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "base,shell"

    # Run only systemd-networkd and firewalld tasks
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "systemd-network,firewalld"
    
    # Run only audio configuration
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "audio"
    
    # Run only tools installation
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "tools,code-packager,whisper-stream"
    ```

* **Skip Specific Tags:**

    ```bash
    # Run everything EXCEPT docker and libvirt
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --skip-tags "docker,libvirt"
    
    # Run everything EXCEPT X11 related configurations
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --skip-tags "x,i3,picom,dunst,sxhkd"
    ```

* **List Available Tags:**

    ```bash
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml --list-tags
    # Or for the pull playbook:
    ansible-playbook -i inventory/inventory.ini main.yml --list-tags
    ```

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
