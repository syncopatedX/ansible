# Ansible Role - gnfzdz.base.kernel_cmdline

This role is intended to provided support for configuring the kernel cmdline in a way that decouples the configuration from any specific bootloader. The role accomplishes this objective by maintaining a facts file local to each host where the cmdline parameters are written and providing a variable that is the result of reading these local facts and appropriately formatting them to a single set of command line parameters (for use by a specific bootloader role).

## Limitations
-------

This role doesn't support multiple sets of command line parameters for use with different entries.

Before using the provided cmdline parametes, you should always attempt to refresh ansible local facts


## Usage
-------

### Add/update/delete kernel cmdline parameters

```yaml

- name: Configure kernel cmdline for apparmor
  ansible.builtin.include_role:
    name: "gnfzdz.base.kernel_cmdline"
    tasks_from: "parameters.yml"
  loop:
      - name: apparmor
        value: 1
        state: present 
      - name: selinux
        state: absent
      - name: security
        value: apparmor
        state: present
  loop_control:
    loop_var: parameter

```

### Use the full set of configured cmdline parameters

```yaml

# More likely this would be configured as a role dependency
- name: Configure kernel cmdline for apparmor
  ansible.builtin.import_role:
    name: "gnfzdz.base.kernel_cmdline"

- name: Refresh custom local facts
  ansible.builtin.setup:
    filter: ansible_local

# Or more likely generate a configuration file using the cmdline parameters
- name: Print the full cmdline entry
  ansible.builtin.debug:
    msg: "{{ boot_cmdline_full }}"

```
