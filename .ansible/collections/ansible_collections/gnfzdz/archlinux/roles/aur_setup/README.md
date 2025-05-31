# Ansible Role - gnfzdz.archlinux.aur_setup

Prepare the system to manage aur packages from Ansible. The default configuration uses the aur helper pikaur and leverages it's support for systemd dynamic users to actually build the packages. If another aur helper is configured -or- dynamic users are not believed to be available (ex: running inside an unpriveleged container or chroot), a custom build user with passwordless sudo will be created instead.

## Usage
-------

### Prepare for aur management with a dedicated aur user

```yaml
- vars:
    archlinux_aur_dynamic_user: False
# Based on the above variable, the below defaults are set. You can override them to suite your needs.
#    archlinux_aur_helper: "pikaur"
#    archlinux_aur_become: Yes
#    archlinux_aur_become_user: "aurbuilder"
#    archlinux_aur_create_user: Yes 
  roles:
  - role: gnfzdz.archlinux.aur_setup
```

### Prepare for aur management with pikaur and systemd dynamic users

```yaml
- vars:
    archlinux_aur_dynamic_user: True
# Based on the above variable, the below defaults are set. You can override them to suite your needs.
#    archlinux_aur_helper: "pikaur"
#    archlinux_aur_become: No
#    archlinux_aur_become_user: "root"
#    archlinux_aur_create_user: No
  roles:
  - role: gnfzdz.archlinux.aur_setup
```

### Directly use kewlfft.aur.aur module

```yaml
- vars:
    archlinux_aur_dynamic_user: True/False
  roles:
  - role: gnfzdz.archlinux.aur_setup
  tasks:
  - name: Install a package from the aur
    kewlfft.aur.aur:
      name: "spotify"
      state: "present"
      use: "{{ archlinux_aur_helper }}"
    become: "{{ archlinux_aur_become }}"
    become_user: "{{ archlinux_aur_become_user }}"
```

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`archlinux_aur_helper` | A helper used for interacting with the aur. | str | pikaur
`archlinux_aur_dynamic_user` | A flag controlling whether to use systemd dynamic users to build aur packages | bool | "{{ not (ansible_is_chroot or archlinux_aur_helper != 'pikaur' or ansible_virtualization_type == 'podman' or ansible_virtualization_type == 'docker') }}"
`archlinux_aur_username` | The name of a permanent user to use when building aur packages. This value is ignored if `archlinux_aur_dynamic_user` is `True` | str | aurbuilder
`archlinux_aur_create_user` | Whether to create the user indicated by `archlinux_aur_username`. The user will be configured with passwordless sudo. Regardless of the value, this process is skipped if `archlinux_aur_dynamic_user` is `True`. | bool | True

The contents of the below variables are populated based on the above configuration. They may be useful when directly using the kewlfft.aur.aur module or performing other operations related to the aur.

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`archlinux_aur_become` | Whether to become a new user when managing aur packages. You shouldn't need to configure this flag directly. | bool | "{{ not archlinux_aur_dynamic_user }}"
`archlinux_aur_become_user` | A user to become when managing aur packages. The indicated user requires passwordless sudo. | str | "{{ 'root' if archlinux_aur_dynamic_user else archlinux_aur_username }}"
