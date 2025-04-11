# 🤖 Ansible Workstation Archlinux 🚀

This Ansible playbook automates the configuration of a development-focused workstation, primarily targeting Arch Linux 🐧 and its derivatives. It leverages Ansible roles for modularity and maintainability, setting up everything from base system utilities to a complete development environment.

## ✨ Features

This playbook provides a comprehensive workstation setup, including:

* **🔧 Base System:**
  * Package manager configuration (pacman, paru via custom `aur` module).
  * Repository setup (`archaudio`, `chaotic-aur`).
  * Essential system utilities (`mlocate`, `reflector`).
  * Mirrorlist update automation.
* **👤 User Environment:**
  * User account creation and configuration.
  * Shell customization (zsh, oh-my-zsh, aliases).
  * Terminal emulator setup (kitty).
  * File manager configuration (ranger).
  * Optional passwordless sudo/polkit setup.
* **📦 Containerization & Virtualization:**
  * Docker installation and configuration (including optional NVIDIA support).
  * Libvirt installation and configuration (with optional Vagrant support).
* **🖥️ X11 & Window Manager:**
  * Xorg installation and configuration.
  * i3 window manager setup.
  * Rofi application launcher.
  * sxhkd (Simple X Hotkey Daemon).
  * XDG Base Directory Specification compliance.
  * Picom compositor configuration.
  * Dunst notification daemon setup.
* **🛠️ Development Tools:**
  * Ruby environment setup (system gems, optional RVM).
  * Custom tools installation (`code-packager`, `whisper-stream`).
  * Go language environment setup.
  * Fabric (AI scripting tool) setup.
* **⌨️ Input Device Management:**
  * `input-remapper` installation and configuration.
* **🌐 Networking & Services:**
  * NetworkManager configuration.
  * Firewalld setup.
  * OpenSSH configuration.
  * NTP (Time Synchronization) via systemd-timesyncd.
  * NFS server setup (optional).
  * Samba server setup (optional).
* **📄 Homepage:**
  * Sets a simple static HTML homepage with configurable links.

## ✅ Requirements

* **Ansible:** Version 2.9 or higher recommended[cite: 1].
* **Target Host:** An Arch Linux-based distribution. While some tasks might work elsewhere, the playbook is primarily tested and designed for Arch[cite: 1].
* **SSH Access:** Ansible requires SSH access to the target host[s](cite: 1).
* **Root/Sudo Privileges:** The playbook needs root or sudo privileges to install packages and modify system configurations[cite: 1]. An `aur_builder` user is recommended for AUR operations.

## ⚙️ Installation

1. **Clone the Repository:**

    ```bash
    # Replace with your repository URL if forked
    git clone [https://github.com/your-username/syncopated-ansible.git](https://github.com/your-username/syncopated-ansible.git)
    cd syncopated-ansible
    ```

2. **(Optional) Install Ansible Roles via Galaxy:**
    If the playbook utilized external roles defined in `requirements.yml` (not present in the provided files), you would run:

    ```bash
    # ansible-galaxy install -r requirements.yml
    ```

## 🚀 Usage

### Method 1: Standard Ansible Playbook Execution

This is the typical method for running Ansible playbooks.

1. **Create/Edit Inventory:**
    Define your target host(s) in an inventory file. The default is `inventory/inventory.ini`[cite: 2]. Create or modify it.

    *Example `inventory/inventory.ini`:* [cite: 4]

    ```ini
    [all:vars]
    # Define variables applicable to all hosts
    ansible_user="{{lookup('env', 'USER')}}" # Uses environment variable USER
    ansible_connection=ssh

    [workstation:children]
    dev # Group containing development workstations

    [dev]
    # Hostname (e.g., 'my-arch-box')
    # Optional host-specific variables follow
    my-arch-box ansible_host=192.168.1.100 # Replace with actual IP or hostname

    # Example with specific settings from provided files
    ninjabot rvm_install=true # Installs RVM on ninjabot
    soundbot ansible_connection=local rvm_install=true # Runs locally on soundbot [cite: 4]
    lapbot distro=Manjaro rvm_install=false # Example for a Manjaro derivative [cite: 4, 8]

    [server:children]
    virt # Group for virtualization hosts

    [virt]
    crambot

    [pi] # Group for Raspberry Pi devices
    steve
    ```

    * **Note:** You can define variables directly here, or more commonly in `inventory/host_vars/<hostname>.yml` and `inventory/group_vars/<groupname>.yml`[cite: 5, 6, 7, 8].

2. **Run the Playbook:**
    Execute the main playbook (`main.yml` [cite: 3]) using the inventory file.

    ```bash
    # Basic execution (Ansible will likely prompt for sudo password)
    ansible-playbook -i inventory/inventory.ini main.yml

    # Using 'become' (-b) for privilege escalation (sudo)
    ansible-playbook -i inventory/inventory.ini main.yml -b

    # Specifying the remote user (-u) and using become (-b)
    ansible-playbook -i inventory/inventory.ini main.yml -b -u your_remote_username

    # Targeting a specific host or group (--limit)
    ansible-playbook -i inventory/inventory.ini main.yml -b --limit ninjabot
    ansible-playbook -i inventory/inventory.ini main.yml -b --limit dev
    ```

3. **Dry Run (Check Mode):**
    Simulate the playbook run without making actual changes. Useful for testing.

    ```bash
    ansible-playbook -i inventory/inventory.ini main.yml -b --check
    ```

### Method 2: Ansible Pull (Agent-based)

This method is useful for initial setup on a fresh machine or for periodic updates pulled *by* the target machine itself.

1. **Bootstrap Script (Recommended for Fresh Installs):**
    A bootstrap script (`scripts/bin/bootstrap-ansible-pull.sh`) is provided to automate the initial setup. Run this on the *target machine*:

    ```bash
    # Download and execute the bootstrap script (replace URL if needed)
    curl -sSL [https://raw.githubusercontent.com/your-username/syncopated-ansible/main/scripts/bin/bootstrap-ansible-pull.sh](https://www.google.com/search?q=https://raw.githubusercontent.com/your-username/syncopated-ansible/main/scripts/bin/bootstrap-ansible-pull.sh) | bash
    ```

    This script installs prerequisites (git, ansible), clones the repository, and runs `ansible-pull` with detected user info.

2. **Manual `ansible-pull` Execution:**
    Run this command on the *target machine*:

    ```bash
    # Replace with your repository URL
    sudo ansible-pull -U [https://github.com/your-username/syncopated-ansible.git](https://github.com/your-username/syncopated-ansible.git) main.yml
    ```

    * `ansible-pull` clones/updates the repository locally and then runs the specified playbook (`main.yml` by default if not specified) against `localhost`.

3. **Customizing `ansible-pull`:**
    Pass extra variables (`-e`) to customize the pull:

    ```bash
    # Example overriding user details
    sudo ansible-pull -U [https://github.com/your-username/syncopated-ansible.git](https://github.com/your-username/syncopated-ansible.git) main.yml \
      -e "user_name=myuser" \
      -e "user_home=/home/myuser" \
      -e "user_shell=/bin/zsh"

    # Example skipping docker and libvirt roles using tags
    sudo ansible-pull -U [https://github.com/your-username/syncopated-ansible.git](https://github.com/your-username/syncopated-ansible.git) main.yml --skip-tags "docker,libvirt"

    # Example running only base and user roles
    sudo ansible-pull -U [https://github.com/your-username/syncopated-ansible.git](https://github.com/your-username/syncopated-ansible.git) main.yml --tags "base,user"
    ```

## 🎨 Customization

Tailor the playbook using Ansible variables.

* **Locations:**
  * Inventory file (`inventory/inventory.ini`) [cite: 4]
  * Group Variables (`inventory/group_vars/all/`, `inventory/group_vars/<groupname>/`) [cite: 5, 6, 7]
  * Host Variables (`inventory/host_vars/<hostname>.yml`) [cite: 8]
  * Role Defaults (`roles/<rolename>/defaults/main.yml`) - Lowest priority.
  * Command Line (`-e "var=value"`) - Highest priority.
* **Key Variables (Examples):**
  * `user`: Dictionary defining user details [name, group, uid, home, shell, sudoers status](cite: 6).
  * `use_docker`: `true`/`false` to enable/disable Docker role.
  * `use_libvirt`: `true`/`false` to enable/disable Libvirt role.
  * `use_vagrant`: `true`/`false` to enable/disable Vagrant (requires `use_libvirt=true`)[cite: 1].
  * `nvidia`: Set to `true` (or any value) to enable Docker NVIDIA support[cite: 1].
  * `rvm_install`: `true`/`false` to enable/disable RVM installation.
  * `zsh_theme`: Set the desired Oh My Zsh theme.
  * `packages`: Lists of packages to install per role (defined in `vars/main.yml` and role vars).
  * `colors`: Defines color schemes used by various components [e.g., terminal, i3](cite: 5).
  * `i3`: Dictionary for i3 settings (autostart commands, workspace assignments, keybindings, tray output).
  * `x`: Dictionary for X11 settings (autostart commands).
  * `homepage_groups`, `homepage_intranet_hosts`: Define links for the static homepage.
  * `network_interfaces`: List of dictionaries defining network interface configurations.
* **Example (Command Line Override):**

    ```bash
    ansible-playbook -i inventory/inventory.ini main.yml -b -e "use_docker=false" -e "user.name=newuser"
    ```

## 🏷️ Using Tags

Run specific parts of the playbook using tags defined in `main.yml` [cite: 3] and role tasks.

* **Run Only Specific Tags:**

    ```bash
    # Run only base setup and user configuration tasks
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "base,user"

    # Run only networking and firewall tasks
    ansible-playbook -i inventory/inventory.ini main.yml -b --tags "networking,firewalld"
    ```

* **Skip Specific Tags:**

    ```bash
    # Run everything EXCEPT docker and libvirt
    ansible-playbook -i inventory/inventory.ini main.yml -b --skip-tags "docker,libvirt"
    ```

* **List Available Tags:**

    ```bash
    ansible-playbook -i inventory/inventory.ini main.yml --list-tags
    ```

## 🧩 Roles Overview

The playbook is organized into modular roles found in the `roles/` directory:

* `base`: Core system, packages, user, shell
* `docker`: Docker & Docker Compose
* `fabric`: Fabric AI tool
* `firewalld`: Firewall configuration
* `fonts`: Font installation (tasks seem empty currently)
* `grub`: GRUB bootloader tweaks
* `homepage`: Static HTML homepage setup
* `i3`: i3 Window Manager, i3status-rust, Rofi
* `input-remapper`: Input device mapping
* `libvirt`: Libvirt & Vagrant
* `lightdm`: LightDM Display Manager (tasks seem empty currently)
* `media`: Media server components (e.g., Musikcube)
* `nas`: NFS & Samba server configuration
* `networking`: NetworkManager and interface configuration
* `ntp`: Time synchronization
* `ruby`: Ruby environment (System gems, RVM optional)
* `ssh`: OpenSSH server/client setup
* `tools`: Custom scripts (`code-packager`, `whisper-stream`)
* `x`: X11 server, drivers, utils (picom, dunst), sxhkd, XDG dirs

*(Refer to individual `roles/<role_name>/tasks/main.yml` for specifics)*

## 🤔 Troubleshooting

* **SSH Issues:** Ensure SSH connectivity to the target host with the correct user and authentication method. Check firewall rules (`firewalld` role, `ssh` role).
* **Package Errors:** Check Ansible output for specific `pacman` or AUR helper errors. Ensure the target host has internet access and configured repositories are reachable. Verify the `aur_builder` user (if used) has passwordless `pacman` rights.
* **Idempotency Problems:** If the playbook makes unexpected changes on subsequent runs, review task `when` conditions and ensure checks for existing configurations are correct.
* **Check Mode:** Use `ansible-playbook --check` to preview changes before applying them.
* **Variable Issues:** Use `-v` or `-vvv` flags with `ansible-playbook` for verbose output to see how variables are being interpreted. Ensure variables are defined in the correct precedence scope (host > group > inventory > role defaults). Check `ansible.cfg` for `error_on_undefined_vars = True`[cite: 2].

## 🤝 Contributing

Contributions are welcome! Please fork the repository, create a feature branch, make your changes following Ansible best practices, and submit a pull request.

## 📜 License

Please refer to the `LICENSE` file (not provided in the context, assuming MIT based on a template reference).
