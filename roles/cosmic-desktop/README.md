# COSMIC Desktop Ansible Role

This Ansible role installs and configures the COSMIC Desktop environment across multiple Linux distributions, following a resilient design philosophy for handling this pre-release desktop environment.

## Supported Platforms

- **Arch Linux**: Uses official repositories (stable) or AUR packages (dev)
- **Fedora**: Uses official repositories (stable) or COPR (dev)
- **Pop!_OS/Ubuntu/Debian**: Uses System76 PPA repositories

## Features

- **Multi-distribution support** with automatic package mapping
- **Installation method toggle**: stable vs development packages
- **Configuration management**: RON file templating for compositor and panel settings
- **Service integration**: Display manager and session management
- **Privilege separation**: Proper AUR helper usage for Arch Linux
- **Idempotent operations**: Following Ansible best practices

## Role Variables

### Core Settings

```yaml
# Installation method: 'stable' or 'dev' 
cosmic_install_method: stable

# Installation toggles
cosmic_install_apps: true          # Install COSMIC applications
cosmic_install_greeter: true       # Install COSMIC greeter
cosmic_manage_configs: true        # Deploy configuration files
cosmic_keyring_install: true       # Install keyring support

# User configuration
cosmic_user: "{{ ansible_user_id }}"
```

### Configuration Examples

#### COSMIC Compositor Settings

```yaml
cosmic_comp_settings:
  workspaces: 6
  shortcuts:
    terminal: "Super+Return"
    launcher: "Super+Space"
    close: "Super+q"
  window_management:
    focus_follows_mouse: false
    click_to_focus: true
  animations:
    enable: true
    duration: 300
```

#### COSMIC Panel Settings

```yaml
cosmic_panel_settings:
  - id: "top_panel"
    position: "Top"
    height: 32
    autohide: false
    applets:
      - "workspaces"
      - "applications"
      - "clock"
      - "system-tray"
  
  - id: "dock"  
    position: "Bottom"
    height: 48
    autohide: true
    applets:
      - "launcher"
      - "applications"
      - "trash"
```

## Usage Examples

### Basic Installation

```yaml
- hosts: workstations
  become: true
  roles:
    - role: cosmic-desktop
      vars:
        cosmic_install_method: stable
```

### Development Installation with Custom Config

```yaml
- hosts: localhost
  connection: local
  become: true
  roles:
    - role: cosmic-desktop
      vars:
        cosmic_install_method: dev
        cosmic_comp_settings:
          workspaces: 8
          shortcuts:
            terminal: "Super+T"
            browser: "Super+B"
        cosmic_panel_settings:
          - id: "main_panel"
            position: "Top"
            applets: ["workspaces", "clock", "system-tray"]
```

### Playbook Integration

Add to your main playbook:

```yaml
roles:
  - { role: cosmic-desktop, tags: ["cosmic", "desktop"], when: "window_manager == 'cosmic'" }
```

## Tags

- `cosmic`: All COSMIC-related tasks
- `packages`: Package installation tasks
- `config`: Configuration management tasks  
- `repos`: Repository setup tasks
- `aur`: Arch Linux AUR-specific tasks
- `keyring`: Keyring setup tasks

## Dependencies

The role automatically handles dependencies based on the target distribution:

- **Arch Linux**: `base-devel`, `git` (for AUR builds)
- **Fedora**: Standard build tools via dnf
- **Debian/Ubuntu**: Essential development packages

## Architecture

This role follows the established patterns from the audio workstation framework:

- **Distribution-specific variables**: `vars/{Archlinux,Fedora,Debian}.yml`
- **Task organization**: OS-family specific task files
- **Configuration templating**: Jinja2 templates for RON files
- **Service handling**: Proper systemd service management
- **Multi-user support**: User-scoped configuration deployment

## Security Considerations

- AUR builds use dedicated non-privileged user account
- Sudo permissions are scoped to package management only  
- Configuration files maintain proper ownership and permissions
- SELinux compatibility on Fedora systems

## Troubleshooting

### Common Issues

1. **AUR build failures on Arch**: Ensure `base-devel` and `git` are installed
2. **Missing configurations**: Enable `cosmic_deploy_defaults: true` for incomplete packages
3. **Display manager conflicts**: Check `cosmic_install_greeter` setting
4. **SELinux denials**: Consider `cosmic_fedora_set_permissive: true` for development installs

### Debug Mode

Run with increased verbosity:

```bash
ansible-playbook -i inventory playbook.yml --tags cosmic -vvv
```

## License

GPL-2.0-or-later

## Contributing

This role is part of the professional audio workstation automation framework. Contributions should maintain compatibility with the multi-distribution, audio-focused design principles.
