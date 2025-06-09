# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an Ansible-based workstation automation framework that provides comprehensive multi-distribution support for provisioning development and audio production workstations. Originally designed for Arch Linux, it now supports Rocky Linux 9 through sophisticated package mapping and alternative installation strategies.

## Architecture

### Role-Based Modular Design
The system uses Ansible roles organized in a dependency hierarchy:

**Foundation Layer**: `base` → `ssh` → `firewalld` → `networking` → `ntp`
**Environment Layer**: `shell` → `ruby` → `docker`/`libvirt` (optional)
**Desktop Layer**: `audio` → `video` → `x`/`sway` → `rofi` → `i3`/`sway`
**Services Layer**: `nas` → `tools` → `media`

### Multi-Distribution Support
- **Distribution detection**: Automatic `ansible_os_family` and `ansible_distribution` detection
- **Variable abstraction**: OS-specific variables in `roles/*/vars/Archlinux.yml` and `roles/*/vars/RedHat.yml`
- **Package mapping**: Complex alternatives system for unavailable packages (Cargo, pip, source builds, binary downloads)
- **Unified execution**: Same playbook works across Arch Linux and Rocky Linux 9

### Key Architectural Patterns
- **Conditional role execution**: Based on variables like `use_docker`, `window_manager`, `nfs_host`
- **Alternative package resolution**: Sophisticated fallback system in `install_alternatives.yml`
- **Template-driven configuration**: Extensive Jinja2 templates for dynamic system configuration
- **Tag-based granular control**: Comprehensive tagging for selective execution

## Development Guidelines
- **Documentation-Driven Development**: Before implementing a new role or feature, create a comprehensive README file that outlines its purpose, variables, dependencies, and example usage.

## Common Development Commands

### Playbook Execution
```bash
# Full workstation setup
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --ask-become-pass

# Arch Linux execution
ansible-playbook -i inventory/inventory.ini playbooks/full.yml -b

# Rocky Linux 9 execution  
ansible-playbook -i inventory/inventory.ini playbooks/full.yml \
  -e "ansible_python_interpreter=/usr/bin/python3" --ask-become-pass

# Tag-based selective execution
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --tags "base,audio,shell"
ansible-playbook -i inventory/inventory.ini playbooks/full.yml --skip-tags "docker,libvirt"
```

[... rest of the existing content remains unchanged ...]