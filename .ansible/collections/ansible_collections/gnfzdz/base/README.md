# Ansible Collection - gnfzdz.base

This repository contains Ansible roles providing configuration for the core of the system including system initializating and cross-cutting functionality

## Roles

Name | Description
-------- | -----------
[gnfzdz.base.all](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/all/README.md) | A meta role automatically applying all configuration within this collection
[gnfzdz.base.boot](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/boot/README.md) | A support role providing a common contract and defaults for variables and handlers related to system boot. This role is intended to be a dependency for roles providing configuration of bootloaders, initramfs, etc
[gnfzdz.base.dotfiles](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/dotfiles/README.md) | Install and configure a user's dotfiles from a public git repository
[gnfzdz.base.grub](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/grub/README.md) | Install and configure the grub bootloader
[gnfzdz.base.kernel](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/kernel/README.md) | Install the Linux kernel and supporting packages
[gnfzdz.base.kernel_cmdline](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/kernel_cmdline/README.md) | Provides a mechanism to set individual linux command line parameters while remaining decoupled from any specific bootloader configuration format.
[gnfzdz.base.kernel_parameters](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/kernel_parameters/README.md) | Provides support for setting override kernel parameters from inventory and handlers to reload all kernel parameters.
[gnfzdz.base.lifecycle](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/lifecycle/README.md) | Provides handlers to reboot the system
[gnfzdz.base.local_facts](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/local_facts/README.md) | Creates a directory on the host to store custom Ansible facts about the system.
[gnfzdz.base.locale](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/locale/README.md) | Configures the system's locale as used by GCC and other tools
[gnfzdz.base.microcode](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/microcode/README.md) | Installs the appropriate microcode based on the detected processor
[gnfzdz.base.mkinitcpio](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/mkinitcpio/README.md) | Configures mkinitcpio used to generate the system's initial ram filesystem
[gnfzdz.base.systemd](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/systemd/README.md) | Systemd configuration and handlers related to the core init daemon
[gnfzdz.base.time](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/time/README.md) | Configures the system's time zone and hardware clock
[gnfzdz.base.user](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/user/README.md) | Create and/or configure local users based on inventory variables

## Plugins

### [filter] gnfzdz.base.dict2ini
Converts a structure of nested dicts (with depth=2) intended to represent ini configuration into a list of contains containing the paired section, option and value. This filter is intended for use with the module [community.general.ini_file](https://docs.ansible.com/ansible/latest/collections/community/general/ini_file_module.html)

Given the below configuration
```yaml
config:
    Settings:
        AutoConnect: True
        Hidden: False
    Security:
        Passphrase: 'letmein'

```

```jinja
"{{ config | gnfzdz.base.dict2ini }}"

```

```json
[
    { "section": "Settings", "option": "AutoConnect", "value": true },
    { "section": "Settings", "option": "Hidden", "value": false },
    { "section": "Security", "option": "Passphrase", "value": "letmein" }
]
```

### [lookup] gnfzdz.base.prefix
Finds all variables starting with the provided prefix and returns as a dict where the keys have the prefix removed.


```yaml
other_data: True

my_namespace_flag: True
my_namespace_version: 1
my_namespace_items:
    - "a"
    - "b"
    - "c"

other_other_data: True
```

```jinja
"{{ lookup('gnfzdz.base.prefix', 'my_namespace_') }}"
```

```json
{
    'flag': true,
    'version': 1,
    'items': [
        "a",
        "b",
        "c"
    ]
}
```
