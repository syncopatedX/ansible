# Base Role

Foundational system setup for RedHat family distributions (Rocky Linux, Fedora, RHEL) including repository management, package installation, and GRUB bootloader configuration.

## Purpose

The `base` role provides:
- System timezone configuration
- Distribution-specific repository setup (EPEL, PowerTools, RPM Fusion)
- Essential package installation via DNF
- Rust/Cargo package installation
- Python package installation via pip3
- GRUB bootloader configuration with kernel parameters
- rc.local systemd service setup

## Supported Distributions

- Rocky Linux 9+
- Fedora (all versions)
- Red Hat Enterprise Linux 9+
- AlmaLinux 9+ (via RedHat compatibility)

## Dependencies

No external role dependencies. This role is self-contained.

## Variables

### System Configuration

```yaml
# User configuration
user:
  name: "{{ lookup('env','USER') }}"
  shell: "/bin/bash"

# System settings
timezone: "America/New_York"
locale: "en_US.UTF-8"
keymap: "us"
```

### Repository Configuration

```yaml
# Enable third-party repositories
enable_third_party_repos: true

# RedHat-specific repositories
enable_epel: true              # Extra Packages for Enterprise Linux
enable_powertools: true        # PowerTools/CRB repository
enable_rpmfusion: true         # RPM Fusion (free and nonfree)

# Network settings
network_timeout: 30
retry_count: 3
```

### GRUB Bootloader Configuration

```yaml
# Bootloader settings
bootloader: grub

# Kernel parameters for quiet boot
kernel_parameters_default: "splash threadirqs mitigations=off"

# Additional kernel parameters
kernel_parameters: "ipv6.disable=1 net.ifnames=0"

# GRUB background image (optional)
grub_background: "/usr/share/backgrounds/syncopated/syncopated016.png"

# Enable OS detection for multi-boot
grub_enable_os_prober: false
```

#### GRUB Configuration Details

The role templates `/etc/default/grub` with the following settings:

- **Boot timeout**: 5 seconds
- **Save default**: Last booted kernel is remembered
- **Crashkernel**: Automatic memory reservation for kernel crash dumps
- **SELinux**: Disabled by default (`selinux=0`)
- **Graphics mode**: Auto-detection with framebuffer persistence
- **Recovery mode**: Disabled
- **BLS (Boot Loader Specification)**: Enabled for RedHat 9+ systems

## Package Installation

### Base Packages

Packages are defined in distribution-specific variable files:
- `vars/Fedora.yml` - Fedora package names
- `vars/RedHat.yml` - RHEL/Rocky package names
- `vars/Rocky.yml` - Rocky Linux specific packages

### Cargo Packages (Rust)

If `cargo` is installed, the following packages are compiled:
- `bottom` - System monitor
- `du-dust` - Disk usage analyzer
- `eza` - Modern ls replacement
- `gping` - Ping with graph
- `ripgrep_all` - Search tool for all file types
- `sd` - Find & replace tool

### Python Packages (pip3)

If `pip3` is available, the following packages are installed:
- `trafilatura` - Web scraping tool
- `edge-tts` - Text-to-speech
- `ueberzug` - Terminal image display

## Usage

### Basic Usage

```yaml
- name: Setup base system
  hosts: workstation
  become: true
  roles:
    - base
```

### With Custom GRUB Settings

```yaml
- name: Setup base system with custom kernel parameters
  hosts: servers
  become: true
  roles:
    - base
  vars:
    kernel_parameters: "ipv6.disable=1 net.ifnames=0 nomodeset"
    kernel_parameters_default: "quiet splash"
```

### Tag-Based Execution

```bash
# Install only base packages
ansible-playbook site.yml --tags packages

# Configure only repositories
ansible-playbook site.yml --tags repos

# Configure only GRUB bootloader
ansible-playbook site.yml --tags grub,bootloader

# Skip GRUB configuration
ansible-playbook site.yml --skip-tags grub
```

### Available Tags

- `timezone` - Set system timezone
- `repos` - Configure distribution repositories
- `packages` - Install all packages
- `packages__base` - Install base system packages only
- `cargo` - Install Rust/Cargo packages
- `python` - Install Python/pip packages
- `grub` / `bootloader` - Configure GRUB bootloader

## File Structure

```
base/
├── defaults/main.yml          # Default variables
├── handlers/main.yml          # Service handlers (rebuild grub, update cache)
├── meta/main.yml             # Role metadata
├── tasks/
│   ├── main.yml              # Main orchestration tasks
│   ├── grub.yml              # GRUB bootloader configuration
│   ├── rclocal.yml           # rc.local systemd service
│   └── distro/
│       ├── Fedora/main.yml   # Fedora repository setup
│       └── Rocky/main.yml    # Rocky Linux repository setup
├── templates/
│   └── etc/default/grub.j2   # GRUB configuration template
└── vars/
    ├── Fedora.yml            # Fedora package lists
    ├── RedHat.yml            # RHEL/Rocky package lists
    └── Rocky.yml             # Rocky-specific packages
```

## Handlers

### Update cache
Refreshes DNF package cache when repositories are modified.

### Rebuild grub
Regenerates GRUB configuration file (`/boot/grub2/grub.cfg`) when GRUB settings change. Automatically triggered when:
- GRUB configuration template is modified
- Kernel parameters are changed

### Generate locales
Regenerates system locales when locale configuration changes.

### Update hwclock
Synchronizes hardware clock with system time.

## GRUB Bootloader Configuration

The role automatically configures GRUB with RedHat-optimized settings:

1. **Templates** `/etc/default/grub` with kernel parameters
2. **Applies** crashkernel memory reservations for kernel dump analysis
3. **Rebuilds** GRUB configuration using `grub2-mkconfig`
4. **Supports** distribution-specific paths:
   - Rocky/RHEL: `/boot/grub2/grub.cfg`
   - Fedora: `/boot/grub2/grub.cfg`

### Customizing Kernel Parameters

```yaml
# Disable IPv6 and use traditional network interface names
kernel_parameters: "ipv6.disable=1 net.ifnames=0"

# Quiet boot with threading optimizations
kernel_parameters_default: "quiet splash threadirqs"

# For systems requiring specific graphics settings
kernel_parameters: "ipv6.disable=1 net.ifnames=0 nomodeset"
```

### Crashkernel Configuration

The role automatically configures crashkernel memory based on system RAM:
- **1-4 GB RAM**: 192 MB reserved
- **4-64 GB RAM**: 256 MB reserved
- **64+ GB RAM**: 512 MB reserved

This enables kdump for kernel crash analysis.

## Best Practices

1. **Repository Management**: Enable only required repositories to minimize package conflicts
2. **Kernel Parameters**: Test kernel parameters in a non-production environment first
3. **GRUB Background**: Ensure background image path exists or set to empty string
4. **Package Lists**: Customize `packages__base` in vars files for your distribution
5. **Cargo/pip**: These require respective package managers to be pre-installed

## Troubleshooting

### GRUB Not Rebuilding

If GRUB configuration doesn't rebuild:

```bash
# Manually trigger GRUB rebuild
grub2-mkconfig -o /boot/grub2/grub.cfg

# Check GRUB template rendering
ansible-playbook site.yml --tags grub --check --diff
```

### Repository Failures

If repository setup fails:

```bash
# Test repository connectivity
dnf repolist

# Clear DNF cache
dnf clean all

# Re-run with verbose output
ansible-playbook site.yml --tags repos -vvv
```

### Package Installation Issues

```bash
# Check package availability
dnf search <package-name>

# Install with debug output
ansible-playbook site.yml --tags packages -vvv
```

## Migration from grub Role

The previous standalone `grub` role has been consolidated into `base` role. If you were using the `grub` role:

1. Remove `grub` from your playbook dependencies
2. The `base` role now handles GRUB configuration automatically
3. All previous `grub` role variables are supported (no changes needed)
4. GRUB configuration runs when `ansible_os_family == "RedHat"` and `bootloader == "grub"`

## Related Documentation

- [Project README](../../README.md)
- [Multi-Distribution Support](../../CLAUDE.md)
- [Audio Role](../audio/README.md) - Professional audio setup
- [Networking Role](../networking/README.md) - Network configuration
