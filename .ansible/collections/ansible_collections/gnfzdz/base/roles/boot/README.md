# Ansible Role - gnfzdz.base.boot

A support role providing shared default variables and stub handlers related to system initialization (bootloader, kernel, initramfs, etc). This role is only intended to be used as a dependency for other more specific roles that support this functionality and primarily serves to ensure that a common contract use used by alternative roles providing bootloader / initramfs support.

## Variables
-------

TODO update default values explaining how they are calculated. Update to identify which are documented intending to be configured by the end user vs which are documented for usage by implementation specific roles.

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`boot_mode` | Whether the system should be configured to boot based on the `uefi` or `bios` specifications. | string | bios
`boot_efi_mount_path` | The mountpoint where the efi system partition is mounted. | string | <none>
`boot_mbr_device` | The block device where the master boot record is installed | string | <none>
`boot_lvm_enabled` | Whether system boot requires support for the Linux Volume Manager.<br>This is primarily required if critical system partitions are logical volumes within a LVM partition. | string | <none>
`boot_encryption_enabled` | Whether system boot requires support for LUKS encryption.<br>This is primarily required if the system's root is located within a LUKS container. | string | <none>
`boot_encryption_device` | The block device where the LUKS container that should be mounted by the initramfs is located. | string | <none>
`boot_encryption_dm_name` | The name that should be used by the Linux device manager when opening the LUKS container. | string | <none>
`boot_encryption_keyfile` | Path to a keyfile to embed in initramfs for use in automatically unlocking the luks container. Primarily useful when /boot is within an encrypted root container initially decrypted by GRUB. The keyfile prevents the user from being prompted for the password twice. | string | <none>
`boot_root_device` | The block device containing the root filesystem. This may be a phsical partition, opened luks container, etc. The value is used to populate the [root linux cmdline parameter](https://www.kernel.org/doc/html/v4.14/admin-guide/kernel-parameters.html) | string | <none> 
`boot_root_fs_type` | The filesystem type used for the system's root. | string | <none>
