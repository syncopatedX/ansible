# Ansible Role - gnfzdz.network.autoconfigure

A meta role including all other roles within the gnfzdz.network collection

## Variables
-------
Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_autoconfigure_bluetooth` | A flag indicating whether bluetooth should automatically be configured for the system | bool | No
`network_autoconfigure_manager` | Indicates the daemon to use for network management. One of `systemd-networkd`, `network-manager`, or `none`. | str | networkd

## Examples
-------

### Automatically configure system networking

```yaml
- name: Configure system networking
  ansible.builtin.import_role:
      name: 'gnfzdz.network.autoconfigure'
```

### Automatically configure GUI controls for system networking

```yaml
- name: Configure system networking
  ansible.builtin.import_role:
      name: 'gnfzdz.network.autoconfigure'
      tasks_from: "gui"
```
