# 🤖 Syncopated Ansible Workstation Automation 🚀

This Ansible playbook automates the configuration of a development-focused workstation with **multi-distribution support**. Originally designed for Arch Linux 🐧, it now supports **Rocky Linux 9** and provides a unified automation framework for professional workstations. It leverages Ansible roles for modularity and maintainability, setting up everything from base system utilities to a complete development environment.

**Current Version**: v0.9.0 - Enhanced Ruby development environment with RVM support and improved role management.

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

2. **Install Ansible Roles via Galaxy:**
    The playbook utilizes external roles for RVM Ruby support. Install required dependencies:

    ```bash
    ansible-galaxy install -r requirements.yml
    ```

    Note: The roles path has been configured in `ansible.cfg` to automatically locate both local and Galaxy-installed roles.

## 🧩 Roles Overview

The playbook is organized into modular roles found in the `roles/` directory:

| Role               | Description                                                                                                                            |
| :----------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| [audio](roles/audio/)            | Professional Linux audio setup with configurable server selection (JACK, PulseAudio, PipeWire). Includes system tuning for low-latency performance. |
| [base](roles/base/)             | Core system setup, package management (pacman/paru), repositories, user creation, and sudoers configuration.                   |
| [display-manager](roles/display-manager/) | Manages the display manager, including greetd and getty autologin.                                                        |
| [docker](roles/docker/)           | Installs and configures Docker Engine and Docker Compose.                                       |
| [dunst](roles/dunst/)           | Configures the Dunst notification daemon.                                                                                               |
| [firewalld](roles/firewalld/)        | Manages firewall rules using firewalld.                                                                       |
| [grub](roles/grub/)             | Configures the GRUB bootloader.                                                       |
| [i3](roles/i3/)                 | Installs and configures the i3 window manager.                                                                          |
| [libvirt](roles/libvirt/)          | Sets up the Libvirt virtualization stack and optional Vagrant integration.                                                                           |
| [media](roles/media/)            | Configures media-related applications like Musikcube.                                                                                        |
| [nas](roles/nas/)              | Configures NFS and Samba server settings.                                                                                                      |
| [networking](roles/networking/)     | Manages network configurations, supporting multiple backends like NetworkManager and systemd-networkd. |
| [ntp](roles/ntp/)              | Configures time synchronization using `systemd-timesyncd`.                                                                                        |
| [picom](roles/picom/)           | Configures the Picom compositor for X11.                                                                                               |
| [rofi](roles/rofi/)             | Installs and configures the Rofi application launcher.                                                                  |
| [shell](roles/shell/)            | Configures the shell environment, including Zsh, Oh My Zsh, aliases, and terminal tools.                                                                       |
| [ssh](roles/ssh/)              | Configures and hardens the OpenSSH server and client.                                                                                     |
| [sway](roles/sway/)             | Installs and configures the Sway window manager.                                                                        |
| [sxhkd](roles/sxhkd/)           | Configures the Simple X Hotkey Daemon (sxhkd).                                                                          |
| [theme](roles/theme/)           | Manages system-wide and user-specific themes, including GTK, Qt, icons, and fonts.                                    |
| [tools](roles/tools/)            | Installs custom scripts and development tools.                               |
| [user-manager](roles/user-manager/) | Manages user accounts and sudo privileges.                                                            |
| [video](roles/video/)            | Configures video drivers and related settings.                                                           |
| [xdg](roles/xdg/)               | Manages XDG base directories and user directory configurations.                                                          |
| [xorg](roles/xorg/)             | Installs and configures the Xorg server and core X11 utilities.                                                         |
| [xwayland](roles/xwayland/)          | Configures XWayland for running X11 applications on Wayland.                                                         |

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

### Tag Summary

* **aliases**: `tools`, `shell`
* **always**: `theme`, `base`
* **amd**: `video`
* **archaudio**: `base`
* **audio**: `audio`
* **autostart**: `video`
* **avahi**: `networking`
* **backgrounds**: `theme`
* **base**: `base`
* **base_pkgs**: `base`
* **cache**: `base`
* **cache_update**: `base`
* **cargo**: `base`
* **chaotic_aur**: `base`
* **cleanup**: `video`
* **code-packager**: `tools`
* **config**: `rofi`
* **cpupower**: `audio`
* **crb**: `base`
* **debug**: `video`
* **dnf_config**: `base`
* **dnf_configuration**: `base`
* **docker**: `docker`
* **docker_pkgs**: `docker`
* **dunst**: `dunst`
* **env**: `xorg`, `tools`
* **epel**: `base`
* **fabric**: `tools`
* **firewalld**: `firewalld`
* **folders**: `sway`, `i3`, `user-manager`
* **fonts**: `theme`
* **functions**: `shell`
* **getty**: `display-manager`
* **gpu**: `video`
* **greetd**: `display-manager`
* **groups**: `docker`
* **grub**: `video`, `grub`
* **grub_pkgs**: `grub`
* **gtk**: `theme`
* **hosts**: `networking`
* **i3**: `i3`
* **i3_config**: `i3`
* **icons**: `theme`
* **input-remapper**: `tools`
* **intel**: `video`
* **iwd**: `networking`
* **jack**: `audio`
* **jack_pkgs**: `audio`
* **kernel**: `video`
* **keybindings**: `i3`, `sxhkd`
* **keymap**: `base`
* **libvirt**: `libvirt`
* **locale**: `base`
* **modprobe**: `audio`
* **monitors**: `video`
* **musikcube**: `nas`
* **nas**: `nas`
* **network**: `networking`
* **network_check**: `base`
* **networkd**: `networking`
* **networking**: `networking`
* **nfs**: `nas`, `firewalld`
* **nfstest**: `nas`
* **ntp**: `firewalld`
* **nvidia**: `video`
* **oh-my-zsh**: `shell`
* **packages**: `theme`, `nas`, `rofi`, `picom`, `xorg`, `display-manager`, `audio`, `tools`, `sway`, `xdg`, `dunst`, `i3`, `docker`, `libvirt`, `networking`, `xwayland`, `shell`, `base`, `video`, `grub`, `user-manager`
* **paru**: `base`
* **performance**: `video`
* **picom**: `picom`
* **pipewire**: `audio`
* **pipewire_pkgs**: `audio`
* **plugins**: `shell`
* **power**: `video`
* **powertools**: `base`
* **profile**: `theme`, `sxhkd`, `shell`
* **pulseaudio**: `audio`
* **pulseaudio_pkgs**: `audio`
* **qt**: `theme`
* **repo_check**: `base`
* **repo_setup**: `base`
* **repositories**: `base`
* **repos**: `base`
* **rofi**: `rofi`
* **rpmfusion**: `base`
* **rsyncd**: `nas`, `firewalld`
* **rtirq**: `audio`
* **rtkit**: `audio`
* **ruby**: `ruby`
* **rvm**: `ruby`
* **samba**: `nas`
* **service**: `video`
* **setup**: `docker`
* **shell**: `shell`
* **shell_pkgs**: `shell`
* **ssh**: `firewalld`
* **status**: `base`
* **sudo**: `user-manager`
* **sudoers**: `user-manager`
* **sway**: `sway`
* **sxhkd**: `sxhkd`
* **sysctl**: `audio`
* **systemd-mounts**: `networking`
* **systemd-networkd**: `networking`
* **theme**: `grub`
* **timezone**: `base`
* **tools**: `tools`
* **tuned**: `audio`
* **tuning**: `audio`
* **udev**: `networking`
* **updatedb**: `base`
* **update_cache**: `base`
* **user**: `video`, `user-manager`
* **vagrant**: `libvirt`
* **validation**: `video`
* **video**: `video`
* **whisper-stream**: `tools`
* **wireless**: `networking`
* **x**: `xorg`
* **x11**: `video`
* **xdg**: `xdg`
* **xorg**: `xorg`
* **xprofile**: `xorg`
* **xwayland**: `xwayland`
* **zsh**: `shell`
* **zsh_functions**: `shell`
* **zprofile**: `shell`

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
