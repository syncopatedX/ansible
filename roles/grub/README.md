# Ansible Role: GRUB Configuration

## Description

This role configures the GRUB bootloader settings on Linux systems. It allows for customization of kernel parameters, enables GRUB submenus, sets the default boot entry to be the last saved entry, and can install a GRUB hook for automatic updates (specifically for Arch User Repository - AUR).

The primary configuration file targeted by this role is `/etc/default/grub`. After making changes, the role triggers a handler to rebuild the GRUB configuration using `grub-mkconfig`.

## Requirements

- Ansible 2.1 or higher.

- The target system must use GRUB as the bootloader for the tasks to be effective.

- If using the `grub-hook` installation task, an AUR helper (like `yay` or `paru`) that the `ansible.builtin.aur` module can use must be configured on Arch-based systems.

- Root or sudo privileges on the target machine to modify `/etc/default/grub` and run `grub-mkconfig`.

## Role Variables

The following variables can be set to customize the behavior of this role. Default values are defined in `defaults/main.yml`.

### General Configuration

- `bootloader`:

  - **Description**: Specifies the bootloader type. The handler to rebuild GRUB configuration only runs if this is set to `"grub"`.

  - **Default**: `"grub"`

  - **Example**: `bootloader: "grub"`

### Kernel Parameters

These variables control the kernel parameters passed during boot.

- `kernel_parameters_default`:

  - **Description**: Sets the `GRUB_CMDLINE_LINUX_DEFAULT` line in `/etc/default/grub`. These parameters are typically applied to normal boot entries.

  - **Default**: `"splash threadirqs mitigations=off"`

  - **How to customize**: Override this variable with a string containing all desired default kernel parameters.

  - **Example**: `kernel_parameters_default: "quiet splash loglevel=3"`

- `kernel_parameters`:

  - **Description**: Sets the `GRUB_CMDLINE_LINUX` line in `/etc/default/grub`. These parameters are applied to both normal and recovery boot entries.

  - **Default**: `"ipv6.disable=1 net.ifnames=0"`

  - **How to customize**: Override this variable with a string containing all desired kernel parameters.

  - **Example**: `kernel_parameters: "nomodeset iommu=pt"`

### GRUB Behavior

- **Enabling GRUB Submenus**:

  - **Description**: The role ensures that `GRUB_DISABLE_SUBMENU` is commented out (effectively setting it to `false` or relying on GRUB's default behavior, which is usually to enable submenus if multiple kernels of the same type are found). This is achieved by ensuring the line reads `#GRUB_DISABLE_SUBMENU=y`.

  - **Customization**: This is a fixed task. To explicitly disable submenus, you would need to manage this line outside of this role or modify the role.

- **Setting Default Boot to Saved**:

  - **Description**: The role configures GRUB to boot the last saved entry by default.

    - Sets `GRUB_DEFAULT=saved`.

    - Ensures `GRUB_SAVEDEFAULT=true` (by changing `#GRUB_SAVEDEFAULT=true` to `GRUB_SAVEDEFAULT=true`).

  - **Customization**: These are fixed tasks. To use a different `GRUB_DEFAULT` behavior (e.g., booting a specific menu entry by index), you would need to manage this line outside of this role or modify the role.

### Package Management

- `grub_pkgs` (Tag):

  - **Description**: This tag can be used to specifically run or skip the task related to installing the `grub-hook` package.

  - **Task**: Installs `grub-hook` from AUR using the `ansible.builtin.aur` module. This hook likely helps in automatically running `grub-mkconfig` after kernel updates on Arch-based systems.

  - **Customization**:

    - To skip: `ansible-playbook playbook.yml --skip-tags "grub_pkgs"`

    - To run only this: `ansible-playbook playbook.yml --tags "grub_pkgs"`

  - **Note**: This task is set to `become: false` initially, assuming the AUR helper might be run as a regular user. However, package installation typically requires privileges. The `aur` module itself might handle privilege escalation if needed, or this might require adjustment based on the specific AUR helper and system setup.

## Tasks Overview

The role performs the following main tasks:

1. **Set `GRUB_CMDLINE_LINUX_DEFAULT`**: Modifies `/etc/default/grub` to set the default kernel parameters using the `kernel_parameters_default` variable. Notifies the `Rebuild grub` handler.

2. **Set `GRUB_CMDLINE_LINUX`**: Modifies `/etc/default/grub` to set the kernel parameters for all entries using the `kernel_parameters` variable. Notifies the `Rebuild grub` handler.

3. **Enable Grub Submenus**: Ensures `GRUB_DISABLE_SUBMENU` is commented out in `/etc/default/grub`. Notifies the `Rebuild` grub handler.

4. **Enable Saved as Default (GRUB_DEFAULT)**: Sets `GRUB_DEFAULT=saved` in `/etc/default/grub`. Notifies the `Rebuild grub` handler.

5. **Enable Saved as Default (GRUB_SAVEDEFAULT)**: Sets `GRUB_SAVEDEFAULT=true` in `/etc/default/grub`. Notifies the `Rebuild grub` handler.

6. **Install grub-hook (Optional, Tagged)**: Installs the `grub-hook` package from AUR. This task includes a rescue block to output a debug message if the installation fails. Notifies the `Rebuild grub` handler.

## Handlers

- `Rebuild grub`:

  - **Description**: This handler is triggered by changes to the `/etc/default/grub` file.

  - **Action**: Executes the command `grub-mkconfig -o /boot/grub/grub.cfg`.

  - **Condition**: Only runs if the `bootloader` variable is set to `"grub"`.

## Dependencies

This role has no explicit dependencies listed in `meta/main.yml`.

## Example Playbook

Here's an example of how to use this role in a playbook:

```yaml
- hosts: all
  become: yes # Most tasks require root privileges
  roles:
    - role: your_username.grub # Or the path to the role if not from Galaxy
      vars:
        kernel_parameters_default: "quiet splash mitigations=off"
        kernel_parameters: "ipv6.disable=1 net.ifnames=0 pcie_aspm=force"
        # To skip installing grub-hook, even on Arch systems
        # ansible_playbook_run_tags: 'all,!grub_pkgs'
        # Or, more directly if the task had a conditional:
        # install_grub_hook: false # (This variable doesn't exist, just an example of a common pattern)

# Example for an Arch Linux host where you want grub-hook
- hosts: archlinux_servers
  become: yes
  roles:
    - role: your_username.grub
      vars:
        kernel_parameters_default: "quiet loglevel=3"
      tags:
        - grub_config # Apply a custom tag to the role inclusion

# To run only the grub-hook installation part on archlinux_servers
# ansible-playbook playbook.yml --tags "grub_pkgs" -l archlinux_servers
```

### Customizing Kernel Parameters

To customize kernel parameters, you would typically define `kernel_parameters_default` and/or `kernel_parameters` in your playbook, inventory variables (host_vars or group_vars), or via the command line.

**Example: group_vars/all/grub_settings.yml**

```yaml
kernel_parameters_default: "quiet splash audit=1"
kernel_parameters: "net.ifnames=0 biosdevname=0"
```

**Example: group_vars/webservers/grub_settings.yml** (Overrides defaults for webservers group)

```yaml
kernel_parameters_default: "quiet splash mitigations=auto"
```

## License

The `meta/main.yml` file specifies: `license (GPL-2.0-or-later, MIT, etc)`. Please replace this with a specific SPDX license identifier (e.g., `MIT`, `GPL-3.0-only`). The original template mentioned `BSD`.

## Author Information

This role was created by [Your Name/Organization Here].

(An optional section for the role authors to include contact information, or a website.)
