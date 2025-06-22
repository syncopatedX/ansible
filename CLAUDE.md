# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Running Playbooks

```bash
# Full workstation setup
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --ask-become-pass

# Run with specific tags only
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --tags "base,shell,ruby" --ask-become-pass

# Check mode (dry run) with diff output
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --check --diff

# Skip specific roles
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --skip-tags "docker,libvirt" --ask-become-pass

# Target specific hosts
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --limit "soundbot" --ask-become-pass

# Rocky Linux 9 execution (requires Python 3 interpreter specification)
ansible-playbook -i inventory/inventory.ini playbooks/full.yml -e "ansible_python_interpreter=/usr/bin/python3" --ask-become-pass
```

### Testing and Validation

```bash
# Test specific role functionality
ansible-playbook -i inventory/inventory.ini roles/package-manager/tests/test.yml --ask-become-pass

# List available tags
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --list-tags

# List hosts from dynamic inventory
ansible-inventory -i inventory/dynamic_inventory.py --list

# Syntax check
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --syntax-check

# Lint roles (if ansible-lint is installed)
ansible-lint roles/
```

### Development Utilities

```bash
# Install required collections
ansible-galaxy collection install -r requirements.yml

# Bootstrap system with essential packages (run as root on Arch Linux)
./scripts/bin/bootstrap.sh

# Install Ruby gems for development tools
./scripts/bin/install_gems.sh
```

## Architecture Overview

### Dynamic Inventory System

The project uses a sophisticated dynamic inventory (`inventory/dynamic_inventory.py`) that combines:

- Static hostname definitions with mDNS resolution
- Dynamic subnet scanning via nmap for host discovery  
- Host group mapping based on hostname patterns
- Configurable IP whitelists and discovery controls
- Local connection override for self-targeting execution

### Modular Role Architecture

Roles are decomposed by function rather than by system, with clear separation of concerns:

- `base` role orchestrates `repository-manager`, `system-base`, `user-manager`, and `package-manager`
- Each role follows consistent internal structure: `tasks/`, `vars/`, `templates/`, `files/`
- OS family detection enables cross-platform support through `tasks/{{ ansible_os_family }}/main.yml` pattern
- Configuration management via hierarchical `group_vars/` and `host_vars/`

### Multi-Distribution Package Management

The `package-manager` role provides sophisticated cross-platform package installation:

- **Installation Methods**: system packages → AUR → cargo → binary downloads → pip → source builds
- **Distribution Mapping**: Automatic package name translation between Arch Linux and Rocky Linux
- **Fallback Hierarchies**: Multiple installation attempts with comprehensive error handling
- **Package Validation**: Post-installation verification and reporting
- **Source Builds**: Automated compilation for packages not available in repositories (libvips, chromaprint)

### Desktop Environment Abstraction

Supports both X11 and Wayland workflows through:

- Window manager selection via `window_manager` variable (`i3` for X11, `sway` for Wayland)
- Audio subsystem management (PipeWire, PulseAudio, JACK) with hardware-specific tuning
- Display manager flexibility (lightdm, greetd) with automatic login configuration
- Consistent theming across desktop environments via centralized color/theme variables

### Plugin Ecosystem

- **Custom AUR Module**: Arch User Repository package management with multiple helper tools
- **LLM Callback Plugin**: Real-time Ansible task analysis with AI providers (OpenAI, Gemini, Groq, Anthropic)
- **DebOps Filter Plugins**: Complex configuration parsing and merging capabilities
- **Langfuse Integration**: Prompt management and analysis tracking for AI-powered features

## Key Variables and Configuration

### Core System Variables

- `user_name`, `user_home`, `user_shell`: Primary user configuration
- `ansible_os_family`: Distribution detection for cross-platform tasks
- `window_manager`: Desktop environment selection (`i3` or `sway`)

### Service Control Variables  

- `use_docker`, `docker_nvidia_support`: Container orchestration
- `use_libvirt`, `use_vagrant`: Virtualization stack
- `use_jack`, `use_pipewire`: Audio subsystem selection
- `nfs_host`, `samba_host`: Network attached storage services

### Package Management Variables

- `packages`: List of packages with installation method specifications
- `package_groups`: Grouped package definitions for role-based installation
- `package_mappings`: Cross-distribution package name translation
- `fallback_packages`: Alternative installation methods and descriptions

## Network Configuration

The `networking` role supports both NetworkManager and systemd-networkd backends:

- Automatic wireless interface detection with interactive Wi-Fi setup
- Bridge network creation for virtualization workloads
- Static and DHCP configuration options
- Comprehensive DNS and mDNS resolution setup

## Testing and Development Patterns

### Role Testing

Each role includes test playbooks in `roles/*/tests/test.yml` with:

- Package installation verification
- Service status validation  
- Configuration file syntax checking
- Cross-distribution compatibility testing

### Tag-Based Execution

Comprehensive tagging system enables granular control:

- **Functional Tags**: `packages`, `repos`, `users`, `system`
- **Technology Tags**: `docker`, `libvirt`, `audio`, `video`, `ruby`
- **Component Tags**: `picom`, `dunst`, `sxhkd`, `xdg`

### Variable Precedence (Highest to Lowest)

1. Command line (`-e "var=value"`)
2. Host variables (`inventory/host_vars/*.yml`)
3. Group variables (`inventory/group_vars/*.yml`)
4. Global variables (`inventory/group_vars/all/`)
5. Role defaults (`roles/*/defaults/main.yml`)

## Common Troubleshooting

- **Multi-Distribution Issues**: Check `ansible_os_family` detection and distribution-specific task inclusion
- **Package Installation Failures**: Review fallback hierarchy and package mapping for target distribution
- **Dynamic Inventory Problems**: Verify network connectivity and mDNS resolution for target hosts
- **Permission Issues**: Ensure `aur_builder` user exists and has proper sudo configuration
- **Audio Configuration**: Check hardware-specific settings and realtime privilege configuration
