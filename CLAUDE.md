# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a comprehensive Ansible automation framework for professional audio workstations with multi-distribution support (Arch Linux, Rocky Linux 9, Fedora). The project sets up complete development environments with professional audio production capabilities, desktop environments, and development tools.

## Key Architecture

- **Role-based modular design**: Each major component is a separate role in `roles/` with consistent structure
- **Multi-distribution support**: Automatic distribution detection with package mapping via role `vars/` files
- **Dynamic inventory**: `inventory/dynamic_inventory.py` provides automatic host discovery with mDNS and group hierarchies
- **Professional audio focus**: Low-latency audio configurations with JACK, PulseAudio, and PipeWire support
- **Tag-based execution**: Granular control over deployment components via tags
- **Custom plugins**: Extended functionality via custom callback plugins, modules, and filters

## Common Development Commands

### Running Playbooks
```bash
# Navigate to ansible directory first
cd ansible/

# Full workstation setup
ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b

# Rocky Linux 9 support (requires explicit Python interpreter)
ansible-playbook -i inventory/inventory.ini playbooks/full.yml \
  -e "ansible_python_interpreter=/usr/bin/python3" --ask-become-pass

# Tag-based execution for specific components
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

# Syntax check
ansible-playbook --syntax-check playbooks/full.yml

# Test connectivity
ansible -i inventory/inventory.ini all -m ping
```

### Galaxy Dependencies
```bash
# Install required external roles and collections
ansible-galaxy install -r requirements.yml
```

## Project Structure

### Core Configuration
- `ansible.cfg`: Main configuration with custom plugins, fact caching, and multi-inventory support
- `inventory/`: Dynamic inventory script, static inventory files, and variable hierarchies
- `playbooks/`: Main orchestration playbooks (`full.yml` for complete setup)
- `plugins/`: Custom Ansible extensions (callbacks, filters, modules)

### Key Ansible Roles

Essential roles that work together:

- **user**: User account creation and management with sudo configuration
- **base**: Core system setup, package management, repositories, distribution-specific tasks
- **audio**: Professional audio setup (JACK/PulseAudio/PipeWire) with low-latency tuning and hardware optimizations
- **networking**: Unified network configuration (NetworkManager/systemd-networkd/resolved)
- **sway**: Wayland compositor with comprehensive desktop environment and themes
- **shell**: Zsh with Oh My Zsh, terminal customization, and productivity tools
- **docker/libvirt**: Containerization and virtualization stacks
- **tools**: Development tools (VSCode, Obsidian, fabric.ai, input-remapper)
- **video**: GPU drivers and display configuration (AMD/Intel/NVIDIA)
- **theme**: System-wide theming (GTK, Qt, fonts, icons)

### Variable Hierarchy (highest to lowest precedence)
1. Command line (`-e "var=value"`)
2. Host variables (`inventory/host_vars/*.yml`)
3. Group variables (`inventory/group_vars/*.yml`)
4. Global variables (`inventory/group_vars/all/`)
5. Role defaults (`roles/*/defaults/main.yml`)

## Key Configuration Patterns

### Audio System Selection
```yaml
# Primary audio system configuration
audio_system: "pipewire"  # or "pulseaudio_jack"
```

### Window Manager Selection
```yaml
# Desktop environment choice
window_manager: "sway"  # Wayland with XWayland
```

### Multi-Distribution Package Mapping
- **Arch Linux**: Uses pacman, paru (AUR), custom `aur` module in `plugins/modules/aur/`
- **Rocky Linux 9**: Uses dnf with EPEL, PowerTools/CRB, RPM Fusion
- **Fedora**: Uses dnf with RPM Fusion, Flathub, and copr repositories
- **Automatic source builds**: For missing packages (libvips, chromaprint)

## Custom Ansible Components

### Dynamic Inventory (`inventory/dynamic_inventory.py`)
- Automatic host discovery with mDNS resolution
- Group hierarchy management (workstation/server parent groups)
- Host-specific variable loading

### Custom Modules (`plugins/modules/`)
- **aur**: AUR package management for Arch Linux with multiple helper support (yay, paru, etc.)

### Callback Plugins (`plugins/callback/`)
- **llm_analyzer**: AI-powered analysis of Ansible runs (configurable, supports multiple providers)

## Development Standards

### Ansible Configuration
- Fact caching enabled (`/tmp/ansible_cache`)
- Error on undefined variables enforced
- Custom plugin paths configured
- Multi-inventory support (dynamic + static)
- Strict ansible-lint configuration with `.ansible-lint`

### Role Structure Pattern
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

### Testing Approach
- Each role includes `tests/test.yml` for standalone testing
- Check mode support for dry runs (`--check --diff`)  
- Tag-based selective execution for development
- Ansible-lint with strict rules and custom configuration

### Distribution-Specific Variables
- Package mappings in `vars/Archlinux.yml`, `vars/Fedora.yml`, `vars/RedHat.yml`
- Service name mapping for different distributions
- Repository configuration per distribution

## Important Considerations

### Professional Audio Workstation Focus
- Realtime kernel privileges configured via `audio` role
- Low-latency audio tuning and optimization
- Hardware-specific audio optimizations
- Professional audio application stack (JACK tools, DAWs, plugins)

### Multi-Distribution Support
- **Arch Linux**: Native AUR support, rolling release optimizations
- **Rocky Linux 9**: Enterprise stability, source compilation fallbacks
- **Fedora**: Modern packages with RPM Fusion support
- Package mapping automatically handled in role `vars/` files

### Security and Best Practices
- No secrets or credentials stored in repository
- Sudo configuration with security considerations via `user` role
- Firewall management through dedicated `firewalld` role
- SSH hardening configurations

## Role Development and Refactoring Notes

- Use the ansible-role-reviewer agent to ascertain the context of the collection when a role is being refactored

When working with this codebase, always consider the multi-distribution nature and professional audio requirements. Test changes across supported distributions and verify audio functionality doesn't regress. Use the tag system for selective testing during development.

The codebase uses a modular approach where each role is self-contained but designed to work together as part of a complete workstation setup. Always check role dependencies in `meta/main.yml` files when modifying roles.