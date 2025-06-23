# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a comprehensive Ansible automation framework for professional audio workstations with multi-distribution support (Arch Linux, Rocky Linux 9). The playbook sets up everything from base system utilities to complete development environments with audio production capabilities.

## Key Architecture

- **Role-based modular design**: Each major component (audio, networking, virtualization, etc.) is a separate role in `roles/`
- **Multi-distribution support**: Automatic distribution detection with package mapping for Arch Linux and Rocky Linux 9
- **Dynamic inventory**: `inventory/dynamic_inventory.py` provides automatic host discovery with group hierarchies
- **Professional audio focus**: Low-latency audio configurations with JACK, PulseAudio, and PipeWire support
- **Tag-based execution**: Granular control over which components to deploy

## Common Development Commands

### Running Playbooks
```bash
# Full workstation setup
ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b

# Rocky Linux 9 support
ansible-playbook -i inventory/inventory.ini playbooks/full.yml \
  -e "ansible_python_interpreter=/usr/bin/python3" --ask-become-pass

# Tag-based execution
ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --tags "base,audio,shell"

# Skip specific components
ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b --skip-tags "docker,libvirt"
```

### Testing and Validation
```bash
# Dry run (check mode)
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --check --diff

# Lint playbooks and roles
ansible-lint

# List available tags
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --list-tags

# Test individual roles
ansible-playbook roles/audio/tests/test.yml
```

### Development Workflow
```bash
# Syntax check
ansible-playbook --syntax-check playbooks/full.yml

# Gather facts only
ansible -i inventory/inventory.ini all -m setup

# Test connectivity
ansible -i inventory/inventory.ini all -m ping
```

## Project Structure

### Core Configuration
- `ansible.cfg`: Main Ansible configuration with custom plugins and fact caching
- `inventory/`: Dynamic inventory script, static inventory, and variable hierarchies
- `playbooks/`: Main orchestration playbooks (`full.yml` for complete setup)

### Role Architecture
Key roles that work together:

- **base**: Core system setup, package management, user configuration
- **audio**: Professional audio setup (JACK/PulseAudio/PipeWire) with low-latency tuning
- **networking**: Unified network configuration (NetworkManager/systemd-networkd)
- **window-manager**: Tiling window managers (i3/Sway) with XWayland support
- **shell**: Zsh with Oh My Zsh, terminal customization
- **docker/libvirt**: Containerization and virtualization stacks
- **ruby**: Ruby development environment with RVM support
- **tools**: Custom development tools and utilities

### Variable Hierarchy (highest to lowest precedence)
1. Command line (`-e "var=value"`)
2. Host variables (`inventory/host_vars/*.yml`)
3. Group variables (`inventory/group_vars/*.yml`)
4. Global variables (`inventory/group_vars/all/`)
5. Role defaults (`roles/*/defaults/main.yml`)

## Key Configuration Files

### Audio System Selection
```yaml
# Primary audio system (in group_vars or host_vars)
audio_system: "pipewire"  # or "pulseaudio_jack"
```

### Multi-Distribution Package Mapping
- Arch Linux: Uses pacman, paru (AUR), custom `aur` module
- Rocky Linux 9: Uses dnf with EPEL, PowerTools/CRB, RPM Fusion
- Automatic source builds for missing packages (libvips, chromaprint)

### Window Manager Selection
```yaml
# Desktop environment choice
window_manager: "sway"  # Wayland with XWayland
# or
window_manager: "i3"    # X11 (default)
```

## Development Standards

### Ansible Lint Configuration
- Strict mode enabled with `.ansible-lint` configuration
- Task names must be prefixed with role names
- Password variables must use `no_log`
- Loop variables should use role-specific prefixes

### Role Structure
Each role follows consistent structure:
```
roles/role-name/
├── defaults/main.yml     # Default variables
├── vars/main.yml        # Role-specific variables
├── tasks/main.yml       # Main task orchestration
├── handlers/main.yml    # Service handlers
├── templates/           # Jinja2 templates
├── files/              # Static files
├── meta/main.yml       # Role metadata
└── tests/test.yml      # Role testing
```

### Testing Pattern
- Each role includes `tests/test.yml` for standalone testing
- Inventory-based testing with `tests/inventory`
- Check mode support for dry runs

## Important Notes

### Audio Workstation Focus
This is primarily designed for professional audio production:
- Realtime kernel privileges configured
- Low-latency audio tuning
- Professional audio application stack
- Hardware-specific optimizations

### Multi-Host Dynamic Inventory
The dynamic inventory automatically discovers:
- Local hostname assignment to groups
- mDNS resolution for `.local` hosts
- Group hierarchy (workstation/server parent groups)
- Host-specific variable loading

### Distribution-Specific Considerations
- **Arch Linux**: Native AUR support, rolling release optimizations
- **Rocky Linux 9**: Enterprise stability, source compilation fallbacks
- Package mapping automatically handled in role `vars/` files

When working with this codebase, always consider the multi-distribution nature and professional audio requirements. Test changes across both supported distributions and verify audio functionality doesn't regress.