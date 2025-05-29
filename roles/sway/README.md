# Ansible Role: Sway Tiling Window Manager

## Overview

This Ansible role installs and configures Sway, a tiling Wayland compositor designed as a drop-in replacement for the i3 window manager on X11. It aims to provide a complete and aesthetically pleasing Sway environment out-of-the-box.

The role handles:

- Installation of Sway and essential ecosystem packages (via `paru` AUR helper).
- Deployment of a structured configuration for Sway, Waybar, Mako, Wlogout, Foot terminal, and other tools.
- A theming system that applies a consistent look and feel across Sway and related applications.
- Default configurations for inputs, outputs, keybindings, and modes.
- Autostart setup for necessary services and user applications.

## Sway vs. i3: Key Differences

While Sway aims for configuration compatibility with i3, there are fundamental differences due to Sway running on Wayland and i3 on X11:

1. **Display Server Protocol**:
    - **Sway**: Uses Wayland, a modern display server protocol aiming for better security, performance, and simplicity.
    - **i3**: Uses X11, an older, well-established protocol with a vast ecosystem but also known architectural limitations.

2. **Configuration Compatibility**:
    - Most of your i3 configuration will work with Sway.
    - Command-line interaction: Use `swaymsg` instead of `i3-msg`.
    - Input device configuration (`man 5 sway-input`) and output configuration (`man 5 sway-output`) are specific to Sway and differ from X11 methods (e.g., `xinput`, `xrandr`).

3. **Ecosystem Tools**:
    - Many X11-specific utilities have Wayland-native equivalents. This role installs several:
        - **Screenshot**: `grim` and `slurp` (instead of `scrot`).
        - **Screen Recording**: `wf-recorder`.
        - **Application Launcher**: `fuzzel` (a `rofi` alternative for Wayland).
        - **Status Bar**: `waybar`.
        - **Notification Daemon**: `mako`.
        - **Output Management**: `kanshi` or manual `swaymsg output` commands.
    - Sway uses XWayland to run X11 applications, providing good compatibility for most legacy GUI applications.

4. **Graphics & Performance**:
    - Wayland aims for "every frame perfect," potentially leading to smoother rendering and reduced screen tearing.
    - Direct rendering in Wayland can reduce overhead compared to X11's model.

5. **Security**:
    - Wayland is designed with stronger isolation between clients, enhancing security.

## Requirements

- Ansible >= 2.1
- A target system with an Arch User Repository (AUR) helper. This role specifically uses `paru`.
- The target user (specified by `user.name`) should have `sudo` privileges for package installation and system-wide configuration tasks.

## Role Variables

This role uses several variables to customize the installation. Key variables include:

**From `defaults/main.yml`:**
These variables control the creation of necessary directories in the user's home:

- `sway_directory_default_mode`: Default mode for created directories (e.g., `'0750'`).
- `sway_directory_default_owner`: Default owner (e.g., `"{{ user.name }}"`).
- `sway_directory_default_group`: Default group (e.g., `"{{ user.group }}"`).
- `sway_directory_default_location`: Base location for user directories (e.g., `"{{ user.home }}"`).
- `sway_directory_definitions`: A list defining directories to create. Example:

    ```yaml
    sway_directory_definitions:
      - dest: ".config/sway"
      - dest: ".config/waybar"
      - dest: ".config/mako"
      - dest: ".config/wlogout"
      # ... and others
    ```

**From `vars/main.yml`:**

- `packages__sway`: A list of packages to be installed for the Sway environment. You can extend this list to include your preferred applications.

    ```yaml
    packages__sway:
      - foot
      - fuzzel
      - greetd
      # ... and others
    ```

**Playbook-level Variables (expected):**
You need to define the `user` variable in your playbook or inventory:

- `user.name`: The username for whom Sway is being configured.
- `user.group`: The primary group of the user.
- `user.home`: The home directory of the user.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: your_sway_desktop
  vars:
    user:
      name: myuser         # Replace with your username
      group: myuser        # Replace with your user's group
      home: /home/myuser   # Replace with your user's home directory
  roles:
    - role: sway
      # or the fully qualified collection name if applicable
      # - role: your_namespace.your_collection.sway
```

## Configuration Structure

This role establishes a layered configuration system, allowing for system-wide defaults and user-specific overrides:

1. **System-wide Base (`/etc/sway/`)**:

    - Managed by Ansible task `Update sway system configs`.
    - Contains default configurations for Sway itself (`config`), variables (`definitions`), input devices (`inputs/`), modes (`modes/`), outputs (`outputs/`), and pre-defined themes (`themes/`).
    - The main system config `/etc/sway/config` includes snippets from `/etc/sway/config.d/*`.
2. **User Configuration (`{{ user.home }}/.config/sway/`)**:

    - Managed by Ansible task `Update sway user configs`.
    - This is where you'll make most of your personalizations.
    - **`config`**: The primary Sway configuration file loaded on startup. It orchestrates the inclusion of other files:
        - `$HOME/.config/sway/definitions`: User-defined global variables (e.g., `$mod` key, selected `$theme`).
        - `$theme/definitions`: Variables specific to the selected theme (colors, fonts, application theme names).
        - `$HOME/.config/sway/inputs/*`: User-specific input device configurations.
        - `$HOME/.config/sway/outputs/*`: User-specific output (monitor) configurations.
        - `$HOME/.config/sway/modes/*`: User-specific keybinding modes (default, resize, etc.).
        - `/etc/sway/config.d/*`: System-wide configuration snippets (e.g., for systemd user environment).
        - `$HOME/.config/sway/themes/scripts/*`: Scripts that run on Sway reload to apply the current theme to GTK, Kvantum, Mako, and link Waybar/Wlogout CSS.
        - `$HOME/.config/sway/config.d/*`: User-specific additional configuration snippets (e.g., `98-application-defaults`, `99-autostart-applications`).
3. **Application Configurations**:

    - **Foot Terminal**: `{{ user.home }}/.config/foot/foot.ini` (themed by Sway theme scripts).
    - **Mako Notifications**: `{{ user.home }}/.config/mako/config` (themed by Sway theme scripts).
    - **Waybar**: `{{ user.home }}/.config/waybar/` (`config`, `style.css`, `theme.css`). `style.css` and `theme.css` are templated by Ansible.
    - **Wlogout**: `{{ user.home }}/.config/wlogout/` (`layout`, `style.css`, `theme.css`). `style.css` and `theme.css` are templated by Ansible.
    - **GTK/Kvantum**: Settings are applied by scripts in `$HOME/.config/sway/themes/scripts/` based on variables from the selected theme.

## Customization Guide

Here’s how to tailor your Sway environment:

### 1. Changing Themes

The role comes with pre-defined themes in `/etc/sway/themes/` (e.g., `matcha-green`, `matcha-blue`).

1. Edit your user's Sway definitions file: `{{ user.home }}/.config/sway/definitions`.
2. Modify the `$theme` variable to point to your desired theme path. For example:

```shell
# In {{ user.home }}/.config/sway/definitions
# set $theme /etc/sway/themes/matcha-green
set $theme /etc/sway/themes/matcha-blue
```

3. Reload Sway (default: `$mod+Shift+c`). The scripts in `$HOME/.config/sway/themes/scripts/` will apply the new theme settings to GTK, Kvantum, Mako, Foot, and attempt to link theme-specific CSS for Waybar and Wlogout.

**Creating Custom Themes**:

- Copy an existing theme directory from `/etc/sway/themes/` to a custom location (e.g., `{{ user.home }}/.config/sway/themes/my-custom-theme`).
- Customize the `definitions` file within your new theme directory (colors, fonts, application theme names).
- Modify other theme-specific files like `foot.ini`.
- If you want Waybar and Wlogout to use theme-specific colors, create/edit `theme.css` inside your custom theme directory (e.g., `my-custom-theme/theme.css`). The `04-link-theme-files` script will symlink this.
- Update the `$theme` variable in `{{ user.home }}/.config/sway/definitions` to point to your new theme path.

### 2. Modifying Keybindings

- Default keybindings are defined in `/etc/sway/modes/default` and other files within `/etc/sway/modes/`.
- User-specific overrides are located in `{{ user.home }}/.config/sway/modes/`. For example, to edit default mode keybindings, modify `{{ user.home }}/.config/sway/modes/default`.
- Example: Change the terminal launch key in `{{ user.home }}/.config/sway/modes/default`:

```shell
# Original: bindsym $mod+Return exec $term
bindsym $mod+Shift+Return exec $term # Changed to Mod+Shift+Return
```

- You can also add new keybindings directly in `{{ user.home }}/.config/sway/config` or by creating a new `.conf` file in `{{ user.home }}/.config/sway/config.d/`.

### 3. Adding Autostart Applications

1. Edit `{{ user.home }}/.config/sway/config.d/99-autostart-applications`.
2. Add `exec <your_application>` lines.
    - For applications that should not generate a startup notification (e.g., background services), use `exec --no-startup-id <your_application>`.

```shell
# In {{ user.home }}/.config/sway/config.d/99-autostart-applications
exec --no-startup-id dropbox
exec firefox
```

### 4. Input Configuration (Keyboard, Touchpad)

1. System defaults are in `/etc/sway/inputs/`.
2. User overrides are in `{{ user.home }}/.config/sway/inputs/`.
3. To customize, edit the relevant files, e.g., `{{ user.home }}/.config/sway/inputs/default-keyboard` or `default-touchpad`.

```shell
# Example: Add German layout to {{ user.home }}/.config/sway/inputs/default-keyboard
input type:keyboard {
    xkb_layout "us,de"
    xkb_options "grp:alt_shift_toggle,ctrl:nocaps" # Toggle with Alt+Shift, CapsLock as Ctrl
}
```

Consult `man 5 sway-input` for all available options.

### 5. Output Configuration (Monitors, Wallpaper)

1. System default is in `/etc/sway/outputs/default-screen`.
2. User override is in `{{ user.home }}/.config/sway/outputs/default-screen`.
3. The wallpaper is set via the `$background` variable, defined in the active theme's `definitions` file (e.g., `/etc/sway/themes/matcha-green/definitions`).
4. To configure specific monitor resolutions, positions, or different wallpapers per output, edit `{{ user.home }}/.config/sway/outputs/default-screen`:

```shell
# In {{ user.home }}/.config/sway/outputs/default-screen
output HDMI-A-1 resolution 1920x1080 position 0,0 bg /path/to/my/wallpaper_hdmi.png fill
output DP-1 resolution 2560x1440 position 1920,0 bg /path/to/my/wallpaper_dp.png fill
# Fallback for any other outputs (optional, if $background is set by theme)
# output * bg $background fill
```

### 6. Waybar and Wlogout Styling

**General Styling (padding, non-color fonts):** The files `style.css` for Waybar and Wlogout are templated by Ansible from `roles/sway/templates/home/.config/{waybar,wlogout}/style.css.j2`. 

To make persistent changes, you can:

- Modify these `.j2` template files within the role itself.
- Copy the generated `style.css` files from your `~/.config/{waybar,wlogout}/` after the first run and manage them manually (Ansible will overwrite them on subsequent runs if `backup: yes` is not sufficient or if you want to prevent Ansible from touching them).

**Color Theming:** The color scheme for Waybar and Wlogout is primarily controlled by `theme.css`.

1. Ansible templates default `theme.css` files into `{{ user.home }}/.config/waybar/theme.css` and `{{ user.home }}/.config/wlogout/theme.css` using the `*.css.j2` files in the role's templates directory. These currently use colors similar to the `matcha-green` theme.
2. However, the Sway theme script `04-link-theme-files` (located in `{{ user.home }}/.config/sway/themes/scripts/`) attempts to symlink `$theme/theme.css` to `{{ user.home }}/.config/waybar/theme.css` and `{{ user.home }}/.config/wlogout/theme.css` every time Sway reloads.
3. **This means if your selected Sway theme (e.g., `/etc/sway/themes/my-theme/`) contains a `theme.css` file, that file will be used for Waybar and Wlogout, overriding the one templated by Ansible.** This is the recommended way to ensure Waybar/Wlogout colors match your Sway theme.
4. If your chosen Sway theme does _not_ provide a `theme.css`, the Ansible-templated version (with default colors) will be in effect.

## License

Please update the `license` field in `roles/sway/meta/main.yml`. (Currently: `license (GPL-2.0-or-later, MIT, etc)`)

## Author Information

Please update the `author` and `company` fields in `roles/sway/meta/main.yml`. (Currently: `your name`, `your company (optional)`)
