# Ansible Workstation Archlinux

This Ansible playbook automates the configuration of a development-focused workstation, primarily targeting Arch Linux and its derivatives. It leverages Ansible roles for modularity and maintainability, setting up everything from base system utilities to a complete development environment.

## Table of Contents

- [Ansible Workstation Archlinux](#ansible-workstation-archlinux)
 	- [Table of Contents](#table-of-contents)
 	- [Features](#features)
 	- [Requirements](#requirements)
 	- [Installation](#installation)
 	- [Usage](#usage)
 	- [Customization](#customization)
 	- [Roles Overview](#roles-overview)
 	- [Playbook Structure](#playbook-structure)
 	- [Contributing](#contributing)
 	- [License](#license)
 	- [Troubleshooting](#troubleshooting)

## Features

This playbook provides a comprehensive workstation setup, including:

- **Base System:**
  - Package manager configuration (pacman, paru).
  - Repository setup (archaudio, chaotic-aur).
  - System utilities (mlocate, reflector).
  - Mirrorlist update automation.
- **User Environment:**
  - User account creation and configuration.
  - Shell customization (zsh, oh-my-zsh, aliases).
  - Terminal emulator setup (kitty).
  - File manager configuration (ranger).
  - Optional passwordless sudo/polkit.
- **Containerization & Virtualization:**
  - Docker installation and configuration (including NVIDIA support).
  - Libvirt installation and configuration (with Vagrant support).
- **X11 & Window Manager:**
  - Xorg installation.
  - i3 window manager setup.
  - Rofi application launcher.
  - sxhkd (Simple X Hotkey Daemon).
  - XDG Base Directory Specification compliance.
- **Development Tools:**
  - Ruby environment setup (rvm, bundler, gems).
  - Custom tools: `code-packager` and `whisper-stream`.
- **Input Device Management:**
  - `input-remapper` installation and configuration.
- **Homepage:**
  - Sets a simple static homepage.

## Requirements

- **Ansible:** Version 2.9 or higher is recommended.
- **Target Host:** An Arch Linux-based distribution.  While some tasks are distribution-agnostic, the playbook is primarily tested and designed for Arch.
- **SSH Access:** Ansible requires SSH access to the target host(s).
- **Root/Sudo Privileges:** The playbook requires root or sudo privileges to install packages and modify system configurations.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ansible-workstation.git  # Replace with your repository URL
    cd ansible-workstation
    ```

2. **Install required Ansible roles (if using Galaxy):**

    ```bash
    ansible-galaxy install -r requirements.yml  # If you have a requirements.yml file
    ```

## Usage

1. **Inventory:** Create an inventory file (e.g., `hosts`) to define your target host(s).  A minimal example:

    ```ini
    [workstation]
    myworkstation ansible_host=your_workstation_ip_or_hostname ansible_user=your_username
    ```

2. **Run the playbook:**

    ```bash
    ansible-playbook -i hosts playbooks/workstation.yml
    ```

    To use `become` (sudo) to run with elevated privileges:

    ```bash
    ansible-playbook -i hosts playbooks/workstation.yml -b
    ```

    You can also specify the user with `-u <user>`:

     ```bash
    ansible-playbook -i hosts playbooks/workstation.yml -b -u <user>
    ```

3. **Dry Run**:

   ```bash
    ansible-playbook -i hosts playbooks/workstation.yml --check
   ```

## Customization

The playbook's behavior can be customized using Ansible variables. You can define these variables in several ways:

- **Inventory file:** Add variables directly to your `hosts` file.
- **Group/Host variable files:** Create files in `group_vars/` or `host_vars/` directories.
- **Extra variables (`-e`):** Pass variables on the command line using the `-e` flag.
- **Variable files included in roles:** Some roles might include their own variable files (e.g., `roles/ruby/vars/main.yml`).

**Key Customizable Variables:**

| Variable              | Description                                                                  | Default Value |
| --------------------- | ---------------------------------------------------------------------------- | ------------- |
| `user`                | Dictionary containing user settings (name, shell, groups, sudoers, etc.)     | (See `defaults/main.yml` within relevant roles) |
| `use_docker`          | Enable/disable Docker installation and configuration.                        | `true`        |
| `use_libvirt`         | Enable/disable Libvirt installation and configuration.                       | `false`       |
| `use_vagrant`         | Enable/disable Vagrant installation (requires `use_libvirt`).               | `false`       |
| `disable_vblank`      | Disable vertical synchronization in X11.                                     | (Undefined)   |
| `debugging`         | Define to see debug messages, for example mirror status. | (Undefined) |
| `update_mirrors`      | Force update of mirrorlist. | (Undefined) |
| `nvidia`              | Enables Docker NVIDIA support. | (Undefined) |
| `rvm_install`           | Enable/disable Ruby Version Manager (RVM) installation.              | `false`        |

**Example (using extra variables):**

```bash
ansible-playbook -i hosts playbooks/workstation.yml -b -e "use_docker=false use_libvirt=true user.sudoers=true"
```

This command disables Docker, enables Libvirt, and configures passwordless sudo for the user defined in the `user` variable.

## Roles Overview

The playbook is organized into the following roles:

- **`base`:** Core system setup, package management, and repository configuration.
- **`user`:** User account management, shell configuration, and SSH key setup.
- **`docker`:** Docker installation and configuration.
- **`libvirt`:** Libvirt and Vagrant installation and configuration.
- **`x11`:** X Window System setup.
- **`sxhkd`:** sxhkd configuration.
- **`rofi`:** Rofi configuration.
- **`xdg`:** XDG Base Directory Specification compliance.
- **`i3`:** i3 window manager installation and configuration.
- **`homepage`:** Homepage setup
- **`ruby`:** Ruby environment setup.

## Playbook Structure

The `playbooks/workstation.yml` file is structured into four main plays:

1. **Play #1 (workstation):**  The primary play, targeting the `workstation` host group. This play handles the majority of the workstation configuration, including all the roles mentioned above.

2. **Play #2 (workstation):** Installs the `code-packager` utility.

3. **Play #3 (all):** Installs the `whisper-stream` utility.  This play targets all hosts in the inventory.

4. **Play #4 (all):** Installs and configures `input-remapper`.  This play also targets all hosts.

## Contributing

Contributions are welcome!  Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes, ensuring that your code adheres to Ansible best practices.
4. Write tests for your changes (if applicable).
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE) (or choose another appropriate license).

## Troubleshooting

- **SSH Connectivity Issues:** Ensure that you can SSH into the target host(s) using the specified user and credentials.
- **Package Installation Errors:** Check the Ansible output for specific error messages.  Make sure your target host has a working internet connection and that the configured repositories are accessible.
- **Idempotency Problems:** If the playbook makes unintended changes on subsequent runs, review the `when` conditions and registered variables to ensure they are correctly checking for existing configurations.
- **Use the `--check` flag**: If you are unsure about the results, use the dry run mode.
