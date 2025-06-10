---
title: Ansible Playbook for Source Installation of Specified Packages on Red Hat Family Systems
last updated: Monday, June 9th 2025, 5:31:00 am
tags:
  - ansible
  - ansible-playbooks
  - automation
  - development-environment
  - linux
  - package-management
  - redhat
  - source-installation
  - system-configuration
---

[‎Gemini - Ansible Package Installation Failure](https://g.co/gemini/share/d76986500131)
## I. Introduction

This document outlines a comprehensive approach to installing a specified list of software packages from their source code on Red Hat Enterprise Linux (RHEL) and Fedora systems using Ansible. The necessity to compile packages from source often arises when specific versions are required, when packages are not available in standard repositories, or when custom compile-time configurations are needed. While package managers like DNF simplify software management, source compilation offers greater flexibility at the cost of increased complexity in installation and maintenance.

Ansible, an open-source automation tool, can effectively manage the process of source compilation, ensuring consistency, repeatability, and a degree of idempotency. This report details the prerequisites, Ansible playbook design considerations, and specific tasks for installing the target software. The goal is to provide a robust and maintainable automated solution.

The packages that were reported as unavailable through standard package management and are targeted for source installation include: `bandwhich`, `base-devel` (interpreted as the "Development Tools" group), `bash-language-server`, `bottom`, `choose`, `chromaprint`, `cpupower`, `curlie`, `dex`, `downgrade`, `duf`, `dust`, `eza`, `faac`, `fd`, `fsarchiver`, `github-cli`, `glow`, `gping`, `graphicsmagick`, `gst-libav`, `gstreamer`, `gum`, `i7z`, `imagemagick`, `inetutils`, `libgit2-glib`, `libvips`, `mako`, `micro`, `nano-syntax-highlighting`, `nuspell`, `python-adblock`, `python-edge-tts`, `python-j2cli`, `python-sphinx-intl`, `ripgrep-all`, `realtime-privileges`, `sd`, `swappy`, `ueberzug`, `v4l-utils`, and `yt-dlp`.

## II. Prerequisites and Build Environment Setup

A well-prepared build environment is crucial for successful source compilation. This section details the necessary components and their setup using Ansible on a Fedora/RHEL system.

### A. Core Build Utilities (Equivalent to `base-devel`)

On Red Hat family systems, the equivalent of the `base-devel` group (common in Arch Linux) or `build-essential` (common in Debian/Ubuntu) is the "Development Tools" group. This group provides essential compilers and tools like GCC, G++, make, and others necessary for compiling software from source.1

YAML

```shell
- name: Install Development Tools group
  ansible.builtin.dnf:
    name: "@Development Tools"
    state: present
  become: true
```

Additionally, `kernel-devel` and `kernel-headers` are often required for building kernel modules or software that interacts closely with the kernel. `elfutils-libelf-devel` and `openssl-devel` are common dependencies for many C/C++ projects.

YAML

```shell
- name: Install essential development headers and libraries
  ansible.builtin.dnf:
    name:
      - kernel-devel
      - kernel-headers
      - elfutils-libelf-devel
      - openssl-devel
      - autoconf
      - automake
      - libtool
      - pkgconf # Provides pkg-config
      - gettext-devel
      - cmake
      - python3-devel # For tools with Python bindings or build scripts
      - python3-pip # For installing Python-based build tools or dependencies
      - patch
      - bzip2-devel
      - xz-devel
      - zlib-devel
      - readline-devel
      - sqlite-devel
      - libffi-devel
    state: present
  become: true
```

### B. Git Installation

Source code is almost universally managed and distributed via Git. The `git` package is required to clone repositories.

YAML

```shell
- name: Install Git
  ansible.builtin.dnf:
    name: git
    state: present
  become: true
```

This task ensures that Git is available for subsequent tasks that involve cloning source repositories.1

### C. Installing Rust and Cargo

Several of the requested tools (`bandwhich`, `eza`, `dust`, `fd-find`, `bottom`, `ripgrep-all`, `sd`) are written in Rust and built using Cargo, Rust's package manager and build tool. The recommended way to install Rust is via `rustup`.3

YAML

```shell
- name: Check if rustup is installed
  ansible.builtin.stat:
    path: "{{ ansible_env.HOME }}/.cargo/bin/rustup"
  register: rustup_stat

- name: Download rustup-init.sh
  ansible.builtin.get_url:
    url: https://sh.rustup.rs
    dest: /tmp/rustup-init.sh
    mode: '0755'
  when: not rustup_stat.stat.exists

- name: Install rustup and default toolchain
  ansible.builtin.command:
    cmd: /tmp/rustup-init.sh -y --no-modify-path
    creates: "{{ ansible_env.HOME }}/.cargo/bin/rustup"
  when: not rustup_stat.stat.exists
  environment:
    RUSTUP_HOME: "{{ ansible_env.HOME }}/.cargo"
    CARGO_HOME: "{{ ansible_env.HOME }}/.cargo"

- name: Ensure.cargo/bin is in PATH for current Ansible user (for this play)
  ansible.builtin.set_fact:
    ansible_env: "{{ ansible_env | combine({'PATH': ansible_env.HOME + '/.cargo/bin:' + ansible_env.PATH}) }}"

# Ensure.cargo/bin is in PATH for future interactive shell sessions
- name: Add.cargo/bin to.bashrc for persistent PATH
  ansible.builtin.lineinfile:
    path: "{{ ansible_env.HOME }}/.bashrc"
    line: 'export PATH="$HOME/.cargo/bin:$PATH"'
    create: true
    regexp: '^export PATH="\$HOME/\.cargo/bin:\$PATH"$'
  when: ansible_shell_type == "bash" # Adjust for other shells if necessary

- name: Add.cargo/bin to.profile for persistent PATH (often used by sh and for login shells)
  ansible.builtin.lineinfile:
    path: "{{ ansible_env.HOME }}/.profile"
    line: 'export PATH="$HOME/.cargo/bin:$PATH"'
    create: true
    regexp: '^export PATH="\$HOME/\.cargo/bin:\$PATH"$'
  when: ansible_shell_type == "bash" # Or if.profile is generally used
```

The installation of Rust via `rustup` is preferred as it allows easy management of toolchains and updates.6 The `ansible.builtin.set_fact` task updates the `PATH` for the current Ansible execution context, while `lineinfile` ensures it's set for future user sessions.

### D. Installing Go

A number of tools in the list (`gping`, `curlie`, `github-cli`, `duf`, `micro`, `gum`) are Go-based. Installing the Go toolchain involves downloading the official binary release, extracting it, and setting up environment variables.8

YAML

```shell
- name: Define Go version and checksum
  ansible.builtin.set_fact:
    go_version: "1.22.3" # Check go.dev/dl for the latest stable version
    go_checksum: "sha256:90a9ef369090418dec537969fb31e88549743091f1e20915558c67f63791726e" # SHA256 for go1.22.3.linux-amd64.tar.gz

- name: Check if Go is installed
  ansible.builtin.stat:
    path: "/usr/local/go/bin/go"
  register: go_stat

- name: Download Go binary
  ansible.builtin.get_url:
    url: "https://go.dev/dl/go{{ go_version }}.linux-amd64.tar.gz"
    dest: "/tmp/go{{ go_version }}.linux-amd64.tar.gz"
    checksum: "{{ go_checksum }}"
  when: not go_stat.stat.exists or (go_version not in (go_installed_version.stdout | default(''))) # Heuristic for version check

- name: Get installed Go version (if exists)
  ansible.builtin.command: /usr/local/go/bin/go version
  register: go_installed_version
  changed_when: false
  failed_when: false
  when: go_stat.stat.exists

- name: Remove previous Go installation if different version needed
  ansible.builtin.file:
    path: /usr/local/go
    state: absent
  become: true
  when: go_stat.stat.exists and (go_version not in (go_installed_version.stdout | default('')))

- name: Extract Go binary
  ansible.builtin.unarchive:
    src: "/tmp/go{{ go_version }}.linux-amd64.tar.gz"
    dest: /usr/local
    remote_src: true
  become: true
  when: not go_stat.stat.exists or (go_version not in (go_installed_version.stdout | default('')))

- name: Ensure Go binary path is in /etc/profile.d
  ansible.builtin.copy:
    dest: /etc/profile.d/go_custom.sh # Use a distinct name
    content: |
      export PATH=$PATH:/usr/local/go/bin
      export GOPATH=$HOME/go
      export PATH=$PATH:$GOPATH/bin
    mode: '0644' # Scripts in profile.d are sourced, not executed directly
  become: true

- name: Ensure Go bin is in current Ansible execution PATH
  ansible.builtin.set_fact:
    ansible_env: "{{ ansible_env | combine({'PATH': '/usr/local/go/bin:' + ansible_env.PATH}) }}"
  when: not '/usr/local/go/bin' in ansible_env.PATH

- name: Ensure GOPATH/bin is in current Ansible execution PATH
  ansible.builtin.set_fact:
    ansible_env: "{{ ansible_env | combine({'PATH': ansible_env.HOME + '/go/bin:' + ansible_env.PATH}) }}"
  when: not (ansible_env.HOME + '/go/bin') in ansible_env.PATH
```

This setup ensures that Go binaries can be found and that Go-based tools can be compiled and installed correctly, often into `$GOPATH/bin`.8

### E. (Optional but Recommended) Configuring Additional Repositories (EPEL, RPM Fusion)

Some build dependencies, particularly for multimedia packages like FFmpeg or GStreamer plugins, might reside in third-party repositories such as EPEL (Extra Packages for Enterprise Linux) for RHEL derivatives or RPM Fusion for Fedora.10 Enabling these can simplify the installation of complex dependencies that are not the primary target for source compilation but are needed to build other tools.

YAML

```shell
- name: Install EPEL release package (for RHEL/CentOS/AlmaLinux/Rocky)
  ansible.builtin.dnf:
    name: epel-release
    state: present
  become: true
  when: ansible_facts['os_family'] == 'RedHat' and ansible_facts['distribution']!= 'Fedora'

- name: Install RPM Fusion free release package (for Fedora)
  ansible.builtin.dnf:
    name: "https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-{{ ansible_facts['distribution_major_version'] }}.noarch.rpm"
    state: present
    disable_gpg_check: false # GPG keys should be imported or handled by dnf
  become: true
  when: ansible_facts['distribution'] == 'Fedora'

- name: Install RPM Fusion non-free release package (for Fedora)
  ansible.builtin.dnf:
    name: "https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{{ ansible_facts['distribution_major_version'] }}.noarch.rpm"
    state: present
    disable_gpg_check: false # GPG keys should be imported or handled by dnf
  become: true
  when: ansible_facts['distribution'] == 'Fedora'
```

These repositories are crucial for packages like `ffmpeg` and `gst-libav` which often have licensing or patent encumbrances that prevent their inclusion in official Fedora or RHEL repositories.12

## III. Ansible Playbook Design and Structure

A well-structured Ansible playbook is essential for managing the complexity of compiling multiple packages from source.

### A. Recommended Playbook/Role Structure

For maintainability and reusability, a role-based structure is highly recommended. A `common_build_env` role can handle the prerequisite setup described in Section II. Individual roles can then be created for each complex package or for groups of packages that share similar build systems (e.g., `rust_tools`, `go_tools`).

Example directory structure:

```shell
playbook.yml
roles/
  common_build_env/
    tasks/main.yml   # Tasks from Section II
    vars/main.yml    # Variables for Go/Rust versions, etc.
  package_bandwhich/ # Example for a single package
    tasks/main.yml
    vars/main.yml
  rust_tools/        # Example for a group of Rust tools
    tasks/main.yml
    vars/main.yml    # List of Rust tools, repo URLs, etc.
    # templates/     # If any config files needed by these tools
  #... other roles
```

This modular approach allows for easier updates and management of individual components.

### B. Key Ansible Modules for Source Installation

The following Ansible modules are fundamental for automating source installations:

* `ansible.builtin.dnf`: Installs build dependencies from system repositories.
* `ansible.builtin.git`: Clones source code repositories.
* `ansible.builtin.unarchive`: Extracts downloaded source tarballs.
* `ansible.builtin.command` / `ansible.builtin.shell`: Executes compilation and installation commands (e.g., `make`, `cargo build`, `./configure`). The `shell` module should be used when shell-specific features like pipes or complex variable expansion are needed; otherwise, `command` is preferred for security and predictability. The `creates` argument is vital for ensuring these tasks are idempotent.
* `ansible.builtin.stat`: Checks for the existence of files or directories to determine if a build or installation step can be skipped.
* `ansible.builtin.file`: Manages files and directories, including creating source/build directories, setting permissions, and creating symbolic links.
* `ansible.builtin.copy` / `ansible.builtin.template`: Deploys configuration files, helper scripts, or service files.
* `ansible.builtin.pip`: Installs Python packages from source or PyPI, useful for Python-based tools or build dependencies.
* `ansible.builtin.make`: A more specialized module for running `make` targets, offering better control over `chdir`, `target`, and `params`.

### C. Variables and Idempotency Considerations

Using variables for source URLs, package versions, compilation flags, and installation paths (e.g., `/usr/local/src` for sources, `/usr/local/bin` for executables) enhances playbook flexibility and maintainability.

Idempotency is a core principle of Ansible. For source compilation, this is primarily achieved by:

1. Using the `creates` parameter with `ansible.builtin.command`, `ansible.builtin.shell`, or `ansible.builtin.make`. This parameter specifies a file path; if the file exists, the task is skipped. For example, `creates: /usr/local/bin/myprogram` would prevent recompilation if `myprogram` is already installed.
2. Employing `ansible.builtin.stat` to check for the existence of target binaries or key build artifacts before attempting to clone, compile, or install.
3. Ensuring that package dependency installation tasks (`ansible.builtin.dnf`, `ansible.builtin.pip`) are inherently idempotent.

### D. Error Handling and Verbosity

Robust error handling involves:

* Using the `failed_when` conditional in tasks to define custom failure conditions based on return codes or output.
* Registering the output of critical tasks (`register: task_output`) and using `ansible.builtin.debug: var=task_output` for troubleshooting.
* Running Ansible with increased verbosity (`-v`, `-vv`, `-vvv`) during development to inspect task execution details.

## IV. Playbook Tasks: Installing Packages from Source

This section provides a general overview of the information required for each package and then details the installation process for representative packages based on their build systems.

### Package Installation Overview

The following table summarizes key information for the packages to be installed from source. This aids in planning and understanding the requirements for each.

|   |   |   |   |   |
|---|---|---|---|---|
|**Package Name**|**Primary Source URL**|**Build System**|**Key System Dependencies (Fedora/RHEL) Example**|**Notes/Complexity**|
|`bandwhich`|`https://github.com/imsnif/bandwhich` 3|Cargo (Rust)|`rustc`, `cargo`, `libcap` (for `setcap`)|Requires `setcap` post-install 3|
|`bash-language-server`|`https://github.com/bash-lsp/bash-language-server`|npm|`nodejs`, `npm`|Node.js package|
|`bottom`|`https://github.com/ClementTsang/bottom` 16|Cargo (Rust)|`rustc`, `cargo`|Cross-platform system monitor 16|
|`choose`|`https://github.com/theryangeary/choose` 5|Cargo (Rust)|`rustc`, `cargo`|Text manipulation utility 5|
|`chromaprint`|`https://github.com/acoustid/chromaprint` 17|CMake|`cmake`, `gcc-c++`, `ffmpeg-devel`, `fftw-devel` 17|Audio fingerprinting library 17|
|`cpupower`|Part of `kernel-tools`|System Package|`kernel-tools`|System utility, not typically compiled standalone 19|
|`curlie`|`https://github.com/rs/curlie` 20|Go|`golang`|Frontend for curl 20|
|`dex`|`https://github.com/jceb/dex` 21|Python (setup.py/make)|`python3`, `python3-setuptools`, `make`|Desktop entry runner 21|
|`duf`|`https://github.com/muesli/duf` 23|Go|`golang`|Disk usage/free utility 23|
|`dust`|`https://github.com/bootandy/dust` 24|Cargo (Rust)|`rustc`, `cargo`|`du` alternative 24|
|`eza`|`https://github.com/eza-community/eza` 25|Cargo (Rust)|`rustc`, `cargo`|`ls` replacement 4|
|`faac`|`https://github.com/knik0/faac` (example)|Autotools|`gcc`, `make`, `autoconf`, `automake`|AAC encoder|
|`fd` (`fd-find`)|`https://github.com/sharkdp/fd` 26|Cargo (Rust)|`rustc`, `cargo`|`find` alternative 26|
|`fsarchiver`|`https://github.com/fdupoux/fsarchiver` 27|Autotools/CMake|`gcc-c++`, `make`, `zlib-devel`, `bzip2-devel`, `lzo-devel`, `xz-devel`, `e2fsprogs-devel`, `attr-devel`|Filesystem archiver 27|
|`github-cli` (`gh`)|`https://github.com/cli/cli` 28|Go (`make`)|`golang`, `make`|GitHub command-line tool 28|
|`glow`|`https://github.com/charmbracelet/glow` 29|Go|`golang`|Markdown reader 29|
|`gping`|`https://github.com/orf/gping` 30|Cargo (Rust)|`rustc`, `cargo`|Ping with a graph 30|
|`graphicsmagick`|`http://www.graphicsmagick.org/` (Mercurial) 31|Autotools|`gcc-c++`, `make`, `libjpeg-turbo-devel`, `libpng-devel`, `libtiff-devel`, `ghostscript-devel`, `freetype-devel`, `libxml2-devel`|Image processing 31|
|`gst-libav`|`https://gstreamer.freedesktop.org/src/gst-libav/`|Meson|`meson`, `gstreamer1-devel`, `ffmpeg-devel` (from RPM Fusion)|GStreamer FFmpeg plugin 14|
|`gstreamer` (core)|`https://gstreamer.freedesktop.org/src/gstreamer/`|Meson|`meson`, `glib2-devel`, `gobject-introspection-devel`, `bison`, `flex`|Multimedia framework 32|
|`gum`|`https://github.com/charmbracelet/gum` 33|Go|`golang`|CLI tool for shell scripts 33|
|`i7z`|`https://github.com/ajaiantilal/i7z` 34|Make (C)|`gcc`, `make`, `ncurses-devel` (for TUI)|CPU reporting tool 34|
|`imagemagick`|`https://github.com/ImageMagick/ImageMagick` 35|Autotools|`gcc-c++`, `make`, `libjpeg-turbo-devel`, `libpng-devel`, etc.|Image processing 35|
|`inetutils`|`https://ftp.gnu.org/gnu/inetutils/` 37|Autotools|`gcc`, `make`, `texinfo` (for docs), `ncurses-devel` (for some tools)|GNU network utilities 37|
|`libgit2-glib`|`https://gitlab.gnome.org/GNOME/libgit2-glib` 39|Meson|`meson`, `libgit2-devel`, `glib2-devel`, `gobject-introspection-devel`|GLib wrapper for libgit2 39|
|`libvips`|`https://github.com/libvips/libvips` 41|Meson|`meson`, `glib2-devel`, `expat-devel`, `libjpeg-turbo-devel`, etc.|Image processing library 41|
|`mako` (notification daemon)|`https://github.com/emersion/mako` 42|Meson|`meson`, `wayland-devel`, `pango-devel`, `cairo-devel`, `systemd-devel` (or `elogind-devel`), `gdk-pixbuf2-devel`|Wayland notification daemon 42|
|`micro`|`https://github.com/zyedidia/micro` 43|Go (`make build`)|`golang`, `make`|Terminal text editor 43|
|`nano-syntax-highlighting`|`https://github.com/scopatz/nanorc` 44|File copy|`git`|Nano editor syntax files 44|
|`nuspell`|`https://github.com/nuspell/nuspell` 45|CMake|`cmake`, `gcc-c++`, `icu-devel` (libicu-devel)|Spell checker 45|
|`python-adblock`|`https://pypi.org/project/adblock/` 46|Maturin (Rust/Python)|`python3-pip`, `rustc`, `cargo`, `maturin`|Python adblocking library 46|
|`python-edge-tts`|`https://github.com/rany2/edge-tts` 47|Python (pip)|`python3-pip`, `mpv` (runtime for edge-playback)|Microsoft Edge TTS from Python 47|
|`python-j2cli`|`https://github.com/m000/jj2cli` 49|Python (pip)|`python3-pip`|Jinja2 CLI tool 49|
|`python-sphinx-intl`|`https://github.com/sphinx-doc/sphinx-intl` 50|Python (pip/pyproject)|`python3-pip`, `python3-setuptools`, `wheel`|Sphinx internationalization utility 50|
|`ripgrep-all`|`https://github.com/phiresky/ripgrep-all` 52|Cargo (Rust)|`rustc`, `cargo`, `pandoc`, `poppler-utils`, `ffmpeg`, `ripgrep`|Ripgrep with more file types 52|
|`sd` (intuitive find & replace)|`https://github.com/chmln/sd` 55|Cargo (Rust)|`rustc`, `cargo`|Find & replace CLI tool 55|
|`swappy`|`https://github.com/jtheoof/swappy` 56|Meson|`meson`, `ninja-build`, `cairo-devel`, `pango-devel`, `gtk3-devel`, `glib2-devel`, `scdoc`|Wayland screenshot tool 56|
|`ueberzug`|`https://github.com/ueber-devel/ueberzug` 57|Mesonpy (Python/C)|`python3-pip`, `meson`, `meson-python`, `libX11-devel`, `libXext-devel`, `libXRes-devel`, `python3-devel`|Image display in terminal 57|
|`v4l-utils`|`https://git.linuxtv.org/v4l-utils.git` 58|Autotools/Meson|`make`, `gcc`, `libtool`, `gettext`, `udev-devel`, `alsa-lib-devel`, `jpeg-devel`, (potentially `qt5-qtbase-devel` for qv4l2)|Video4Linux utilities 58|
|`yt-dlp`|`https://github.com/yt-dlp/yt-dlp` 62|Python (pip/make)|`python3-pip`, `ffmpeg` (runtime)|Video downloader 62|

*(Note: Specific versions for dependencies and source checkouts should be determined based on compatibility and stability requirements. The `-devel` suffix is typical for Fedora/RHEL library packages needed for compilation.)*

A general structure for Ansible tasks to compile a package from source includes:

1. **Install Build Dependencies:** Use `ansible.builtin.dnf` to install system-level libraries and tools.
2. **Create Source Directory:** Use `ansible.builtin.file` to create a directory (e.g., `/usr/local/src/packagename`).
3. **Clone Repository:** Use `ansible.builtin.git` to clone the source code.
4. **Compile:** Use `ansible.builtin.command`, `ansible.builtin.shell`, or `ansible.builtin.make` module with `chdir` to the source directory. Include the `creates` argument pointing to an expected build artifact (e.g., the main executable or a key library file) to ensure idempotency.
5. **Install:** Use `ansible.builtin.command`, `ansible.builtin.shell`, or `ansible.builtin.make install`. Include the `creates` argument pointing to the final installed location of the primary executable or library.
6. **Post-Installation:** Any necessary steps like running `ldconfig` (for shared libraries installed in non-standard paths that are configured in `ld.so.conf.d`), or using `setcap`.

### A. Rust-Based Tools

Tools like `bandwhich`, `eza`, `dust`, `fd`, `bottom`, `gping` (orf/gping), and `sd` (chmln/sd) are built using Cargo. The general process involves cloning the repository and running `cargo build --release` followed by copying the binary from `target/release/` to a directory in the `$PATH`.

**Example Package: `eza`** 4

* Source: `https://github.com/eza-community/eza.git`
* Build System: Cargo
* Dependencies: Rust/Cargo (from prerequisites). `libgit2-devel` might be needed if its git features are compiled in and not vendored. For Fedora, `zlib-devel` is also a common implicit dependency for Rust projects.

YAML

```shell
- name: Install eza build dependencies (if any beyond Rust)
  ansible.builtin.dnf:
    name:
      - zlib-devel # Often needed by Rust projects
      # - libgit2-devel # If eza's git feature requires system libgit2
    state: present
  become: true

- name: Clone eza repository
  ansible.builtin.git:
    repo: 'https://github.com/eza-community/eza.git'
    dest: "/usr/local/src/eza"
    version: 'main' # Or a specific release tag like 'v0.18.18'
  become: true # If /usr/local/src requires root

- name: Compile eza
  ansible.builtin.command:
    cmd: "{{ ansible_env.HOME }}/.cargo/bin/cargo build --release"
    chdir: "/usr/local/src/eza"
    creates: "/usr/local/src/eza/target/release/eza"
  environment:
    PATH: "{{ ansible_env.PATH }}" # Assumes.cargo/bin was added earlier

- name: Install eza
  ansible.builtin.copy:
    src: "/usr/local/src/eza/target/release/eza"
    dest: "/usr/local/bin/eza"
    mode: '0755'
    remote_src: true
  become: true
```

This pattern can be adapted for other Rust-based tools, adjusting repository URLs, versions, and any specific system dependencies. For `bandwhich`, post-installation involves `setcap` to grant necessary network capabilities.3

YAML

```shell
# Example specific post-install for bandwhich
- name: Set capabilities for bandwhich
  ansible.builtin.command:
    cmd: "setcap cap_sys_ptrace,cap_dac_read_search,cap_net_raw,cap_net_admin+ep /usr/local/bin/bandwhich"
  become: true
  changed_when: false # setcap output is not ideal for changed status
  when: "'bandwhich' in item.name" # Assuming a loop or specific task
```

### B. Go-Based Tools

Go tools such as `micro`, `github-cli` (`gh`), `duf`, `curlie`, and `gum` are typically built using `go build` or `go install`. The resulting binary is often statically linked and self-contained.

**Example Package: `micro`** 43

* Source: `https://github.com/zyedidia/micro.git`
* Build System: Go (often via a `Makefile` which calls `go build`)
* Dependencies: Go toolchain (from prerequisites).

YAML

```shell
- name: Clone micro text editor repository
  ansible.builtin.git:
    repo: 'https://github.com/zyedidia/micro.git'
    dest: "/usr/local/src/micro"
    version: 'v2.0.13' # Use a specific stable tag

- name: Compile micro text editor
  ansible.builtin.make: # Using make module as micro has a Makefile
    chdir: "/usr/local/src/micro"
    target: build # 'build' target is specified in micro's Makefile [43]
    params:
      # CGO_ENABLED: 0 # For a static binary if desired and supported, Makefile might handle this
  environment:
    PATH: "/usr/local/go/bin:{{ ansible_env.GOPATH | default(ansible_env.HOME + '/go') }}/bin:{{ ansible_env.PATH }}"
    GOPATH: "{{ ansible_env.GOPATH | default(ansible_env.HOME + '/go') }}"
  register: micro_compile_result
  changed_when: "'already up to date' not in micro_compile_result.stdout" # Make is often idempotent
  # 'creates' is harder with 'make' if the binary is not in the chdir path directly after build.
  # A stat check before this task or relying on make's idempotency is an alternative.

- name: Install micro text editor
  ansible.builtin.copy:
    src: "/usr/local/src/micro/micro" # Makefile puts binary here [43]
    dest: "/usr/local/bin/micro"
    mode: '0755'
    remote_src: true
  become: true
  # Add 'creates: /usr/local/bin/micro' to a stat task before cloning/compiling for full idempotency
```

For Go tools that don't use a Makefile, a direct `go build` command can be used:

YAML

```shell
# Generic Go build example (e.g., for curlie if it had no Makefile)
- name: Compile Go tool {{ item.name }}
  ansible.builtin.command:
    cmd: "/usr/local/go/bin/go build -ldflags='-s -w' -o {{ item.binary_name }}"
    chdir: "/usr/local/src/{{ item.name }}"
    creates: "/usr/local/src/{{ item.name }}/{{ item.binary_name }}"
  environment:
    PATH: "/usr/local/go/bin:{{ ansible_env.GOPATH | default(ansible_env.HOME + '/go') }}/bin:{{ ansible_env.PATH }}"
    GOPATH: "{{ ansible_env.GOPATH | default(ansible_env.HOME + '/go') }}"
  loop: "{{ go_packages }}" # Assuming go_packages is a list of dicts
```

### C. C/C++ Tools with Autotools/CMake/Meson

This category includes many traditional Unix utilities and libraries like `imagemagick`, `graphicsmagick`, `chromaprint`, `fsarchiver`, `libvips`, and `v4l-utils`. The build process typically involves `./configure && make && make install` (Autotools), or `cmake. && make && make install` (CMake), or `meson setup builddir && ninja -C builddir && ninja -C builddir install` (Meson). Identifying all `-devel` packages for dependencies is critical.

**Example Package: `ImageMagick`** 35

* Source: `https://github.com/ImageMagick/ImageMagick.git`
* Build System: Autotools
* Dependencies (Fedora names): `libjpeg-turbo-devel`, `libpng-devel`, `libtiff-devel`, `giflib-devel`, `freetype-devel`, `libxml2-devel`, `lcms2-devel`, `libwebp-devel`, `ghostscript`, `make`, `gcc-c++`. `libheif-devel` might require an external repository or its own source build if HEIC support is crucial and not easily available.

YAML

```shell
- name: Install ImageMagick build dependencies
  ansible.builtin.dnf:
    name:
      - libjpeg-turbo-devel
      - libpng-devel
      - libtiff-devel
      - giflib-devel
      - freetype-devel
      - libxml2-devel
      - lcms2-devel
      - libwebp-devel
      # - libheif-devel # May need COPR or to be built from source
      - ghostscript
      - make
      - gcc-c++
    state: present
  become: true

- name: Clone ImageMagick repository
  ansible.builtin.git:
    repo: 'https://github.com/ImageMagick/ImageMagick.git'
    dest: "/usr/local/src/ImageMagick"
    version: '7.1.1-30' # Example: Use a specific, tested release tag
    depth: 1 # Shallow clone for a specific tag is faster
  become: true # If /usr/local/src requires root

- name: Configure ImageMagick
  ansible.builtin.command:
    cmd: "./configure --with-modules" # Add other flags like --with-heic=yes if libheif-devel is available
    chdir: "/usr/local/src/ImageMagick"
    creates: "/usr/local/src/ImageMagick/config.status"
  become: true # Configure might check for system paths

- name: Compile ImageMagick
  ansible.builtin.make:
    chdir: "/usr/local/src/ImageMagick"
    jobs: "{{ ansible_processor_vcpus }}"
  become: true # If source dir is root-owned and make writes build artifacts there
  register: imagemagick_make_result
  changed_when: "'Nothing to be done' not in imagemagick_make_result.stdout"
  # `creates` for make target is tricky if it's not a single binary.
  # Rely on make's idempotency or check for a key library/binary.

- name: Install ImageMagick
  ansible.builtin.make:
    chdir: "/usr/local/src/ImageMagick"
    target: install
  become: true
  register: imagemagick_install_result
  changed_when: "'Nothing to be done' not in imagemagick_install_result.stdout and 'is up to date' not in imagemagick_install_result.stdout"
  # Add creates: /usr/local/bin/magick to a pre-flight stat check for better idempotency

- name: Update dynamic linker run-time bindings
  ansible.builtin.command:
    cmd: ldconfig
  become: true
  changed_when: false # ldconfig output varies and doesn't indicate change reliably
```

For CMake-based projects like `chromaprint` 17, the configure and compile steps would change:

YAML

```shell
# Example CMake steps for a package like chromaprint
- name: Configure {{ item.name }} with CMake
  ansible.builtin.command:
    cmd: "cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TOOLS=ON." # Example flags from [17]
    chdir: "/usr/local/src/{{ item.name }}"
    creates: "/usr/local/src/{{ item.name }}/CMakeCache.txt"
  become: true

- name: Compile {{ item.name }} with make (after CMake)
  ansible.builtin.make:
    chdir: "/usr/local/src/{{ item.name }}"
    jobs: "{{ ansible_processor_vcpus }}"
  become: true
  #... then make install
```

For Meson-based projects like `libvips` 41 or `mako` (notification daemon) 42:

YAML

```shell
# Example Meson steps for a package like libvips or mako
- name: Setup {{ item.name }} with Meson
  ansible.builtin.command:
    cmd: "meson setup build --prefix=/usr/local -Dsome_option=true" # Adjust prefix and options
    chdir: "/usr/local/src/{{ item.name }}"
    creates: "/usr/local/src/{{ item.name }}/build/meson-private/coredata.dat"
  become: true # if prefix is a system path

- name: Compile {{ item.name }} with Ninja
  ansible.builtin.command:
    cmd: "ninja -C build"
    chdir: "/usr/local/src/{{ item.name }}"
  become: true # If build dir needs root
  register: meson_compile_result
  changed_when: "'ninja: no work to do.' not in meson_compile_result.stdout"

- name: Install {{ item.name }} with Ninja
  ansible.builtin.command:
    cmd: "ninja -C build install"
    chdir: "/usr/local/src/{{ item.name }}"
  become: true
  register: meson_install_result
  changed_when: "'ninja: no work to do.' not in meson_install_result.stdout"
  # Add creates: /usr/local/bin/{{ item.binary_name }} for idempotency check
```

### D. Python-Based Tools

Python tools like `yt-dlp`, `python-adblock`, `python-edge-tts`, `python-j2cli`, and `python-sphinx-intl` are typically installed using `pip install.` from the cloned source directory or by running `python setup.py install`.

**Example Package: `yt-dlp`** 62

* Source: `https://github.com/yt-dlp/yt-dlp.git`
* Build System: Python (setup.py / pyproject.toml)
* Dependencies: `python3-pip`. `ffmpeg` is a highly recommended runtime dependency.62 For building the executable from source, `make`, `pandoc`, and `zip` are needed.62

YAML

```shell
- name: Install yt-dlp dependencies
  ansible.builtin.dnf:
    name:
      - python3-pip
      - ffmpeg # Recommended runtime dependency
      # For building the executable from source as per [62]:
      # - make
      # - pandoc # Fedora package name for pandoc is 'pandoc' [53, 66]
      # - zip
    state: present
  become: true

- name: Clone yt-dlp repository
  ansible.builtin.git:
    repo: 'https://github.com/yt-dlp/yt-dlp.git'
    dest: "/usr/local/src/yt-dlp"
    version: '2023.12.30' # Use a specific release tag

# Option 1: Install as a Python package (most common)
- name: Install yt-dlp using pip
  ansible.builtin.pip:
    name:. # Installs from current directory
    chdir: "/usr/local/src/yt-dlp"
    # To install globally, pip needs to be run with become: true
    # and potentially --break-system-packages on newer pip/Python if not in a venv.
    # Consider installing to user site-packages or using a virtual environment
    # For system-wide CLI tool, global install is often intended by such requests.
  become: true # If installing globally to system Python
  # Check if yt-dlp is already installed by pip to make this idempotent
  # command: pip show yt-dlp
  # register: ytdlp_pip_check
  # when: "'yt-dlp' not in ytdlp_pip_check.stdout"

# Option 2: Build standalone binary using make [62]
# - name: Build yt-dlp standalone binary
#   ansible.builtin.make:
#     chdir: "/usr/local/src/yt-dlp"
#     target: yt-dlp # Or appropriate target from Makefile
#   environment:
#     PATH: "{{ ansible_env.PATH }}" # Ensure make, python3 etc. are found
#   creates: "/usr/local/src/yt-dlp/yt-dlp" # Assuming binary is named yt-dlp in source dir
#
# - name: Install yt-dlp binary
#   ansible.builtin.copy:
#     src: "/usr/local/src/yt-dlp/yt-dlp"
#     dest: "/usr/local/bin/yt-dlp"
#     mode: '0755'
#     remote_src: true
#   become: true
#   when: # Condition if binary build path was chosen
```

The `python-adblock` package uses `maturin` for its build, indicating a Rust component.46 This would require `maturin` to be installed via pip and Rust to be available.

YAML

```shell
# For python-adblock
- name: Install Maturin for python-adblock build
  ansible.builtin.pip:
    name: maturin
    state: present
  become: true

- name: Clone python-adblock repository
  ansible.builtin.git:
    repo: 'https://github.com/ArniDagur/python-adblock.git' # From [46] PyPI links to this
    dest: "/usr/local/src/python-adblock"
    version: 'v0.6.0' # Example tag

- name: Build and install python-adblock with maturin
  ansible.builtin.command:
    cmd: "{{ ansible_env.HOME }}/.local/bin/maturin develop --release" # Or 'pip install.' if pyproject.toml handles it
    chdir: "/usr/local/src/python-adblock"
  become: true # If installing globally
  environment:
    PATH: "{{ ansible_env.PATH }}:{{ ansible_env.HOME }}/.cargo/bin:{{ ansible_env.HOME }}/.local/bin"
    # Ensure Rust is available
```

### E. Other/Special Cases

* **`bash-language-server`**: This is a Node.js package. Installation requires `npm`.
    
    YAML

    ```shell
    - name: Install Node.js and npm
      ansible.builtin.dnf:
        name:
          - nodejs # This usually includes npm on Fedora
          - npm # Explicitly, if nodejs package doesn't include it or for specific version
        state: present
      become: true
    
    - name: Install bash-language-server using npm
      ansible.builtin.npm:
        name: bash-language-server
        global: true
        state: present
      become: true # For global install
      # Add creates: /usr/bin/bash-language-server (or wherever npm global installs it) for idempotency
    ```

* **`cpupower`**: This utility is part of the `kernel-tools` package on Fedora/RHEL systems.19 The task is to ensure this package is installed.
    
    YAML

    ```shell
    - name: Ensure cpupower (kernel-tools) is installed
      ansible.builtin.dnf:
        name: kernel-tools
        state: present
      become: true
    ```

* **`dex` (DesktopEntry Execution)**: This tool, from `jceb/dex`, is Python-based and uses a `Makefile` that likely wraps `setup.py`.21
    
    YAML

    ```shell
    - name: Install dex (jceb/dex) dependencies
      ansible.builtin.dnf:
        name:
          - python3-setuptools # For setup.py
          - make
        state: present
      become: true
    
    - name: Clone dex (jceb/dex) repository
      ansible.builtin.git:
        repo: 'httpsible://github.com/jceb/dex.git'
        dest: "/usr/local/src/dex-jceb" # Avoid conflict if another 'dex' exists
        version: '0.10.1' # From [22]
    
    - name: Install dex (jceb/dex) using make
      ansible.builtin.make:
        chdir: "/usr/local/src/dex-jceb"
        target: install # Assuming 'install' target in Makefile
      become: true
      # Add creates: /usr/local/bin/dex (or actual path)
    ```

* **`nano-syntax-highlighting`**: These are configuration files, not compiled code.44 Installation involves cloning the repository and including the `.nanorc` files in the main nano configuration.
    
    YAML

    ```shell
    - name: Define nano syntax highlighting install path
      ansible.builtin.set_fact:
        nano_syntax_path: "{{ ansible_env.HOME }}/.nano/syntax" # User-specific
    
    - name: Ensure nano syntax highlighting directory exists
      ansible.builtin.file:
        path: "{{ nano_syntax_path }}"
        state: directory
        mode: '0755'
    
    - name: Clone nano-syntax-highlighting (scopatz/nanorc)
      ansible.builtin.git:
        repo: 'httpsible://github.com/scopatz/nanorc.git' # [44] refers to scopatz/nanorc
        dest: "{{ nano_syntax_path }}/scopatz-nanorc" # Keep it in a subdirectory
        version: 'master'
    
    - name: Include all nanorc files from scopatz-nanorc in user's.nanorc
      ansible.builtin.lineinfile:
        path: "{{ ansible_env.HOME }}/.nanorc"
        line: "include {{ nano_syntax_path }}/scopatz-nanorc/*.nanorc"
        create: true
        regexp: "^include {{ nano_syntax_path }}/scopatz-nanorc/\\*\\.nanorc$"
    ```

* **`ueberzug`**: Python with C extensions, built using `mesonpy`.57
    
    YAML

    ```shell
    - name: Install ueberzug build dependencies
      ansible.builtin.dnf:
        name:
          - meson
          - python3-pip # For meson-python and build module
          - python3-devel # For C extensions
          - libX11-devel
          - libXext-devel
          - libXRes-devel # As per [57]
        state: present
      become: true
    
    - name: Install Python build and meson-python
      ansible.builtin.pip:
        name:
          - build
          - meson-python
        state: present
      become: true # If installing globally, or use user install
    
    - name: Clone ueberzug repository
      ansible.builtin.git:
        repo: 'httpsible://github.com/ueber-devel/ueberzug.git'
        dest: "/usr/local/src/ueberzug"
        version: '18.1.9' # Example tag
    
    - name: Build ueberzug wheel
      ansible.builtin.command:
        cmd: "python3 -m build --wheel"
        chdir: "/usr/local/src/ueberzug"
        creates: "/usr/local/src/ueberzug/dist/ueberzug-*.whl" # Pattern match the wheel
      register: ueberzug_wheel_build
      changed_when: ueberzug_wheel_build.rc == 0 and "already built" not in ueberzug_wheel_build.stdout
    
    - name: Find the ueberzug wheel file
      ansible.builtin.find:
        paths: "/usr/local/src/ueberzug/dist"
        patterns: "ueberzug-*.whl"
      register: ueberzug_wheel_file
      when: ueberzug_wheel_build.changed or not ueberzug_wheel_file_check.stat.exists # Only find if built or not previously found
    
    - name: Check if ueberzug wheel exists (for idempotency)
      ansible.builtin.stat:
        path: "{{ (ueberzug_wheel_file.files | first).path | default('') }}"
      register: ueberzug_wheel_file_check
    
    - name: Install ueberzug from built wheel
      ansible.builtin.pip:
        name: "{{ (ueberzug_wheel_file.files | first).path }}"
        state: present
      become: true # If installing globally
      when: ueberzug_wheel_file.files | length > 0
    ```

* ripgrep-all: This tool wraps ripgrep and adds support for more file types using various converters.52
    
    Dependencies include pandoc 53, poppler-utils 54, ffmpeg 12, and ripgrep itself.
    
    YAML

    ```shell
    - name: Install ripgrep-all dependencies
      ansible.builtin.dnf:
        name:
          - pandoc
          - poppler-utils
          - ffmpeg # From RPM Fusion
          - ripgrep # Usually available in Fedora repos
        state: present
      become: true
    
    # Then proceed with cargo build for ripgrep-all as per Rust pattern
    - name: Clone ripgrep-all repository
      ansible.builtin.git:
        repo: 'httpsible://github.com/phiresky/ripgrep-all.git'
        dest: "/usr/local/src/ripgrep-all"
        version: 'master' # Or a specific tag
    
    - name: Compile ripgrep-all
      ansible.builtin.command:
        cmd: "{{ ansible_env.HOME }}/.cargo/bin/cargo build --release"
        chdir: "/usr/local/src/ripgrep-all"
        creates: "/usr/local/src/ripgrep-all/target/release/rga"
      environment:
        PATH: "{{ ansible_env.PATH }}"
    
    - name: Install ripgrep-all (rga)
      ansible.builtin.copy:
        src: "/usr/local/src/ripgrep-all/target/release/rga"
        dest: "/usr/local/bin/rga"
        mode: '0755'
        remote_src: true
      become: true
    ```

## V. Handling Specific Error List Items and Common Dependencies

### A. Addressing `base-devel`

As covered in Section II.A, the "Development Tools" group on Fedora/RHEL systems provides the core compilation utilities analogous to `base-devel`.1 The playbook ensures this group is installed.

### B. `downgrade` - An Arch Linux Specific Tool

The `downgrade` utility is a script designed for Arch Linux and its package manager, `pacman`. It is not intended for compilation or direct use on Fedora/RHEL systems. If the functionality of downgrading packages is required on a Fedora system, alternative methods such as `dnf downgrade <package_name>`, `dnf versionlock`, or manually installing older RPM versions should be considered. These are outside the scope of "compiling from source" for this specific tool.

### C. `realtime-privileges` - System Configuration

"Realtime privileges" refers to configuring the operating system to allow user-space processes to acquire real-time scheduling priorities, which can be crucial for latency-sensitive applications (e.g., audio/video processing). This is not a single package to compile but a system capability.

One common way to manage this on Linux is by using `rtkit`. `rtkit` is a D-Bus daemon that grants real-time scheduling privileges to processes in a controlled manner.72

* **Source:** `https://github.com/heftig/rtkit` 72
* **Build System:** Likely Autotools or Meson (C-based).
* **Dependencies:** `dbus-devel`, `polkit-devel`, `libcap-ng-devel`, C compiler, make/meson/ninja.

YAML

```shell
# Example tasks for rtkit (assuming Autotools, adjust if Meson)
- name: Install rtkit build dependencies
  ansible.builtin.dnf:
    name:
      - dbus-devel
      - polkit-devel
      - libcap-ng-devel
      - systemd-devel # For D-Bus service files and PAM integration
      - gcc
      - make
      - autoconf
      - automake
      - libtool
    state: present
  become: true

- name: Clone rtkit repository
  ansible.builtin.git:
    repo: 'httpsible://github.com/heftig/rtkit.git' # Official repo for rtkit
    dest: "/usr/local/src/rtkit"
    version: 'master' # Or a specific tag

- name: Configure rtkit (Autogen if needed, then configure)
  ansible.builtin.shell: |
   ./autogen.sh # If configure script is not present
   ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var # Adjust paths as needed
  args:
    chdir: "/usr/local/src/rtkit"
    creates: "/usr/local/src/rtkit/config.status"
  become: true

- name: Compile rtkit
  ansible.builtin.make:
    chdir: "/usr/local/src/rtkit"
    jobs: "{{ ansible_processor_vcpus }}"
  become: true

- name: Install rtkit
  ansible.builtin.make:
    chdir: "/usr/local/src/rtkit"
    target: install
  become: true
  # creates: /usr/libexec/rtkit-daemon # Check actual installed path

- name: Enable and start rtkit D-Bus service
  ansible.builtin.systemd:
    name: rtkit-daemon.service
    enabled: true
    state: started
  become: true
```

Alternatively, or in conjunction, `/etc/security/limits.conf` or files in `/etc/security/limits.d/` can be used to grant specific users or groups the ability to set real-time priorities.73

YAML

```shell
- name: Allow 'audio' group to set realtime priorities
  ansible.builtin.copy:
    dest: /etc/security/limits.d/99-realtime-audio.conf
    content: |
      @audio   -  rtprio     95
      @audio   -  memlock    unlimited
    mode: '0644'
  become: true
```

### D. Managing Common Libraries (`-devel` packages)

Many C/C++ projects depend on a common set of libraries. A baseline of `-devel` packages is included in the `common_build_env` role (Section II.A) to cover frequent needs, such as `openssl-devel`, `zlib-devel`, `libcurl-devel`, `pkgconf`, and `gettext-devel`. Specific, less common `-devel` packages are installed on a per-tool basis.

## VI. Example: A Consolidated Ansible Role for a Subset of Tools

To manage the installation of multiple tools efficiently, a consolidated Ansible role can be created. This example outlines a role named `custom_source_builds` that could manage Rust and Go tools.

### A. Illustrative Role Structure (`custom_source_builds`)

```shell
roles/
  custom_source_builds/
    tasks/
      main.yml
      rust_tools.yml
      go_tools.yml
      _common_build_steps.yml # Reusable include for git clone, compile, install
    vars/
      main.yml
      rust_vars.yml
      go_vars.yml
    meta/
      main.yml
```

**`vars/rust_vars.yml`:**

YAML

```shell
rust_packages_to_build:
  - name: bandwhich
    repo: 'https://github.com/imsnif/bandwhich.git'
    version: 'master' # Or specific tag like 'v0.20.0'
    binary_name: bandwhich
    build_dependencies: ['libcap'] # For setcap
    post_install_cmds:
      - "setcap cap_sys_ptrace,cap_dac_read_search,cap_net_raw,cap_net_admin+ep /usr/local/bin/bandwhich"
  - name: eza
    repo: 'httpsible://github.com/eza-community/eza.git'
    version: 'main'
    binary_name: eza
    build_dependencies: ['zlib-devel']
```

**`vars/go_vars.yml`:**

YAML

```shell
go_packages_to_build:
  - name: micro
    repo: 'httpsible://github.com/zyedidia/micro.git'
    version: 'v2.0.13'
    binary_name: micro
    build_command: "make build" # Uses Makefile
    source_binary_path: "micro" # Relative to source dir after build
  - name: duf
    repo: 'httpsible://github.com/muesli/duf.git'
    version: 'v0.8.1'
    binary_name: duf
    build_command: "go build -ldflags='-s -w'" # Direct go build
    source_binary_path: "duf"
```

### B. Using Loops and Conditionals for Multiple Packages

**`tasks/main.yml`:**

YAML

```shell
- name: Include Rust tools installation tasks
  ansible.builtin.include_tasks: rust_tools.yml

- name: Include Go tools installation tasks
  ansible.builtin.include_tasks: go_tools.yml
#... include other task files for C/C++, Python, etc.
```

**`tasks/rust_tools.yml`:**

YAML

```shell
- name: Load Rust package variables
  ansible.builtin.include_vars: rust_vars.yml

- name: Ensure build dependencies for Rust packages are installed
  ansible.builtin.dnf:
    name: "{{ item.build_dependencies | default() }}"
    state: present
  become: true
  loop: "{{ rust_packages_to_build }}"
  when: item.build_dependencies is defined

- name: Build and install Rust packages
  ansible.builtin.include_tasks: _common_build_steps.yml
  loop: "{{ rust_packages_to_build }}"
  loop_control:
    loop_var: pkg_item
  vars:
    build_type: rust
```

**`tasks/_common_build_steps.yml` (simplified example):**

YAML

```shell
- name: Check if {{ pkg_item.binary_name }} is already installed
  ansible.builtin.stat:
    path: "/usr/local/bin/{{ pkg_item.binary_name }}"
  register: binary_stat

- name: Clone {{ pkg_item.name }} repository
  ansible.builtin.git:
    repo: "{{ pkg_item.repo }}"
    dest: "/usr/local/src/{{ pkg_item.name }}"
    version: "{{ pkg_item.version }}"
  become: true
  when: not binary_stat.stat.exists

- name: Compile {{ pkg_item.name }} (Rust)
  ansible.builtin.command:
    cmd: "{{ ansible_env.HOME }}/.cargo/bin/cargo build --release"
    chdir: "/usr/local/src/{{ pkg_item.name }}"
    creates: "/usr/local/src/{{ pkg_item.name }}/target/release/{{ pkg_item.binary_name }}"
  environment:
    PATH: "{{ ansible_env.PATH }}"
  when: build_type == 'rust' and not binary_stat.stat.exists

- name: Compile {{ pkg_item.name }} (Go)
  ansible.builtin.command:
    cmd: "{{ pkg_item.build_command }}"
    chdir: "/usr/local/src/{{ pkg_item.name }}"
    creates: "/usr/local/src/{{ pkg_item.name }}/{{ pkg_item.source_binary_path }}"
  environment:
    PATH: "/usr/local/go/bin:{{ ansible_env.GOPATH | default(ansible_env.HOME + '/go') }}/bin:{{ ansible_env.PATH }}"
    GOPATH: "{{ ansible_env.GOPATH | default(ansible_env.HOME + '/go') }}"
  when: build_type == 'go' and not binary_stat.stat.exists

- name: Install {{ pkg_item.name }}
  ansible.builtin.copy:
    src: "/usr/local/src/{{ pkg_item.name }}/{{ pkg_item.source_binary_path if build_type == 'go' else 'target/release/' + pkg_item.binary_name }}"
    dest: "/usr/local/bin/{{ pkg_item.binary_name }}"
    mode: '0755'
    remote_src: true
  become: true
  when: not binary_stat.stat.exists

- name: Run post-install commands for {{ pkg_item.name }}
  ansible.builtin.command:
    cmd: "{{ cmd_item }}"
  become: true
  loop: "{{ pkg_item.post_install_cmds | default() }}"
  loop_control:
    loop_var: cmd_item
  changed_when: false # Assuming post_install_cmds are idempotent or their change status is not critical
  when: pkg_item.post_install_cmds is defined and not binary_stat.stat.exists # Run only on initial install
```

This structure allows for adding new packages by primarily updating the `vars` files and ensuring the `_common_build_steps.yml` (or more specialized build step files) can handle the build system.

## VII. Troubleshooting and Best Practices

### A. Common Compilation Errors

* **Missing `-devel` packages:** Errors like "header file not found" or "undefined reference to" often indicate a missing development library. Use `dnf provides '*/filename.h'` or `dnf provides 'pkgconfig(libraryname)'` to find the required `-devel` package.
* **Compiler/Toolchain Issues:** Ensure GCC, Go, Rust versions meet the package's requirements.
* **PATH and Library Paths:** Incorrect `PATH` can mean build tools are not found. `LD_LIBRARY_PATH` might be needed during compilation for locally built dependencies, though it's better to install dependencies to standard system paths or use `rpath`. After installation, `ldconfig` updates the shared library cache for standard locations.
* **Network Failures:** `cargo`, `go get`, and `npm` fetch dependencies over the network. Ensure connectivity and consider local proxies if needed.

### B. Ensuring Playbook Idempotency

Idempotency is crucial. The creates argument in command/shell/make tasks is the primary mechanism. For example, creates: /usr/local/bin/mytool ensures that if /usr/local/bin/mytool exists, the compilation and installation steps are skipped.

Using ansible.builtin.stat to check for the existence of the final installed binary before attempting any build steps for that package is a robust approach.

Version checking for already installed custom-compiled tools can be complex. A simple strategy is to remove the old version (if the creates path exists) before installing a new one if the desired version (defined in Ansible vars) has changed. More sophisticated version management would require storing metadata about compiled versions.

### C. Keeping Source-Built Packages Updated

Packages compiled from source are not managed by dnf update. Updating them requires manually (or via Ansible) pulling the latest changes from their Git repositories and re-compiling.

Strategies:

1. **Re-run Playbook:** Update the `version` variable in the playbook for the package to a new Git tag/commit and re-run. The `creates` logic (if based on a versioned file or if the old binary is removed first) would trigger a rebuild.
2. **Dedicated Update Playbook/Role:** A separate playbook could iterate through source directories in `/usr/local/src/`, run `git pull`, and then re-run compile and install commands. This requires careful management of versions.
3. **Version Pinning:** Check out specific Git tags for releases rather than `master`/`main` to ensure reproducible builds and control when updates occur.

### D. Security Considerations

* **`setcap`:** Granting capabilities (e.g., for `bandwhich` 3) should be done judiciously as it elevates privileges for specific binaries.
* **Checksums:** For downloaded source tarballs (though this playbook primarily uses Git), verify checksums. For `rustup-init.sh` or similar scripts downloaded via `get_url`, checksums should also be used.
* **Repository Trust:** The playbook clones from generally well-known GitHub/GitLab repositories. For less common sources, verify their authenticity.
* **Compilation Flags:** Be aware of default compilation flags and consider security-hardening flags if appropriate for the environment (e.g., `-D_FORTIFY_SOURCE=2`, `-fstack-protector-strong`).

## VIII. Conclusion

### A. Summary of the Playbook's Capabilities

This document has provided a detailed framework for an Ansible playbook designed to install a diverse set of software packages from their source code on Fedora/RHEL systems. It addresses the initial "No package available" errors by shifting from package manager installation to a controlled, automated source compilation process. The playbook structure emphasizes:

* **Prerequisite Management:** Systematic installation of development tools, language toolchains (Rust, Go), and essential libraries.
* **Modularity:** Using roles for better organization and maintainability.
* **Idempotency:** Ensuring tasks run only when necessary, preventing redundant compilations.
* **Flexibility:** Using variables for package sources and versions.
* **Handling Diversity:** Addressing various build systems (Cargo, Go, Autotools, CMake, Meson, Python pip/setup.py, npm).

By following this approach, administrators can reliably deploy these custom-compiled tools across their infrastructure.

### B. Further Considerations for Managing a Custom Toolset

Managing a suite of source-compiled software introduces long-term considerations:

* **Maintenance Overhead:** Updating source-compiled packages is more involved than running `dnf update`. A strategy for tracking upstream releases and re-compiling will be necessary.
* **Dependency Hell (Minimized but Possible):** While system dependencies are managed by DNF, conflicts could arise if multiple source-compiled tools require different, incompatible versions of the same unmanaged library.
* **Security Patching:** Vulnerabilities in compiled tools or their statically linked libraries must be addressed by re-compiling with patched versions. This requires active monitoring of security advisories for each tool.
* **Build Artifact Management:** Consider storing compiled binaries or creating custom RPMs from the source builds for easier distribution or rollback, rather than compiling on every target machine. Tools like `fpm` can assist in creating packages from compiled sources.
* **Transition to Packaged Versions:** Periodically check if any of these tools become available in official Fedora/RHEL repositories, EPEL, or trusted COPRs. Migrating to a packaged version, when available and suitable, generally reduces maintenance burden and improves security responsiveness.

While compiling from source offers maximum control, it should be balanced against the ease of maintenance and security benefits provided by official or well-maintained third-party package repositories. This Ansible playbook provides a solid foundation for managing the source compilation process when it is the chosen or necessary approach.
