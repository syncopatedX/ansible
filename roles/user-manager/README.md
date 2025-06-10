# User Manager Role

This role handles user account management, including user creation, group assignments, sudo configuration, and basic user environment setup.

## Purpose

The `user-manager` role is responsible for:
- Creating user accounts with proper shell and group assignments
- Configuring sudo access with appropriate permissions
- Setting up polkit rules for privilege escalation
- Creating essential user directories (.local/bin, .local/share)
- Installing user configuration templates (aliases, profiles)

## Dependencies

This role should be run after basic system setup but before user-specific application configurations.

## Variables

### Required Variables

```yaml
user:
  name: "username"               # Username to create/manage
```

### Optional Variables

```yaml
user:
  name: "username"               # Username (required)
  shell: "/usr/bin/zsh"         # User shell (default: /bin/bash)
  groups: ["wheel", "audio"]     # Additional groups (default: ["wheel", "audio", "video"])
  home: "/home/username"         # Home directory path (auto-detected)
  group: "username"              # Primary group (auto-detected)
  sudoers: true                  # Enable sudo access (default: true)

# Profile configuration
profile_config_dir: "{{ user.home }}"  # Where to place profile configs
```

## Example Usage

```yaml
- name: Setup user account
  include_role:
    name: user-manager
  vars:
    user:
      name: "myuser"
      shell: "/usr/bin/zsh"
      groups: ["wheel", "audio", "video", "docker"]
      sudoers: true
```

## Tags

- `user` - User account creation and configuration
- `sudoers` - Sudo and polkit configuration  
- `aliases` - Shell aliases configuration
- `profile` - Profile configuration
- `folders` - User directory creation

## Security Considerations

This role configures passwordless sudo access for convenience in development environments. For production systems, consider:
- Removing NOPASSWD sudo access
- Using more restrictive sudo rules
- Implementing proper password policies

## Distribution Support

- **Arch Linux**: Full support including polkit rules
- **Rocky Linux 9**: Basic user management and sudo configuration
- **Other systemd distributions**: Basic functionality

## Files and Templates

The role can deploy user configuration files:
- Shell aliases template (`templates/home/.aliases.j2`)
- Profile configuration template (`templates/home/.profile.j2`)

## Privilege Separation

Tasks are properly separated between:
- System-level operations requiring root privileges
- User-level operations running as the target user