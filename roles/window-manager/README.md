# Window Manager Role

A unified Ansible role for managing window managers, supporting both i3 (X11) and sway (Wayland).

## Role Variables

### Main Configuration

- `window_manager`: Select window manager (`i3` or `sway`, default: `i3`)
- `wm_config`: Common window manager configuration
  - `autostart`: Autostart configuration
  - `assignments`: Window assignments
  - `workspaces`: Workspace configuration
  - `keybindings`: Key bindings
  - `tray_output`: System tray output

### Terminal Configuration

- `terminal`: Primary terminal application (default: `terminator`)
- `terminal_alt`: Alternative terminal application (default: `urxvt`)

## Dependencies

None

## Example Playbook

```yaml
- hosts: workstations
  roles:
    - role: window-manager
      vars:
        window_manager: sway
        wm_config:
          autostart: "custom"
          tray_output: "DP-1"
```

## Supported Platforms

- Arch Linux

## License

GPL-2.0-or-later