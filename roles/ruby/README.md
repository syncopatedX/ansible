# Ansible Role: Ruby Environment ✨💎

[![Galaxy Role](https://img.shields.io/badge/galaxy-your_namespace.ruby-blue.svg)](https://galaxy.ansible.com/your_namespace/ruby) <!-- Replace with your actual Galaxy link if applicable -->
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) <!-- Choose your license -->
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](.) <!-- Link to your CI if you have one -->

Set up your Ruby development environment with ease! This role handles installing Ruby development packages, managing system-wide gems, and optionally installing and configuring the powerful **Ruby Version Manager (RVM)**.

Whether you need a specific system Ruby setup or the flexibility of multiple Ruby versions via RVM, this role has you covered.

## 🚀 Features

* Installs necessary Ruby development packages based on OS family.
* Manages system-wide Ruby gems (`/usr/bin/gem`).
* Configures `gemrc` for predictable system vs. user gem installation.
* **Optional RVM Installation:**
  * Installs RVM for the specified user.
  * Handles GPG key verification securely (with fallback).
  * Idempotently installs or updates RVM to the desired version.
  * Configures RVM `autolibs` for dependency management.
  * Installs an RVM-managed OpenSSL if needed.
  * Installs specified Ruby versions via RVM.
  * Installs gems within specific RVM Ruby environments.

## ✅ Requirements

* **Ansible:** Version 2.10 or higher.
* **Target OS:** Tested primarily on Arch Linux, but designed to be adaptable via OS-specific variable files (`vars/{{ ansible_os_family }}.yml`).
* **User:** Requires a target user defined (often via `user` variable in the playbook or inventory). RVM installation runs as this user. System package/gem tasks require `become: true`.
* **Dependencies:** `gpg2` is required on the target host for RVM GPG key verification.

## ⚙️ Role Variables

Here are the key variables you can use to customize the role:

### **Main Role Variables** (Defined in `vars/main.yml` or Playbook)

| Variable      | Description                                                                 | Type         | Default                                  |
| :------------ | :-------------------------------------------------------------------------- | :----------- | :--------------------------------------- |
| `gems`        | List of Ruby gems to install system-wide using `/usr/bin/gem`.              | `list`       | `[]`                                     |
| `rvm_install` | Set to `true` to enable RVM installation tasks.                             | `boolean`    | `false`                                  |
| `user`        | Dictionary with target user info (used for RVM path, `.gemrc`).             | `dictionary` | `{ name: "...", home: "..." }` (See Note) |

*Note: `user` is often defined globally in the playbook, e.g., `{ name: "{{ lookup('env', 'USER') }}", home: "{{ lookup('env', 'HOME') }}" }`*

---

### **RVM Specific Variables** (Used when `rvm_install: true`)

| Variable                    | Description                                                                     | Type      | Default                                                              |
| :-------------------------- | :------------------------------------------------------------------------------ | :-------- | :------------------------------------------------------------------- |
| `rvm1_user`                 | Username RVM should be installed for.                                           | `string`  | `{{ user.name }}`                                                    |
| `rvm1_install_path`         | Base directory for the RVM installation.                                        | `string`  | `{{ user.home }}/.rvm`                                               |
| `rvm1_rvm`                  | Expected path to the RVM executable after installation.                         | `string`  | `{{ rvm1_install_path }}/bin/rvm`                                    |
| `rvm1_temp_download_path`   | Temporary directory for downloading the installer.                              | `string`  | `/tmp`                                                               |
| `rvm1_rvm_latest_installer` | URL for the RVM installer script.                                               | `string`  | `https://get.rvm.io`                                                 |
| `rvm1_rvm_version`          | RVM version to install/update to (e.g., `stable`, `latest`).                    | `string`  | `stable`                                                             |
| `rvm1_install_flags`        | Additional flags for the RVM installer.                                         | `string`  | `""`                                                                 |
| `rvm1_gpg_keys`             | Space-separated GPG Key IDs for RVM verification.                               | `string`  | `"409B6B... 7D2BAF..."` (See defaults file for full keys)            |
| `rvm1_gpg_key_servers`      | List of GPG keyservers to try first.                                            | `list`    | `["hkp://keyserver.ubuntu.com", "hkp://pgp.mit.edu", ...]`           |
| `rvm1_rvm_check_for_updates`| If RVM is installed, check for updates?                                         | `boolean` | `true`                                                               |
| `rvm1_autolib_mode`         | RVM autolibs mode (dependency handling). See RVM docs.                          | `string`  | `read-fail`                                                          |
| `rvm1_rubies`               | List of Rubies to install via RVM (dictionaries with `version`, optional `gems`). | `list`    | `[]`                                                                 |

**Example `rvm1_rubies` structure:**

```yaml
rvm1_rubies:
  - version: "ruby-3.1.2"
    gems: ["bundler", "rails"]
    default: true # Optional: Make this the default Ruby
  - version: "ruby-2.7.6"
```

## 🧩 Dependencies

* This role relies on OS-specific package lists defined in `vars/{{ ansible_os_family }}.yml`. Ensure a file exists for your target OS family (e.g., `vars/Archlinux.yml`, `vars/Debian.yml`).
* Requires `gpg2` on the target for RVM installation.

## playbook Example

```yaml
---
- name: Setup Development Workstation
  hosts: localhost
  connection: local
  become: true
  vars:
    # Define the primary user for RVM
    user:
      name: "{{ lookup('env', 'USER') }}"
      home: "{{ lookup('env', 'HOME') }}"

    # --- System Ruby ---
    # List of gems to install globally
    gems:
      - bundler
      - rake

    # --- RVM Configuration ---
    rvm_install: true # Enable RVM installation
    rvm1_rubies:
      - version: "ruby-3.1.2" # Install Ruby 3.1.2
        gems: ["rails", "puma"] # Install these gems for 3.1.2
      - version: "ruby-2.7.6" # Install Ruby 2.7.6
        default: true # Make this the default Ruby
  roles:
    - role: ruby # Use your role name here
```
