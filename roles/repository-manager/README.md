# Repository Manager Role

This role handles repository configuration for different Linux distributions, including setting up additional repositories and configuring package managers.

## Purpose

The `repository-manager` role is responsible for:
- Setting up distribution-specific repositories (EPEL, RPM Fusion for RHEL family; AUR, Chaotic-AUR for Arch)
- Configuring package manager settings for optimal performance
- Managing repository priorities and keys
- Providing fallback mechanisms for repository setup failures

## Dependencies

This role should be run before any package installation roles. It has no role dependencies but requires appropriate privileges to modify system repository configuration.

## Variables

### Required Variables

None - the role automatically detects the distribution and applies appropriate configurations.

### Optional Variables

```yaml
# Repository configuration
enable_third_party_repos: true    # Enable additional repositories
network_timeout: 30              # Network timeout for repository operations
retry_count: 3                   # Number of retries for failed operations

# Arch Linux specific
enable_chaotic_aur: true         # Enable Chaotic AUR repository
enable_archaudio: true           # Enable ArchAudio repository

# RHEL family specific  
enable_epel: true                # Enable EPEL repository
enable_rpmfusion: true           # Enable RPM Fusion repositories
enable_powertools: true          # Enable PowerTools/CRB repository
```

## Example Usage

```yaml
- name: Configure system repositories
  include_role:
    name: repository-manager
  vars:
    enable_chaotic_aur: false
    network_timeout: 60
```

## Tags

- `repos` - All repository tasks
- `archaudio` - ArchAudio repository setup (Arch Linux)
- `chaotic_aur` - Chaotic AUR repository setup (Arch Linux)
- `epel` - EPEL repository setup (RHEL family)
- `rpmfusion` - RPM Fusion repository setup (RHEL family)
- `network_check` - Network connectivity verification
- `update_cache` - Package cache updates

## Error Handling

The role includes comprehensive error handling:
- Network connectivity pre-checks
- Multiple fallback key servers for GPG key imports
- Graceful degradation when repositories fail to setup
- Detailed error reporting and troubleshooting information

## Distribution Support

- **Arch Linux**: Chaotic AUR, ArchAudio repositories
- **Rocky Linux 9**: EPEL, RPM Fusion, PowerTools/CRB repositories
- **RHEL family**: CentOS Stream, RHEL with appropriate repository mappings

## Files

The role includes pre-configured mirrorlist files in the `files/` directory for reliable repository access.