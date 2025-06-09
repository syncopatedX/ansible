# 🤖 Syncopated Ansible Workstation Automation 🚀

This Ansible playbook automates the configuration of a development-focused workstation with **multi-distribution support**. Originally designed for Arch Linux 🐧, it now supports **Rocky Linux 9** and provides a unified automation framework for professional workstations. It leverages Ansible roles for modularity and maintainability, setting up everything from base system utilities to a complete development environment.

## 🌟 **Multi-Distribution Support**

* **✅ Arch Linux**: Full native support with AUR integration
* **✅ Rocky Linux 9**: Complete RHEL family support with EPEL, PowerTools/CRB, and RPM Fusion
* **🔄 Unified Package Management**: Automatic distribution detection and package mapping
* **📦 Alternative Installation Methods**: Source builds, Cargo/Rust tools, binary downloads, Flatpak fallbacks

## ✨ Features

This playbook provides a comprehensive workstation setup, including:

* **🔧 Base System:**
  * **Multi-Distribution Package Management:**
    * **Arch Linux**: pacman, paru via custom `aur` module, Chaotic AUR, ArchAudio repos
    * **Rocky Linux 9**: dnf with EPEL, PowerTools/CRB, RPM Fusion repositories
  * **Unified Package Installation**: Automatic distribution detection and package mapping
  * **Alternative Methods**: Source builds (libvips, chromaprint), Cargo/Rust tools, binary downloads
  * Essential system utilities and configuration
  * User account creation and sudo configuration
  * Distribution-specific optimizations
* **🐚 Shell Environment:**
  * Shell customization (zsh, oh-my-zsh, aliases, functions).
  * Terminal emulator setup (kitty).
  * File manager configuration (ranger with devicons).
* **📦 Containerization & Virtualization:**
  * Docker installation and configuration (including optional NVIDIA support).
  * Libvirt installation and configuration (with optional Vagrant support).
* **🖥️ Desktop Environment:**
  * **X11:**
    * Xorg server, drivers, and utilities.
    * i3 window manager setup (including i3status-rust, rofi).
    * Picom compositor configuration.
    * Dunst notification daemon setup.
    * sxhkd (Simple X Hotkey Daemon).
  * **Wayland:**
    * Sway window manager setup.
    * XWayland for X11 application compatibility.
  * XDG Base Directory Specification compliance and user directories.
  * GRUB theme and configuration.
  * Font installation.
  * Optional LightDM setup (currently minimal).
* **🛠️ Development Tools:**
  * Ruby environment setup (system gems, optional RVM) with comprehensive knowledge base documentation.
  * Go language environment setup.
  * Fabric (AI scripting tool) setup.
  * Custom tools installation (`code-packager`, `whisper-stream` via `tools` role).
* **⌨️ Input Device Management:**
  * `input-remapper` installation and configuration.
* **🌐 Networking & Services:**
  * Unified network configuration with support for both `systemd-networkd` and NetworkManager.
  * Automatic wireless interface detection and interactive Wi-Fi setup using the pause module.
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
* **🎬 Video:**
  * Mesa graphics packages installation.
  * Vendor-specific video drivers (Intel, AMD) configuration.
* **🔍 Dynamic Inventory:**
  * Enhanced inventory management with group and host variable support.
  * Flexible group hierarchy and variable inheritance.
  * See [Dynamic-Inventory.md](docs/Dynamic-Inventory.md) for detailed documentation.

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
| [audio](roles/audio/)            | Professional Linux audio setup with configurable server selection (JACK, PulseAudio, PipeWire) via `use_jack` and `use_pipewire` variables. Includes comprehensive system tuning for low-latency performance, realtime privileges, CPU optimization, and audio normalization tools.                                                                         |
| [base](roles/base/)             | Core system setup, package management (pacman/paru), repositories, base packages, user creation, sudoers, `rc.local`.                   |
| [desktop](roles/desktop/)          | General desktop applications, fonts, and themes.                                                                                       |
| [docker](roles/docker/)           | Docker Engine & Docker Compose installation and configuration (including optional NVIDIA support).                                       |
| `fabric`           | Fabric AI scripting tool setup and configuration.                                                                                      |
| [firewalld](roles/firewalld/)        | Firewall configuration using firewalld, opening necessary ports.                                                                       |
| [grub](roles/grub/)             | GRUB bootloader configuration tweaks (kernel parameters, submenus, savedefault).                                                       |
| [homepage](roles/homepage/)         | Simple static HTML homepage setup.                                                                                                     |
| [i3](roles/i3/)               | i3 Window Manager, i3status-rust, Rofi configuration.                                                                                  |
| [input-remapper](roles/input-remapper/)   | Input device mapping tool setup.                                                                                                       |
| [libvirt](roles/libvirt/)          | Libvirt virtualization stack & optional Vagrant integration.                                                                           |
| `media`            | Media-related configurations (e.g., Musikcube).                                                                                        |
| [nas](roles/nas/)              | NFS & Samba server configuration.                                                                                                      |
| [network](roles/network/)           | Comprehensive network management supporting multiple backends (NetworkManager, systemd-networkd). Features automatic wireless interface detection, interactive Wi-Fi configuration using the pause module, and support for ethernet, Wi-Fi, bridges, static/DHCP configurations, and udev rules. |
| [ntp](roles/ntp/)              | Time synchronization using `systemd-timesyncd`.                                                                                        |
| [ruby](roles/ruby/)             | Ruby environment setup (System gems, optional RVM) with comprehensive knowledge base documentation.                                                                                    |
| [shell](roles/shell/)            | Zsh, Oh My Zsh, aliases, functions, kitty, ranger configuration.                                                                       |
| [ssh](roles/ssh/)              | OpenSSH server/client configuration and hardening.                                                                                     |
| [sway](roles/sway/)             | Tiling Window Manager for Wayland.                                                                                    |
| [tools](roles/tools/)            | Installation of custom scripts/tools like `code-packager`, `whisper-stream`.                                                           |
| [video](roles/video/)            | Video driver configuration including mesa packages and vendor-specific drivers (Intel, AMD).                                                           |
| [x](roles/x/)                | X11 server, drivers, core X utilities, Picom, Dunst, sxhkd, XDG configuration.                                                         |
| [xwayland](roles/xwayland/)          | XWayland configuration for running X11 applications on Wayland (Sway).                                                         |

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
| `window_manager`        | Multiple            | `inventory/group_vars/workstation/desktop_environment.yml` | Determines which window manager to use. Set to "sway" for Wayland with XWayland support, or "i3" (default) for X11. |
| `i3_*`                  | `i3`                | `roles/i3/defaults/main.yml`                | Collection of variables for i3 window manager configuration.                                            |
| `x_*`                   | `x`                 | `roles/x/defaults/main.yml`                 | Variables controlling X11 environment settings.                                                         |

#### Development Environment

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `rvm_install`           | `ruby`              | `roles/ruby/defaults/main.yml`              | When `true`, installs Ruby Version Manager instead of system Ruby.                                      |

#### Networking

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `network_interfaces`    | `network`           | `roles/network/defaults/main.yml`           | List of network interfaces to configure (ethernet, Wi-Fi, bridge).                                      |
| `etc_hosts`             | `network`           | `roles/network/defaults/main.yml`           | Content for the `/etc/hosts` file.                                                                      |

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

#### Interactive Configuration

| Variable                | Role(s)             | File Location                                | Description                                                                                             |
| :---------------------- | :------------------ | :------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| N/A                     | `network`           | `roles/network/tasks/iwd.yml`               | Uses the `pause` module to interactively prompt for wireless SSID and passphrase during playbook execution, allowing for interactive input anywhere in a task sequence (unlike `vars_prompt` which can only be used at the beginning of a play). |

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
network_interfaces:
  - ifname: "eth0"
    conn_name: "Wired connection eth0"
    type: "ethernet"
    method4: "manual"
    ip4: "192.168.1.100/24"
    gw4: "192.168.1.1"
    dns4: ["192.168.1.1", "8.8.8.8"]
```

### Example (Command Line Override)

```bash
ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b -e "use_docker=false" -e "user_name=newuser"
```

## 🐧 **Rocky Linux 9 Usage**

The playbook now supports **Rocky Linux 9** with automatic distribution detection and package mapping. 

### Prerequisites for Rocky Linux 9

1. **Python 3**: Ensure Python 3 is available for Ansible
   ```bash
   sudo dnf install -y python3
   ```

2. **Set Python Interpreter**: Rocky Linux 9 uses Python 3.9, so specify the interpreter:
   ```bash
   ansible-playbook -i inventory/inventory.ini playbooks/full.yml \
     -e "ansible_python_interpreter=/usr/bin/python3"
   ```

### Rocky Linux 9 Package Sources

The automation automatically configures these repositories:

* **BaseOS & AppStream**: Core Rocky Linux packages
* **EPEL 9**: Extra Packages for Enterprise Linux (aria2, bat, fd-find, ripgrep, etc.)
* **PowerTools/CRB**: Code Ready Builder for development headers
* **RPM Fusion Free/Non-Free**: Multimedia packages (codecs, media tools)
* **GitHub CLI**: Official repository for `gh` command

### Rocky Linux 9 Example Usage

```bash
# Full workstation setup on Rocky Linux 9
ansible-playbook -i inventory/inventory.ini playbooks/full.yml \
  -e "ansible_python_interpreter=/usr/bin/python3" \
  --ask-become-pass

# Install only base system and development tools
ansible-playbook -i inventory/inventory.ini playbooks/full.yml \
  -e "ansible_python_interpreter=/usr/bin/python3" \
  --tags "base,ruby,docker" --ask-become-pass

# Test repository setup only
ansible-playbook -i inventory/inventory.ini playbooks/full.yml \
  -e "ansible_python_interpreter=/usr/bin/python3" \
  --tags "repos" --check --diff
```

### Source Build Packages

Some packages are built from source on Rocky Linux 9:

* **libvips**: Image processing library (meson build)
* **chromaprint**: Audio fingerprinting library (cmake build)

Build dependencies are automatically installed and compilation happens in `/tmp/build-*` directories.

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
| `network` | Configure network settings |
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
| `sway` | Install and configure Sway window manager |
| `sxhkd` | Configure Simple X Hotkey Daemon |
| `systemd-mounts` | Configure systemd mount units |
| `tools` | Install and configure custom tools |
| `updatedb` | Configure and run updatedb for file indexing |
| `user` | Manage user accounts |
| `vagrant` | Install and configure Vagrant |
| `video` | Configure video drivers and related packages |
| `whisper-stream` | Install and configure whisper-stream tool |
| `x` | Configure X11 environment |
| `xdg` | Configure XDG Base Directory settings |
| `xprofile` | Configure X11 profile settings |
| `xwayland` | Configure XWayland for X11 application compatibility on Wayland |
| `zprofile` | Configure Zsh profile |
| `zsh` | Install and configure Zsh shell |
| `zsh_functions` | Configure Zsh functions |

### Usage Examples

* **Run Only Specific Tags:**

    ```bash
    # Run only base setup and shell configuration tasks
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "base,shell"

    # Run only network and firewalld tasks
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "network,firewalld"
    
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
    
    # Run only Wayland-related configurations
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --tags "sway,xwayland"
    
    # Run only video driver configuration
    ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --tags "video"
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
* **Networking Issues:** Verify configurations applied by the `network` role. For NetworkManager-based setups, use `nmcli` on the target host for diagnostics. For systemd-networkd setups, check `networkctl` status. For wireless issues, examine `/var/lib/iwd/` configurations. Check `firewalld` status and rules.
* **Display/Graphics Issues:** For video driver problems, check which packages were installed by the `video` role. For Wayland/XWayland issues, verify that the correct window manager is set in your variables (`window_manager: "sway"`) and that XWayland packages were properly installed.
* **Idempotency Problems:** Review task `when` conditions and checks for existing states.
* **Check Mode:** Use `ansible-playbook --check` to preview changes. Note that `--check` mode might not perfectly simulate all state changes, especially with shell commands or complex services.
* **Variable Issues:** Use `-v`, `-vv`, or `-vvv` for verbose output. Check variable precedence and definitions in inventory, group/host vars, and role defaults. Verify `ansible.cfg` settings like `error_on_undefined_vars`.

## 🤝 Contributing

Contributions are welcome! Please fork the repository, create a feature branch, make your changes following Ansible best practices, test thoroughly (using Vagrant, VMs, or dedicated hardware), and submit a pull request with a clear description of the changes.

## 📜 License

This project is likely licensed under the MIT License. Please refer to the `LICENSE` file in the repository root for details.
