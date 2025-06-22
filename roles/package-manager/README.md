# Package Manager Role

## Purpose

The `package-manager` role provides a unified, distribution-agnostic interface for package installation across Arch Linux and Rocky Linux 9. It centralizes package management logic, handles alternative installation methods (Cargo, binary downloads, source builds), and ensures idempotent operations.

## Features

- **Multi-distribution support**: Automatic detection and handling of Arch Linux and Rocky Linux 9
- **Intelligent fallback strategies**: Attempts multiple installation methods when primary method fails
- **Idempotent operations**: Proper checking to prevent unnecessary reinstallations
- **Alternative installation methods**: 
  - System package managers (pacman, dnf)
  - Cargo/Rust packages
  - Binary downloads from GitHub releases
  - Source compilation
  - Flatpak packages
  - Python pip packages
- **Validation and reporting**: Post-installation verification and detailed reporting
- **Repository management**: Automatic setup of required repositories (EPEL, RPM Fusion, etc.)

## Dependencies

### Role Dependencies
None - this is a foundational role.

### System Requirements
- **Arch Linux**: `pacman`, optionally `paru` for AUR
- **Rocky Linux 9**: `dnf`, EPEL repository access
- **Common**: `git`, `curl`, `tar` for alternative installations

## Variables

### Required Variables

```yaml
# No required variables - role uses sensible defaults
```

### Optional Variables

```yaml
# Package manager configuration
package_manager:
  cleanup_temp: true                    # Clean temporary files after installation
  validate_installs: true              # Verify packages after installation  
  retry_count: 3                       # Number of retry attempts
  timeout: 300                         # Installation timeout in seconds
  
  # Fallback strategy order
  fallback_strategy:
    - system                           # Try system package manager first
    - cargo                            # Then Rust/Cargo
    - binary                           # Then binary downloads
    - flatpak                          # Finally Flatpak

# Distribution-specific settings
arch_linux:
  aur_helper: paru                     # AUR helper to use
  aur_builder: "{{ user.name }}"       # User for AUR operations
  makepkg_flags: "--noconfirm --needed" # Makepkg flags

rocky_linux:
  epel_enabled: true                   # Enable EPEL repository
  rpmfusion_enabled: true              # Enable RPM Fusion repositories
  powertools_enabled: true             # Enable PowerTools/CRB repository

# Force installation method for specific packages
package_overrides:
  ripgrep:
    method: system                     # Force system installation
  bottom:
    method: cargo                      # Force Cargo installation
```

### Package Definition Format

```yaml
# Simple package installation
packages:
  - name: "git"
    
# Package with specific method
packages:
  - name: "ripgrep"
    method: "system"
    required: true                     # Fail if installation fails
    
# Package with fallback options
packages:
  - name: "bottom"
    method: "auto"                     # Try multiple methods
    fallbacks: ["cargo", "binary"]
    
# Binary download package
packages:
  - name: "glow"
    method: "binary"
    source: "https://github.com/charmbracelet/glow/releases/latest/download/glow_Linux_x86_64.tar.gz"
    binary_name: "glow"
    install_path: "/usr/local/bin"
    
# Source build package
packages:
  - name: "libvips"
    method: "source"
    source: "https://github.com/libvips/libvips.git"
    build_system: "meson"
    build_deps: ["meson", "ninja-build", "glib2-devel"]
```

## Usage Examples

### Basic Package Installation

```yaml
- name: Install basic development tools
  include_role:
    name: package-manager
  vars:
    packages:
      - name: "git"
      - name: "curl"
      - name: "wget"
```

### Mixed Installation Methods

```yaml
- name: Install tools with different methods
  include_role:
    name: package-manager
  vars:
    packages:
      - name: "ripgrep"
        method: "system"
      - name: "bottom"
        method: "cargo"
      - name: "glow"
        method: "binary"
        source: "https://github.com/charmbracelet/glow/releases/latest"
```

### Package Groups

```yaml
- name: Install development packages
  include_role:
    name: package-manager
  vars:
    package_groups:
      - name: "development"
        packages:
          - git
          - gcc
          - make
          - cmake
      - name: "cli_tools"
        packages:
          - ripgrep
          - fd-find
          - bat
```

### Role Integration

```yaml
# In another role's tasks/main.yml
- name: Install role-specific packages
  include_role:
    name: package-manager
  vars:
    packages: "{{ role_packages }}"
  when: role_packages is defined
```

## File Structure

```
package-manager/
├── README.md                          # This documentation
├── defaults/main.yml                  # Default configuration
├── vars/
│   ├── Archlinux.yml                 # Arch Linux package mappings
│   ├── RedHat.yml                    # Rocky Linux package mappings
│   └── fallbacks.yml                 # Alternative installation methods
├── tasks/
│   ├── main.yml                      # Entry point with distribution detection
│   ├── Archlinux/                    # Arch Linux specific tasks
│   │   ├── main.yml                  # Arch Linux task coordinator
│   │   ├── setup_repositories.yml    # Pacman/AUR repository setup
│   │   └── install_system.yml        # Pacman/AUR package installation
│   ├── RedHat/                       # Rocky Linux specific tasks
│   │   ├── main.yml                  # Rocky Linux task coordinator
│   │   ├── setup_repositories.yml    # DNF/EPEL/RPM Fusion setup
│   │   └── install_system.yml        # DNF package installation
│   ├── install_cargo.yml             # Rust/Cargo packages (cross-distro)
│   ├── install_binary.yml            # Binary downloads (cross-distro)
│   ├── install_source.yml            # Source compilation (cross-distro)
│   ├── install_flatpak.yml           # Flatpak packages (cross-distro)
│   ├── install_pip.yml               # Python pip packages (cross-distro)
│   └── validate.yml                  # Post-installation validation
├── templates/
│   ├── package_report.j2             # Installation summary
│   └── failed_packages.j2            # Failed installation report
├── meta/main.yml                     # Role metadata
└── tests/
    ├── inventory                     # Test inventory
    └── test.yml                      # Test playbook
```

## Error Handling

The role implements comprehensive error handling:

- **Graceful degradation**: Falls back to alternative installation methods
- **Detailed logging**: Reports success/failure for each package
- **Partial success**: Continues with other packages if some fail
- **Validation**: Verifies package installation success
- **Cleanup**: Removes temporary files even on failure

## Performance Considerations

- **Idempotent operations**: Checks for existing installations before attempting
- **Parallel operations**: Where possible, installs multiple packages simultaneously
- **Caching**: Leverages system package manager caches
- **Minimal downloads**: Only downloads what's necessary

## Testing

```bash
# Test the role
ansible-playbook -i tests/inventory tests/test.yml

# Test specific distribution
ansible-playbook -i tests/inventory tests/test.yml -e "ansible_os_family=Archlinux"
ansible-playbook -i tests/inventory tests/test.yml -e "ansible_os_family=RedHat"

# Test specific installation method
ansible-playbook -i tests/inventory tests/test.yml --tags "cargo"
```

## Integration with Existing Roles

This role is designed to replace package installation logic in existing roles:

### Before (in role tasks)
```yaml
- name: Install packages (Arch)
  pacman:
    name: "{{ item }}"
    state: present
  loop: "{{ arch_packages }}"
  when: ansible_os_family == "Archlinux"

- name: Install packages (Rocky)
  dnf:
    name: "{{ item }}"
    state: present
  loop: "{{ rocky_packages }}"
  when: ansible_os_family == "RedHat"
```

### After (using package-manager)
```yaml
- name: Install packages
  include_role:
    name: package-manager
  vars:
    packages: "{{ role_packages }}"
```

## Troubleshooting

### Common Issues

1. **Package not found**: Check distribution-specific variable files
2. **Permission errors**: Ensure proper become/sudo configuration
3. **Network timeouts**: Adjust timeout values in configuration
4. **Build failures**: Verify build dependencies are installed

### Debug Mode

Enable debug output:
```yaml
package_manager:
  debug: true
  verbose: true
```

### Manual Testing

```bash
# Test package availability
ansible-playbook -i inventory test-packages.yml --check

# Validate installations
ansible-playbook -i inventory validate-packages.yml
```