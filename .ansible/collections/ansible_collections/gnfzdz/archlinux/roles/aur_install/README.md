# Ansible Role - gnfzdz.archlinux.aur_install

Build and install packages from the Arch User Repository and configure trusted keys for source validation.

This role is primarily intended to be used with include_role by shared roles/playbooks. If you wish to indicate a full list of aur packages for installation specific to your use case, it's recommended that you use [gnfzdz.archlinux.aur](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/aur/README.md) and the `archlinux_aur_packages_auto` and `archlinux_aur_trustedkeys_auto` variables documented therein.

## Usage
-------

### Install a package from the aur
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
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`archlinux_aur_install_keyserver` | Keyserver to use when fetching pgp keys for makepkg validations | str | "hkp://keyserver.ubuntu.com:11371"
`archlinux_aur_install_packages` | A list of packages to build and install | list of str | []
`archlinux_aur_install_trustedkeys` | A list of pgp keyids trusted for use in validating package sources | list of str | []
`archlinux_aur_install_upgrade` | Whether to initiate an upgrade of installed aur packages | bool | No
