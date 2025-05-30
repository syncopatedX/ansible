# Ansible Role - gnfzdz.network.openssh

Install and configure the openssh daemon

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_openssh_service_config_template` | The path to a jinja template used to prepare the sshd_config. The default template is entirely static based on the upstream default configuration, but with both PermitRootLogin and PasswordAuthentication set to `no`. | str | `sshd_config.j2`
`network_openssh_service_enabled` | A flag indicating whether the sshd should automatically started on system boot. | bool | `True`
`network_openssh_service_name` | The name of the openssh server service. | str | distribution specific name
`network_openssh_service_packages` | A list of packages to install for the openssh server. | list of str | distribution specific list of packages
