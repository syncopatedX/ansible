# Ansible Role - gnfzdz.network.systemd_resolved

Configure/enable systemd-resolved and improve compatability with resolve-conf

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`network_systemd_resolved_config` | Ansible managed configuration for systemd-resolved. See `man 5 resolved.conf` for all available options. | dict | ```json { 'Resolve': { 'DNS': "1.1.1.1#cloudflare-dns.com 1.0.0.1#cloudflare-dns.com 2606:4700:4700::1111#cloudflare-dns.com 2606:4700:4700::1001#cloudflare-dns.com", 'Domains': "~.", 'DNSSEC': true, 'DNSOverTLS': true } } ```
`network_systemd_resolved_enabled` | Flag deteterming whether the systemd-resolved service should be started and enabled | bool | True
`network_systemd_resolved_packages` | A list of packages to install for Systemd Resolved support | list of str | A distribution specific list of packages
