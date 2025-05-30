# Ansible Role - gnfzdz.archlinux.pikaur

This role installs the aur helper pikaur using only core Ansible tasks.

## Purpose
-------
The purpose of this module is to install the aur helper pikaur without using the primary community provided aur module kewlfft.aur.aur. This module recommends executing as a non-root user configured with passwordless sudo. Pikaur (when run as root) has the capability to execute the package build as a systemd dynamic user and as root install the built package. This combination means that no user with passwordless root is required.

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`archlinux_pikaur_bootstrap_version` | A git tag, branch or commit to be used from the pikaur repository for bootstrapping the installation of Pikaur. Note, the final installed version will actually be based on the aur pkgbuild. | str | "707c66f597cf20c1f301becda462c4c3556f0f3a"

## Issues
------
* Systemd's dynamic user functionality fails to create required namespaces when executed within an unpriveleged container
