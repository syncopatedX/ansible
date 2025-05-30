# Ansible Role: Docker

This Ansible role installs and configures Docker on Arch Linux-based systems (due to the use of `paru` and AUR packages). It handles Docker installation, Docker Compose, Docker Buildx, Lazydocker, NVIDIA container support, and basic Docker daemon configuration.

---

## Role Variables

The role utilizes several variables to customize its behavior.

**Default Variables (`defaults/main.yml`):**

- `docker`: A dictionary containing Docker-specific settings.
  - `storage`: Defines the path for Docker's data-root. The default is `/var/lib/docker`.
- `use_docker`: A boolean flag that can be used to conditionally run this role. Defaults to `true`.

**Main Variables (`vars/main.yml`):**

- `packages__docker`: A list of essential Docker-related packages to be installed. By default, this includes:
  - `docker`
  - `docker-compose`
  - `docker-buildx`
  - `lazydocker`

**Variables from `tasks/setup.yml` (implicitly used):**

- `user.name`: This variable is used when adding a user to the `docker` group. It's expected to be defined elsewhere, perhaps as a global variable or passed in via command line/inventory.
- `nvidia`: This variable is checked in `tasks/main.yml`. If defined, it triggers the installation of NVIDIA container toolkit packages.
- `ansible_check_mode`: This is an Ansible built-in variable used to control whether tasks make changes or just report what would be changed. Several tasks use `ignore_errors: "{{ ansible_check_mode }}"` to prevent failures during check mode runs.

---

### Role Tasks

**Main Tasks (`tasks/main.yml`):**

1. **Check Docker Installation**: Verifies if Docker is already installed by running `docker --version`.
2. **Print Docker Version**: If Docker is found, its version is printed to the console.
3. **Install Docker Packages**: Installs the packages listed in the `packages__docker` variable using `paru` (AUR helper). This task is tagged with `packages` and `docker_pkgs`.
4. **Install Docker NVIDIA Packages**: If the `nvidia` variable is defined, this task installs `nvidia-container-toolkit` and `nvidia-docker-compose` using `paru`. This is useful for enabling GPU support within Docker containers. This task is tagged with `packages` and `docker_pkgs`.
5. **Import Setup Tasks**: Includes tasks from `setup.yml` to perform further Docker configuration. This is tagged with `setup`.

**Setup Tasks (`tasks/setup.yml`):**

1. **Ensure "docker" Group Exists**: Creates a system group named `docker`. Tagged `groups`.
2. **Add User to Docker Group**: Adds the user specified by `{{ user.name }}` to the `docker` group. This allows the user to run Docker commands without `sudo`. Tagged `groups`.
3. **Create Docker Config Directory**: Creates the `/etc/docker` directory if it doesn't exist.
4. **Ensure Docker Data Directory Exists**: Creates the Docker storage directory (defined by `{{ docker.storage }}`) if it doesn't exist.
5. **Set Docker Storage Location**: Creates or updates `/etc/docker/daemon.json` to configure the `data-root` for Docker, pointing it to the path specified in `{{ docker.storage }}`. This notifies the `Reload systemd daemon` handler.
6. **Disable Overlay Redirect**: Creates a modprobe configuration file (`/etc/modprobe.d/disable-overlay-redirect-dir.conf`) to set `options overlay metacopy=off redirect_dir=off`. This can help with certain OverlayFS issues.
7. **Set Docker Service Preset**: Ensures the `docker` service is enabled to start on boot.

---

### Handlers

**Main Handlers (`handlers/main.yml`):**

- **Reload systemd daemon**: This handler is triggered by changes to the Docker daemon configuration (`daemon.json`). It executes `ansible.builtin.systemd` with `daemon_reload: true` to make systemd aware of any changes to service files or configurations.

---

### Files

**Shell Script (`files/etc/profile.d/compose.sh`):**

- This script adds `/usr/libexec/docker/cli-plugins` to the system `PATH` environment variable. This is often where Docker Compose (as a CLI plugin) might be installed or linked.

---

### Requirements

- **Ansible**: Version 2.1 or higher (as specified in `meta/main.yml`).
- **`paru`**: This role uses `paru` as an AUR (Arch User Repository) helper to install packages. `paru` (or another compatible AUR helper like `yay`) must be installed on the target Arch Linux systems.
- **User Variable**: The `user.name` variable must be defined for the "Add user to docker group" task.

---

### Dependencies

- None explicitly listed in `dependencies: []` within `meta/main.yml`.

---

### Example Playbook

Here's a basic example of how to use this role in a playbook (`tests/test.yml`):

YAML

```yaml
---
- hosts: localhost
  remote_user: root # Or a user with sudo privileges if 'become: true' is added to the role invocation
  roles:
    - docker
  vars:
    user:
      name: your_username # Replace with the actual username
    # Optional: define nvidia if you have an NVIDIA GPU and want container support
    # nvidia: true
    # Optional: override default storage path
    # docker:
    #   storage: /mnt/mydockerdata
```

**To run this playbook:**

1. Save the playbook (e.g., as `docker_playbook.yml`).
2. Ensure the `docker` role directory is in your Ansible roles path or in a `roles/` subdirectory relative to the playbook.
3. Run the playbook: `ansible-playbook docker_playbook.yml`

---

### How to Best Utilize This Role

1. **User Configuration**:

    - **Crucial**: Define the `user.name` variable in your playbook or inventory to ensure the specified user is added to the `docker` group. This is essential for non-root users to manage Docker containers.
    - Example:YAML

        ```yaml
        - hosts: my_arch_servers
          vars:
            user:
              name: developer01
          roles:
            - docker
        ```

2. **NVIDIA GPU Support**:

    - If your target machines have NVIDIA GPUs and you need Docker containers to access them (e.g., for machine learning), define the `nvidia: true` variable.
    - Example:YAML

        ```yaml
        - hosts: gpu_workstations
          vars:
            user:
              name: data_scientist
            nvidia: true
          roles:
            - docker
        ```

3. **Customize Docker Storage Path**:

    - By default, Docker data is stored in `/var/lib/docker`. If you need to change this (e.g., to a larger disk or a specific partition), override the `docker.storage` variable.
    - Example:YAML

        ```yaml
        - hosts: all
          vars:
            user:
              name: sysadmin
            docker:
              storage: /opt/docker_data
          roles:
            - docker
        ```

4. **Package Customization**:

    - While `packages__docker` in `vars/main.yml` lists common Docker packages, you can override this variable in your playbook or inventory if you need a different set of packages or specific versions (though version pinning with AUR helpers like `paru` can be tricky and might require specific `extra_args`).
5. **Conditional Execution**:

    - The `use_docker: true` default variable can be overridden to `false` if you want to skip the execution of this role for certain hosts or under specific conditions in a larger playbook.
6. **Tags**:

    - Utilize tags to run specific parts of the role:
        - `packages`, `docker_pkgs`: To only manage Docker package installations.
        - `groups`: To only manage Docker group creation and user addition.
        - `setup`: To run the Docker daemon configuration tasks.
    - Example: `ansible-playbook docker_playbook.yml --tags "packages"`
7. **Check Mode**:

    - Run the playbook in check mode (`ansible-playbook docker_playbook.yml --check`) to see what changes would be made without actually applying them. The role attempts to handle check mode gracefully for several tasks using `ignore_errors: "{{ ansible_check_mode }}"`.
8. **`compose.sh` Profile Script**:

    - The script in `files/etc/profile.d/compose.sh` adds `/usr/libexec/docker/cli-plugins` to the `PATH`. This is generally useful for Docker Compose v2, which is installed as a CLI plugin. Users will need to source their profile or log out and log back in for this change to take effect in their shell sessions.
