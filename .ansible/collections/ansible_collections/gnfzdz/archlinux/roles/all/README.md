# Ansible Role - gnfzdz.archlinux.all

A meta role automatically applying all ArchLinux configuration within the gnfzdz.archlinux collection

## Usage
-------

### Install a collection of packages from the official repositories and aur

```yaml
vars:
    archlinux_pacman_packages_auto:
        - btrfs-progs
    archlinux_aur_packages_auto:
        - zfs-utils
        - zfs-dkms
tasks:
-   name: Prepare to use aur packages
    ansible.builtin.import_role:
        name: "gnfzdz.archlinux.all"

```


## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`archlinux_aur_enabled` | A flag controlling whether to setup support for the Arch User Repository | bool | True
