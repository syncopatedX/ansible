# Syncopated i3 Desktop Collection

An Ansible collection for configuring a complete i3 window manager desktop environment on Linux systems. This collection provides comprehensive setup for X11-based workstations with professional-grade configurations.

## Overview

This collection includes roles for:

- **xorg**: X11 server and core utilities setup
- **i3**: i3 window manager configuration with customizable layouts
- **dunst**: Notification daemon for desktop notifications
- **picom**: X11 compositor for effects and transparency
- **sxhkd**: Simple X hotkey daemon for global key bindings

## Supported Distributions

- **Arch Linux**: Full native support with AUR integration
- **Rocky Linux 9**: Complete RHEL family support with EPEL and RPM Fusion
- **Fedora**: Native dnf package management

## Requirements

- Ansible >= 2.9
- ansible.posix collection
- Target system with X11 support
- Sudo privileges on target hosts

## Installation

### From Local Source

```bash
# Clone the repository
git clone https://github.com/b08x/OS.git
cd OS

# Install the collection
ansible-galaxy collection install ansible_collections/syncopated/i3_desktop/ -p ./collections

# Or install dependencies including this collection
ansible-galaxy install -r ansible/requirements.yml
```

### From Ansible Galaxy (when published)

```bash
ansible-galaxy collection install syncopated.i3_desktop
```

## Quick Start

### Basic Usage

1. **Set up inventory**: Copy the example inventory files and customize for your environment:

```bash
cp ansible_collections/syncopated/i3_desktop/inventory_examples/* your_inventory/
```

2. **Configure variables**: Edit the group_vars and host_vars files to match your requirements:

```yaml
# group_vars/i3_workstations.yml
window_manager: "i3"
display_manager: "lightdm"
```

3. **Run the playbook**:

```bash
# Complete i3 desktop setup
ansible-playbook -i inventory/inventory.ini \
  ansible_collections/syncopated/i3_desktop/playbooks/i3_setup.yml

# Or use individual roles in your own playbook
```

### Integration with Existing Playbooks

```yaml
---
- name: Workstation Setup
  hosts: workstations
  become: true
  roles:
    # Your base roles
    - base
    - networking
    
    # i3 desktop environment
    - syncopated.i3_desktop.xorg
    - syncopated.i3_desktop.i3
    - syncopated.i3_desktop.dunst
    - syncopated.i3_desktop.picom
    - syncopated.i3_desktop.sxhkd
```

## Configuration

### Key Variables

#### Window Manager Selection
```yaml
window_manager: "i3"  # Required for conditional role execution
```

#### i3 Configuration
```yaml
i3:
  autostart:
    - "nitrogen --restore"
    - "picom --daemon"
  tray_output: "primary"
  assignments: "default"
  workspaces:
    - "$ws1 output HDMI-1"
    - "$ws2 output DP-2"
  keybindings: "default"
```

#### Display Configuration
```yaml
primary_display_output: "DP-2"
secondary_display_output: "HDMI-1"
desired_scale: 1.5
toolkit_scale: 2
```

#### X11 Autostart
```yaml
x:
  autostart:
    - "bash ~/.screenlayout/setup.sh"
    - "redshift-gtk"
```

### Per-Host Customization

Create host-specific configurations in `inventory/host_vars/hostname.yml`:

```yaml
---
window_manager: i3

i3:
  tray_output: "HDMI-1"
  workspaces:
    - "$ws1 output HDMI-1"
    - "$ws6 output DP-2"

x:
  autostart:
    - "bash ~/.screenlayout/dual_monitor.sh"
```

## Role Details

### syncopated.i3_desktop.xorg
- Installs X11 server and utilities
- Configures display drivers
- Sets up X11 session management
- Configures display scaling and DPI

### syncopated.i3_desktop.i3
- Installs and configures i3 window manager
- Sets up workspace assignments
- Configures key bindings and shortcuts
- Manages autostart applications

### syncopated.i3_desktop.dunst
- Installs dunst notification daemon
- Configures notification appearance and behavior
- Sets up desktop integration

### syncopated.i3_desktop.picom
- Installs picom X11 compositor
- Configures transparency and effects
- Optimizes for performance

### syncopated.i3_desktop.sxhkd
- Installs Simple X hotkey daemon
- Configures global key bindings
- Manages hotkey profiles

## Usage Examples

### Tag-Based Execution

```bash
# Install only X11 components
ansible-playbook -i inventory playbooks/i3_setup.yml --tags "xorg"

# Configure just the window manager
ansible-playbook -i inventory playbooks/i3_setup.yml --tags "i3"

# Set up compositor and notifications
ansible-playbook -i inventory playbooks/i3_setup.yml --tags "picom,dunst"
```

### Conditional Deployment

```yaml
# Deploy i3 only on specific hosts
- role: syncopated.i3_desktop.i3
  when: 
    - window_manager == "i3"
    - inventory_hostname in groups['workstations']
```

### Multi-Distribution Support

The collection automatically detects the target distribution and uses appropriate package managers and repositories.

## File Structure

```
ansible_collections/syncopated/i3_desktop/
├── galaxy.yml                 # Collection metadata
├── README.md                 # This file
├── roles/                    # Collection roles
│   ├── i3/                  # i3 window manager
│   ├── dunst/               # Notification daemon
│   ├── picom/               # X11 compositor
│   ├── sxhkd/               # Hotkey daemon
│   └── xorg/                # X11 server
├── playbooks/               # Example playbooks
│   └── i3_setup.yml        # Complete setup playbook
└── inventory_examples/      # Sample inventory structure
    ├── group_vars/
    ├── host_vars/
    └── inventory.ini
```

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following Ansible best practices
4. Test across supported distributions
5. Submit a pull request

### Testing

```bash
# Syntax check
ansible-playbook --syntax-check playbooks/i3_setup.yml

# Dry run
ansible-playbook -i inventory playbooks/i3_setup.yml --check --diff

# Role-specific testing
ansible-playbook roles/i3/tests/test.yml
```

## Troubleshooting

### Common Issues

1. **Missing X11**: Ensure target system supports X11
2. **Permission Issues**: Verify sudo access for the ansible user
3. **Package Conflicts**: Check for conflicting window managers
4. **Display Issues**: Verify display driver compatibility

### Debug Mode

```bash
ansible-playbook -i inventory playbooks/i3_setup.yml -vvv
```

## License

GPL-2.0-or-later

## Author

b08x <b08x@syncopated.net>

## Repository

https://github.com/b08x/OS