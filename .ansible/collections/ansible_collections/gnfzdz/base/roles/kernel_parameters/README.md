# Ansible Role - gnfzdz.base.kernel_parameters

This role provides support for specifying override linux parameters from Ansible inventory and a handler to reload the parameters

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`base_kernel_parameters_overrides` | A dictionary where each key/value pair is the the kernel parameter name and the override value  | dictionary of string=>string | {}
`base_kernel_parameters_overrides_name` | A descriptive name used for the configuration file containing the override kernel parameters | string | overrides
`base_kernel_parameters_overrides_priority` | A number indicating the prescedence of the provided kernel parameters. High numbers have a higher prescedence. | int | 99
