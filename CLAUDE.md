# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Architecture

This is an Ansible-based workstation automation system that provides a comprehensive setup for Arch Linux development environments. The project follows a modular role-based architecture with support for both traditional ansible-playbook execution and ansible-pull agent-based deployment.

### Core Architecture

#### Inventory Management

- **Dynamic Inventory**: Custom Python script (`inventory/dynamic_inventory.py`) that combines static host definitions with mDNS discovery and subnet scanning
- **Static Inventory**: Traditional INI format (`inventory/inventory.ini`) with group hierarchies (workstation→dev, server→virt)
- **Host/Group Variables**: Organized under `inventory/host_vars/` and `inventory/group_vars/` for per-host and per-group customization

#### Role-Based Modular Design

The system is organized into 25+ roles covering:

- **Base System**: Package management (pacman/paru), repositories, user setup
- **Desktop Environment**: Support for both X11 (i3) and Wayland (Sway) with XWayland compatibility
- **Development Tools**: Ruby (RVM/system), Docker, libvirt, custom tools
- **Professional Audio**: Configurable audio servers (JACK/PulseAudio/PipeWire) with low-latency tuning
- **Networking**: Unified support for NetworkManager and systemd-networkd with automatic wireless setup
- **Security**: SSH hardening, firewalld configuration

#### Plugin System

- **Custom AUR Module**: Native Arch User Repository package management
- **LLM Analyzer Callback**: AI-powered playbook analysis for idempotency and best practices
- **Debops Filter Plugins**: Enhanced variable processing capabilities

## Common Development Commands

### Ansible Playbook Execution

#### Main Playbooks

```bash
# Complete workstation setup (localhost)
ansible-playbook main.yml

# Full setup targeting all hosts
ansible-playbook playbooks/full.yml

# NAS-specific configuration
ansible-playbook playbooks/nas.yml

# Network-only configuration
ansible-playbook playbooks/networking.yml
```

#### Using Tags for Selective Execution

```bash
# Base system setup only
ansible-playbook main.yml --tags "base"

# Audio configuration
ansible-playbook main.yml --tags "audio"

# Desktop environment (X11 or Wayland)
ansible-playbook main.yml --tags "x,i3" # For X11/i3
ansible-playbook main.yml --tags "sway,xwayland" # For Wayland

# Development tools
ansible-playbook main.yml --tags "ruby,docker,libvirt"

# Skip specific roles
ansible-playbook playbooks/full.yml --skip-tags "docker,libvirt"
```

#### Inventory Operations

```bash
# List hosts and groups
ansible-inventory --graph

# Test dynamic inventory
ansible-inventory -i inventory/dynamic_inventory.py --graph

# Export dynamic inventory to YAML
./inventory/dynamic_inventory.py --export inventory_export.yml

# Debug dynamic inventory
ANSIBLE_INVENTORY_DEBUG=true ./inventory/dynamic_inventory.py --list
```

### Configuration and Validation

#### Syntax Checking

```bash
# Validate playbook syntax
ansible-playbook main.yml --syntax-check

# List available tags
ansible-playbook playbooks/full.yml --list-tags

# List target hosts
ansible-playbook playbooks/full.yml --list-hosts
```

#### Dry Run Testing

```bash
# Check mode (dry run)
ansible-playbook main.yml --check

# Diff mode (show changes)
ansible-playbook main.yml --diff

# Combined check and diff
ansible-playbook main.yml --check --diff
```

### Variable Management

#### Override Variables

```bash
# Command line variable override
ansible-playbook main.yml -e "use_docker=false" -e "window_manager=sway"

# Load extra variables file
ansible-playbook main.yml -e "@custom_vars.yml"
```

#### Variable Precedence (highest to lowest)

1. Command line (`-e "var=value"`)
2. Host variables (`inventory/host_vars/*.yml`)
3. Group variables (`inventory/group_vars/*.yml`)
4. Role defaults (`roles/*/defaults/main.yml`)

### Ansible Pull (Agent Mode)

```bash
# Initial setup for ansible-pull
sudo pacman -S ansible-core git

# Run ansible-pull
ansible-pull -U https://github.com/user/syncopated-ansible.git main.yml

# With specific inventory
ansible-pull -U https://github.com/user/syncopated-ansible.git -i inventory/inventory.ini main.yml
```

## Key Configuration Points

### Audio Server Selection

The audio role supports multiple backends controlled by variables:

- `use_jack: true` - JACK audio server for professional audio
- `use_pipewire: true` - Modern PipeWire server
- Default: PulseAudio

### Network Backend Selection

Network configuration supports dual backends:

- NetworkManager (default) - User-friendly with GUI integration
- systemd-networkd - Minimal, systemd-native networking

### Window Manager Selection

Desktop environment is configurable:

- `window_manager: "i3"` - X11 with i3 window manager (default)
- `window_manager: "sway"` - Wayland with Sway, includes XWayland

### Virtualization and Containers

Optional containerization/virtualization:

- `use_docker: "true"` - Docker with optional NVIDIA support
- `use_libvirt: "true"` - KVM/QEMU virtualization
- `use_vagrant: "true"` - Vagrant integration (requires libvirt)

### Development Environment

Ruby environment configuration:

- `rvm_install: true` - Use Ruby Version Manager
- `rvm_install: false` - Use system Ruby packages

## Plugin Configuration

### LLM Analyzer Callback

AI-powered analysis for idempotency and best practices:

```ini
# ansible.cfg
callbacks_enabled = llm_analyzer

[callback_llm_analyzer]
provider = gemini
model = gemini-2.0-flash
temperature = 0.4
```

Supported providers: openai, gemini, groq, openrouter, cohere, anthropic

### Custom AUR Module

Native AUR package management without external helpers:

```yaml
- name: Install AUR package
  aur:
    name: package-name
    state: present
  become_user: aur_builder
```

## Architecture Patterns

### Idempotency Focus

All roles are designed for idempotency with proper conditionals and state checking:

- Use of `creates`, `removes`, and `changed_when` conditions
- Preference for native Ansible modules over shell commands
- Comprehensive error handling with `block/rescue/always`

### Variable Inheritance

Complex variable inheritance through group hierarchies:

- Global variables in `inventory/group_vars/all/`
- Workstation-specific in `inventory/group_vars/workstation/`
- Host-specific overrides in `inventory/host_vars/hostname.yml`

### Conditional Role Execution

Roles are conditionally included based on host characteristics:

- Window manager detection for X11 vs Wayland roles
- Hardware-specific driver installation
- Service conflicts resolution (e.g., audio servers)

### Dynamic Host Discovery

Hybrid inventory approach combining:

- Static host definitions for known machines
- mDNS resolution for local network discovery
- Subnet scanning with IP whitelisting for unknown hosts

## Troubleshooting

### Common Issues

- **Package conflicts**: Check for conflicting audio servers or display systems
- **Network setup**: Verify wireless credentials for interactive setup
- **Permissions**: Ensure proper sudo configuration and AUR builder user
- **Hardware drivers**: Check video driver compatibility for your GPU

### Debug Commands

```bash
# Verbose playbook execution
ansible-playbook main.yml -vvv

# Debug dynamic inventory
ANSIBLE_INVENTORY_DEBUG=true ./inventory/dynamic_inventory.py --list

# Check variable precedence
ansible-inventory --host hostname --vars

# Test host connectivity
ansible all -m ping
```

### Log Analysis

- Ansible logs: `/tmp/ansible.log`
- LLM analysis output: `llm_analysis/` directory
- Service logs: `journalctl -u service-name`
