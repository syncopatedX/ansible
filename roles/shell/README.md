# Ansible Role: Shell Environment Setup

This role configures a user's shell environment, primarily focusing on Zsh with Oh My Zsh. It installs essential packages, sets up useful Oh My Zsh plugins like `fd` and `ripgrep`, syncs custom Zsh functions, and deploys Zsh profile configuration files (`.zlogin`, `.zprofile`, `.zshenv`, `.zshrc`) from templates.

## Requirements

- **Ansible:** Version 2.1 or higher.

- **Target System:** This role is primarily designed for Arch Linux-based systems or any system where packages can be installed using an AUR (Arch User Repository) helper that `ansible.builtin.aur` can utilize (e.g., `yay`, `paru`). If not using an AUR-based system, the package installation tasks will need modification.

- **User Variables:** The role relies on certain user-specific variables being defined. These are typically set as Ansible facts or in your inventory's group/host variables:

  - `user.name`: The username for whom the shell environment is being configured (e.g., `john_doe`).

  - `user.group`: The primary group of the user (e.g., `users`).

  - `user.home`: The absolute path to the user's home directory (e.g., `/home/john_doe`).

## Role Variables

This role uses several variables to customize the setup. You can override these in your playbook or inventory.

### Default Variables (`defaults/main.yml`)

These variables have default values that can be easily changed.

- `profile_config_dir`:

  - **Description:** Specifies the directory where the Zsh profile configuration files (`.zlogin`, `.zprofile`, `.zshenv`, `.zshrc`) will be placed.

  - **Default:** `{{ user.home }}` (resolves to the user's home directory).

  - **Customization:** You can change this if you prefer to store these dotfiles in a different location, for example, within a subdirectory like `{{ user.home }}/.config/zsh`. However, standard Zsh behavior expects them in the home directory.

- `desktop`:

  - **Description:** Defines the window manager being used. This variable is intended for use within the Zsh configuration templates (e.g., `home/.zshrc.j2`) to conditionally set environment variables, aliases, or source specific configurations relevant to the window manager.

  - **Default:** `"i3"`

  - **Customization:** Set this to your window manager of choice (e.g., `"sway"`, `"gnome"`, `"kde"`, `"hyprland"`). You will then need to ensure your Zsh template files (`*.j2`) utilize this variable to apply specific settings. For example, in `.zshrc.j2`:

        ```yaml
        {% if desktop == "sway" %}
        export MOZ_ENABLE_WAYLAND=1
        {% endif %}
        ```

### Core Variables (`vars/main.yml`)

These variables define the core packages to be installed for the Zsh environment.

- `packages__zsh`:

  - **Description:** A list of Zsh-related packages to be installed using the `ansible.builtin.aur` module.

  - **Default List:**

        ```yaml
        - oh-my-zsh-git  # Oh My Zsh framework
        - zoxide         # Smarter cd command
        - zsh            # The Z shell
        - zsh-autocomplete # Real-time type-ahead autocompletion
        - zsh-completions  # Additional completion definitions
        - zsh-syntax-highlighting # Fish-like syntax highlighting
        ```

  - **Customization:** Modify this list to add or remove Zsh packages. For instance, if you don't use `zoxide`, you can remove it. If you need other Zsh plugins available via the AUR (like `zsh-autosuggestions` if not included by `oh-my-zsh-git` or `zsh-autocomplete`), add them here. If you are not on an AUR-based system, you will need to change the installation task to use `ansible.builtin.package` and adjust package names accordingly.

## Tasks Overview

The role executes the following main tasks, primarily defined in `tasks/zsh.yml`:

1. **Install Zsh Packages:**

    - Uses the `ansible.builtin.aur` module to install all packages listed in the `packages__zsh` variable.

    - This task is tagged with `packages` and `shell_pkgs`.

    - A rescue block is included to output a debug message if package installation fails.

2. **Install Oh My Zsh Plugins (fd and ripgrep):**

    - Copies pre-packaged Oh My Zsh plugins for `fd` (a user-friendly `find` alternative) and `ripgrep` (a fast `grep` alternative) from the role's `files/usr/share/oh-my-zsh/plugins/` directory to the system-wide Oh My Zsh plugins directory (`/usr/share/oh-my-zsh/plugins/`).

    - These plugins provide completions and potentially aliases for these tools.

    - **Note:** To enable these plugins, you'll need to add `fd` and `ripgrep` to the `plugins=(...)` array in your `.zshrc` file (or the `.zshrc.j2` template within this role).

3. **Install/Sync Zsh Custom Functions:**

    - Uses `ansible.posix.synchronize` (which wraps `rsync`) to copy custom Zsh functions from the role's `files/home/.local/share/zsh/` directory to `{{ user.home }}/.local/share/zsh/` on the target machine.

    - This allows you to maintain a collection of custom shell scripts and functions within the role and have them synced to the user's environment.

    - The `synchronize` module is configured to update files, omit directory times, show progress, itemize changes, and set correct ownership.

    - This task is tagged with `zsh_functions`.

4. **Set Zsh Profile Configurations:**

    - Uses `ansible.builtin.template` to generate Zsh configuration files from Jinja2 templates located in the role's `templates/home/` directory.

    - The following files are templated:

        - `.zlogin`

        - `.zprofile`

        - `.zshenv`

        - `.zshrc`

    - These files are placed in the `{{ profile_config_dir }}` (defaulting to the user's home directory).

    - Ownership is set to `{{ user.name }}:{{ user.group }}`, and permissions are set to `0644`.

    - Backups of existing files are created.

    - This task is tagged with `env` and `profile`.

## Customization Guide

Here’s how you can customize this role to better suit your needs:

### 1. Overriding Variables

You can override any of the defined variables (see "Role Variables" section) in your Ansible playbook or inventory.

**Example Playbook Override:**

```yaml
- hosts: your_target_host
  become: yes # Or no, depending on tasks that need privilege
  vars:
    user:
      name: myuser
      group: mygroup
      home: /home/myuser
    profile_config_dir: "{{ user.home }}/.config/zsh_custom_location" # Example override
    desktop: "sway"
    packages__zsh:
      - zsh
      - oh-my-zsh-git
      - zsh-autosuggestions # Added a new package
      - zsh-syntax-highlighting
      # zoxide removed
  roles:
    - role: shell # Assuming your role is named 'shell'
```

### 2. Managing Zsh Packages

- **Add/Remove Packages:** Modify the `packages__zsh` list variable as shown in the example above.

- **Non-AUR Systems:** If your target system doesn't use AUR, you'll need to modify the "Install zshell packages" task in `tasks/zsh.yml`. Change `aur:` to `ansible.builtin.package:` and ensure the package names are correct for your system's package manager (e.g., `apt`, `yum`, `dnf`).

    **Example modification for Debian/Ubuntu:**

    ```yaml
    # tasks/zsh.yml
    # ...
    - name: Install zshell packages
      ansible.builtin.package: # Changed from aur
        name: "{{ item }}"
        state: present
      with_items:
        # Adjust package names as needed for your distro
        - zsh
        - zsh-syntax-highlighting 
        # oh-my-zsh might need manual install or a different package
        # zoxide might have a different package name or need compilation
      become: true # Package installation usually requires sudo
    # ...
    ```

### 3. Managing Oh My Zsh Plugins

- **Included Plugins (`fd`, `ripgrep`):** To enable the `fd` and `ripgrep` plugins copied by the role, ensure they are listed in the `plugins` array within your `templates/home/.zshrc.j2` file:

    ```yaml
    # templates/home/.zshrc.j2
    # ...
    plugins=(
      git
      # other_plugins
      fd
      ripgrep
    )
    # ...
    ```

- **Adding More Pre-packaged Plugins:** If you have other Oh My Zsh plugins you want to manage similarly:

    1. Place the plugin's directory into `files/usr/share/oh-my-zsh/plugins/` within your role.

    2. Update the "Install fd and ripgrep ohmyzsh plugins" task in `tasks/zsh.yml` to include your new plugin in the `with_items` list.

    3. Add the plugin's name to the `plugins` array in `templates/home/.zshrc.j2`.

- **Using Oh My Zsh's Built-in Plugin Manager:** For plugins managed directly by Oh My Zsh (those listed in `~/.oh-my-zsh/plugins` or that Oh My Zsh can download), you only need to add their names to the `plugins=(...)` array in your `templates/home/.zshrc.j2`. The `oh-my-zsh-git` package should handle their availability.

### 4. Customizing Zsh Functions

- Place any custom shell scripts or `.zsh` function files you want to be available in your Zsh environment into the `files/home/.local/share/zsh/` directory within your role structure.

- The `ansible.posix.synchronize` task will copy them to `{{ user.home }}/.local/share/zsh/`.

- Ensure your `.zshrc` (via `templates/home/.zshrc.j2`) sources files from this directory or adds it to `fpath` if it contains autoloadable functions. For example:

    ```yaml
    # templates/home/.zshrc.j2
    # Add custom functions directory to fpath
    fpath=($HOME/.local/share/zsh/functions $fpath)
    
    # Source scripts directly if needed
    for custom_script in $HOME/.local/share/zsh/scripts/*.sh; do
      if [ -f "$custom_script" ]; then
        source "$custom_script"
      fi
    done
    ```

### 5. Modifying Zsh Profile Templates

- The core of your Zsh configuration (aliases, environment variables, prompt, options, etc.) is defined in the Jinja2 templates:

  - `templates/home/.zshenv.j2` (sourced on all invocations of Zsh, for environment variables)

  - `templates/home/.zprofile.j2` (for login shells, after `.zshenv`, for commands)

  - `templates/home/.zshrc.j2` (for interactive shells, after `.zshenv`)

  - `templates/home/.zlogin.j2` (for login shells, after `.zshrc`, for commands)

- Edit these files to change your Zsh prompt (e.g., Powerlevel10k if installed and configured here), set aliases, define environment variables, configure Zsh options (`setopt`), and manage Oh My Zsh settings.

- Remember you can use the `desktop` variable (and any other variables you define) within these templates for conditional logic.

## Example Playbook

Here's a basic example of how to use this role in a playbook:

```yaml
---
- hosts: workstations
  become: false # Most tasks in this role run as the user, package install might need become if not using AUR helper that handles it.
  vars:
    user:
      name: "johndoe"
      group: "users"
      home: "/home/johndoe"
    # Optional: Override other defaults if needed
    # desktop: "sway"
    # packages__zsh:
    #   - zsh
    #   - oh-my-zsh-git

  roles:
    - role: your_namespace.shell # Or just 'shell' if in the same directory/configured roles_path
      tags: ["shell_setup"]
```

Remember to replace `your_namespace.shell` with the actual name or path to your role. The `user` variables are crucial and must be defined.

## License

Please refer to the `meta/main.yml` file for license information. (The provided `meta/main.yml` has a placeholder `license: license (GPL-2.0-or-later, MIT, etc)`).

## Author Information

Please refer to the `meta/main.yml` file for author information. (The provided `meta/main.yml` has placeholder author details).
