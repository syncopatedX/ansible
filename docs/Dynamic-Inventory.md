# Dynamic Inventory Script Fixed with Group Support and YAML Export

I've successfully enhanced the dynamic inventory script with several key improvements:

1. **Fixed the Inventory Format**: The script now generates the correct Ansible inventory structure with:
   - "hosts" as a list instead of a dictionary
   - Host variables in the "_meta.hostvars" section
   - Proper structure that Ansible can parse correctly

2. **Added Group Support**: The script now maintains the same group structure as your inventory.ini file:
   - Hosts are assigned to their proper groups (dev, virt, pi)
   - Group hierarchy is preserved (workstation → dev, server → virt)
   - Group variables like "rvm_install" are correctly applied
   - Host-specific overrides (like soundbot's local connection) are applied

3. **Added YAML Export Capability**: You can now export the dynamic inventory to a YAML file:
   - Use `--yaml` to print the inventory in YAML format to stdout
   - Use `--export <filename>` to save the inventory to a YAML file
   - The exported YAML is fully compatible with Ansible's inventory format
   - Uses YAML anchors and references to avoid duplication

4. **Added Filtering for Unmanaged Hosts**: The script now includes:
   - IP whitelist filtering to exclude unmanaged devices (like the router at 192.168.41.1 and other devices)
   - Improved duplicate detection to avoid adding the same host twice
   - Better error handling and logging

5. **Added Configuration Options**:
   - Option to enable/disable subnet scanning completely
   - Support for a configuration file (dynamic_inventory.cfg)
   - Debug mode for troubleshooting (enabled with ANSIBLE_INVENTORY_DEBUG=true)
   - Sample config generation with `--config` parameter

## How Groups Work in the Dynamic Inventory

The script now maintains the same group structure as your static inventory:

1. **All hosts** are placed in the "all" group
2. **Group assignments** are based on the hostname:
   - "dev" group: soundbot, lapbot, ninjabot
   - "virt" group: crambot
   - "pi" group: steve
3. **Group hierarchy** is maintained:
   - "workstation" is a parent group of "dev"
   - "server" is a parent group of "virt"
4. **Host-specific variables** are applied from:
   - The dynamic inventory script (basic connection details)
   - Group variables (like rvm_install=true)
   - Host-specific overrides (like soundbot's local connection)
   - Your existing host_vars files (which Ansible reads automatically)

## Using YAML Export

You can now export the dynamic inventory to a YAML file that's compatible with Ansible's inventory format:

```bash
# Print the inventory in YAML format
./inventory/dynamic_inventory.py --yaml

# Export the inventory to a YAML file
./inventory/dynamic_inventory.py --export inventory_export.yml
```

The exported YAML file can be used directly as an Ansible inventory:

```bash
# Use the exported inventory
ansible-inventory -i inventory_export.yml --graph
ansible-playbook -i inventory_export.yml playbooks/full.yml --list-hosts
```

This allows you to:

1. Generate a static inventory file from the dynamic discovery
2. Review and potentially edit the inventory before using it
3. Share the inventory with others who might not have access to your dynamic inventory script
4. Use the generated inventory file with other tools that might not support dynamic inventory scripts

## Testing and Usage

You can test the inventory structure with:

```bash
# Show the inventory graph
ansible-inventory -i inventory/dynamic_inventory.py --graph

# List hosts in specific groups
ansible-playbook -i inventory/dynamic_inventory.py playbooks/full.yml --list-hosts --limit dev
ansible-playbook -i inventory/dynamic_inventory.py playbooks/full.yml --list-hosts --limit workstation
```

For debugging, you can use:

```bash
# Run with debug output
ANSIBLE_INVENTORY_DEBUG=true ./inventory/dynamic_inventory.py --list
```

The script now provides a complete replacement for your static inventory.ini file, with the added benefits of dynamic host discovery and YAML export capabilities.
