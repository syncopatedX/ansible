# Ansible Workstation Archlinux

This Ansible playbook automates the configuration of a development-focused workstation, primarily targeting Arch Linux and its derivatives. It leverages Ansible roles for modularity and maintainability, setting up everything from base system utilities to a complete development environment.

## Table of Contents

- [Ansible Workstation Archlinux](#ansible-workstation-archlinux)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Customization](#customization)
  - [Roles Overview](#roles-overview)
  - [Playbook Structure](#playbook-structure)
  - [Contributing](#contributing)
  - [License](#license)
  - [Troubleshooting](#troubleshooting)

## Features

This playbook provides a comprehensive workstation setup, including:

*   **Base System:**
    *   Package manager configuration (pacman, paru).
    *   Repository setup (archaudio, chaotic-aur).
    *   System utilities (mlocate, reflector).
    *   Mirrorlist update automation.
*   **User Environment:**
    *   User account creation and configuration.
    *   Shell customization (zsh, oh-my-zsh, aliases).
    *   Terminal emulator setup (kitty).
    *   File manager configuration (ranger).
    *   Optional passwordless sudo/polkit.
*   **Containerization & Virtualization:**
    *   Docker installation and configuration (including NVIDIA support).
    *   Libvirt installation and configuration (with Vagrant support).
*   **X11 & Window Manager:**
    *   Xorg installation.
    *   i3 window manager setup.
    *   Rofi application launcher.
    *   sxhkd (Simple X Hotkey Daemon).
    *   XDG Base Directory Specification compliance.
*   **Development Tools:**
    *   Ruby environment setup (rvm, bundler, gems).
    *   Custom tools: `code-packager` and `whisper-stream`.
*   **Input Device Management:**
    *   `input-remapper` installation and configuration.
* **Homepage:**
    * Sets a simple static homepage.

## Requirements

*   **Ansible:** Version 2.9 or higher is recommended.
*   **Target Host:** An Arch Linux-based distribution.  While some tasks are distribution-agnostic, the playbook is primarily tested and designed for Arch.
*   **SSH Access:** Ansible requires SSH access to the target host(s).
*   **Root/Sudo Privileges:** The playbook requires root or sudo privileges to install packages and modify system configurations.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ansible-workstation.git  # Replace with your repository URL
    cd ansible-workstation
    ```

2.  **Install required Ansible roles (if using Galaxy):**

    ```bash
    ansible-galaxy install -r requirements.yml  # If you have a requirements.yml file
    ```

## Usage

1.  **Inventory:** Create an inventory file (e.g., `hosts`) to define your target host(s).  A minimal example:

    ```ini
    [workstation]
    myworkstation ansible_host=your_workstation_ip_or_hostname ansible_user=your_username
    ```

2.  **Run the playbook:**

    ```bash
    ansible-playbook -i hosts playbooks/workstation.yml
    ```
    To use `become` (sudo) to run with elevated privileges:

    ```bash
    ansible-playbook -i hosts playbooks/workstation.yml -b
    ```

    You can also specify the user with `-u <user>`:

     ```bash
    ansible-playbook -i hosts playbooks/workstation.yml -b -u <user>
    ```
3. **Dry Run**:
   ```bash
    ansible-playbook -i hosts playbooks/workstation.yml --check
   ```

## Customization

The playbook's behavior can be customized using Ansible variables. You can define these variables in several ways:

*   **Inventory file:** Add variables directly to your `hosts` file.
*   **Group/Host variable files:** Create files in `group_vars/` or `host_vars/` directories.
*   **Extra variables (`-e`):** Pass variables on the command line using the `-e` flag.
*   **Variable files included in roles:** Some roles might include their own variable files (e.g., `roles/ruby/vars/main.yml`).

**Key Customizable Variables:**

| Variable              | Description                                                                  | Default Value |
| --------------------- | ---------------------------------------------------------------------------- | ------------- |
| `user`                | Dictionary containing user settings (name, shell, groups, sudoers, etc.)     | (See `defaults/main.yml` within relevant roles) |
| `use_docker`          | Enable/disable Docker installation and configuration.                        | `true`        |
| `use_libvirt`         | Enable/disable Libvirt installation and configuration.                       | `false`       |
| `use_vagrant`         | Enable/disable Vagrant installation (requires `use_libvirt`).               | `false`       |
| `disable_vblank`      | Disable vertical synchronization in X11.                                     | (Undefined)   |
| `debugging`         | Define to see debug messages, for example mirror status. | (Undefined) |
| `update_mirrors`      | Force update of mirrorlist. | (Undefined) |
| `nvidia`              | Enables Docker NVIDIA support. | (Undefined) |
| `rvm_install`           | Enable/disable Ruby Version Manager (RVM) installation.              | `false`        |

**Example (using extra variables):**

```bash
ansible-playbook -i hosts playbooks/workstation.yml -b -e "use_docker=false use_libvirt=true user.sudoers=true"
```

This command disables Docker, enables Libvirt, and configures passwordless sudo for the user defined in the `user` variable.

## Roles Overview

The playbook is organized into the following roles:

*   **`base`:** Core system setup, package management, and repository configuration.
*   **`user`:** User account management, shell configuration, and SSH key setup.
*   **`docker`:** Docker installation and configuration.
*   **`libvirt`:** Libvirt and Vagrant installation and configuration.
*   **`x11`:** X Window System setup.
*   **`sxhkd`:** sxhkd configuration.
*   **`rofi`:** Rofi configuration.
*   **`xdg`:** XDG Base Directory Specification compliance.
*   **`i3`:** i3 window manager installation and configuration.
* **`homepage`:** Homepage setup
*   **`ruby`:** Ruby environment setup.

## Playbook Structure

The `playbooks/workstation.yml` file is structured into four main plays:

1.  **Play #1 (workstation):**  The primary play, targeting the `workstation` host group. This play handles the majority of the workstation configuration, including all the roles mentioned above.

2.  **Play #2 (workstation):** Installs the `code-packager` utility.

3.  **Play #3 (all):** Installs the `whisper-stream` utility.  This play targets all hosts in the inventory.

4.  **Play #4 (all):** Installs and configures `input-remapper`.  This play also targets all hosts.

```mermaid
---
title: "Ansible Playbook Grapher"
---
%%{ init: { "flowchart": { "curve": "bumpX" } } }%%
flowchart LR
	%% Start of the playbook 'playbooks/workstation.yml'
	playbook_f9a782fc("playbooks/workstation.yml")
		%% Start of the play 'play #1 (workstation): 3'
		play_ed63c3e8["play #1 (workstation): 3"]
		style play_ed63c3e8 stroke:#10bca9,fill:#10bca9,color:#ffffff
		playbook_f9a782fc --> |"1"| play_ed63c3e8
		linkStyle 0 stroke:#10bca9,color:#10bca9
			pre_task_a34928fc["[pre_task] Set profile config directory fact"]
			style pre_task_a34928fc stroke:#10bca9,fill:#ffffff
			play_ed63c3e8 --> |"1 "| pre_task_a34928fc
			linkStyle 1 stroke:#10bca9,color:#10bca9
			pre_task_eee3a387["[pre_task] Set distro name"]
			style pre_task_eee3a387 stroke:#10bca9,fill:#ffffff
			play_ed63c3e8 --> |"2 [when: distro is defined]"| pre_task_eee3a387
			linkStyle 2 stroke:#10bca9,color:#10bca9
			pre_task_571c0fde["[pre_task] Display ansible_distribution"]
			style pre_task_571c0fde stroke:#10bca9,fill:#ffffff
			play_ed63c3e8 --> |"3 "| pre_task_571c0fde
			linkStyle 3 stroke:#10bca9,color:#10bca9
			%% Start of the role '[role] base'
			play_ed63c3e8 --> |"4 "| role_54e63543
			linkStyle 4 stroke:#10bca9,color:#10bca9
			role_54e63543(["[role] base"])
			style role_54e63543 fill:#10bca9,color:#ffffff,stroke:#10bca9
				task_875ed8a5["base : Set pacman.conf config"]
				style task_875ed8a5 stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"1 "| task_875ed8a5
				linkStyle 5 stroke:#10bca9,color:#10bca9
				task_9b4439a8["base : Check pacman.conf contents"]
				style task_9b4439a8 stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"2 [when: ansible_architecture != 'aarch64']"| task_9b4439a8
				linkStyle 6 stroke:#10bca9,color:#10bca9
				task_e2c4ec26["base : Import archaudio repo key"]
				style task_e2c4ec26 stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"3 [when: ansible_architecture != 'aarch64']"| task_e2c4ec26
				linkStyle 7 stroke:#10bca9,color:#10bca9
				task_0f6fd5da["base : Add archaudio repository to pacman.conf"]
				style task_0f6fd5da stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"4 [when: ansible_architecture != 'aarch64' and '[proaudio]' not in pacman_conf_output.stdout]"| task_0f6fd5da
				linkStyle 8 stroke:#10bca9,color:#10bca9
				task_b340d3ee["base : Install chaotic-aur repo key"]
				style task_b340d3ee stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"5 [when: ansible_architecture != 'aarch64']"| task_b340d3ee
				linkStyle 9 stroke:#10bca9,color:#10bca9
				task_13b17c3c["base : Install chaotic keyring and mirrorlist"]
				style task_13b17c3c stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"6 [when: ansible_architecture != 'aarch64']"| task_13b17c3c
				linkStyle 10 stroke:#10bca9,color:#10bca9
				task_0b669766["base : Add repository to pacman.conf"]
				style task_0b669766 stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"7 [when: ansible_architecture != 'aarch64' and '[chaotic-aur]' not in pacman_conf_output.stdout]"| task_0b669766
				linkStyle 11 stroke:#10bca9,color:#10bca9
				task_2c4f69bc["base : Update cache"]
				style task_2c4f69bc stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"8 [when: ansible_architecture != 'aarch64']"| task_2c4f69bc
				linkStyle 12 stroke:#10bca9,color:#10bca9
				task_31898982["base : Check if paru installed"]
				style task_31898982 stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"9 [when: ansible_architecture != 'aarch64']"| task_31898982
				linkStyle 13 stroke:#10bca9,color:#10bca9
				%% Start of the block 'Install paru if not installed'
				block_17db4a79["[block] Install paru if not installed"]
				style block_17db4a79 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_54e63543 --> |"10 [when: ansible_architecture != 'aarch64' and not paru.stat.exists]"| block_17db4a79
				linkStyle 14 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_17db4a79["Install paru if not installed "]
					task_14cbe721["base : Install paru"]
					style task_14cbe721 stroke:#10bca9,fill:#ffffff
					block_17db4a79 --> |"1 [when: ansible_architecture != 'aarch64' and not paru.stat.exists]"| task_14cbe721
					linkStyle 15 stroke:#10bca9,color:#10bca9
					task_3e11a245["base : Adjust paru config"]
					style task_3e11a245 stroke:#10bca9,fill:#ffffff
					block_17db4a79 --> |"2 [when: ansible_architecture != 'aarch64']"| task_3e11a245
					linkStyle 16 stroke:#10bca9,color:#10bca9
				end
				%% End of the block 'Install paru if not installed'
				%% Start of the block ''
				block_7d6dbdfd["[block]"]
				style block_7d6dbdfd fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_54e63543 --> |"11 "| block_7d6dbdfd
				linkStyle 17 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_7d6dbdfd[" "]
					task_6619dd35["base : Install base packages"]
					style task_6619dd35 stroke:#10bca9,fill:#ffffff
					block_7d6dbdfd --> |"1 "| task_6619dd35
					linkStyle 18 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				task_d01c3985["base : Check if mirrors have been updated within the past 24h"]
				style task_d01c3985 stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"12 "| task_d01c3985
				linkStyle 19 stroke:#10bca9,color:#10bca9
				task_8d1936cd["base : Print mirror file status"]
				style task_8d1936cd stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"13 [when: ( mirror_status.stdout_lines | length < 0 or update_mirrors is defined ) and debugging is defined]"| task_8d1936cd
				linkStyle 20 stroke:#10bca9,color:#10bca9
				task_ca553d51["base : update mirrorlist"]
				style task_ca553d51 stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"14 [when: ( mirror_status.stdout_lines | length < 0 or update_mirrors is defined )]"| task_ca553d51
				linkStyle 21 stroke:#10bca9,color:#10bca9
				task_7b87fa7e["base : Set makepkg to use aria2"]
				style task_7b87fa7e stroke:#10bca9,fill:#ffffff
				role_54e63543 --> |"15 "| task_7b87fa7e
				linkStyle 22 stroke:#10bca9,color:#10bca9
				%% Start of the block ''
				block_618e68df["[block]"]
				style block_618e68df fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_54e63543 --> |"16 "| block_618e68df
				linkStyle 23 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_618e68df[" "]
					task_92d82264["base : Install mlocate"]
					style task_92d82264 stroke:#10bca9,fill:#ffffff
					block_618e68df --> |"1 "| task_92d82264
					linkStyle 24 stroke:#10bca9,color:#10bca9
					task_4fbe4802["base : Check if locate command is available"]
					style task_4fbe4802 stroke:#10bca9,fill:#ffffff
					block_618e68df --> |"2 "| task_4fbe4802
					linkStyle 25 stroke:#10bca9,color:#10bca9
					task_a50eb40d["base : Set locate_available variable"]
					style task_a50eb40d stroke:#10bca9,fill:#ffffff
					block_618e68df --> |"3 "| task_a50eb40d
					linkStyle 26 stroke:#10bca9,color:#10bca9
					%% Start of the block ''
					block_1c8d4def["[block]"]
					style block_1c8d4def fill:#10bca9,color:#ffffff,stroke:#10bca9
					block_618e68df --> |"4 [when: locate_available|bool]"| block_1c8d4def
					linkStyle 27 stroke:#10bca9,color:#10bca9
					subgraph subgraph_block_1c8d4def[" "]
						task_5becdc9c["base : Set directories to not be indexed"]
						style task_5becdc9c stroke:#10bca9,fill:#ffffff
						block_1c8d4def --> |"1 [when: locate_available|bool]"| task_5becdc9c
						linkStyle 28 stroke:#10bca9,color:#10bca9
						task_21181eb0["base : Run updatedb"]
						style task_21181eb0 stroke:#10bca9,fill:#ffffff
						block_1c8d4def --> |"2 [when: locate_available|bool and updatedb_conf.changed]"| task_21181eb0
						linkStyle 29 stroke:#10bca9,color:#10bca9
					end
					%% End of the block ''
				end
				%% End of the block ''
			%% End of the role '[role] base'
			%% Start of the role '[role] user'
			play_ed63c3e8 --> |"5 "| role_9697d384
			linkStyle 30 stroke:#10bca9,color:#10bca9
			role_9697d384(["[role] user"])
			style role_9697d384 fill:#10bca9,color:#ffffff,stroke:#10bca9
				%% Start of the block ''
				block_88243da8["[block]"]
				style block_88243da8 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_9697d384 --> |"1 [when: user.sudoers |default(false)]"| block_88243da8
				linkStyle 31 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_88243da8[" "]
					task_7dc27770["user : Ensure /etc/sudoers.d exists"]
					style task_7dc27770 stroke:#10bca9,fill:#ffffff
					block_88243da8 --> |"1 [when: user.sudoers |default(false)]"| task_7dc27770
					linkStyle 32 stroke:#10bca9,color:#10bca9
					task_85af38a7["user : Set NOPASSWD for user in sudoers"]
					style task_85af38a7 stroke:#10bca9,fill:#ffffff
					block_88243da8 --> |"2 [when: user.sudoers |default(false) and user.name != 'root']"| task_85af38a7
					linkStyle 33 stroke:#10bca9,color:#10bca9
					task_18b9ded1["user : Ensure rules.d directory exists"]
					style task_18b9ded1 stroke:#10bca9,fill:#ffffff
					block_88243da8 --> |"3 [when: user.sudoers |default(false)]"| task_18b9ded1
					linkStyle 34 stroke:#10bca9,color:#10bca9
					task_6023edf9["user : Set NOPASSWD for user in polkit"]
					style task_6023edf9 stroke:#10bca9,fill:#ffffff
					block_88243da8 --> |"4 [when: user.sudoers |default(false) and ansible_os_family == 'Archlinux']"| task_6023edf9
					linkStyle 35 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				%% Start of the block ''
				block_da450925["[block]"]
				style block_da450925 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_9697d384 --> |"2 "| block_da450925
				linkStyle 36 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_da450925[" "]
					task_af0c0e08["user : Install shell packages"]
					style task_af0c0e08 stroke:#10bca9,fill:#ffffff
					block_da450925 --> |"1 "| task_af0c0e08
					linkStyle 37 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				task_34ef45d9["user : Push aliases template"]
				style task_34ef45d9 stroke:#10bca9,fill:#ffffff
				role_9697d384 --> |"3 "| task_34ef45d9
				linkStyle 38 stroke:#10bca9,color:#10bca9
				task_1901b7ca["user : Ensure user is present with proper shell and groups"]
				style task_1901b7ca stroke:#10bca9,fill:#ffffff
				role_9697d384 --> |"4 "| task_1901b7ca
				linkStyle 39 stroke:#10bca9,color:#10bca9
				task_d2a2c0bc["user : Install fd and ripgrep ohmyzsh plugins"]
				style task_d2a2c0bc stroke:#10bca9,fill:#ffffff
				role_9697d384 --> |"5 "| task_d2a2c0bc
				linkStyle 40 stroke:#10bca9,color:#10bca9
				task_b822f6b9["user : Install zsh custom functions configs"]
				style task_b822f6b9 stroke:#10bca9,fill:#ffffff
				role_9697d384 --> |"6 "| task_b822f6b9
				linkStyle 41 stroke:#10bca9,color:#10bca9
				task_08d67ad7["user : Set zsh profile configs"]
				style task_08d67ad7 stroke:#10bca9,fill:#ffffff
				role_9697d384 --> |"7 "| task_08d67ad7
				linkStyle 42 stroke:#10bca9,color:#10bca9
				task_1955b4ad["user : Ensure ~/.local/bin exists"]
				style task_1955b4ad stroke:#10bca9,fill:#ffffff
				role_9697d384 --> |"8 "| task_1955b4ad
				linkStyle 43 stroke:#10bca9,color:#10bca9
				task_fc216d5a["user : Sync kitty configs plugins"]
				style task_fc216d5a stroke:#10bca9,fill:#ffffff
				role_9697d384 --> |"9 "| task_fc216d5a
				linkStyle 44 stroke:#10bca9,color:#10bca9
				task_a6d37513["user : Sync ranger configs plugins"]
				style task_a6d37513 stroke:#10bca9,fill:#ffffff
				role_9697d384 --> |"10 "| task_a6d37513
				linkStyle 45 stroke:#10bca9,color:#10bca9
			%% End of the role '[role] user'
			%% Start of the role '[role] docker'
			play_ed63c3e8 --> |"6 "| role_a7a2768d
			linkStyle 46 stroke:#10bca9,color:#10bca9
			role_a7a2768d(["[role] docker"])
			style role_a7a2768d fill:#10bca9,color:#ffffff,stroke:#10bca9
				task_6603e3c1["docker : Check if Docker is installed"]
				style task_6603e3c1 stroke:#10bca9,fill:#ffffff
				role_a7a2768d --> |"1 [when: use_docker | default(true) | bool]"| task_6603e3c1
				linkStyle 47 stroke:#10bca9,color:#10bca9
				task_30352a75["docker : Print Docker version if installed"]
				style task_30352a75 stroke:#10bca9,fill:#ffffff
				role_a7a2768d --> |"2 [when: use_docker | default(true) | bool and docker_check.rc == 0]"| task_30352a75
				linkStyle 48 stroke:#10bca9,color:#10bca9
				task_ced8240a["docker : Install docker package"]
				style task_ced8240a stroke:#10bca9,fill:#ffffff
				role_a7a2768d --> |"3 [when: use_docker | default(true) | bool]"| task_ced8240a
				linkStyle 49 stroke:#10bca9,color:#10bca9
				task_e52b2bd4["docker : Install docker nvidia packages"]
				style task_e52b2bd4 stroke:#10bca9,fill:#ffffff
				role_a7a2768d --> |"4 [when: use_docker | default(true) | bool and nvidia is defined]"| task_e52b2bd4
				linkStyle 50 stroke:#10bca9,color:#10bca9
				task_437fe4ef["docker : Ensure group &#34;docker&#34; exists"]
				style task_437fe4ef stroke:#10bca9,fill:#ffffff
				role_a7a2768d --> |"5 [when: use_docker | default(true) | bool]"| task_437fe4ef
				linkStyle 51 stroke:#10bca9,color:#10bca9
				task_7594eb29["docker : Add user to docker group"]
				style task_7594eb29 stroke:#10bca9,fill:#ffffff
				role_a7a2768d --> |"6 [when: use_docker | default(true) | bool]"| task_7594eb29
				linkStyle 52 stroke:#10bca9,color:#10bca9
				%% Start of the block ''
				block_1b6ffd53["[block]"]
				style block_1b6ffd53 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_a7a2768d --> |"7 [when: use_docker | default(true) | bool]"| block_1b6ffd53
				linkStyle 53 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_1b6ffd53[" "]
					task_897ae32e["docker : Create docker config directory"]
					style task_897ae32e stroke:#10bca9,fill:#ffffff
					block_1b6ffd53 --> |"1 [when: use_docker | default(true) | bool]"| task_897ae32e
					linkStyle 54 stroke:#10bca9,color:#10bca9
					task_4f14d140["docker : Ensure docker data directory exists"]
					style task_4f14d140 stroke:#10bca9,fill:#ffffff
					block_1b6ffd53 --> |"2 [when: use_docker | default(true) | bool]"| task_4f14d140
					linkStyle 55 stroke:#10bca9,color:#10bca9
					task_b816ebee["docker : Set docker storage location"]
					style task_b816ebee stroke:#10bca9,fill:#ffffff
					block_1b6ffd53 --> |"3 [when: use_docker | default(true) | bool]"| task_b816ebee
					linkStyle 56 stroke:#10bca9,color:#10bca9
					task_bc63d473["docker : Disable overlay redirect"]
					style task_bc63d473 stroke:#10bca9,fill:#ffffff
					block_1b6ffd53 --> |"4 [when: use_docker | default(true) | bool]"| task_bc63d473
					linkStyle 57 stroke:#10bca9,color:#10bca9
					task_fe0e6119["docker : Set docker service preset"]
					style task_fe0e6119 stroke:#10bca9,fill:#ffffff
					block_1b6ffd53 --> |"5 [when: use_docker | default(true) | bool]"| task_fe0e6119
					linkStyle 58 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
			%% End of the role '[role] docker'
			%% Start of the role '[role] libvirt'
			play_ed63c3e8 --> |"7 "| role_feb5d6aa
			linkStyle 59 stroke:#10bca9,color:#10bca9
			role_feb5d6aa(["[role] libvirt"])
			style role_feb5d6aa fill:#10bca9,color:#ffffff,stroke:#10bca9
				task_76e38a73["libvirt : Libvirt Tasks"]
				style task_76e38a73 stroke:#10bca9,fill:#ffffff
				role_feb5d6aa --> |"1 [when: use_libvirt | default(false) | bool]"| task_76e38a73
				linkStyle 60 stroke:#10bca9,color:#10bca9
				%% Start of the block ''
				block_0330652e["[block]"]
				style block_0330652e fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_feb5d6aa --> |"2 [when: use_libvirt | default(false) | bool]"| block_0330652e
				linkStyle 61 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_0330652e[" "]
					task_1a45ad0b["libvirt : Remove conflicting packages"]
					style task_1a45ad0b stroke:#10bca9,fill:#ffffff
					block_0330652e --> |"1 [when: use_libvirt | default(false) | bool]"| task_1a45ad0b
					linkStyle 62 stroke:#10bca9,color:#10bca9
					task_ec6577f6["libvirt : Install libvirt packages"]
					style task_ec6577f6 stroke:#10bca9,fill:#ffffff
					block_0330652e --> |"2 [when: use_libvirt | default(false) | bool]"| task_ec6577f6
					linkStyle 63 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				task_89181995["libvirt : Set socket group and perms to allow for remote access"]
				style task_89181995 stroke:#10bca9,fill:#ffffff
				role_feb5d6aa --> |"3 [when: use_libvirt | default(false) | bool]"| task_89181995
				linkStyle 64 stroke:#10bca9,color:#10bca9
				task_8b8231d2["libvirt : Disable lvmetad for remote access reasons"]
				style task_8b8231d2 stroke:#10bca9,fill:#ffffff
				role_feb5d6aa --> |"4 [when: use_libvirt | default(false) | bool]"| task_8b8231d2
				linkStyle 65 stroke:#10bca9,color:#10bca9
				task_ca12f409["libvirt : Add user to libvirt group"]
				style task_ca12f409 stroke:#10bca9,fill:#ffffff
				role_feb5d6aa --> |"5 [when: use_libvirt | default(false) | bool]"| task_ca12f409
				linkStyle 66 stroke:#10bca9,color:#10bca9
				task_b294be71["libvirt : set libvirtd service preset"]
				style task_b294be71 stroke:#10bca9,fill:#ffffff
				role_feb5d6aa --> |"6 [when: use_libvirt | default(false) | bool and libvirt.service == 'enabled']"| task_b294be71
				linkStyle 67 stroke:#10bca9,color:#10bca9
				%% Start of the block ''
				block_8ae5c5b5["[block]"]
				style block_8ae5c5b5 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_feb5d6aa --> |"7 [when: use_libvirt | default(false) | bool and use_vagrant|default(false)|bool == True]"| block_8ae5c5b5
				linkStyle 68 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_8ae5c5b5[" "]
					task_0088e167["libvirt : Install vagrant"]
					style task_0088e167 stroke:#10bca9,fill:#ffffff
					block_8ae5c5b5 --> |"1 [when: use_libvirt | default(false) | bool and use_vagrant|default(false)|bool == True]"| task_0088e167
					linkStyle 69 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
			%% End of the role '[role] libvirt'
			%% Start of the role '[role] x11'
			play_ed63c3e8 --> |"8 "| role_cbc2f209
			linkStyle 70 stroke:#10bca9,color:#10bca9
			role_cbc2f209(["[role] x11"])
			style role_cbc2f209 fill:#10bca9,color:#ffffff,stroke:#10bca9
				task_94f5fe9c["x11 : install xorg packages"]
				style task_94f5fe9c stroke:#10bca9,fill:#ffffff
				role_cbc2f209 --> |"1 "| task_94f5fe9c
				linkStyle 71 stroke:#10bca9,color:#10bca9
				%% Start of the block ''
				block_4aad5025["[block]"]
				style block_4aad5025 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_cbc2f209 --> |"2 "| block_4aad5025
				linkStyle 72 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_4aad5025[" "]
					task_d54bc35e["x11 : Disable vblank"]
					style task_d54bc35e stroke:#10bca9,fill:#ffffff
					block_4aad5025 --> |"1 [when: disable_vblank is defined]"| task_d54bc35e
					linkStyle 73 stroke:#10bca9,color:#10bca9
					task_e994e5da["x11 : Set xserver configs"]
					style task_e994e5da stroke:#10bca9,fill:#ffffff
					block_4aad5025 --> |"2 "| task_e994e5da
					linkStyle 74 stroke:#10bca9,color:#10bca9
					task_e35ef3d2["x11 : Set xinitrc config"]
					style task_e35ef3d2 stroke:#10bca9,fill:#ffffff
					block_4aad5025 --> |"3 "| task_e35ef3d2
					linkStyle 75 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
			%% End of the role '[role] x11'
			%% Start of the role '[role] sxhkd'
			play_ed63c3e8 --> |"9 "| role_dbab8513
			linkStyle 76 stroke:#10bca9,color:#10bca9
			role_dbab8513(["[role] sxhkd"])
			style role_dbab8513 fill:#10bca9,color:#ffffff,stroke:#10bca9
				%% Start of the block ''
				block_81dc0884["[block]"]
				style block_81dc0884 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_dbab8513 --> |"1 "| block_81dc0884
				linkStyle 77 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_81dc0884[" "]
					task_95a2c495["sxhkd : Install SXHKD on Arch Linux"]
					style task_95a2c495 stroke:#10bca9,fill:#ffffff
					block_81dc0884 --> |"1 "| task_95a2c495
					linkStyle 78 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				task_5da393e6["sxhkd : Install sxhkd reload function"]
				style task_5da393e6 stroke:#10bca9,fill:#ffffff
				role_dbab8513 --> |"2 "| task_5da393e6
				linkStyle 79 stroke:#10bca9,color:#10bca9
				task_cb2c7d03["sxhkd : Ensure SXHKD configuration directory exists"]
				style task_cb2c7d03 stroke:#10bca9,fill:#ffffff
				role_dbab8513 --> |"3 "| task_cb2c7d03
				linkStyle 80 stroke:#10bca9,color:#10bca9
				task_fa9621f1["sxhkd : Copy SXHKD configuration file"]
				style task_fa9621f1 stroke:#10bca9,fill:#ffffff
				role_dbab8513 --> |"4 "| task_fa9621f1
				linkStyle 81 stroke:#10bca9,color:#10bca9
			%% End of the role '[role] sxhkd'
			%% Start of the role '[role] rofi'
			play_ed63c3e8 --> |"10 "| role_3cf01757
			linkStyle 82 stroke:#10bca9,color:#10bca9
			role_3cf01757(["[role] rofi"])
			style role_3cf01757 fill:#10bca9,color:#ffffff,stroke:#10bca9
				%% Start of the block ''
				block_7d1e1263["[block]"]
				style block_7d1e1263 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_3cf01757 --> |"1 "| block_7d1e1263
				linkStyle 83 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_7d1e1263[" "]
					task_848bdbf7["rofi : Install rofi"]
					style task_848bdbf7 stroke:#10bca9,fill:#ffffff
					block_7d1e1263 --> |"1 "| task_848bdbf7
					linkStyle 84 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				task_729a605a["rofi : Ensure rofi directories exist"]
				style task_729a605a stroke:#10bca9,fill:#ffffff
				role_3cf01757 --> |"2 "| task_729a605a
				linkStyle 85 stroke:#10bca9,color:#10bca9
				task_81a201a1["rofi : Synchronize templates - rofi"]
				style task_81a201a1 stroke:#10bca9,fill:#ffffff
				role_3cf01757 --> |"3 "| task_81a201a1
				linkStyle 86 stroke:#10bca9,color:#10bca9
			%% End of the role '[role] rofi'
			%% Start of the role '[role] xdg'
			play_ed63c3e8 --> |"11 "| role_1a6e839b
			linkStyle 87 stroke:#10bca9,color:#10bca9
			role_1a6e839b(["[role] xdg"])
			style role_1a6e839b fill:#10bca9,color:#ffffff,stroke:#10bca9
				%% Start of the block ''
				block_8c64d6dd["[block]"]
				style block_8c64d6dd fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_1a6e839b --> |"1 "| block_8c64d6dd
				linkStyle 88 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_8c64d6dd[" "]
					task_1e24ccde["xdg : Install xdg packages"]
					style task_1e24ccde stroke:#10bca9,fill:#ffffff
					block_8c64d6dd --> |"1 "| task_1e24ccde
					linkStyle 89 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				%% Start of the block ''
				block_bb019c2a["[block]"]
				style block_bb019c2a fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_1a6e839b --> |"2 "| block_bb019c2a
				linkStyle 90 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_bb019c2a[" "]
					task_e3e63ec9["xdg : Ensure /etc/xdg exists"]
					style task_e3e63ec9 stroke:#10bca9,fill:#ffffff
					block_bb019c2a --> |"1 "| task_e3e63ec9
					linkStyle 91 stroke:#10bca9,color:#10bca9
					task_e110df61["xdg : Set XDG env vars"]
					style task_e110df61 stroke:#10bca9,fill:#ffffff
					block_bb019c2a --> |"2 "| task_e110df61
					linkStyle 92 stroke:#10bca9,color:#10bca9
					task_e30fa4bd["xdg : Create /etc/xdg/menus and /usr/share/desktop-entries"]
					style task_e30fa4bd stroke:#10bca9,fill:#ffffff
					block_bb019c2a --> |"3 "| task_e30fa4bd
					linkStyle 93 stroke:#10bca9,color:#10bca9
					task_50d19e5d["xdg : Set xdg user-dirs defaults"]
					style task_50d19e5d stroke:#10bca9,fill:#ffffff
					block_bb019c2a --> |"4 "| task_50d19e5d
					linkStyle 94 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				task_74caef1b["xdg : Enable xdg-user-dirs-update service"]
				style task_74caef1b stroke:#10bca9,fill:#ffffff
				role_1a6e839b --> |"3 "| task_74caef1b
				linkStyle 95 stroke:#10bca9,color:#10bca9
				task_ddcfd065["xdg : Remove existing user-dirs.dirs"]
				style task_ddcfd065 stroke:#10bca9,fill:#ffffff
				role_1a6e839b --> |"4 "| task_ddcfd065
				linkStyle 96 stroke:#10bca9,color:#10bca9
				task_19fde963["xdg : Run xdg-user-dirs-update"]
				style task_19fde963 stroke:#10bca9,fill:#ffffff
				role_1a6e839b --> |"5 [when: xdg_defaults.changed or xdg_userdirs.changed]"| task_19fde963
				linkStyle 97 stroke:#10bca9,color:#10bca9
				task_8a0adc97["xdg : Update desktop database"]
				style task_8a0adc97 stroke:#10bca9,fill:#ffffff
				role_1a6e839b --> |"6 "| task_8a0adc97
				linkStyle 98 stroke:#10bca9,color:#10bca9
			%% End of the role '[role] xdg'
			%% Start of the role '[role] i3'
			play_ed63c3e8 --> |"12 "| role_7eb52b9c
			linkStyle 99 stroke:#10bca9,color:#10bca9
			role_7eb52b9c(["[role] i3"])
			style role_7eb52b9c fill:#10bca9,color:#ffffff,stroke:#10bca9
				%% Start of the block ''
				block_4c61b1ab["[block]"]
				style block_4c61b1ab fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_7eb52b9c --> |"1 "| block_4c61b1ab
				linkStyle 100 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_4c61b1ab[" "]
					task_ae06c539["i3 : Install wm packages"]
					style task_ae06c539 stroke:#10bca9,fill:#ffffff
					block_4c61b1ab --> |"1 "| task_ae06c539
					linkStyle 101 stroke:#10bca9,color:#10bca9
					task_dd40c640["i3 : Ensure i3 directories exist"]
					style task_dd40c640 stroke:#10bca9,fill:#ffffff
					block_4c61b1ab --> |"2 "| task_dd40c640
					linkStyle 102 stroke:#10bca9,color:#10bca9
					task_d6405523["i3 : Set dmrc to selected window manager"]
					style task_d6405523 stroke:#10bca9,fill:#ffffff
					block_4c61b1ab --> |"3 "| task_d6405523
					linkStyle 103 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				%% Start of the block ''
				block_53b325e7["[block]"]
				style block_53b325e7 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_7eb52b9c --> |"2 "| block_53b325e7
				linkStyle 104 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_53b325e7[" "]
					task_238db22a["i3 : Set i3status-rs configuration"]
					style task_238db22a stroke:#10bca9,fill:#ffffff
					block_53b325e7 --> |"1 "| task_238db22a
					linkStyle 105 stroke:#10bca9,color:#10bca9
					task_a2add91d["i3 : Set i3 configuration"]
					style task_a2add91d stroke:#10bca9,fill:#ffffff
					block_53b325e7 --> |"2 "| task_a2add91d
					linkStyle 106 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
			%% End of the role '[role] i3'
			%% Start of the role '[role] homepage'
			play_ed63c3e8 --> |"13 "| role_73426c5e
			linkStyle 107 stroke:#10bca9,color:#10bca9
			role_73426c5e(["[role] homepage"])
			style role_73426c5e fill:#10bca9,color:#ffffff,stroke:#10bca9
				task_1c9296f5["homepage : Create homepage folder"]
				style task_1c9296f5 stroke:#10bca9,fill:#ffffff
				role_73426c5e --> |"1 "| task_1c9296f5
				linkStyle 108 stroke:#10bca9,color:#10bca9
				task_45706c25["homepage : sync folder"]
				style task_45706c25 stroke:#10bca9,fill:#ffffff
				role_73426c5e --> |"2 "| task_45706c25
				linkStyle 109 stroke:#10bca9,color:#10bca9
				task_3251b6e0["homepage : Set index.html template"]
				style task_3251b6e0 stroke:#10bca9,fill:#ffffff
				role_73426c5e --> |"3 "| task_3251b6e0
				linkStyle 110 stroke:#10bca9,color:#10bca9
			%% End of the role '[role] homepage'
			%% Start of the role '[role] ruby'
			play_ed63c3e8 --> |"14 "| role_b84ebaf4
			linkStyle 111 stroke:#10bca9,color:#10bca9
			role_b84ebaf4(["[role] ruby"])
			style role_b84ebaf4 fill:#10bca9,color:#ffffff,stroke:#10bca9
				task_b3777ca6["ruby : Load a variable file based on the OS type, or a default if not found."]
				style task_b3777ca6 stroke:#10bca9,fill:#ffffff
				role_b84ebaf4 --> |"1 "| task_b3777ca6
				linkStyle 112 stroke:#10bca9,color:#10bca9
				task_d3cdbf53["ruby : Load the main vars"]
				style task_d3cdbf53 stroke:#10bca9,fill:#ffffff
				role_b84ebaf4 --> |"2 "| task_d3cdbf53
				linkStyle 113 stroke:#10bca9,color:#10bca9
				task_a0332798["ruby : setup"]
				style task_a0332798 stroke:#10bca9,fill:#ffffff
				role_b84ebaf4 --> |"3 "| task_a0332798
				linkStyle 114 stroke:#10bca9,color:#10bca9
				task_3fc9209f["ruby : debug"]
				style task_3fc9209f stroke:#10bca9,fill:#ffffff
				role_b84ebaf4 --> |"4 "| task_3fc9209f
				linkStyle 115 stroke:#10bca9,color:#10bca9
				%% Start of the block ''
				block_e15572a4["[block]"]
				style block_e15572a4 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_b84ebaf4 --> |"5 "| block_e15572a4
				linkStyle 116 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_e15572a4[" "]
					task_fbfe1ba6["ruby : Set --no-user-install in /root/.gemrc"]
					style task_fbfe1ba6 stroke:#10bca9,fill:#ffffff
					block_e15572a4 --> |"1 "| task_fbfe1ba6
					linkStyle 117 stroke:#10bca9,color:#10bca9
					task_e75f4fc7["ruby : Set --user-install in /home/user/.gemrc"]
					style task_e75f4fc7 stroke:#10bca9,fill:#ffffff
					block_e15572a4 --> |"2 "| task_e75f4fc7
					linkStyle 118 stroke:#10bca9,color:#10bca9
					task_dfbaa541["ruby : Set --no-user-install in /etc/gemrc"]
					style task_dfbaa541 stroke:#10bca9,fill:#ffffff
					block_e15572a4 --> |"3 "| task_dfbaa541
					linkStyle 119 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				task_a10661a8["ruby : Install Ruby dev packages"]
				style task_a10661a8 stroke:#10bca9,fill:#ffffff
				role_b84ebaf4 --> |"6 "| task_a10661a8
				linkStyle 120 stroke:#10bca9,color:#10bca9
				%% Start of the block ''
				block_21ef7f10["[block]"]
				style block_21ef7f10 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_b84ebaf4 --> |"7 "| block_21ef7f10
				linkStyle 121 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_21ef7f10[" "]
					task_ed66cbb1["ruby : Update system bundler"]
					style task_ed66cbb1 stroke:#10bca9,fill:#ffffff
					block_21ef7f10 --> |"1 "| task_ed66cbb1
					linkStyle 122 stroke:#10bca9,color:#10bca9
					task_1415185d["ruby : Gather list of installed gems"]
					style task_1415185d stroke:#10bca9,fill:#ffffff
					block_21ef7f10 --> |"2 "| task_1415185d
					linkStyle 123 stroke:#10bca9,color:#10bca9
					task_692526fb["ruby : Set list of gems to install"]
					style task_692526fb stroke:#10bca9,fill:#ffffff
					block_21ef7f10 --> |"3 "| task_692526fb
					linkStyle 124 stroke:#10bca9,color:#10bca9
					task_7b050e95["ruby : Install system Ruby gems"]
					style task_7b050e95 stroke:#10bca9,fill:#ffffff
					block_21ef7f10 --> |"4 [when: ruby__gems | length > 0]"| task_7b050e95
					linkStyle 125 stroke:#10bca9,color:#10bca9
				end
				%% End of the block ''
				%% Start of the block ''
				block_b09b9a82["[block]"]
				style block_b09b9a82 fill:#10bca9,color:#ffffff,stroke:#10bca9
				role_b84ebaf4 --> |"8 [when: rvm_install|default(false)|bool == True]"| block_b09b9a82
				linkStyle 126 stroke:#10bca9,color:#10bca9
				subgraph subgraph_block_b09b9a82[" "]
					task_337b4293["ruby : Detect rvm binary"]
					style task_337b4293 stroke:#10bca9,fill:#ffffff
					block_b09b9a82 --> |"1 [when: rvm_install|default(false)|bool == True]"| task_337b4293
					linkStyle 127 stroke:#10bca9,color:#10bca9
					task_05ab08f8["ruby : Detect rvm installer"]
					style task_05ab08f8 stroke:#10bca9,fill:#ffffff
					block_b09b9a82 --> |"2 [when: rvm_install|default(false)|bool == True]"| task_05ab08f8
					linkStyle 128 stroke:#10bca9,color:#10bca9
					task_77b8a7a9["ruby : Detect current rvm version"]
					style task_77b8a7a9 stroke:#10bca9,fill:#ffffff
					block_b09b9a82 --> |"3 [when: rvm_install|default(false)|bool == True and rvm_binary.stat.exists]"| task_77b8a7a9
					linkStyle 129 stroke:#10bca9,color:#10bca9
					task_47dea611["ruby : Install rvm installer"]
					style task_47dea611 stroke:#10bca9,fill:#ffffff
					block_b09b9a82 --> |"4 [when: rvm_install|default(false)|bool == True and not rvm_installer.stat.exists]"| task_47dea611
					linkStyle 130 stroke:#10bca9,color:#10bca9
					%% Start of the block ''
					block_6d074e8a["[block]"]
					style block_6d074e8a fill:#10bca9,color:#ffffff,stroke:#10bca9
					block_b09b9a82 --> |"5 [when: rvm_install|default(false)|bool == True and not rvm_binary.stat.exists]"| block_6d074e8a
					linkStyle 131 stroke:#10bca9,color:#10bca9
					subgraph subgraph_block_6d074e8a[" "]
						task_812fdc5e["ruby : Import GPG keys from keyservers"]
						style task_812fdc5e stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"1 [when: rvm_install|default(false)|bool == True and not rvm_binary.stat.exists]"| task_812fdc5e
						linkStyle 132 stroke:#10bca9,color:#10bca9
						task_5860a906["ruby : Install rvm"]
						style task_5860a906 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"2 [when: rvm_install|default(false)|bool == True and not rvm_binary.stat.exists]"| task_5860a906
						linkStyle 133 stroke:#10bca9,color:#10bca9
						task_6ea58809["ruby : Update rvm"]
						style task_6ea58809 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"3 [when: rvm_install|default(false)|bool == True and rvm_binary.stat.exists and rvm1_rvm_check_for_updates]"| task_6ea58809
						linkStyle 134 stroke:#10bca9,color:#10bca9
						task_3fecf321["ruby : Configure rvm"]
						style task_3fecf321 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"4 [when: rvm_install|default(false)|bool == True and not rvm_binary.stat.exists]"| task_3fecf321
						linkStyle 135 stroke:#10bca9,color:#10bca9
						task_81f70bf7["ruby : Detect rvm openssl"]
						style task_81f70bf7 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"5 [when: rvm_install|default(false)|bool == True]"| task_81f70bf7
						linkStyle 136 stroke:#10bca9,color:#10bca9
						task_8ee22922["ruby : Install openssl"]
						style task_8ee22922 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"6 [when: rvm_install|default(false)|bool == True and not rvm_openssl.stat.exists]"| task_8ee22922
						linkStyle 137 stroke:#10bca9,color:#10bca9
						task_c40db006["ruby : Detect rubies"]
						style task_c40db006 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"7 [when: rvm_install|default(false)|bool == True]"| task_c40db006
						linkStyle 138 stroke:#10bca9,color:#10bca9
						task_6ff1ff82["ruby : Install 3.2.4"]
						style task_6ff1ff82 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"8 [when: rvm_install|default(false)|bool == True]"| task_6ff1ff82
						linkStyle 139 stroke:#10bca9,color:#10bca9
						task_8e6b9b39["ruby : Detect default ruby version"]
						style task_8e6b9b39 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"9 [when: rvm_install|default(false)|bool == True]"| task_8e6b9b39
						linkStyle 140 stroke:#10bca9,color:#10bca9
						task_1f0589a2["ruby : Select default ruby"]
						style task_1f0589a2 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"10 [when: rvm_install|default(false)|bool == True and detect_default_ruby_version.stdout|default() == '' or rvm1_default_ruby_version not in detect_default_ruby_version.stdout]"| task_1f0589a2
						linkStyle 141 stroke:#10bca9,color:#10bca9
						task_8e214e54["ruby : Detect installed ruby patch number"]
						style task_8e214e54 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"11 [when: rvm_install|default(false)|bool == True]"| task_8e214e54
						linkStyle 142 stroke:#10bca9,color:#10bca9
						task_3b7c2117["ruby : Install bundler if not installed"]
						style task_3b7c2117 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"12 [when: rvm_install|default(false)|bool == True and rvm1_bundler_install]"| task_3b7c2117
						linkStyle 143 stroke:#10bca9,color:#10bca9
						task_994fdfba["ruby : Symlink ruby related binaries on the system path"]
						style task_994fdfba stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"13 [when: rvm_install|default(false)|bool == True and not '--user-install' in rvm1_install_flags and rvm1_symlink]"| task_994fdfba
						linkStyle 144 stroke:#10bca9,color:#10bca9
						task_19dddab4["ruby : Symlink bundler binaries on the system path"]
						style task_19dddab4 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"14 [when: rvm_install|default(false)|bool == True and not '--user-install' in rvm1_install_flags and rvm1_bundler_install and rvm1_symlink]"| task_19dddab4
						linkStyle 145 stroke:#10bca9,color:#10bca9
						task_b7255ac7["ruby : Delete ruby if relevant"]
						style task_b7255ac7 stroke:#10bca9,fill:#ffffff
						block_6d074e8a --> |"15 [when: rvm_install|default(false)|bool == True and rvm1_delete_ruby is defined and rvm1_delete_ruby]"| task_b7255ac7
						linkStyle 146 stroke:#10bca9,color:#10bca9
					end
					%% End of the block ''
				end
				%% End of the block ''
			%% End of the role '[role] ruby'
		%% End of the play 'play #1 (workstation): 3'
		%% Start of the play 'play #2 (workstation): 3'
		play_25b4c236["play #2 (workstation): 3"]
		style play_25b4c236 stroke:#7b04c8,fill:#7b04c8,color:#ffffff
		playbook_f9a782fc --> |"2"| play_25b4c236
		linkStyle 147 stroke:#7b04c8,color:#7b04c8
			%% Start of the block ''
			block_678d9304["[block]"]
			style block_678d9304 fill:#7b04c8,color:#ffffff,stroke:#7b04c8
			play_25b4c236 --> |"1 "| block_678d9304
			linkStyle 148 stroke:#7b04c8,color:#7b04c8
			subgraph subgraph_block_678d9304[" "]
				task_a0a978f0["[task] Install dependencies"]
				style task_a0a978f0 stroke:#7b04c8,fill:#ffffff
				block_678d9304 --> |"1 "| task_a0a978f0
				linkStyle 149 stroke:#7b04c8,color:#7b04c8
			end
			%% End of the block ''
			task_ce4b1fc6["[task] Clone code-packager repository"]
			style task_ce4b1fc6 stroke:#7b04c8,fill:#ffffff
			play_25b4c236 --> |"2 "| task_ce4b1fc6
			linkStyle 150 stroke:#7b04c8,color:#7b04c8
			task_3c331774["[task] Move code-packager file to ~/.local/bin"]
			style task_3c331774 stroke:#7b04c8,fill:#ffffff
			play_25b4c236 --> |"3 "| task_3c331774
			linkStyle 151 stroke:#7b04c8,color:#7b04c8
			task_746e638b["[task] Remove temp folder"]
			style task_746e638b stroke:#7b04c8,fill:#ffffff
			play_25b4c236 --> |"4 "| task_746e638b
			linkStyle 152 stroke:#7b04c8,color:#7b04c8
		%% End of the play 'play #2 (workstation): 3'
		%% Start of the play 'play #3 (all): 5'
		play_95ee3f07["play #3 (all): 5"]
		style play_95ee3f07 stroke:#575f75,fill:#575f75,color:#ffffff
		playbook_f9a782fc --> |"3"| play_95ee3f07
		linkStyle 153 stroke:#575f75,color:#575f75
			%% Start of the block ''
			block_056a8b63["[block]"]
			style block_056a8b63 fill:#575f75,color:#ffffff,stroke:#575f75
			play_95ee3f07 --> |"1 "| block_056a8b63
			linkStyle 154 stroke:#575f75,color:#575f75
			subgraph subgraph_block_056a8b63[" "]
				task_38688b83["[task] Install dependencies"]
				style task_38688b83 stroke:#575f75,fill:#ffffff
				block_056a8b63 --> |"1 "| task_38688b83
				linkStyle 155 stroke:#575f75,color:#575f75
			end
			%% End of the block ''
			task_c9d3c04a["[task] Clone whisper-stream repository"]
			style task_c9d3c04a stroke:#575f75,fill:#ffffff
			play_95ee3f07 --> |"2 "| task_c9d3c04a
			linkStyle 156 stroke:#575f75,color:#575f75
			task_70dc756c["[task] Move whisper-stream file to ~/.local/bin"]
			style task_70dc756c stroke:#575f75,fill:#ffffff
			play_95ee3f07 --> |"3 "| task_70dc756c
			linkStyle 157 stroke:#575f75,color:#575f75
			task_cc749eb8["[task] Remove temp folder"]
			style task_cc749eb8 stroke:#575f75,fill:#ffffff
			play_95ee3f07 --> |"4 "| task_cc749eb8
			linkStyle 158 stroke:#575f75,color:#575f75
		%% End of the play 'play #3 (all): 5'
		%% Start of the play 'play #4 (all): 5'
		play_c734e4b1["play #4 (all): 5"]
		style play_c734e4b1 stroke:#7ab11b,fill:#7ab11b,color:#ffffff
		playbook_f9a782fc --> |"4"| play_c734e4b1
		linkStyle 159 stroke:#7ab11b,color:#7ab11b
			%% Start of the block ''
			block_5b2b2239["[block]"]
			style block_5b2b2239 fill:#7ab11b,color:#ffffff,stroke:#7ab11b
			play_c734e4b1 --> |"1 "| block_5b2b2239
			linkStyle 160 stroke:#7ab11b,color:#7ab11b
			subgraph subgraph_block_5b2b2239[" "]
				task_88b2fa00["[task] Install input-remapper"]
				style task_88b2fa00 stroke:#7ab11b,fill:#ffffff
				block_5b2b2239 --> |"1 "| task_88b2fa00
				linkStyle 161 stroke:#7ab11b,color:#7ab11b
			end
			%% End of the block ''
			%% Start of the block 'Ensure input-remapper preset synchronization'
			block_29ff0c68["[block] Ensure input-remapper preset synchronization"]
			style block_29ff0c68 fill:#7ab11b,color:#ffffff,stroke:#7ab11b
			play_c734e4b1 --> |"2 "| block_29ff0c68
			linkStyle 162 stroke:#7ab11b,color:#7ab11b
			subgraph subgraph_block_29ff0c68["Ensure input-remapper preset synchronization "]
				task_09fefe61["[task] Ensure destination directory exists"]
				style task_09fefe61 stroke:#7ab11b,fill:#ffffff
				block_29ff0c68 --> |"1 "| task_09fefe61
				linkStyle 163 stroke:#7ab11b,color:#7ab11b
				task_16120b4a["[task] Sync input-remapper presets folder"]
				style task_16120b4a stroke:#7ab11b,fill:#ffffff
				block_29ff0c68 --> |"2 "| task_16120b4a
				linkStyle 164 stroke:#7ab11b,color:#7ab11b
			end
			%% End of the block 'Ensure input-remapper preset synchronization'
			task_39f25432["[task] Enable input-remapper service"]
			style task_39f25432 stroke:#7ab11b,fill:#ffffff
			play_c734e4b1 --> |"3 "| task_39f25432
			linkStyle 165 stroke:#7ab11b,color:#7ab11b
		%% End of the play 'play #4 (all): 5'
	%% End of the playbook 'playbooks/workstation.yml'
```

## Contributing

Contributions are welcome!  Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes, ensuring that your code adheres to Ansible best practices.
4.  Write tests for your changes (if applicable).
5.  Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE) (or choose another appropriate license).

## Troubleshooting

*   **SSH Connectivity Issues:** Ensure that you can SSH into the target host(s) using the specified user and credentials.
*   **Package Installation Errors:** Check the Ansible output for specific error messages.  Make sure your target host has a working internet connection and that the configured repositories are accessible.
*   **Idempotency Problems:** If the playbook makes unintended changes on subsequent runs, review the `when` conditions and registered variables to ensure they are correctly checking for existing configurations.
* **Use the `--check` flag**: If you are unsure about the results, use the dry run mode.
