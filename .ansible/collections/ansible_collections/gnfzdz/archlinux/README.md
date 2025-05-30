# Ansible Collection - gnfzdz.archlinux

This repository contains Ansible roles specific to configuring an ArchLinux (or derivative) system.

## Roles

Name | Description
-------- | -----------
[gnfzdz.archlinux.all](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/all/README.md) | A meta role automatically applying all ArchLinux configuration within this collection
[gnfzdz.archlinux.aur](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/aur/README.md) | A meta role for aur setup/installation providing api compatability with earlier versions of the collection. This role delegates to [gnfzdz.archlinux.aur_setup](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/aur_setup/README.md) and [gnfzdz.archlinux.aur_install](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/aur_install/README.md) for common setup and package installation/upgrades respectively.
[gnfzdz.archlinux.aur_install](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/aur_install/README.md) | Build/install/update packages from the aur. This role provides a simple wrapper around the [kewlfft.aur.aur module](https://galaxy.ansible.com/kewlfft/aur) using the configuration setup in [gnfzdz.archlinux.aur_setup](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/aur_setup/README.md) and optionally configures additional trusts pgp keys for use when validating sources from the aur.
[gnfzdz.archlinux.aur_setup](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/aur_setup/README.md) | Prepare the system to manage aur packages from Ansible by either creating a user with passwordless sudo or pre-installing pikaur which can instead use systemd dynamic users for the builds. This role is intended for use with the [kewlfft.aur.aur module](https://galaxy.ansible.com/kewlfft/aur)
[gnfzdz.archlinux.install](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/install/README.md) | Opinionated partitioning and configuration of a new ArchLinux system
[gnfzdz.archlinux.install_prompt](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/install_prompt/README.md) | Interactive prompt for configuration of a new ArchLinux installation.
[gnfzdz.archlinux.pacman](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/pacman/README.md) | Initiate a full system update attempting to work around common failures. Optionally enable timers for purging the pacman cache and downloading the most recent filesdb.
 [gnfzdz.archlinux.pikaur](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/pikaur/README.md) | Install the aur helper 'pikaur' without requiring creation of a user with password-less sudo. This is automatically imported by the aur role as kewlfft.aur.aur requires creation of a user with passwordless sudo unless pikaur is already available.

## Usage

### Apply all configurations, including full system upgrade and package installations

```yaml
vars:
    archlinux_pacman_upgrade: Yes
    archlinux_pacman_packages_auto:
        - 'btrfs-progs'
    archlinux_aur_upgrade: Yes
    archlinux_aur_trustedkeys_auto:
      - '4F3BA9AB6D1F8D683DC2DFB56AD860EED4598027'
      - 'C33DF142657ED1F7C328A2960AB9E991C6AF658B'
    archlinux_aur_packages_auto:
      - 'zfs-utils'
      - 'zfs-dkms'
roles:
- role: 'gnfzdz.archlinux.all'

```

### Install packages from the aur


```yaml
- tasks:
  - name: Prepare to use aur packages
    ansible.builtin.include_role:
      name: "gnfzdz.archlinux.aur_install"
    vars:
      archlinux_aur_install_packages:
      - zfs-utils
      archlinux_aur_install_trustedkeys:
      - '4F3BA9AB6D1F8D683DC2DFB56AD860EED4598027'
      - 'C33DF142657ED1F7C328A2960AB9E991C6AF658B'
```

## Variables
See relevant role for configuration
