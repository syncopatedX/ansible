# Ansible Role - gnfzdz.archlinux.pacman

This role initiates a full system update attempting to work around common failures. Optionally enable timers for purging the pacman cache and downloading the most recent filesdb.

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`archlinux_pacman_cache_timer_enabled` | Enable a systemd timer to purge old packages | boolean | Yes
`archlinux_pacman_filesdb_timer_enabled` | Enable a systemd timer to refresh the files database | boolean | Yes
`archlinux_pacman_upgrade` | Whether to attempt an upgrade as part of role's execution | boolean | Yes
`archlinux_pacman_packages_auto` | A list of packages to automatically install. If you'd like to extend the default, the packages are available to extend in the variable `archlinux_pacman_packages_default`  | list of string | A collection of packages formerly in base: <br>base<br>base-devel<br>git<br>vim<br>nano<br>less<br>man-db<br>man-pages<br>which<br>texinfo<br>diffutils<br>usbutils<br>logrotate
