# Unified Package Management Design

This document outlines the design for distribution-agnostic package management across Arch Linux and Rocky Linux 9.

## Architecture Overview

### Current State (Arch-centric)

```yaml
- name: Install packages
  community.general.pacman:
    name: "{{ packages__base }}"
    state: present
```

### Target State (Multi-distribution)

```yaml
- name: Include distribution-specific variables
  include_vars: "{{ ansible_os_family }}.yml"

- name: Install packages
  include_tasks: "install_packages.yml"
  vars:
    package_list: "{{ packages__base }}"
```

## Distribution Detection Strategy

### Primary Detection Variables

- `ansible_os_family`: 'Archlinux', 'RedHat', 'Debian'
- `ansible_distribution`: 'Arch', 'Rocky', 'AlmaLinux', 'CentOS', 'Fedora'
- `ansible_distribution_major_version`: '9', '8', etc.

### Variable File Structure

```
roles/base/vars/
├── main.yml           # Common variables
├── Archlinux.yml      # Arch Linux packages
├── RedHat.yml         # Rocky/RHEL/CentOS packages
└── Debian.yml         # Ubuntu/Debian packages (future)
```

## Package Installation Task Design

### Master Package Installation Task

File: `roles/base/tasks/install_packages.yml`

```yaml
---
- name: Install packages (Arch Linux)
  community.general.pacman:
    name: "{{ package_list }}"
    state: present
  when: ansible_os_family == 'Archlinux'

- name: Install packages (Red Hat family)
  ansible.builtin.dnf:
    name: "{{ package_list }}"
    state: present
  when: ansible_os_family == 'RedHat'

- name: Install packages (Debian family)
  ansible.builtin.apt:
    name: "{{ package_list }}"
    state: present
    update_cache: yes
  when: ansible_os_family == 'Debian'
```

### AUR Package Handling

File: `roles/base/tasks/install_aur_packages.yml`

```yaml
---
- name: Install AUR packages (Arch Linux only)
  aur:
    name: "{{ aur_package_list }}"
    state: present
  become_user: "{{ aur_builder_user }}"
  when: 
    - ansible_os_family == 'Archlinux'
    - aur_package_list is defined

- name: AUR packages not available on {{ ansible_distribution }}
  debug:
    msg: "AUR packages {{ aur_package_list }} are Arch Linux specific"
  when: ansible_os_family != 'Archlinux'
```

### Alternative Package Installation

File: `roles/base/tasks/install_alternatives.yml`

```yaml
---
- name: Install alternatives via Flatpak
  flatpak:
    name: "{{ item.flatpak }}"
    state: present
  loop: "{{ alternative_packages }}"
  when: 
    - item.flatpak is defined
    - ansible_facts['os_family'] != 'Archlinux'

- name: Install alternatives via cargo
  shell: cargo install {{ item.cargo }}
  loop: "{{ alternative_packages }}"
  when: 
    - item.cargo is defined
    - ansible_facts['os_family'] != 'Archlinux'
  environment:
    PATH: "{{ ansible_env.PATH }}:{{ ansible_env.HOME }}/.cargo/bin"
```

## Repository Management

### Distribution-Specific Repository Setup

```yaml
- name: Setup repositories
  include_tasks: "repos_{{ ansible_os_family }}.yml"
```

#### Arch Linux Repositories

File: `roles/base/tasks/repos_Archlinux.yml`

```yaml
---
- name: Configure pacman repositories
  template:
    src: etc/pacman.conf.j2
    dest: /etc/pacman.conf
    backup: yes
  notify: update package cache

- name: Install paru AUR helper
  include_tasks: paru.yml
```

#### Red Hat Repositories  

File: `roles/base/tasks/repos_RedHat.yml`

```yaml
---
- name: Install EPEL repository
  ansible.builtin.dnf:
    name: epel-release
    state: present

- name: Enable PowerTools/CRB repository
  ansible.builtin.shell: |
    dnf config-manager --set-enabled powertools || 
    dnf config-manager --set-enabled crb
  changed_when: false

- name: Install RPM Fusion repositories
  ansible.builtin.dnf:
    name:
      - "https://download1.rpmfusion.org/free/el/rpmfusion-free-release-{{ ansible_distribution_major_version }}.noarch.rpm"
      - "https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-{{ ansible_distribution_major_version }}.noarch.rpm"
    state: present
    disable_gpg_check: yes
```

## Variable File Structure

### Main Variables (roles/base/vars/main.yml)

```yaml
---
# Common configuration
packages__gpg_keyserver: keyserver.ubuntu.com

# Distribution-agnostic package categories
package_categories:
  - base_system
  - development
  - multimedia
  - networking
  - desktop

# Alternative installation methods for missing packages
alternative_packages:
  - name: "bat"
    cargo: "bat"
    flatpak: null
    binary_url: "https://github.com/sharkdp/bat/releases/download/v0.24.0/bat-v0.24.0-x86_64-unknown-linux-gnu.tar.gz"
  
  - name: "bottom"
    cargo: "bottom"
    flatpak: null
    
  - name: "glow"
    binary_url: "https://github.com/charmbracelet/glow/releases/download/v1.5.1/glow_1.5.1_Linux_x86_64.tar.gz"
```

### Arch Linux Variables (roles/base/vars/Archlinux.yml)

```yaml
---
packages__base:
  - aria2
  - aspell
  - aspell-en
  # ... (existing Arch packages)

packages__aur:
  - paru
  - yay
  # ... (AUR-specific packages)

packages__reflector_args: >-
  --latest 200
  --sort rate
  --protocol http --protocol https
  --threads {{ ansible_facts.processor_vcpus }}
  --save /etc/pacman.d/mirrorlist
```

### Red Hat Variables (roles/base/vars/RedHat.yml)

```yaml
---
packages__base:
  - aria2
  - aspell
  - aspell-en
  - atool
  - audiofile-devel
  - "@Development Tools"
  - bash-completion
  - bat
  - bind-utils
  # ... (Rocky Linux equivalent packages)

packages__epel:
  - bat
  - fd-find
  - inxi
  - lnav
  - ncdu
  - numlockx
  - pandoc
  - playerctl
  - ripgrep
  - sshpass
  # ... (EPEL-specific packages)

packages__rpmfusion_free:
  - faac
  - faad2
  - gstreamer1-libav
  - x264
  - x265
  # ... (RPM Fusion Free packages)

packages__rpmfusion_nonfree:
  - unrar
  # ... (RPM Fusion Non-Free packages)
```

## Role Task Structure

### Updated Main Task File (roles/base/tasks/main.yml)

```yaml
---
- name: Include distribution-specific variables
  include_vars: "{{ ansible_os_family }}.yml"

- name: Setup repositories
  include_tasks: "repos_{{ ansible_os_family }}.yml"
  tags: ['repos']

- name: Install base packages
  include_tasks: install_packages.yml
  vars:
    package_list: "{{ packages__base }}"
  tags: ['packages']

- name: Install EPEL packages (Red Hat family)
  include_tasks: install_packages.yml
  vars:
    package_list: "{{ packages__epel }}"
  when: 
    - ansible_os_family == 'RedHat'
    - packages__epel is defined
  tags: ['packages', 'epel']

- name: Install RPM Fusion packages (Red Hat family)
  include_tasks: install_packages.yml
  vars:
    package_list: "{{ packages__rpmfusion_free + packages__rpmfusion_nonfree }}"
  when: 
    - ansible_os_family == 'RedHat'
    - packages__rpmfusion_free is defined
  tags: ['packages', 'rpmfusion']

- name: Install AUR packages (Arch Linux)
  include_tasks: install_aur_packages.yml
  vars:
    aur_package_list: "{{ packages__aur }}"
  when: ansible_os_family == 'Archlinux'
  tags: ['packages', 'aur']

- name: Install alternative packages
  include_tasks: install_alternatives.yml
  when: alternative_packages is defined
  tags: ['packages', 'alternatives']

- name: Update package cache
  include_tasks: "update_cache_{{ ansible_os_family }}.yml"
  tags: ['cache']
```

## Testing Strategy

### Package Installation Verification

```yaml
- name: Verify critical packages are installed
  ansible.builtin.package_facts:
    manager: auto

- name: Check for missing critical packages
  debug:
    msg: "Package {{ item }} not found"
  loop: "{{ critical_packages }}"
  when: item not in ansible_facts.packages
  failed_when: item not in ansible_facts.packages

- name: Test alternative installations
  command: which {{ item }}
  loop: "{{ alternative_binaries }}"
  changed_when: false
  failed_when: false
  register: alternative_check
```

### Distribution-Specific Testing

```yaml
- name: Test Arch-specific functionality
  include_tasks: test_arch.yml
  when: ansible_os_family == 'Archlinux'

- name: Test Red Hat-specific functionality  
  include_tasks: test_redhat.yml
  when: ansible_os_family == 'RedHat'
```

## Migration Strategy

### Phase 1: Base Role Conversion

1. Create distribution-specific variable files
2. Implement unified package installation tasks
3. Test on ninjabot Rocky Linux 9

### Phase 2: Additional Roles

1. Apply pattern to audio, docker, network roles
2. Validate cross-distribution compatibility
3. Update documentation

### Phase 3: Optimization

1. Performance tuning for package installations
2. Advanced alternative installation methods
3. Automated testing pipeline

## Benefits

1. **Maintainability**: Single codebase for multiple distributions
2. **Extensibility**: Easy addition of new distributions
3. **Flexibility**: Multiple installation methods for missing packages
4. **Testing**: Clear separation of distribution-specific logic
5. **Migration**: Gradual transition path from Arch-centric design

This design provides a robust foundation for multi-distribution support while maintaining compatibility with existing Arch Linux deployments.
