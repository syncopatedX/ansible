# Ansible Role - gnfzdz.base.locale

This role configures locales for use by GCC and other system components.

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`base_locale` | A dict of locale categories and their desired value. See [here](https://sourceware.org/glibc/wiki/Locales) for more information. | dict of string | { 'LANG': 'en_US.UTF-8' }
