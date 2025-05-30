# Ansible Role - gnfzdz.network.bluetooth

Install/configure bluez and supporting utilities for bluetooth support

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_bluez_installed` | A flag controlling whether bluez and supporting utilities should be installed to the system | bool | True
`network_bluez_enabled` | A flag controlling whether the bluetooth service should be currently started and automatically started on reboot | bool | False
