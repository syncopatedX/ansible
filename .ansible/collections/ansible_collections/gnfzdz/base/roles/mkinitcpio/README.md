# Ansible Role - gnfzdz.base.mkinitcpio

This role configures the behavior of mkinitcpio used to generate the initramfs used as part of system boot.

## Usage
-------

### Import role using explicit import_role task or as a role dependency
```yaml

- tasks:
    -   name: Install and configure mkinitcpio
        ansible.builtin.import_role:
            name: "gnfzdz.base.mkinitcpio"

```

### Notify that grub should be reconfigured
```yaml

- tasks:
    -   name: Notify initramfs for update (independent of which tool is being used to generate it)
        ansible.builtin.command: echo 'do something requiring initramfs reconfiguration/installation'
        notify:
        - update initramfs

    -   name: Notify only mkinitcpio for update
        ansible.builtin.command: echo 'do something that only impacts mkinitcpio'
        notify:
        - update mkinitcpio

```


## Variables
-------

See role [gnfzdz.base.boot](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/boot/README.md)
