# Ansible Role: Audio

This Ansible role is designed to set up and configure a Linux system (primarily targeting Arch Linux) for professional audio work. It handles the installation and configuration of audio servers like JACK and PipeWire, essential audio packages, system tuning for real-time performance, and user permissions.

## Requirements

- **Ansible:** Version 2.4 or higher.

- **Operating System:** Primarily tested and designed for Arch Linux and its derivatives.

- **Privileges:** The role requires root privileges for package installation and system-wide configuration. Many tasks also run with `become: false` to configure user-specific settings.

- **AUR Helper:** Assumes an AUR helper (like `paru` or `yay`) is configured and accessible via the `aur` module if AUR packages are included in the `packages__audio` variable. The tasks often use `aur: use: auto`.

## Role Variables

The role's behavior can be customized using the following variables. Default values are defined in `defaults/main.yml`.

### Main Configuration Switches

These variables control which audio server and related components are set up.

- `use_jack`: (Boolean)

  - If `true`, the role will install and configure the JACK Audio Connection Kit (specifically `jack2-dbus`). It will also set up PulseAudio to work alongside JACK.

  - Default: `false`

  - When `true`, tasks from `jack.yml` and `pulseaudio.yml` are executed.

  - Note: Enabling `use_jack` will attempt to remove PipeWire packages to avoid conflicts.

- `use_pipewire`: (Boolean)

  - If `true`, the role will install PipeWire and its related components (ALSA, PulseAudio, and JACK compatibility layers).

  - Default: `true`

  - When `true`, tasks from `pipewire.yml` are executed.

  - Note: If both `use_jack` and `use_pipewire` are true, the behavior might be conflicting. It's generally recommended to choose one primary audio server. The role prioritizes `use_jack` by attempting to remove PipeWire if `use_jack` is true.

### JACK Configuration (`jack`)

These settings are applicable only if `use_jack` is `true`. They configure the JACK D-Bus server.

- `jack`: (Dictionary)

  - `dps`: (Dictionary) Driver parameters for JACK.

    - `device`: The ALSA device to use (e.g., `hw:0`, `hw:PCH`). Default: `hw:0`

    - `capture`: ALSA capture device. Default: `none`

    - `playback`: ALSA playback device. Default: `none`

    - `rate`: Sample rate (e.g., `44100`, `48000`, `96000`). Default: `48000`

    - `period`: Frames per period (buffer size, e.g., `64`, `128`, `256`, `1024`). Default: `1024`

    - `nperiods`: Number of periods (e.g., `2`, `3`). Default: `2`

    - `hwmon`: Hardware monitoring. Default: `false`

    - `hwmeter`: Hardware metering. Default: `false`

    - `duplex`: Enable full-duplex mode. Default: `true`

    - `softmode`: Enable soft-mode (realtime signal processing without a physical device). Default: `false`

    - `monitor`: Enable monitor JACK ports for physical inputs/outputs. Default: `true`

    - `dither`: Dithering mode (e.g., `n` for none, `t` for triangular). Default: `n`

    - `shorts`: Enable 16-bit sample mode. Default: `false`

    - `mididriver`: MIDI driver (e.g., `seq`, `raw`, `none`). Default: `seq`

  - `eps`: (Dictionary) Engine parameters for JACK.

    - `driver`: JACK backend driver (e.g., `alsa`). Default: `alsa`

    - `name`: JACK server name. Default: `default`

    - `realtime`: Enable realtime scheduling. Default: `true`

    - `realtimepriority`: Realtime priority for JACK. Default: `10`

    - `temporary`: Run JACK server temporarily. Default: `false`

    - `verbose`: Enable verbose output. Default: `false`

    - `port-max`: Maximum number of JACK ports. Default: `2048`

    - `replaceregistry`: Replace existing JACK port registry. Default: `false`

    - `sync`: Enable synchronous mode. Default: `false`

    - _(Other parameters like `client-timeout`, `clock-source`, `self-connect-mode`, `slave-drivers` are available but commented out in defaults.)_

### Package Management (`packages__audio`)

This dictionary, defined in `vars/main.yml`, lists all audio-related packages to be installed. You can customize these lists to add or remove software.

- `packages__audio`: (Dictionary)

  - `tuning`: Packages for system tuning (e.g., `realtime-privileges`, `rtirq`).

  - `pipewire`: Core PipeWire packages and compatibility layers.

  - `alsa`: ALSA utilities and libraries.

  - `jack`: JACK server (`jack2-dbus`) and utilities.

  - `pulseaudio`: PulseAudio packages, including JACK and Bluetooth support.

  - `ambisonics`: Packages for ambisonic audio work.

  - `applications`: A list of various audio applications (DAWs, editors, utilities).

  - `plugins`: Audio plugins (LV2, VST, etc.).

    Example structure from `vars/main.yml`:

    ```yaml
    packages__audio:
      tuning:
        - realtime-privileges
        - rtirq
      pipewire:
        - pipewire-alsa
        - pipewire-audio
        # ... and so on
      # ... other categories
    ```

### Chrome Audio Recording Configuration

The `tasks/chrome.yml` playbook includes specific setup for constant recording volume with Google Chrome, primarily for screen recording or streaming scenarios.

- `graphical_patchbay`: (String)

  - Specifies the graphical patchbay to be installed and referenced in helper scripts/messages.

  - Options: `"helvum"`, `"qpwgraph"`

  - Default: `"helvum"`

  - This task installs PipeWire packages independently of the `use_pipewire` variable.

### User and System Tuning

Several tuning parameters are applied directly by tasks in `tuning.yml` and are not exposed as top-level variables, but their configuration files or settings can be modified if needed:

- **Realtime Privileges:** Configured via `/etc/security/limits.d/99-realtime-privileges.conf`.

- **Timer Permissions:** Udev rule `/etc/udev/rules.d/40-timer-permissions.rules`.

- **Sysctl Settings:** `vm.swappiness`, `vm.dirty_background_bytes`, `fs.inotify.max_user_watches`, `dev.hpet.max-user-freq`.

- **Tuned Profile:** A custom `realtime-modified` tuned profile is installed.

- **RTIRQ Configuration:** `/etc/rtirq.conf`.

- **RTKit Configuration:** `/etc/rtkit.conf` and `rtkit-daemon.service`.

- **CPU Power Governor:** `/etc/default/cpupower` (configures `cpupower` service to use `performance` governor).

- **IRQBalance:** The `irqbalance` service is disabled as it can interfere with low-latency audio.

## Dependencies

This role has no explicit Ansible Galaxy role dependencies listed in `meta/main.yml`. However, it relies on system utilities and an AUR helper being present on the target Arch Linux system.

## Example Playbook

Here's an example of how to use this role in a playbook:

```yaml
---
- name: Setup Audio Workstation
  hosts: localhost
  connection: local
  gather_facts: true # Recommended to gather facts, especially for user details

  vars:
    # --- User specific ---
    # The role attempts to derive user information, but you can specify:
    # user:
    #   name: your_username
    #   home: /home/your_username
    #   uid: your_uid
    #   group: your_group

    # --- Audio Role Configuration ---
    use_pipewire: true # Use PipeWire as the primary audio server
    use_jack: false    # Do not install and configure JACK separately

    # Example: Customize JACK settings if use_jack were true
    # jack:
    #   dps:
    #     device: hw:PCH # Use a specific sound card
    #     rate: 48000
    #     period: 128
    #     nperiods: 2
    #   eps:
    #     realtimepriority: 15

    # Example: Add custom packages to an existing category
    # packages__audio:
    #   applications:
    #     - ardour # Add Ardour DAW
    #     - audacity
    #     # ... retain other default applications or list them all explicitly

    # Example: Add completely new packages (requires modifying the role or adding post_tasks)
    # my_additional_audio_packages:
    #  - "some-custom-audio-tool"

  roles:
    - role: audio # Replace 'audio' with the actual path or name if installed via Galaxy
      tags: ['audio']

  # tasks:
  #   - name: Install my additional audio packages
  #     when: my_additional_audio_packages is defined
  #     aur:
  #       use: auto
  #       name: "{{ my_additional_audio_packages }}"
  #       state: present
  #     become: false # Assuming these are user-installable or AUR packages
```

## Customization Guide

### Choosing Between JACK and PipeWire

- **PipeWire (`use_pipewire: true`):** Recommended for modern setups. PipeWire aims to be a unified audio and video server, providing compatibility layers for PulseAudio, ALSA, and JACK applications. It generally offers easier setup and better integration with desktop environments.

- **JACK (`use_jack: true`):** A low-latency audio server primarily for professional audio applications. If you choose JACK, this role also sets up PulseAudio to bridge desktop audio to JACK. This can be more complex to manage but offers fine-grained control for pro-audio workflows.

- It is generally advisable to set one of these to `true` and the other to `false`. If `use_jack` is `true`, the role will attempt to remove PipeWire packages.

### Customizing Package Installations

The primary way to customize packages is by overriding or extending the `packages__audio` dictionary in your playbook's `vars` section.

1. Overriding a Category:

You can redefine an entire category. For example, to install only specific ALSA packages:

```yaml
vars:
  packages__audio:
    alsa:
      - alsa-utils
      - alsa-plugins
    # ... other categories will use defaults unless also overridden
```

_Caution: If you override a category, you must list all packages you want for that category; it won't merge with the defaults._

2. Adding to Default Categories (More Complex):

To add packages to the default lists without redefining the entire packages__audio variable, you would typically need to merge dictionaries. Ansible's default variable precedence means a direct definition in playbook vars will completely overwrite the role's vars/main.yml.

A common approach is to define your additions and then use combine filter if you were to set facts, or structure your playbook vars carefully.

A simpler way for adding a few extra packages is to define a new variable (e.g., `my_custom_audio_apps`) and add a separate task in your playbook's `post_tasks` to install them:

```yaml
vars:
  my_custom_audio_apps:
    - "supercollider"
    - "csound"

# ... in your playbook ...
  post_tasks:
    - name: Install custom audio applications
      aur:
        use: auto
        name: "{{ my_custom_audio_apps }}"
        state: present
      become: false # if they are user-installable or AUR packages
```

3. Modifying Role Variables Directly:

For a more permanent change, you can fork the role and edit vars/main.yml directly.

### Overriding Variables

Any variable defined in `defaults/main.yml` or `vars/main.yml` can be overridden in your playbook:

- In the `vars` section of your playbook.

- Via command-line using `--extra-vars`.

- In inventory variables.

## Task Overview

The role is broken down into several task files:

- `tasks/main.yml`: The main entry point. Includes other task files based on configuration.

- `tasks/packages.yml`: Installs common audio packages (ALSA, tuning) and has commented-out sections for bulk installation of applications and plugins from `packages__audio`.

- `tasks/jack.yml`: Handles installation and configuration of JACK2 D-Bus server and related tools if `use_jack` is `true`.

- `tasks/pulseaudio.yml`: Configures PulseAudio, typically for use with JACK (when `use_jack` is `true`). Sets up user PulseAudio configs and systemd services.

- `tasks/pipewire.yml`: Installs PipeWire packages if `use_pipewire` is `true`.

- `tasks/tuning.yml`: Applies various system tunings for real-time audio performance. This includes:

  - Adding the user to the `audio` group.

  - Setting memory locking and realtime priority limits (`/etc/security/limits.d/`).

  - Configuring udev rules for timer permissions.

  - Adjusting kernel `sysctl` parameters (`vm.swappiness`, `fs.inotify.max_user_watches`, etc.).

  - Setting up and enabling `tuned` with a custom `realtime-modified` profile.

  - Configuring `rtirq` for IRQ thread prioritization.

  - Configuring `rtkit-daemon` for managing realtime priorities for user processes.

  - Setting up `cpupower` to use the `performance` governor.

  - Disabling `irqbalance` service.

- `tasks/chrome.yml`: A specialized set of tasks to configure Google Chrome for consistent audio recording levels, often useful for streaming or screen capture. It creates a separate desktop entry and a setup script. This task installs PipeWire components independently.

## Handlers

Handlers are used to restart services or reload configurations when changes are made:

- `handlers/main.yml`:

  - `Enable and restart rtirq service`

  - `Enable and restart rtkit service`

  - `Restart pulseAudio` (user service)

  - `Reload user systemd`

  - `Reload systemd` (system-wide)

## License

The license for this role is specified in `meta/main.yml` (e.g., MIT, BSD). The provided files indicate "license (BSD, MIT)".

## Author Information

This role was authored by `b08x` (as per `meta/main.yml`).
