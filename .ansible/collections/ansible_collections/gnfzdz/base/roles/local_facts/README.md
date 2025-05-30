# Ansible Role - gnfzdz.base.local_facts

Create a local facts directory at /etc/ansible/facts.d for use in persisting custom local facts to the system. All <name>.facts files within this directory will be available under the `ansible_local` variable. This variable is only populated/updated when the the setup module is run at the start of a play. The variable can be manually refreshed  with the snippet below:

```yaml

- name: Refresh custom local facts
  ansible.builtin.setup:
    filter: ansible_local

```
