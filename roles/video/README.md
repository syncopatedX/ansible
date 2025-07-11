# Video Role

A comprehensive Ansible role for configuring video drivers, X11 settings, and monitor layouts based on host-specific variables.

## Description

This role provides flexible video configuration management that adapts to different GPU vendors (Intel, NVIDIA, AMD), monitor setups, and host-specific requirements. It replaces hardcoded configurations with a host_vars-driven approach.

## Requirements

- Ansible 2.9 or higher
- Target systems running Linux with X11
- Appropriate GPU drivers available in distribution repositories

## Role Variables

### Host Variables Schema

Configure video settings in your `inventory/host_vars/<hostname>.yml`:

```yaml
video:
  # GPU Configuration
  gpu:
    vendor: "intel"           # intel, nvidia, amd
    model: "iris_xe"          # specific model for optimization
    driver: "modesetting"     # X11 driver (optional, uses vendor default)
    
  # X11 Configuration
  x11:
    config_file: "20-gpu-config.conf"  # X11 config filename
    options:                           # Custom X11 driver options
      TearFree: "true"
      DRI: "3"
      AccelMethod: "glamor"
      
  # Monitor Configuration
  monitors:
    primary:
      output: "eDP-1"                  # Display output name
      resolution: "3840x2160"          # Monitor resolution
      refresh_rate: "60.00"            # Refresh rate
      position: "0x0"                  # Position (x,y coordinates)
      scaling: 1.5                     # DPI scaling factor
      
    secondary:
      enabled: true                    # Enable secondary monitor
      output: "DP-2-2"                # Display output name
      resolution: "3840x2160"         # Monitor resolution
      refresh_rate: "60.00"           # Refresh rate
      position: "right-of-primary"    # Position relative to primary
      scaling: 1.5                    # DPI scaling factor
      
  # Package Configuration
  packages:
    additional:                       # Host-specific additional packages
      - intel-gpu-tools
    exclude:                         # Packages to exclude from defaults
      - xf86-video-intel
```

### Default Variables

See [`defaults/main.yml`](defaults/main.yml) for comprehensive default values and fallback configurations.

### GPU-Specific Variables

The role automatically selects appropriate packages and configurations based on the GPU vendor:

- **Intel**: Uses modesetting driver with hardware acceleration
- **NVIDIA**: Configures proprietary driver with power management
- **AMD**: Sets up AMDGPU driver with performance optimization

## Dependencies

None. This role is self-contained.

## Example Playbook

```yaml
- hosts: workstations
  become: true
  roles:
    - role: video
      tags: ["video"]
```

## Example Host Configurations

### Intel Laptop with 4K Display
```yaml
# inventory/host_vars/laptop.yml
video:
  gpu:
    vendor: "intel"
    model: "iris_xe"
  monitors:
    primary:
      output: "eDP-1"
      resolution: "3840x2160"
      refresh_rate: "60.00"
      scaling: 1.5
    secondary:
      enabled: false
```

### NVIDIA Desktop with Dual Monitors
```yaml
# inventory/host_vars/desktop.yml
video:
  gpu:
    vendor: "nvidia"
    model: "rtx_3080"
  monitors:
    primary:
      output: "DP-0"
      resolution: "2560x1440"
      refresh_rate: "144.00"
      scaling: 1.0
    secondary:
      enabled: true
      output: "HDMI-0"
      resolution: "1920x1080"
      refresh_rate: "60.00"
      position: "right-of-primary"
      scaling: 1.0
  packages:
    additional:
      - nvidia-settings
```

### AMD Workstation
```yaml
# inventory/host_vars/workstation.yml
video:
  gpu:
    vendor: "amd"
    model: "rx_6800_xt"
  x11:
    options:
      TearFree: "true"
      DRI: "3"
      VariableRefresh: "true"
  monitors:
    primary:
      output: "DisplayPort-0"
      resolution: "3440x1440"
      refresh_rate: "100.00"
      scaling: 1.0
```

## Features

### Package Management
- Automatic selection of GPU-specific packages
- Distribution-aware package installation (Arch, Fedora, RedHat)
- Legacy package removal
- Host-specific package additions and exclusions

### X11 Configuration
- Dynamic X11 configuration generation
- GPU vendor-specific driver options
- Customizable per-host settings
- Automatic cleanup of old configurations

### Monitor Management
- Flexible monitor layout configuration
- Support for single and multi-monitor setups
- Custom scaling and positioning
- Automatic xrandr script generation
- Desktop environment integration

### GPU-Specific Optimizations
- Intel: Power management and GuC firmware
- NVIDIA: Persistence daemon and power management
- AMD: Performance profiles and frequency scaling

## File Structure

```
roles/video/
├── defaults/main.yml                    # Default variables
├── handlers/main.yml                    # Service restart handlers
├── tasks/
│   ├── main.yml                        # Main task orchestration
│   └── gpu/                           # GPU-specific tasks
│       ├── intel.yml                  # Intel GPU configuration
│       ├── nvidia.yml                 # NVIDIA GPU configuration
│       └── amd.yml                    # AMD GPU configuration
├── templates/
│   ├── etc/X11/xorg.conf.d/
│   │   └── gpu-config.conf.j2         # X11 configuration template
│   └── home/.screenlayout/
│       └── monitor-setup.sh.j2        # Monitor setup script
├── vars/
│   ├── Archlinux.yml                  # Arch Linux packages
│   ├── Fedora.yml                     # Fedora packages
│   └── RedHat.yml                     # RedHat/Rocky packages
└── README.md                          # This file
```

## Tags

- `video`: All video-related tasks
- `packages`: Package installation only
- `x11`: X11 configuration only
- `monitors`: Monitor setup only
- `gpu`: GPU-specific tasks
- `validation`: Configuration validation
- `cleanup`: Remove old configurations

## Migration from Previous Version

If upgrading from the previous hardcoded version:

1. Define video configuration in host_vars
2. Run the role with `--tags cleanup` to remove old files
3. Verify new configuration with `--tags validation`

## License

BSD

## Author Information

This role was refactored to support host_vars-based configuration for flexible video setup management across diverse hardware environments.
