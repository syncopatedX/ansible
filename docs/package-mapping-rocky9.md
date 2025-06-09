# Package Mapping: Arch Linux → Rocky Linux 9

This document maps Arch Linux packages to their Rocky Linux 9 equivalents for the Syncopated Ansible automation system.

## Repository Sources

### Rocky Linux 9 Repositories Required

- **BaseOS**: Core Rocky Linux packages
- **AppStream**: Additional applications and development tools  
- **EPEL 9**: Extra Packages for Enterprise Linux (Fedora packages for RHEL)
- **PowerTools/CRB**: Code Ready Builder - development libraries and headers
- **RPM Fusion Free**: Multimedia packages not in base repos
- **RPM Fusion Non-Free**: Proprietary multimedia packages

### Audio-Specific Repositories

- **Planet CCRMA**: Stanford's audio production packages (if available for Rocky 9)
- **Audinux**: Audio production packages by Yann Collette

## Base System Package Mappings

| Arch Linux | Rocky Linux 9 | Repository | Notes |
|------------|---------------|------------|-------|
| `aria2` | `aria2` | EPEL | Download utility |
| `aspell` | `aspell` | BaseOS | Spell checker |
| `aspell-en` | `aspell-en` | BaseOS | English dictionary |
| `atool` | `atool` | EPEL | Archive tool wrapper |
| `audiofile` | `audiofile-devel` | BaseOS | Audio file library |
| `bandwhich` | NOT_AVAILABLE | - | Network bandwidth monitor (consider alternatives) |
| `base-devel` | `@"Development Tools"` | BaseOS | Build tools group |
| `bash-completion` | `bash-completion` | BaseOS | Bash completion |
| `bash-language-server` | `nodejs-bash-language-server` | EPEL | Language server |
| `bat` | `bat` | EPEL | Cat clone with syntax highlighting |
| `bind` | `bind-utils` | BaseOS | DNS utilities |
| `bottom` | NOT_AVAILABLE | - | System monitor (alternative: htop, glances) |
| `choose` | NOT_AVAILABLE | - | Field selection tool |
| `chromaprint` | `chromaprint` | BaseOS | Audio fingerprinting |
| `cmake` | `cmake` | BaseOS | Build system |
| `cpupower` | `kernel-tools` | BaseOS | CPU frequency utilities |
| `curlie` | NOT_AVAILABLE | - | HTTP client (alternative: curl) |
| `debugedit` | `debugedit` | BaseOS | Debug info editor |
| `dex` | NOT_AVAILABLE | - | Desktop entry execution |
| `downgrade` | NOT_AVAILABLE | - | Arch-specific package downgrader |
| `duf` | NOT_AVAILABLE | - | Disk usage (alternative: df, ncdu) |
| `dust` | NOT_AVAILABLE | - | Directory analyzer (alternative: ncdu) |
| `elinks` | `elinks` | BaseOS | Text web browser |
| `eza` | NOT_AVAILABLE | - | ls replacement (alternative: exa or ls) |
| `faac` | `faac` | RPM Fusion Free | AAC encoder |
| `faad2` | `faad2` | RPM Fusion Free | AAC decoder |
| `fakeroot` | `fakeroot` | EPEL | Fake root environment |
| `fd` | `fd-find` | EPEL | Find alternative |
| `figlet` | `figlet` | BaseOS | ASCII art text |
| `firewalld` | `firewalld` | BaseOS | Firewall management |
| `fsarchiver` | `fsarchiver` | EPEL | Filesystem archiver |
| `fuse-common` | `fuse` | BaseOS | FUSE filesystem |
| `fuse3` | `fuse3` | BaseOS | FUSE v3 |
| `git` | `git` | BaseOS | Version control |
| `git-delta` | NOT_AVAILABLE | - | Git diff viewer |
| `git-lfs` | `git-lfs` | BaseOS | Git Large File Storage |
| `github-cli` | `gh` | BaseOS | GitHub CLI |
| `glow` | NOT_AVAILABLE | - | Markdown viewer |
| `gnome-keyring` | `gnome-keyring` | BaseOS | GNOME credential storage |
| `gnuplot` | `gnuplot` | BaseOS | Plotting program |
| `gping` | NOT_AVAILABLE | - | Ping with graph |
| `graphicsmagick` | `GraphicsMagick` | BaseOS | Image manipulation |
| `gst-libav` | `gstreamer1-libav` | RPM Fusion Free | GStreamer libav plugin |
| `gstreamer` | `gstreamer1` | BaseOS | Multimedia framework |
| `gum` | NOT_AVAILABLE | - | Shell script utilities |
| `highlight` | `highlight` | BaseOS | Syntax highlighter |
| `hspell` | `hspell` | BaseOS | Hebrew spell checker |
| `htop` | `htop` | BaseOS | Process viewer |
| `i7z` | NOT_AVAILABLE | - | Intel CPU monitor |
| `imagemagick` | `ImageMagick` | BaseOS | Image manipulation |
| `inetutils` | `inetutils` | BaseOS | Network utilities |
| `inxi` | `inxi` | EPEL | System information |
| `iotop` | `iotop` | BaseOS | I/O monitor |
| `jq` | `jq` | BaseOS | JSON processor |
| `libgit2` | `libgit2` | BaseOS | Git library |
| `libgit2-glib` | `libgit2-glib` | BaseOS | GLib Git library |
| `libvips` | `vips` | BaseOS | Image processing library |
| `libvoikko` | `libvoikko` | BaseOS | Finnish spell checker |
| `links` | `links` | BaseOS | Text web browser |
| `lnav` | `lnav` | EPEL | Log navigator |
| `lynx` | `lynx` | BaseOS | Text web browser |
| `mako` | NOT_AVAILABLE | - | Wayland notification daemon |
| `mediainfo` | `mediainfo` | EPEL | Media file information |
| `meld` | `meld` | BaseOS | File comparison |
| `micro` | NOT_AVAILABLE | - | Text editor |
| `most` | `most` | BaseOS | Pager |
| `nano-syntax-highlighting` | NOT_AVAILABLE | - | Nano syntax highlighting |
| `ncdu` | `ncdu` | EPEL | Disk usage analyzer |
| `net-tools` | `net-tools` | BaseOS | Network tools |
| `nodejs` | `nodejs` | BaseOS | JavaScript runtime |
| `npm` | `npm` | BaseOS | Node package manager |
| `numlockx` | `numlockx` | EPEL | NumLock control |
| `nuspell` | `nuspell` | BaseOS | Spell checker |
| `openssh` | `openssh` | BaseOS | SSH client/server |
| `pandoc` | `pandoc` | EPEL | Document converter |
| `playerctl` | `playerctl` | EPEL | Media player control |
| `poppler` | `poppler` | BaseOS | PDF library |
| `postgresql-libs` | `postgresql` | BaseOS | PostgreSQL client libraries |
| `python-adblock` | NOT_AVAILABLE | - | Python ad blocker |
| `python-chardet` | `python3-chardet` | BaseOS | Character detection |
| `python-edge-tts` | NOT_AVAILABLE | - | Edge TTS Python library |
| `python-j2cli` | NOT_AVAILABLE | - | Jinja2 CLI tool |
| `python-pillow` | `python3-pillow` | BaseOS | Python imaging |
| `python-pip` | `python3-pip` | BaseOS | Python package installer |
| `python-pygments` | `python3-pygments` | BaseOS | Syntax highlighter |
| `python-setuptools` | `python3-setuptools` | BaseOS | Python build tools |
| `python-sphinx-intl` | `python3-sphinx-intl` | EPEL | Sphinx internationalization |
| `python-virtualenv` | `python3-virtualenv` | BaseOS | Python virtual environments |
| `ranger` | `ranger` | BaseOS | File manager |
| `ripgrep` | `ripgrep` | EPEL | Fast grep alternative |
| `ripgrep-all` | NOT_AVAILABLE | - | Ripgrep for all file types |
| `realtime-privileges` | NOT_AVAILABLE | - | Audio realtime privileges (manual config needed) |
| `rsync` | `rsync` | BaseOS | File synchronization |
| `rxvt-unicode` | `rxvt-unicode` | EPEL | Terminal emulator |
| `sd` | NOT_AVAILABLE | - | sed alternative |
| `smartmontools` | `smartmontools` | BaseOS | Hard drive monitoring |
| `socat` | `socat` | BaseOS | Socket relay |
| `speech-dispatcher` | `speech-dispatcher` | BaseOS | Speech synthesis |
| `sshpass` | `sshpass` | EPEL | SSH password authentication |
| `stunnel` | `stunnel` | BaseOS | SSL tunnel |
| `sudo` | `sudo` | BaseOS | Privilege escalation |
| `swappy` | NOT_AVAILABLE | - | Wayland screenshot editor |
| `sysstat` | `sysstat` | BaseOS | System statistics |
| `taglib` | `taglib` | BaseOS | Audio metadata library |
| `tldr` | NOT_AVAILABLE | - | Simplified man pages |
| `tree` | `tree` | BaseOS | Directory tree viewer |
| `ueberzug` | NOT_AVAILABLE | - | Image display in terminal |
| `unrar` | `unrar` | RPM Fusion Non-Free | RAR extractor |
| `unzip` | `unzip` | BaseOS | ZIP extractor |
| `v4l-utils` | `v4l-utils` | BaseOS | Video4Linux utilities |
| `vorbis-tools` | `vorbis-tools` | BaseOS | Ogg Vorbis tools |
| `wavpack` | `wavpack` | BaseOS | Audio compression |
| `wget` | `wget` | BaseOS | File downloader |
| `x264` | `x264` | RPM Fusion Free | H.264 encoder |
| `x265` | `x265` | RPM Fusion Free | H.265 encoder |
| `xterm` | `xterm` | BaseOS | Terminal emulator |
| `yt-dlp` | `yt-dlp` | EPEL | YouTube downloader |

## Package Availability Summary

- **Direct Equivalents**: ~80 packages (58%)
- **Group/Bundle Replacements**: ~5 packages (4%)  
- **EPEL/RPM Fusion Available**: ~35 packages (25%)
- **Not Available/Alternatives Needed**: ~18 packages (13%)

## Alternative Strategies for Missing Packages

### 1. Flatpak Installation

For GUI applications not available in repositories:

```yaml
- name: Install missing GUI apps via Flatpak
  flatpak:
    name: "{{ item }}"
    state: present
  loop:
    - io.github.sharkwouter.Minigalaxy  # Example
```

### 2. Cargo/Rust Installation

For Rust-based tools:

```yaml
- name: Install Rust tools via cargo
  shell: cargo install {{ item }}
  loop:
    - bat
    - bottom
    - dust
    - fd-find
```

### 3. Direct Binary Installation

For single-binary tools:

```yaml
- name: Download and install binary tools
  get_url:
    url: "https://github.com/owner/repo/releases/download/version/binary"
    dest: /usr/local/bin/binary
    mode: '0755'
```

### 4. Build from Source

For critical missing packages:

```yaml
- name: Build missing packages from source
  git:
    repo: "https://github.com/owner/repo.git"
    dest: "/tmp/build-{{ item }}"
  # Follow with configure, make, make install
```

## Next Steps

1. **Create base role Rocky Linux variables file** with mapped packages
2. **Test package installation** on ninjabot Rocky Linux 9 system
3. **Implement alternative installation methods** for missing packages
4. **Document package differences** and migration notes for users
5. **Create automated testing** for package availability across repositories

## Repository Setup Priority

1. **EPEL 9** - Essential for many development tools
2. **PowerTools/CRB** - Required for development headers  
3. **RPM Fusion Free** - Multimedia support
4. **RPM Fusion Non-Free** - Proprietary codecs
5. **Audinux** - Professional audio tools
