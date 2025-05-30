#!/usr/bin/env python3
import json
import socket
import subprocess
import sys
import re
import os
import configparser
from pathlib import Path

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

# Default configuration
DEFAULT_CONFIG = {
    # Control whether to perform subnet scanning (set to False to disable)
    "ENABLE_SUBNET_SCAN": True,
    
    # Whitelist for IP addresses to include from subnet scan (regex patterns)
    # Only IPs matching these patterns will be included
    "IP_WHITELIST": [
        r"^192\.168\.41\.(2|3|4|10|29|30|31)$"  # Only specific IPs we know are Ansible-managed (excluding router at .1)
    ]
}

# Load configuration from file if it exists
def load_config():
    """Load configuration from config file or use defaults"""
    config = DEFAULT_CONFIG.copy()
    
    config_file = Path(__file__).parent / "dynamic_inventory.cfg"
    if config_file.exists():
        debug_print(f"Loading config from {config_file}")
        parser = configparser.ConfigParser()
        parser.read(config_file)
        
        if "inventory" in parser:
            section = parser["inventory"]
            
            if "enable_subnet_scan" in section:
                config["ENABLE_SUBNET_SCAN"] = section.getboolean("enable_subnet_scan")
                
            if "ip_whitelist" in section:
                # Split the comma-separated list of patterns
                patterns = [p.strip() for p in section["ip_whitelist"].split(",")]
                config["IP_WHITELIST"] = patterns
    
    return config

# Get configuration
CONFIG = load_config()
ENABLE_SUBNET_SCAN = CONFIG["ENABLE_SUBNET_SCAN"]
IP_WHITELIST = CONFIG["IP_WHITELIST"]

# Debug mode - set to True for more verbose output
DEBUG = os.environ.get("ANSIBLE_INVENTORY_DEBUG", "false").lower() == "true"

def debug_print(message):
    """Print debug messages if DEBUG is enabled"""
    if DEBUG:
        sys.stderr.write(f"DEBUG: {message}\n")


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
    Returns a list of IP addresses that match the whitelist.
    """
    if not ENABLE_SUBNET_SCAN:
        debug_print("Subnet scanning is disabled")
        return []
        
    try:
        debug_print(f"Scanning subnet {subnet}")
        result = subprocess.run(
            ["nmap", "-sn", subnet], capture_output=True, text=True, check=True
        )
        
        up_hosts = []
        for line in result.stdout.splitlines():
            if line.startswith("Nmap scan report for"):
                parts = line.split()
                ip = parts[-1].strip("()")
                
                # Check if the IP matches any of our whitelist patterns
                if IP_WHITELIST and not any(re.match(pattern, ip) for pattern in IP_WHITELIST):
                    debug_print(f"Skipping non-whitelisted IP: {ip}")
                    continue
                    
                debug_print(f"Found whitelisted host: {ip}")
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
    debug_print(f"Resolving static hosts: {STATIC_HOSTS}")
    mdns_hosts = resolve_mdns_hosts(STATIC_HOSTS)
    
    debug_print(f"Successfully resolved hosts: {list(mdns_hosts.keys())}")
    for hostname, host_vars in mdns_hosts.items():
        ip = host_vars["ansible_host"]
        discovered_ips[ip] = hostname
        inventory["all"]["hosts"].append(hostname)
        inventory["_meta"]["hostvars"][hostname] = host_vars
    
    # Add dynamically scanned hosts if enabled
    if ENABLE_SUBNET_SCAN:
        debug_print(f"Performing subnet scan on {SUBNET}")
        scanned_ips = scan_subnet_for_up_hosts(SUBNET)
        debug_print(f"Found {len(scanned_ips)} hosts in subnet scan")
        
        for ip in scanned_ips:
            # If this IP is already associated with a hostname, skip it
            if ip in discovered_ips:
                debug_print(f"Skipping already discovered IP: {ip} (hostname: {discovered_ips[ip]})")
                continue
                
            # Otherwise, use the IP as the hostname
            hostname = ip
            debug_print(f"Adding IP-based host: {hostname}")
            inventory["all"]["hosts"].append(hostname)
            inventory["_meta"]["hostvars"][hostname] = {
                "ansible_host": ip,
                "ansible_user": "b08x",
                "ansible_connection": "ssh"
            }
    else:
        debug_print("Subnet scanning disabled, skipping")
    
    debug_print(f"Final inventory contains {len(inventory['all']['hosts'])} hosts")
    return inventory


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        # Enable debug mode with environment variable
        # ANSIBLE_INVENTORY_DEBUG=true ./inventory/dynamic_inventory.py --list
        if DEBUG:
            sys.stderr.write("Running in DEBUG mode\n")
            sys.stderr.write(f"Subnet scanning: {'enabled' if ENABLE_SUBNET_SCAN else 'disabled'}\n")
            if ENABLE_SUBNET_SCAN:
                sys.stderr.write(f"IP whitelist patterns: {IP_WHITELIST}\n")
            
        print(json.dumps(build_inventory(), indent=2))
    elif len(sys.argv) == 2 and sys.argv[1] == "--host":
        # Required for compatibility, even if unused
        print(json.dumps({}, indent=2))
    elif len(sys.argv) == 2 and sys.argv[1] == "--config":
        # Generate a sample config file
        print("""[inventory]
# Enable or disable subnet scanning (true/false)
enable_subnet_scan = true

# Comma-separated list of IP regex patterns to include
# Exclude the router at 192.168.41.1
ip_whitelist = ^192\\.168\\.41\\.(2|3|4|10|29|30|31)$
""")
    else:
        sys.stderr.write("Usage: dynamic_inventory.py --list or --host <hostname> or --config\n")
        sys.exit(1)

