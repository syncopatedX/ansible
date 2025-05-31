# Ansible Role - gnfzdz.network.systemd_networkd_dispatcher

Install, configure and enable systemd-network dispatcher that allows configuring hook scripts executed in response to systemd-networkd events

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_systemd_networkd_dispatcher_service_enabled` | A flag controlling whether the dispatcher service should be currently started and automatically started on reboot | bool | True
