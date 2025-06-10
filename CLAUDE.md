# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an Ansible-based workstation automation framework that provides comprehensive multi-distribution support for provisioning development and audio production workstations. Originally designed for Arch Linux, it now supports Rocky Linux 9 through sophisticated package mapping and alternative installation strategies.

## Architecture

### Role-Based Modular Design
The system uses Ansible roles organized in a dependency hierarchy:

**Foundation Layer**: `package-manager` → `base` → `ssh` → `firewalld` → `networking` → `ntp`
**Environment Layer**: `shell` → `ruby` → `docker`/`libvirt` (optional)
**Desktop Layer**: `audio` → `video` → `x`/`sway` → `rofi` → `i3`/`sway`
**Services Layer**: `nas` → `tools` → `media`

### Package Management System (REFACTORED)
The system now uses a **centralized package-manager role** that provides:
- **Unified interface**: Single entry point for all package installations
- **Multi-method support**: System packages, Cargo, binary downloads, pip, source builds, Flatpak
- **Intelligent fallbacks**: Automatic fallback when primary installation methods fail
- **Cross-distribution compatibility**: Works seamlessly across Arch Linux and Rocky Linux 9
- **Idempotent operations**: Proper state checking and validation
- **Comprehensive reporting**: Detailed installation logs and success/failure tracking

### Multi-Distribution Support
- **Distribution detection**: Automatic `ansible_os_family` and `ansible_distribution` detection
- **Unified package definitions**: Single package format works across distributions
- **Smart fallback strategies**: Distribution-specific fallback priorities
- **Legacy compatibility**: Backwards compatibility with existing package variables

### Key Architectural Patterns
- **Centralized package management**: All package operations go through `package-manager` role
- **Conditional role execution**: Based on variables like `use_docker`, `window_manager`, `nfs_host`
- **Template-driven configuration**: Extensive Jinja2 templates for dynamic system configuration
- **Tag-based granular control**: Comprehensive tagging for selective execution
- **Documentation-driven development**: All new roles start with comprehensive README files

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