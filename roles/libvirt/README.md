# libvirtd

## Overview

This Ansible role is designed to set up and configure a libvirt virtualization environment on a target system, likely an Arch Linux based system given the use of `pacman`. It handles package installation, configuration of libvirtd and related services, user management for libvirt access, and optionally installs Vagrant.

Here's a breakdown:

**What the Role Does:**

1. **Package Management:**

    - Removes `exfat-utils` if present, likely to avoid conflicts.
    - Installs a list of essential libvirt-related packages defined in `packages__libvirt`. These include `libvirt` itself, `qemu-full`, `virt-manager`, `virt-install`, `libguestfs`, etc.
    - Conditionally installs `vagrant` if the `use_vagrant` variable is set to `true`.
2. **Configuration:**

    - **Libvirtd Configuration (`/etc/libvirt/libvirtd.conf`):** Copies a predefined `libvirtd.conf` file. This file likely contains settings to adjust socket group ownership and permissions, potentially for allowing non-root user access or remote access.
    - **QEMU Bridge ACL (`/etc/qemu/bridge.conf`):** Copies a predefined `bridge.conf` file. This is typically used to define an Access Control List (ACL) for network bridges, specifying which bridges QEMU/KVM virtual machines are allowed to use (e.g., allowing `br0`).
    - **LVM Configuration (`/etc/lvm/lvm.conf`):** Modifies the LVM configuration to disable `lvmetad` by setting `use_lvmetad = 0`. This is often done when `lvmetad` causes issues with libvirt's storage pool management or in certain remote access scenarios.
3. **User Management:**

    - Adds the user specified by the `user.name` variable (this variable would need to be defined elsewhere, e.g., in your playbook or inventory) to the `libvirt` and `kvm` groups. This grants the user the necessary permissions to manage virtual machines without needing root privileges.
4. **Service Management:**

    - Enables and starts the `libvirtd` service if the `libvirt.service` variable is set to `"enabled"`.

**Role Variables and Customization:**

Here are the key variables you can use to customize the role's behavior. You would typically set these in your Ansible playbook when calling the role, or in your inventory files (host_vars, group_vars).

1. **`packages__libvirt`**

    - **File:** `vars/main.yml`
    - **Default Value:**YAML

        ```yaml
        packages__libvirt:
          - dmidecode
          - dnsmasq
          - edk2-ovmf
          - libguestfs
          - libvirt
          - qemu-full
          - virt-install
          - virt-manager
          - virt-viewer
        ```

    - **Purpose:** Defines the list of packages to be installed for the libvirt environment.
    - **How to Customize:** You can override this variable in your playbook or inventory to add or remove packages from this list. For example, if you don't need `virt-manager` (the GUI tool), you could provide a modified list. However, since it's defined in `vars/main.yml`, variables in `vars/*` have high precedence. To truly override it, you'd need to pass it directly in the playbook when calling the role, or ensure your inventory variable has higher precedence (which is generally the case for `host_vars` or `group_vars` over `roles/your_role/vars`). The most straightforward way is often to pass it as a parameter to the role in your playbook:YAML

        ```yaml
        - hosts: my_kvm_host
          vars:
            user:
              name: "your_username" # Important: Define the user for libvirt group
            packages__libvirt:
              - libvirt
              - qemu-full
              - dnsmasq
              # Add or remove other packages as needed
          roles:
            - { role: libvirt }
        ```

2. **`libvirt.service`**

    - **File:** `defaults/main.yml`
    - **Default Value:** `"disabled"`
    - **Purpose:** Controls whether the `libvirtd` service is enabled and started at boot.
    - **How to Customize:** Set this variable to `"enabled"` in your playbook or inventory to have the role enable and start the `libvirtd` service.YAML

        ```yaml
        - hosts: my_kvm_host
          vars:
            user:
              name: "your_username"
            libvirt:
              service: "enabled" # This will enable and start libvirtd
          roles:
            - { role: libvirt }
        ```

3. **`use_vagrant`**

    - **File:** Not explicitly in `defaults/main.yml` for its _primary_ use, but the task `tasks/main.yml` uses `when: use_vagrant|default(false)|bool == True`. The `defaults/main.yml` has `use_libvirt: false` which seems unrelated to this conditional.
    - **Default Value (effective):** `false` (due to the `default(false)` filter in the `when` condition).
    - **Purpose:** If set to `true`, the role will also install Vagrant using `pacman`.
    - **How to Customize:** Set this variable to `true` in your playbook or inventory if you need Vagrant installed on the target machine.YAML

        ```yaml
        - hosts: my_kvm_host
          vars:
            user:
              name: "your_username"
            libvirt:
              service: "enabled"
            use_vagrant: true # This will trigger vagrant installation
          roles:
            - { role: libvirt }
        ```

4. **`user.name`** (External Variable)

    - **File:** This variable is _not_ defined within the role's `defaults` or `vars`. It's expected to be provided externally.
    - **Default Value:** None (must be set by the user).
    - **Purpose:** Specifies the username that should be added to the `libvirt` and `kvm` groups. This allows the specified user to manage virtual machines.
    - **How to Customize:** You **must** define this variable in your playbook, inventory, or as an extra variable when running `ansible-playbook`.YAML

        ```yaml
        # In your playbook:
        - hosts: my_kvm_host
          vars:
            user:
              name: "jane_doe" # Replace with the actual username
            libvirt:
              service: "enabled"
          roles:
            - { role: libvirt }
        
        # Or in your inventory (e.g., host_vars/my_kvm_host.yml):
        # user:
        #   name: "jane_doe"
        ```

**Files Used for Configuration:**

The role uses pre-defined configuration files located (presumably) in a `files` subdirectory within the role (e.g., `roles/libvirt/files/etc/libvirt/libvirtd.conf`).

- `etc/libvirt/libvirtd.conf`: Copied to `/etc/libvirt/libvirtd.conf` on the target.
- `etc/qemu/bridge.conf`: Copied to `/etc/qemu/bridge.conf` on the target.

To customize these configurations:

1. **Modify the source files:** The most direct way is to edit these files within the role's `files` directory before running your playbook.
2. **Use `template` module:** For more dynamic configuration, you could change the tasks from using `ansible.builtin.copy` to `ansible.builtin.template`. This would allow you to use Jinja2 templating in your configuration files and control their content with more variables. You would then place template files (e.g., `libvirtd.conf.j2`) in a `templates` directory within your role.

**Example Playbook:**

Here's how you might use this role in a playbook:

YAML

```yaml
---
- hosts: kvm_servers
  become: yes # Most tasks in the role require root privileges
  vars:
    user:
      name: "your_admin_user" # The user you want to manage VMs
    libvirt:
      service: "enabled"     # Enable and start the libvirtd service
    use_vagrant: false         # Set to true if you need Vagrant

  roles:
    - role: libvirt # Assuming the role is named 'libvirt' or you provide the correct path/name
```

**Key Considerations:**

- **User `user.name`:** Ensure this variable is correctly defined, as it's crucial for granting user access to libvirt.
- **Package Manager:** The role uses `community.general.pacman`, indicating it's designed for Arch Linux or derivatives. If you need to use it on other distributions (e.g., Debian/Ubuntu with `apt`, or RHEL/CentOS with `yum`/`dnf`), you would need to significantly modify the package installation tasks.
- **Configuration Files:** The static `libvirtd.conf` and `bridge.conf` files are copied as-is. If you need different settings for different environments or hosts, consider parameterizing these files using the `template` module or managing different versions of these files and conditionally copying them.
- **Idempotency:** The role appears to be largely idempotent (running it multiple times should not cause unwanted changes), thanks to Ansible's module design (e.g., `state: present` for packages, `lineinfile` with `regexp`).
- **Handlers:** The `handlers/main.yml` is currently empty. If changes to configuration files (like `libvirtd.conf`) require the `libvirtd` service to be restarted to take effect, you would add a handler to restart the service and then `notify` that handler from the relevant configuration tasks.
