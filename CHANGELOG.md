# Changelog

All notable changes to this project will be documented in this file.

## [unreleased]

### 🚀 Features

- Enable autologin for virtual console
- Add llm_analyzer callback plugin for AI-powered Ansible analysis
- Integrate Langfuse for prompt management in llm_analyzer.py
- Enhance homepage with AI search portal and tabbed AI assistants
- Implemented audio role with JACK, PulseAudio, PipeWire support
- Added Sway role for configuring the Sway window manager
- Moved rofi role out of i3 role
- Implemented login role with greetd and getty support
- Updated Sway configuration and added new features
- Implemented dynamic inventory script and updated Ansible configuration
- Enhanced dynamic inventory with group and host variable support

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
