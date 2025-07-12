# Changelog

All notable changes to this project will be documented in this file.

## [0.8.7] - 2025-07-12

### 🚀 Features

- Added host-specific zsh config and miscellaneous updates
- Add CLAUDE.md for AI guidance
- Add systemd-network configuration for soundbot
- *(package-manager)* Introduced multi-distribution package management role
- Implement users role and refactor grub configuration
- Expand multi-distribution support with Fedora integration

### 🐛 Bug Fixes

- Use verify parameter for the pacman-key module & full length key strings
- Set 0600 permissions for iwd wifi passphrase file

### 💼 Other

- *(playbooks,inventory)* Added host-specific playbooks and documentation

### 🚜 Refactor

- Consolidate i3 and sway roles into unified window-manager role
- Replace package-manager role with distribution-specific tasks
- Major ansible-lint compliance improvements
- Major networking role restructure and multi-distribution support
- Consolidate repository-manager and system-base roles into base role
- Comprehensive video role restructure with multi-GPU support

### 📚 Documentation

- Remove ansible-pull documentation and standardize playbook examples
- Restructured CLAUDE.md and updated README.md role list

### ⚙️ Miscellaneous Tasks

- Configured ninjabot network using systemd-network
- Deleted main.yml Ansible playbook
- Refactored zcompdump age check in .zshrc template
- Added Ruby version and gemset files to gitignore
- Renamed network role directory to networking
- *(ansible)* Consolidated package installation across roles
- Refactored inventory configuration, updated host variables, and renamed x role to xorg
- Update various configurations and add micro task placeholder
- Renamed login role to display-manager
- Refactor: Consolidate WM roles and restructure base

## [0.8.6] - 2025-05-31

### 🚀 Features

- Dynamically configured ansible_connection based on hostname
- Refactored playbooks for modularity and added IWD support
- Added gnfzdz.archlinux, gnfzdz.base and gnfzdz.network collections
- Implemented rbenv for Ruby version management
- Added video and xwayland roles

### 🐛 Bug Fixes

- Resolved mDNS host resolution and reordered Ansible plugins
- - Commented out the print statement to ensure valid JSON output for Ansible in dynamic_inventory.py
- Refactored playbook imports in full.yml
- Renamed gem.yml to gems.yml in rbenv.yml
- Added `--conservative` flag to gem install commands

### ⚙️ Miscellaneous Tasks

- Updated README to reflect roles directory structure
- Fixed typo in ruby_build_version variable
- Updated shell executable to zsh

## [0.8.5] - 2025-05-30

### 🚀 Features

- Implement polybar configuration with audio, bars, modules, and user modules
- Enable autologin for virtual console
- Add llm_analyzer callback plugin for AI-powered Ansible analysis
- Integrate Langfuse for prompt management in llm_analyzer.py
- Enhance homepage with AI search portal and tabbed AI assistants
- Implemented audio role with JACK, PulseAudio, PipeWire support
- Added sway role for configuring the Sway window manager
- Moved rofi role out of i3 role
- Implemented login role with greetd and getty support
- Updated sway configuration and added new features
- Updated Sway role README
- Implemented dynamic inventory script and updated Ansible configuration
- Enhanced dynamic inventory with group and host variable support
- Added homepageV2

### 🐛 Bug Fixes

- Removed --ultra -20 from COMPRESSZST in makepkg.conf.j2
- - Replaced `rvm_install == 'true'` with `rvm_install|default(false)|bool == true` for proper boolean evaluation in Jinja2 templates.
- Rearranged the rescue and ensure blocks in the sway role
- Changed `ensure` to `always` for block rescue
- Changed loop to with_items in ruby role
- Added window_manager variable to roles/shell/defaults/main.yml
- Added --config-file ~/.gemrc to gem list command

### 🚜 Refactor

- Networkmanager role to network

### ⚙️ Miscellaneous Tasks

- Commented out legacy networking tasks in systemd-networkd role
- Adjusted role order and updated package list
- Fixed typo in libvirt role
- Added rvm_install boolean to lapbot.yml
- Refactored systemd-timesyncd service management
- Standardized capitalization of 'Rebuild grub' in notify handlers
- Updated README files for audio, desktop, tools, and x roles

## [0.8.0] - 2025-05-02

### 🚀 Features

- Enhance user environment configuration
- Add fabric.yml playbook for automating fabric setup
- Configure .profile and .zshenv templates, add aliases, and update tasks
- Update ansible playbooks and roles
- Added i3 config to soundbot, removed dbbot01, updated gitignore
- Add firewall configuration playbook
- Added NFS server role and configured bind mounts
- Add ssh role
- Add tools role with code-packager and whisper-stream tasks
- Enhanced workstation setup with new features and improved documentation
- Enhance bridge configuration playbook
- Rename project to syncopated-ansible and update dependencies
- Added bootloader variable with default value of grub
- Add become_user to grub-hook task
- Add fd and ripgrep zsh plugins
- Enhance Ruby role and update X packages
- Enhance i3 role with rofi and config improvements
- Update code-packager and whisper-stream roles
- Add sxhkd, picom, dunst, and xdg tasks
- Add script to install missing gems
- Refactor package management in docker and libvirt roles
- Update hostvars, grub role, and systemd-networkd role

### 🐛 Bug Fixes

- Set grub as the default bootloader
- Add default ssh port
- Add shell tasks and update user template paths
- Create gemrc files and set --no-user-install
- Corrected gem install path from /use/bin to /usr/bin in ruby role
- Corrected nfs service name in nfs.yml

### ⚙️ Miscellaneous Tasks

- Update i3 configuration and inventory
- Update Ansible roles for i3 and ruby
- Refactor privilege escalation settings in ansible.cfg
- Refactor X11 role for improved flexibility and debugging
- Refactor roles to 'x' and consolidate tasks
- Move rofi configurations to i3 role
- Update sshd_config.j2 template path
- Update SSH role
- Added nas_host, display_manager, and desktop_environment variables to main.yml
- Update input-remapper role
- Commented out debug task in ruby role
- Refactor gemrc file creation in roles/ruby/tasks/main.yml
- Refactor ruby role tasks
- Set become to False for rubies.yml import
- Update ansible configuration and inventory
- Uncomments yaml and fqcn in .ansible-lint

## [0.5.0] - 2025-03-11

### 🚀 Features

- Add script to create network bridges using nmcli
- Added audiosplitter.rb to split audio files based on silence detection
- Add autosync functionality via udev and systemd
- Add bat-preview script for fzf.vim
- Add brightness control scripts
- Added cleanup.sh script to remove old files
- Add convert2ogg.sh and convert_to_mono_and_resample.sh scripts
- Add deepgram_parser.rb to parse Deepgram JSON output
- Add docker-volume-backup.sh script
- Add custom scripts for file opening, link handling, and screenshots
- Added process_video.sh script for video and audio processing
- Add script to create .deja-dup-ignore files in specified folders
- Add errlog.sh to display system logs and failed services
- Add search_web.sh script for web searching and documentation lookup
- Added set-govna.sh script for CPU frequency scaling
- Added stuff2tts.sh script for text-to-speech using edge-playback
- Add script to set PulseAudio card profiles to off
- Enhance user role with script syncing and zsh packages
- Added split_by_silence.sh script

## [0.1.0] - 2025-03-08

### 🚀 Features

- Add ansible-aur module 📦
- Create user role 🧑‍💻
- Create user role 🧑‍💻
- Add ansible-lint configuration and ignore file 🚀
- Added a comprehensive list of shell packages to be installed 🐚
- Enhance user role with Zsh configuration and aliases 🚀
- ✨ Added new zsh completions, functions, and theme
- Rename user.yml to setup.yml and add pre_tasks
- Improve package management and repository handling
- Enhance user role with shell configuration and package management
- Refactor package list into a dedicated vars file
- Add pandoc to list of packages in main.yml
- Refactor base role tasks and add handler flushing
- Update Ansible Configuration and Roles
- Add docker role
- Add tags to docker tasks
- Add bootstrap script and gum helpers
- Added openssh, zsh, oh-my-zsh-git, and desktop packages to vars/main.yml
- Refactor ansible roles for improved package management and user configuration
- Add libvirt role
- Add input-remapper role for key remapping
- Add whisper-stream setup playbook
- Refactor input-remapper role and add x11 role
- Added x11 package list to vars/main.yml
- Add initial Vagrantfile for Arch Linux with libvirt provider
- Add rofi role for application launcher
- Configure i3 as the default window manager
- Add i3 window manager role
- Create sxhkd role
- Add xdg role
- Add color variables to group_vars
- Add server.yml playbook and workstation roles
- Add updatedb task to base role
- Add ruby role for RVM-based Ruby environment management
- Initial commit of homepage role
- Improve inventory structure and enable docker
- Implement NAS role with NFS and Samba support
- Add networking role with firewall, NTP, and interface configurations
- Add code-packager.yml playbook
- Add code-packager, whisper-stream, and input-remapper playbooks to workstation.yml
- Add i3 configuration and update packages
- Updated i3 configuration and added new alias
- Configure Docker storage location and daemon settings
- Add distro name and debugging
- Refactor base role for improved package management and configuration
- Add pi.yml playbook and update host targets
- Add aarch64 support
- Update package list and remove i3 scripts
- Improve user role and sxhkd configuration
- Refactor README.md for comprehensive documentation

### 🐛 Bug Fixes

- Ensure micro is set as the default editor only if not already set or is not micro

### 💼 Other

- Figure out why this isn't being seen by the template
- - Ensures `~/.local/bin` exists for user scripts
- Update host vars and add fabric placeholder

### ⚙️ Miscellaneous Tasks

- Refactor git commit alias to remove -a flag
- Add 'always' tag to set_fact task in setup.yml
- Refactor inventory configurations

<!-- generated by git-cliff -->