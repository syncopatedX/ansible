#!/usr/bin/env python3
import json
import socket
import subprocess
import sys

# Static hostnames that should always be attempted (with .local mDNS support)
STATIC_HOSTS = [
    "soundbot",
    "lapbot",
    "ninjabot",
    "crambot",
    "steve"
]

# Optional subnet to scan for fallback discovery (e.g., if mDNS fails)
SUBNET = "192.168.41.0/24"


def resolve_mdns_hosts(hosts):
    """
    Attempt to resolve hostnames to IP addresses using mDNS.
    Returns a dictionary of hostname -> host variables.
    """
    inventory_hosts = {}
    for host in hosts:
        try:
            # Try to resolve with .local suffix first
            try:
                ip = socket.gethostbyname(f"{host}.local")
            except socket.gaierror:
                # Fall back to no suffix
                ip = socket.gethostbyname(host)
                
            inventory_hosts[host] = {
                "ansible_host": ip,
                "ansible_user": "b08x",
                "ansible_connection": "ssh"
            }
        except Exception as e:
            # More detailed error logging
            sys.stderr.write(f"Failed to resolve host {host}: {str(e)}\n")
            continue  # mDNS resolution failed
    return inventory_hosts


def scan_subnet_for_up_hosts(subnet):
    """
    Scan a subnet for hosts that respond to ping.
    Returns a list of IP addresses.
    """
    try:
        result = subprocess.run(
            ["nmap", "-sn", subnet], capture_output=True, text=True, check=True
        )
        up_hosts = []
        for line in result.stdout.splitlines():
            if line.startswith("Nmap scan report for"):
                parts = line.split()
                ip = parts[-1].strip("()")
                up_hosts.append(ip)
        return up_hosts
    except Exception as e:
        sys.stderr.write(f"Failed to scan subnet {subnet}: {str(e)}\n")
        return []


def build_inventory():
    """
    Build the inventory structure according to Ansible's expected format.
    """
    inventory = {
        "all": {
            "hosts": [],
            "vars": {}
        },
        "_meta": {
            "hostvars": {}
        }
    }
    
    # Track hosts by IP to avoid duplicates
    discovered_ips = {}
    
    # Add statically declared mDNS hosts
    mdns_hosts = resolve_mdns_hosts(STATIC_HOSTS)
    for hostname, host_vars in mdns_hosts.items():
        ip = host_vars["ansible_host"]
        discovered_ips[ip] = hostname
        inventory["all"]["hosts"].append(hostname)
        inventory["_meta"]["hostvars"][hostname] = host_vars
    
    # Add dynamically scanned hosts
    scanned_ips = scan_subnet_for_up_hosts(SUBNET)
    for ip in scanned_ips:
        # If this IP is already associated with a hostname, skip it
        if ip in discovered_ips:
            continue
            
        # Otherwise, use the IP as the hostname
        hostname = ip
        inventory["all"]["hosts"].append(hostname)
        inventory["_meta"]["hostvars"][hostname] = {
            "ansible_host": ip,
            "ansible_user": "b08x",
            "ansible_connection": "ssh"
        }
    
    return inventory


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(json.dumps(build_inventory(), indent=2))
    elif len(sys.argv) == 2 and sys.argv[1] == "--host":
        # Required for compatibility, even if unused
        print(json.dumps({}, indent=2))
    else:
        sys.stderr.write("Usage: dynamic_inventory.py --list or --host <hostname>\n")
        sys.exit(1)

