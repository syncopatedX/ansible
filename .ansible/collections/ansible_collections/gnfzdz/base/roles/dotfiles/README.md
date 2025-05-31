# Ansible Role - gnfzdz.base.dotfiles

Installs dotfiles for managed user(s). This role assumes dotfiles are available in a public git repository, managed with an external tool.

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`users_dotfiles_auto` | A list of user names elligible to automatically manage dotfiles for | list of string | {{ users_auto }}
`user_{{ username }}` | Override configuration for a specific user managed by this role. See below for an explanation of the allowed attributes. | dict | {}

### Default variables for all users

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`users_dotfiles_command` | A command to execute from within the cloned repository to finish configuring the system with the dotfiles | str | make
`users_dotfiles_dependencies` | A list of dependencies that must be installed on the system to complete the dotfiles installation | list of str | [ make ]
`users_dotfiles_install_path` | A path where the dotfiles should be installed relative to the users home directory | str | .dotfiles
`users_dotfiles_source_repository_url` | The url of a public repository containing the user dotfiles | str | N/A
`users_dotfiles_source_repository_version` | The repository versio to checkout as a branch, tag or commit hash | str | main

### Variables for a single user

Similar to the [gnfzdz.base.user](https://gitlab.com/gnfzdz/gnfzdz.base/-/blob/main/roles/user/README.md) role, an individual user's configuration can be provided in a dict under the variable `user_{{ username }}`. If a user's configuration contains the below properties, they will override the default configurations above.

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`dotfiles_command` | A command to execute from within the cloned repository to finish configuring the system with the dotfiles | str | make
`dotfiles_dependencies` | A list of dependencies that must be installed on the system to complete the dotfiles installation | list of str | [ make ]
`dotfiles_install_path` | A path where the dotfiles should be installed relative to the users home directory | str | .dotfiles
`dotfiles_source_repository_url` | The url of a public repository containing the user dotfiles | str | N/A
`dotfiles_source_repository_version` | The repository versio to checkout as a branch, tag or commit hash | str | main
