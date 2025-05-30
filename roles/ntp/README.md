# Ansible Role: NTP Configuration using systemd-timesyncd

## Role Name

`ntp` (or your chosen role name)

## Description

This Ansible role configures Network Time Protocol (NTP) on target systems using `systemd-timesyncd`. It ensures that the system's time is synchronized with reliable NTP servers. The role is designed to be simple and focuses on leveraging the native `systemd-timesyncd` service present in most modern systemd-based Linux distributions.

## Requirements

- **Target System:** Must be a Linux distribution using `systemd`.

- **`systemd-timesyncd` service:** The role checks for the existence of `/usr/lib/systemd/system/systemd-timesyncd.service`. If this service is not available, the role will not apply NTP configuration.

- **Root/Sudo Privileges:** The role requires privileges to install packages, configure services, and update system files.

## Role Variables

This role primarily relies on a configuration file that you provide within the role's structure, rather than Ansible variables in `defaults/main.yml` or `vars/main.yml` for server lists.

- **`ntp_servers` (Implicit via `local.conf`):**

  - While not an explicit Ansible variable, the list of NTP servers is defined in a file you must create: `YOUR_ROLE_PATH/files/etc/systemd/timesyncd.conf.d/local.conf`.

  - This file will be copied to `/etc/systemd/timesyncd.conf.d/local.conf` on the target machine.

  - **Default:** The role does not come with a pre-defined list of servers in this file. You _must_ create this file and populate it.

### Example `files/etc/systemd/timesyncd.conf.d/local.conf`

Create this file structure within your role:

```shell
your_ansible_project/
├── roles/
│   └── your_ntp_role_name/
│       ├── files/
│       │   └── etc/
│       │       └── systemd/
│       │           └── timesyncd.conf.d/
│       │               └── local.conf  <-- CREATE THIS FILE
│       ├── tasks/
│       │   └── main.yml
│       ├── handlers/
│       │   └── main.yml
│       ├── defaults/
│       │   └── main.yml
│       └── meta/
│           └── main.yml
└── playbook.yml
```

The content of `local.conf` should follow the `timesyncd.conf` format. For example:

```yaml
[Time]
NTP=0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org 3.pool.ntp.org
FallbackNTP=0.debian.pool.ntp.org 1.debian.pool.ntp.org 2.debian.pool.ntp.org 3.debian.pool.ntp.org
#RootDistanceMaxSec=5
#PollIntervalMinSec=32
#PollIntervalMaxSec=2048
```

Refer to the `timesyncd.conf(5)` man page for all available options.

## How it Works

The role performs the following actions as defined in `tasks/main.yml`:

1. **Checks for `systemd-timesyncd.service`:** Verifies if the `systemd-timesyncd` service unit file exists.

2. **Creates Configuration Directory:** If the service exists, it ensures the directory `/etc/systemd/timesyncd.conf.d` is present.

3. **Copies `local.conf`:**

    - Copies the user-provided `files/etc/systemd/timesyncd.conf.d/local.conf` from the role's directory to `/etc/systemd/timesyncd.conf.d/local.conf` on the target host.

    - This action notifies the handler to restart `systemd-timesyncd` if the file changes.

    - A backup of any existing `local.conf` on the target will be made.

4. **Synchronizes Hardware Clock:**

    - If the `local.conf` was changed and the distribution is _not_ Debian, it runs `timedatectl set-ntp true` and then `hwclock --systohc` after a short delay. This enables NTP synchronization via `timedatectl` and writes the system time to the hardware clock.

    - Debian systems often handle `hwclock` synchronization differently or it's managed by other mechanisms, hence the exclusion.

## Handlers

As defined in `handlers/main.yml`:

- **`Enable systemd-timesyncd Service`**:

  - This handler is triggered if the `local.conf` file is changed by the role.

  - It ensures the `systemd-timesyncd` service is enabled (to start on boot) and restarts it to apply the new configuration.

## Dependencies

This role has no external dependencies on other Ansible Galaxy roles, as per `meta/main.yml`.

## Example Playbook

Here's an example of how to use this role in a playbook:

```yaml
---
- hosts: all
  become: yes
  roles:
    - your_ntp_role_name # Replace with the actual name of this role directory
```

Ensure you have created the `files/etc/systemd/timesyncd.conf.d/local.conf` file within your role directory with your desired NTP server configuration.

## Configuring for Lowest Latency

To achieve the lowest possible latency with `systemd-timesyncd`:

1. **Choose Geographically Close and Reliable Servers:**

    - The most critical factor is selecting NTP servers that are geographically close to your machines and have low network latency.

    - Public NTP pool projects like `pool.ntp.org` (e.g., `0.country_code.pool.ntp.org`, `1.continent.pool.ntp.org`) are good starting points. They use DNS to return servers close to you.

    - If you have internal NTP servers, prioritize them.

    - You can also use vendor-specific NTP servers if available (e.g., Google's `time.google.com`, Cloudflare's `time.cloudflare.com`).

2. **Populate** `local.conf` with Optimal **Servers:**

    - Edit `YOUR_ROLE_PATH/files/etc/systemd/timesyncd.conf.d/local.conf`.

    - List multiple servers. `systemd-timesyncd` will automatically select the best ones. Four to seven servers are generally recommended.

    Example `local.conf` for potentially lower latency (using a mix of pool and specific servers):

    ```yaml
    [Time]
    NTP=time.google.com time.cloudflare.com 0.us.pool.ntp.org 1.us.pool.ntp.org
    FallbackNTP=0.pool.ntp.org 1.pool.ntp.org
    ```

    _(Adjust_ server FQDNs based _on your location and preferences)_

3. **`systemd-timesyncd` Behavior:**

    - `systemd-timesyncd` is a simpler NTP client compared to `ntpd` or `chrony`. It does not offer the same extensive set of fine-tuning options (like `iburst` in `ntpd`/`chrony`, though `timesyncd` attempts rapid synchronization initially).

    - It periodically queries servers and adjusts the local clock. The frequency of polling can be adjusted with `PollIntervalMinSec` and `PollIntervalMaxSec` in `timesyncd.conf` if needed, but default values are usually sufficient. Lowering `PollIntervalMinSec` aggressively can put unnecessary load on NTP servers.

    - `RootDistanceMaxSec`: Can be used to instruct `timesyncd` to ignore servers whose synchronized time is too far from the local clock, but this is more for correctness than pure latency.

4. **Network Stability:**

    - Ensure stable network connectivity between your servers and the chosen NTP servers. High packet loss or jitter will degrade time synchronization quality regardless of the chosen servers.

5. **Hardware Clock Sync:**

    - The role includes a task to sync the system time to the hardware clock (`hwclock --systohc`) after NTP configuration changes (except on Debian). This ensures the hardware clock is also accurate, which is important for maintaining time across reboots, especially if the system starts without network connectivity.

By focusing on selecting good quality, low-latency NTP servers in your `local.conf`, you will achieve the best possible time synchronization with `systemd-timesyncd`.

## License

Specify your chosen license (e.g., BSD, MIT, GPL-2.0-or-later). The template in `meta/main.yml` suggests some options.

## Author Information

An optional section for the role authors to include contact information or a website.
