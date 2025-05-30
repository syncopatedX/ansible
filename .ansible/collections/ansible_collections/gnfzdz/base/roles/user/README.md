# Ansible Role - gnfzdz.base.user

Creates and configures local users on the host

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`users_auto` | A list of user names to automatically create that should be automatically created | list of string | []
`users_default` | Default configuration to use unless overriden by a user specific option. See user variables below for an explanation of the available options. | dict | { 'shell': '/bin/bash', 'password_lock': No }
`user_{{ username }}` | Configuration for a specific user managed by this role. Allowed parameters are group, shell, home, password, password_lock and authorized_key. See [ansible.builtin.user](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html) and [ansible.posix.authorized_key](https://docs.ansible.com/ansible/latest/collections/ansible/posix/authorized_key_module.html) for an explanation of each parameter. | dict | {}

### Variables for a single user
An individual user's configuration can be provided in a dict under the variable `user_{{ username }}`. If a user's configuration contains the below properties, they will override the default configurations above.

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`group` | The primary group for the user. If not provided, the default behavior will be to create a group with the same name as the user. | str | N/A
`shell` | The default shell for the user | str | /bin/bash
`home` | A list of user names to automatically create that should be automatically created | str | /home/{{ name }}
`password` | A plain text or already hashed password | str | N/A
`password_lock` | Whether the user's account should be locked | bool | N/A
`authorized_key` | A list of user names to automatically create that should be automatically created | str or list of str | []
