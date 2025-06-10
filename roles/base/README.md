# Base Role

This role orchestrates the foundational system setup by coordinating multiple specialized roles for repository management, system configuration, user management, and package installation.

## Purpose

The `base` role serves as an orchestration layer that:
- Configures system repositories through `repository-manager`
- Sets up core system settings through `system-base`
- Manages user accounts through `user-manager`
- Installs essential packages through `package-manager`

## Architecture

This role has been refactored to use a modular approach with the following decomposed roles:

1. **repository-manager**: Handles distribution-specific repository setup
2. **system-base**: Manages timezone, locale, and keymap configuration
3. **user-manager**: Creates and configures user accounts with sudo access
4. **package-manager**: Provides unified package installation across distributions

## Dependencies

This role depends on the following roles which are automatically included:
- `repository-manager`
- `system-base`
- `user-manager` 
- `package-manager`

## Package Definition Format

### New Format (Recommended)

```yaml
base_packages:
  # Core system packages
  - name: git
    method: system
    required: true
  
  # CLI tools with fallbacks
  - name: ripgrep
    method: auto
    fallbacks: [system, cargo]
  
  # Binary downloads
  - name: glow
    method: auto
    fallbacks: [system, binary]
    source: "https://github.com/charmbracelet/glow/releases/latest/download/glow_Linux_x86_64.tar.gz"
  
  # Python packages
  - name: tldr
    method: pip
```

### Legacy Format (Still Supported)

```yaml
packages__base:
  - git
  - curl
  - wget

packages__alternatives:
  - name: bottom
    cargo: bottom
```

## Variables

### Core Configuration

```yaml
# User configuration
user:
  name: "{{ lookup('env','USER') }}"
  group: "{{ lookup('env','USER') }}"
  shell: "{{ lookup('env','SHELL') }}"
  sudoers: true

# Package management
package_manager:
  debug: false
  generate_report: true
  validate_installs: true
  cleanup_temp: true
```

### Package Groups

```yaml
# Core system packages (always installed)
base_packages: [...]

# Development tools (optional)
development_packages: [...]

# Multimedia packages (optional)  
multimedia_packages: [...]
```

## Usage Examples

### Basic Usage

```yaml
- name: Setup base system
  include_role:
    name: base
```

### Selective Installation

```yaml
# Install only core packages
- name: Setup base system (core only)
  include_role:
    name: base
  tags: ["core", "users"]

# Install development packages
- name: Setup development environment
  include_role:
    name: base
  tags: ["development"]
```

### Custom Package Lists

```yaml
- name: Setup base system with custom packages
  include_role:
    name: base
  vars:
    base_packages:
      - name: git
        method: system
        required: true
      - name: custom-tool
        method: binary
        source: "https://example.com/tool.tar.gz"
```

## Migration Guide

### From Legacy Package Variables

**Before:**
```yaml
packages__base:
  - git
  - curl
  - ripgrep

packages__alternatives:
  - name: bottom
    cargo: bottom
```

**After:**
```yaml
base_packages:
  - name: git
    method: system
    required: true
  - name: curl
    method: system
  - name: ripgrep
    method: auto
    fallbacks: [system, cargo]
  - name: bottom
    method: auto
    fallbacks: [cargo, binary]
```

### Migration Steps

1. **Review existing package definitions** in `vars/Archlinux.yml` and `vars/RedHat.yml`
2. **Convert to new format** using `base_packages`, `development_packages`, etc.
3. **Test package installation** with new format
4. **Remove legacy variables** once migration is complete

## Architecture

### Execution Flow

```
base role main.yml
├── User and sudo setup
├── Repository configuration (legacy)
├── Package manager integration
│   ├── Core packages (package-manager role)
│   ├── Development packages (package-manager role)
│   └── Multimedia packages (package-manager role)
├── Legacy package support (backwards compatibility)
└── System finalization
```

### Integration Points

- **`package-manager` role**: Primary package installation
- **Legacy tasks**: Backwards compatibility (`install_packages.yml`, `install_alternatives.yml`)
- **Distribution-specific**: Repository and mirror management

## Related Documentation

- [Package Manager Role](../package-manager/README.md)
- [Multi-Distribution Support](../../docs/unified-package-management.md)
- [Source Installation Guide](../../docs/Ansible%20Playbook%20for%20Source%20Installation%20of%20Specified%20Packages%20on%20Red%20Hat%20Family%20Systems.md)
