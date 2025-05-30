# Ansible Role: SSH Configuration

## Description

This role manages the installation and configuration of OpenSSH services (client and server) and related utilities on systems using the `pacman` package manager (e.g., Arch Linux). It allows for customization of the SSH daemon, installation of tools like `sshfs`, `autossh`, `keychain`, `mosh`, and `x11-ssh-askpass`, and basic user SSH directory setup.

## Requirements

- **Target System:** Must be a system that uses the `pacman` package manager.

- **Ansible Controller:**

  - `community.general.pacman` collection installed (`ansible-galaxy collection install community.general`).

  - Ansible version >= 2.1 (as per `meta/main.yml`).

## Role Variables

Below are the variables that can be set to customize the behavior of this role.

### Main Configuration

- `ssh_config_template_src`:

  - Description: Path to the Jinja2 template for the `sshd_config` file.

  - Default: `etc/sshd/sshd_config.j2` (within the role structure). You should customize this template for a secure setup.

- `ssh_config_dest`:

  - Description: Destination path for the `sshd_config` file on the target host.

  - Default: `/etc/ssh/sshd_config`

### SSH Daemon Settings (`ssh.*`)

These variables are typically accessed within the `sshd_config.j2` template or control service behavior.

- `ssh.port`:

  - Description: The port on which the SSH daemon should listen.

  - Default: `22`

- `ssh.enable_sshd`:

  - Description: Controls whether the `sshd` service should be enabled and started. If set to `false`, it will be disabled and stopped.

  - Default: Not explicitly set (service management tasks will run based on its definition and value). If undefined, the service state won't be actively changed to started/stopped unless it's `true` or `false`. For clarity, explicitly set it to `true` or `false`.

### User SSH Setup (`user.*`)

These variables are used for tasks related to user-specific SSH configurations.

- `user.name`:

  - Description: The username for whom the `.ssh` directory will be created. This variable **must** be **defined** if you intend for the "Make directory for user SSH key" task to run correctly for a specific user.

  - Default: None (the task will likely fail or use an unexpected value if not set in the playbook).

- `user.group`:

  - Description: The group for the user for whom the `.ssh` directory will be created.

  - Default: None (same as `user.name`).

### Optional Component Installation

By default, the role attempts to install several SSH-related tools. You can control this by overriding these variables or by adding conditional logic to your playbook/tasks if finer control is needed (e.g., by setting them to `false` and adding `when` conditions to the tasks).

- `ssh_install_openssh`:

  - Description: Controls the installation of the `openssh` package.

  - Default: `true` (implied by the task being present without a conditional variable)

- `ssh_install_sshfs`:

  - Description: Controls the installation of the `sshfs` package.

  - Default: `true` (implied)

- `ssh_install_autossh`:

  - Description: Controls the installation of the `autossh` package.

  - Default: `true` (implied)

- `ssh_install_keychain`:

  - Description: Controls the installation of the `keychain` package.

  - Default: `true` (implied)

- `ssh_install_x11_askpass`:

  - Description: Controls the installation of the `x11-ssh-askpass` package and the export of the `SSH_ASKPASS` environment variable in `/etc/profile`.

  - Default: `true` (implied)

- `ssh_install_mosh`:

  - Description: Controls the installation of the `mosh` (Mobile Shell) package.

  - Default: `true` (implied)

### Other Files

- `ssh_fuse_config_src`:

  - Description: Path to the `fuse.conf` file to be copied.

  - Default: `etc/fuse.conf` (within the role structure).

- `ssh_fuse_config_dest`:

  - Description: Destination path for the `fuse.conf` file.

  - Default: `/etc/fuse.conf`

## Tasks Overview

This role performs the following tasks:

1. **Install OpenSSH:** Ensures the `openssh` package is present.

2. **Push OpenSSH daemon configuration file:** Deploys `/etc/ssh/sshd_config` from the `sshd_config.j2` template. Notifies `Restart sshd` handler on change.

3. **Enable and start/Disable and stop OpenSSH:** Manages the `sshd.service` based on the `ssh.enable_sshd` variable.

4. **Install sshfs:** Ensures the `sshfs` package is present.

5. **Install autossh:** Ensures the `autossh` package is present.

6. **Copy fuse configuration file:** Deploys `/etc/fuse.conf`.

7. **Install keychain:** Ensures the `keychain` package is present.

8. **Install x11-ask-pass:** Ensures the `x11-ssh-askpass` package is present.

9. **Export SSH_ASKPASS environment variable:** Adds `export SSH_ASKPASS="/usr/lib/ssh/x11-ssh-askpass"` to `/etc/profile`. This is a system-wide change.

10. **Make** directory for user **SSH key:** Creates `~{{ user.name }}/.ssh` with appropriate ownership (`{{ user.name }}:{{ user.group }}`).

11. **Install Mosh:** Ensures the `mosh` package is present.

## Handlers Overview

- **Restart sshd:** Restarts the `sshd.service`. This is typically triggered when the `sshd_config` file is changed.

## Dependencies

None explicitly listed in `meta/main.yml`.

## Example Playbook

Here's an example of how to use this role in a playbook:

```yaml
- hosts: arch_servers
  become: yes
  vars:
    ssh_port: 2222
    ssh_enable_sshd: true
    user_name: "youruser"
    user_group: "yourgroup"
    # Example: To disable password authentication (recommended)
    # This would require your sshd_config.j2 template to use this variable
    ssh_permit_password_authentication: "no"
  roles:
    - { role: your_username.ssh } # Or the path to the role if not in a standard location
```

Remember to customize the `sshd_config.j2` template within the role to reflect your desired security settings. For example, to use `ssh_permit_password_authentication`:

**Example `sshd_config.j2` snippet:**

```yaml
# ... other configurations ...
Port {{ ssh.port | default(22) }}
PasswordAuthentication {{ ssh_permit_password_authentication | default('yes') }}
# ... other configurations ...
```

## Ensuring a Secure SSH Setup

Configuring SSH securely is critical. This role provides the tools, but security is a shared responsibility.

1. **Customize `sshd_config.j2` Thoroughly:**

    - **Password Authentication:** **Strongly disable password authentication.** Rely on SSH key-based authentication.

        ```yaml
        PasswordAuthentication no
        ```

    - **Root Login:** Prohibit direct root login.

        ```yaml
        PermitRootLogin prohibit-password
        # or
        # PermitRootLogin no
        ```

    - **Port:** Change the default SSH port using the `ssh.port` variable. This can help reduce automated attacks.

    - **AllowUsers / AllowGroups:** Restrict which users or groups can log in via SSH.

        ```yaml
        AllowUsers user1 user2
        # AllowGroups sshusers
        ```

    - **X11 Forwarding:** Disable if not needed.

        ```yaml
        X11Forwarding no
        ```

    - **MaxAuthTries:** Set a low number to mitigate brute-force attacks.

        ```yaml
        MaxAuthTries 3
        ```

    - **LoginGraceTime:** Set a short grace time for login.

        ```yaml
        LoginGraceTime 30s
        ```

    - **Use Strong Ciphers, MACs, and Key Exchange Algorithms:** Modern OpenSSH versions have good defaults, but you can explicitly define stronger ones if needed. Avoid legacy algorithms.

        ```yaml
        # Example (consult current best practices):
        # KexAlgorithms curve25519-sha256@libssh.org,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256
        # Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
        # MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-512,hmac-sha2-256,umac-128@openssh.com
        ```

    - **ClientAliveInterval / ClientAliveCountMax:** Configure to terminate idle sessions.

    - **StrictModes:** Keep `StrictModes` yes to ensure permissions on user SSH files are checked.

    - **Banner:** Configure a warning banner.

        ```yaml
        Banner /etc/issue.net
        ```

2. **Principle of Least Privilege:**

    - Only enable the SSH daemon (`ssh.enable_sshd: true`) on servers that require remote access.

    - Do not install unnecessary tools. If you don't need `sshfs`, `mosh`, etc., consider forking the role or adding variables to control their installation individually.

3. **Firewall Configuration:**

    - Implement a host-based firewall (e.g., `iptables`, `nftables`, `ufw`).

    - Only allow incoming connections on the configured `ssh.port` from trusted IP addresses or networks.

    - If using Mosh, remember it uses UDP ports (typically 60000-61000), which also need to be allowed through the firewall.

4. **SSH Key Management:**

    - **Use Strong Keys:** Generate RSA keys of at least 3072 or 4096 bits, or use Ed25519 keys.

    - **Protect Private Keys:** Secure user private keys with strong passphrases. Use an SSH agent (`keychain` is installed by this role) to avoid repeatedly typing passphrases, but understand the security implications.

    - **Authorized Keys:** Manage `authorized_keys` files carefully. This role creates the `~/.ssh` directory; you might want to extend it with tasks to manage `authorized_keys` content, perhaps using `ansible.posix.authorized_key`.

    - **Regularly Audit Keys:** Remove keys for users who no longer need access.

5. **Regular Updates and Monitoring:**

    - Keep the OpenSSH server, client, and the underlying operating system patched and up-to-date.

    - Monitor SSH logs (usually in `/var/log/auth.log` or `/var/log/secure` or via `journalctl -u sshd`) for suspicious activity, failed login attempts, and successful logins from unexpected locations. Consider tools like `fail2ban`.

6. **Mosh Considerations:**

    - Mosh provides session roaming and local echo but relies on SSH for initial authentication. Secure your SSH setup first.

    - Ensure Mosh's UDP ports are appropriately handled by your firewall.

7. **SSHFS and FUSE:**

    - Be cautious when mounting remote filesystems. Ensure the remote server is trusted.

    - The `fuse.conf` file can control who is allowed to mount FUSE filesystems. Review its settings.

8. **`SSH_ASKPASS` Environment Variable:**

    - This role sets `SSH_ASKPASS` system-wide in `/etc/profile`. This is used by tools like `ssh-add` or Git when needing a passphrase in a GUI environment. Understand its implications if graphical sessions are used on the server.

By following these guidelines and thoroughly testing your configuration, you can significantly improve the security of your SSH setup.

## License

(As per `meta/main.yml` - typically BSD, MIT, GPL, etc. The placeholder is "license (GPL-2.0-or-later, MIT, etc)")

## Author Information

(As per `meta/main.yml` - "your name", "your company (optional)")
