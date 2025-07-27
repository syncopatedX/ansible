# Migration Guide: i3 Roles to Collection

This document explains the migration of i3-related roles from the main ansible project to the `syncopated.i3_desktop` collection.

## What Changed

### Moved Roles
The following roles have been moved from `ansible/roles/` to the collection:
- `i3` → `syncopated.i3_desktop.i3`
- `dunst` → `syncopated.i3_desktop.dunst`
- `picom` → `syncopated.i3_desktop.picom`
- `sxhkd` → `syncopated.i3_desktop.sxhkd`
- `xorg` → `syncopated.i3_desktop.xorg`

### Updated Playbooks
- `playbooks/full.yml`: Now uses collection roles with `window_manager == 'i3'` conditions
- `playbooks/i3.yml`: Updated to use all collection roles
- `requirements.yml`: Added collection dependency

### Inventory Variables
All existing inventory variables remain compatible:
- `window_manager: "i3"`
- `i3:` configuration blocks
- `x:` autostart configurations
- Display and scaling variables

## Installation

```bash
# Install collection dependencies
cd ansible/
ansible-galaxy install -r requirements.yml

# This will install the local collection from ../ansible_collections/syncopated/i3_desktop/
```

## Usage

### For New Deployments
Use the collection playbook directly:
```bash
ansible-playbook -i inventory/inventory.ini \
  ../ansible_collections/syncopated/i3_desktop/playbooks/i3_setup.yml
```

### For Existing Deployments
Continue using existing playbooks - they now reference the collection automatically:
```bash
ansible-playbook -i inventory/inventory.ini playbooks/full.yml
ansible-playbook -i inventory/inventory.ini playbooks/i3.yml
```

## Backward Compatibility

- All existing inventory variables work unchanged
- All existing playbook commands work unchanged
- All existing host_vars and group_vars configurations remain valid
- Tag-based execution continues to work: `--tags "i3,dunst,picom"`

## Benefits

1. **Modularity**: i3 components are now packaged as a reusable collection
2. **Distribution**: Collection can be shared and installed independently
3. **Versioning**: Collection has its own version lifecycle
4. **Namespace**: Clear separation from other desktop environments (sway, cosmic)
5. **Maintainability**: Focused scope for i3-specific development

## Rollback

If needed, you can restore the original structure by:
1. Copying roles back from `ansible_collections/syncopated/i3_desktop/roles/` to `ansible/roles/`
2. Reverting playbook changes to use local role names
3. Removing collection references from `requirements.yml`

## Future Enhancements

With this collection structure, future development can focus on:
- Enhanced i3 configuration templates
- Additional i3-ecosystem tools (i3blocks, i3lock, etc.)
- Better multi-monitor support
- Theme integration improvements