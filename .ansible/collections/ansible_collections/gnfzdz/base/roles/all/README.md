# Ansible Role - gnfzdz.base.all

A meta role automatically applying all configuration within the gnfzdz.base collection

## Usage
-------

### Enable cross cutting configuration and configure system initialization

```yaml
tasks:
-   name: Prepare to use aur packages
    ansible.builtin.import_role:
        name: "gnfzdz.base.all"

```
