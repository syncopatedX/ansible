# Ansible Role: Zsh Shell Environment

**Distribution Support:** This role is designed exclusively for RedHat family distributions (Rocky Linux 9, Fedora 39+).

## Overview

Configures a comprehensive Zsh shell environment with Oh My Zsh, custom functions, aliases, and plugins optimized for professional audio workstations and development environments running on RedHat-based systems.

## Features

- ✅ **Oh My Zsh Installation**: Automated installation and configuration
- ✅ **Zoxide Integration**: Smart directory navigation (installed from GitHub releases)
- ✅ **Custom Plugins**: fd and ripgrep Oh My Zsh plugins
- ✅ **Curated Functions**: Professionally selected zsh functions (docker, systemd, git helpers)
- ✅ **Multi-User Support**: Deploys configurations for both user and root
- ✅ **Optional Shell Change**: Optionally set zsh as default shell
- ✅ **Desktop Integration**: X11 auto-start for window managers

## Requirements

### Ansible

- Ansible 2.15 or higher
- `ansible.posix` collection (for `synchronize` module)

### Target System

- **Rocky Linux 9** or **Fedora 39+**
- **EPEL repository** enabled (for Rocky Linux)
- **rsync** installed on control and target machines

### Required Variables

The role requires user-specific variables to be defined:

```yaml
user:
  name: username      # Target username
  group: groupname    # Primary group
  home: /home/username  # Home directory path
```

## Role Variables

### Default Variables (`defaults/main.yml`)

```yaml
# Directory for zsh profile files
profile_config_dir: "{{ user.home }}"

# Desktop environment (affects startx in .zprofile)
# Options: sway, i3, dwm, awesome, bspwm, xmonad, gnome, kde, or empty for server
desktop: "sway"

# Zsh theme selection
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
zsh_theme: "robbyrussell"

# Optional installations
zoxide_install: true  # Install zoxide from GitHub releases
oh_my_zsh_install: true  # Install oh-my-zsh

# Optional features
zsh_set_default_shell: false  # Automatically change user's default shell to zsh

# Hardware-specific settings (override in host_vars)
# libva_driver: "i965"  # For Intel/AMD GPU hardware
```

### Distribution-Specific Variables

**Fedora** (`vars/Fedora.yml`):
```yaml
packages__zsh:
  - zsh
  - zsh-syntax-highlighting
  - zsh-completions
```

**Rocky Linux** (`vars/RedHat.yml`):
```yaml
packages__zsh:
  - zsh
  - zsh-syntax-highlighting
```

**Note**: zsh-completions is available in EPEL for Rocky Linux but not included by default.

## Dependencies

None.

## Example Playbook

### Basic Usage

```yaml
---
- hosts: workstations
  become: true
  vars:
    user:
      name: jdoe
      group: jdoe
      home: /home/jdoe
  roles:
    - role: zsh
```

### Advanced Configuration

```yaml
---
- hosts: workstations
  become: true
  vars:
    user:
      name: audiodev
      group: audiodev
      home: /home/audiodev

    # Customize zsh theme
    zsh_theme: "agnoster"

    # Set zsh as default shell automatically
    zsh_set_default_shell: true

    # Desktop environment
    desktop: "i3"

    # Hardware-specific (Intel GPU)
    libva_driver: "i965"

    # Skip zoxide installation
    zoxide_install: false

  roles:
    - role: zsh
      tags: ['shell']
```

### Rocky Linux 9 Specific

```yaml
---
- hosts: rocky_servers
  become: true
  vars:
    user:
      name: sysadmin
      group: sysadmin
      home: /home/sysadmin

    # Server environment (no X11 auto-start)
    desktop: ""

    # Conservative theme
    zsh_theme: "robbyrussell"

  roles:
    - role: zsh
```

## Tasks Overview

### Main Tasks (`tasks/main.yml`)

1. **Load Distribution Variables**: Automatically loads Fedora or RedHat specific package lists
2. **Install Packages**: Uses `dnf` to install zsh and related packages
3. **Install zsh Configurations**: Imports zsh-specific setup tasks
4. **Deploy Aliases**: Creates `.aliases` files for user and root with dnf package management shortcuts
5. **Deploy Profile Files**: Creates `.profile`, `.zlogin`, `.zprofile`, `.zshenv`, `.zshrc` from templates
6. **Optional Shell Change**: Sets zsh as default shell if `zsh_set_default_shell` is true

### Zsh Configuration Tasks (`tasks/zsh.yml`)

1. **Oh My Zsh Installation**:
   - Downloads and runs the official installation script
   - Installs to `/usr/share/oh-my-zsh`
   - Automatically cleans up installation script

2. **Custom Plugins**:
   - Deploys fd and ripgrep plugins to oh-my-zsh custom plugins directory

3. **Custom Functions**:
   - Syncs curated zsh functions:
     - `docker` - Docker container/image cleanup helpers
     - `systemd` - systemd aliases and status helpers
     - `git` - Git prompt and status functions
     - `mkcd` - Make directory and cd into it
     - `useditor` - Set editor environment variables

4. **Zoxide Installation** (optional):
   - Downloads latest release from GitHub
   - Extracts to `/usr/local/bin`
   - Automatically cleans up archive
   - Can be skipped with `zoxide_install: false`

## Directory Structure

```
roles/zsh/
├── defaults/main.yml           # Default variables
├── vars/
│   ├── Fedora.yml             # Fedora package list
│   └── RedHat.yml             # Rocky Linux package list
├── tasks/
│   ├── main.yml               # Main task orchestration
│   └── zsh.yml                # Zsh-specific setup
├── templates/home/
│   ├── .aliases.j2            # Shell aliases (dnf commands)
│   ├── .profile.j2            # Shell profile
│   ├── .zlogin.j2             # Zsh login configuration
│   ├── .zprofile.j2           # Zsh profile (X11 auto-start)
│   ├── .zshenv.j2             # Zsh environment variables
│   └── .zshrc.j2              # Main zsh configuration
├── files/
│   ├── home/.local/share/zsh/
│   │   ├── completion/        # Zsh completions
│   │   ├── functions/         # Custom shell functions
│   │   └── themes/            # Custom themes
│   └── usr/share/oh-my-zsh/plugins/
│       ├── fd/                # fd plugin for oh-my-zsh
│       └── ripgrep/           # ripgrep plugin for oh-my-zsh
├── meta/main.yml              # Role metadata
└── tests/test.yml             # Role tests
```

## Template Customization

### Aliases (.aliases.j2)

The aliases template includes dnf package management shortcuts:

```bash
# dnf package management
alias dnfsearch="dnf search"
alias dnfinstall="sudo dnf install"
alias dnfremove="sudo dnf remove"
alias dnfupdate="sudo dnf upgrade --refresh"
alias listinstalled="dnf list installed | awk '{ print $1 }'"
alias dnfclean="sudo dnf clean all"
alias provides="sudo dnf provides"
```

### Zsh Theme (.zshrc.j2)

Theme selection is controlled via the `zsh_theme` variable:

```jinja2
{% if zsh_theme is defined %}
ZSH_THEME="{{ zsh_theme }}"
{% else %}
ZSH_THEME="robbyrussell"
{% endif %}
```

### Zoxide Integration (.zshrc.j2)

Zoxide initialization is conditional:

```bash
# Initialize zoxide if available
if command -v zoxide &> /dev/null; then
  eval "$(zoxide init zsh)"
fi
```

### X11 Auto-Start (.zprofile.j2)

For X11-based window managers:

```jinja2
{% if desktop is defined and desktop in ['i3', 'dwm', 'awesome', 'bspwm', 'xmonad'] %}
[[ -z "$DISPLAY" ]] && [[ "${XDG_VTNR}" -eq 1 ]] && startx -- -keeptty >~/.xorg.log 2>&1
{% endif %}
```

## Tags

The role supports the following tags for selective execution:

- `packages` - Install only zsh packages
- `zsh` - All zsh-specific tasks
- `oh-my-zsh` - Only oh-my-zsh installation and plugins
- `functions` - Only custom function deployment
- `zoxide` - Only zoxide installation
- `aliases` - Only aliases template deployment
- `profile` - Only profile file deployment

### Example Tag Usage

```bash
# Install packages only
ansible-playbook playbook.yml --tags packages

# Skip zoxide installation
ansible-playbook playbook.yml --skip-tags zoxide

# Only deploy configuration files
ansible-playbook playbook.yml --tags profile,aliases
```

## Troubleshooting

### Issue: EPEL not available on Rocky Linux

**Solution**: Ensure EPEL is installed:

```bash
sudo dnf install epel-release
sudo dnf makecache
```

### Issue: rsync not found

**Solution**: Install rsync on both control and target:

```bash
sudo dnf install rsync
```

### Issue: zsh not set as default shell

**Solution**: Either set `zsh_set_default_shell: true` or manually change:

```bash
chsh -s /bin/zsh
```

### Issue: Zoxide not working

**Solution**: Verify installation:

```bash
which zoxide
zoxide --version
```

If missing, ensure `zoxide_install: true` and re-run the role.

## Post-Installation

After the role completes:

1. **Verify zsh installation**:
   ```bash
   zsh --version
   ```

2. **Check oh-my-zsh**:
   ```bash
   ls -la /usr/share/oh-my-zsh
   ```

3. **Test zoxide** (if installed):
   ```bash
   zoxide --version
   ```

4. **Start a new shell**:
   ```bash
   zsh
   ```

5. **Customize further** by editing `~/.zshrc` or role templates

## License

MIT

## Author Information

Created by b08x for professional audio workstation deployments on RedHat family distributions.

## Contributing

When contributing:
- Test on both Fedora and Rocky Linux 9
- Follow Ansible best practices
- Use `ansible-lint` for validation
- Update this README with any new features or variables
