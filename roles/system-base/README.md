# System Base Role

This role handles core system configuration including timezone, locale, and keymap settings.

## Purpose

The `system-base` role is responsible for:
- Setting system timezone using timedatectl
- Configuring system locale
- Setting console keymap

## Dependencies

This role has no dependencies and should be run early in the system provisioning process.

## Variables

### Required Variables

None - all variables have sensible defaults.

### Optional Variables

```yaml
# System configuration
timezone: "America/New_York"      # System timezone
locale: "en_US.UTF-8"            # System locale  
keymap: "us"                     # Console keymap
```

## Example Usage

```yaml
- name: Configure base system settings
  include_role:
    name: system-base
  vars:
    timezone: "Europe/London"
    locale: "en_GB.UTF-8"
    keymap: "uk"
```

## Tags

- `timezone` - Only timezone configuration
- `locale` - Only locale configuration  
- `keymap` - Only keymap configuration

## Idempotency

All tasks in this role are idempotent and can be run multiple times safely.

## Distribution Support

- Arch Linux
- Rocky Linux 9
- Other systemd-based distributions