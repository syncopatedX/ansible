# Ansible Role - gnfzdz.archlinux.install

Opinionated partitioning and configuration of a new ArchLinux system

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`archlinux_install_configure_inventory` | Url of local or remote inventory to be used for provisioning the system. | str | N/A
`archlinux_install_configure_inventory_version` | The repository version to checkout when `archlinux_install_configure_inventory` refers to a git repository. The value should refer to an existing branch, tag or commit hash.  | str | main
`archlinux_install_configure_inventory_vars` | Extra variables to be written into an inventory file for use in provisioning | dict | {}
`archlinux_install_configure_local_playbook` | The path to a jinja template used to generate a playbook used for provisioning the system. After templating, the resulting playbook will be executed inside the chroot. | str | N/A
`archlinux_install_configure_remote_roles` | A list of roles to execute inside the arch-chroot. The corresponding collections will be installed from Ansible Galaxy before proceeding. Assumed to follow the format <prefix>.<collection>.<role> | list of str | gnfzdz.base.all<br>gnfzdz.security.all<br>gnfzdz.network.all<br>gnfzdz.storage.all
`archlinux_install_configure_remote_playbook` | The name of a playbook to be executed inside the arch-chroot. The owning collection will be installed from Ansible Galaxy before proceeding. Assumed to follow the format <prefix>.<collection>.<role> | str | N/A
`archlinux_install_disk_path` | A full path to a disk where ArchLinux should be installed | str | N/A
`archlinux_install_encrypt_passphrase` | A passphrase used to unlock the luks device containing the root filesystem. Required if `archlinux_install_encrypt_root` is true | str | N/A
`archlinux_install_encrypt_boot` | A flag controlling whether /boot should be encrypted by placing it inside the encrypted root rather than a separate partition. Requires `archlinux_install_encrypt_root` to be true | bool | Yes
`archlinux_install_encrypt_root` | A flag controlling whether the root filesystem should be encrypted. | bool | Yes
`archlinux_install_encrypt_autounlock` | A flag controlling whether a keyfile should be generated capable of unlocking the root filesystem. Primarily useful with encrypted /boot where GRUB will already require a passphrase and the keyfile may be used to prevent requiring the user to input their passphrase twice. | "{{ archlinux_install_encrypt_boot }}"
`archlinux_install_lvm` | A flag controlling whether the root filesystem should be placed on a LVM logical volume. If `archlinux_install_encrypt_root` is true, the LVM volume will be nested within the LUKS container. |  Yes
`archlinux_install_lvm_lv_root_size` | The size of the created logical volume for the root filesystem. Defaults to using the remainder of available space in the volume group, but you may provide another value to reserve space for later logical volume creation. | "100%FREE"
`archlinux_install_packages_dependencies` | A list of packages that must be available to proceed wtih the installation. This does not install these packages on the target arch installation. | list of str | arch-install-scripts<br>parted<br>dosfstools<br>btrfs-progs<br>cryptsetup<br>lvm2
`archlinux_install_packages_pacstrap` | A list of packages that should be installed to the new system usin pacstrap. | list of str | base<br>base-devel<br>python<br>ansible
`archlinux_install_part_esp_end` | The end position of the created EFI System Partition. The value may be provided with any unit understood by [parted](https://linux.die.net/man/8/parted) | str | "1024MiB"
`archlinux_install_part_boot_end` | The end position of the created boot partition. The value may be provided with any unit understood by [parted](https://linux.die.net/man/8/parted) | str| "512MiB"
`archlinux_install_part_root_end` | The end position of the created root partition. Defaults to using the remainder of the disk, but may be configured to a smaller value to reserve space for later partitioning. The value may be provided with any unit understood by [parted](https://linux.die.net/man/8/parted) | str | "100%"
`archlinux_install_root_fstype` | The filesystem type to format the root partition | str | btrfs
