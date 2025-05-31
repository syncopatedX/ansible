# Ansible Role - gnfzdz.archlinux.aur

A meta role to configure the system for aur package management and to install new system specific packages. This role delegates to [gnfzdz.archlinux.aur_setup](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/aur_setup/README.md) to install an aur helper, (optionally) create a user for build packages and to prepare a gpg home directory to manage trust for packages sources. For package installation/upgrades, the role role [gnfzdz.archlinux.aur_install](https://gitlab.com/gnfzdz/gnfzdz.archlinux/-/blob/main/roles/aur_install/README.md) is included.

Note: this package may be deleted in a future release

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`archlinux_aur_packages_auto` | A collection of packages from the Arch User Repository to automatically install. | list of str | []
`archlinux_aur_trustedkeys_auto` | A list of keyids to automatically receive and trust for use with aur package building | list of str | []
`archlinux_aur_upgrade` | Whether to attempt an upgrade of all aur packages as part of the role. | bool | yes
