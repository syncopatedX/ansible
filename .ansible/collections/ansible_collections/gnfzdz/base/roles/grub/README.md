# Ansible Role - gnfzdz.base.grub

This role installs and configures the GRUB bootloader. It provides handlers listening for bootloader configuration updates allowing downstream roles to request reconfiguration as needed.

## Usage
-------

### Import role using explicit import_role task or as a role dependency
```yaml

- tasks:
    -   name: Install and configure grub
        ansible.builtin.import_role:
            name: "gnfzdz.base.grub"

```

### Notify that grub should be reconfigured
```yaml

- tasks:
    -   name: Notify bootloader for update (independent of which bootloader is currently configured)
        ansible.builtin.command: echo 'do something requiring bootloader reconfiguration/installation'
        notify:
        - update bootloader

    -   name: Notify only grub bootloader for update
        ansible.builtin.command: echo 'do something that only impacts grub'
        notify:
        - update grub

```


## Variables
-------

See role [gnfzdz.base.boot](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/boot/README.md)
