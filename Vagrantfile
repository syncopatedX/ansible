# -*- mode: ruby -*-
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'

# Configuration variables
ROCKY_HOSTNAME = "rocky-test.syncopated.dev"
ARCH_HOSTNAME = "arch-test.syncopated.dev"

Vagrant.configure("2") do |config|
  # Global SSH configuration
  config.ssh.insert_key = false
  config.ssh.forward_agent = true

  # Rocky Linux 9 VM for testing
  config.vm.define "rocky", primary: true do |rocky|
    rocky.vm.box = "rockylinux/9"
    rocky.vm.hostname = ROCKY_HOSTNAME
    
    rocky.vm.network :private_network,
      ip: "192.168.122.10",
      libvirt__network_name: "default"

    rocky.vm.provider :libvirt do |libvirt|
      libvirt.memory = 2048
      libvirt.cpus = 2
      libvirt.nested = true
      libvirt.disk_bus = 'virtio'
      libvirt.cpu_mode = "host-passthrough"
      libvirt.nic_model_type = "virtio"
      libvirt.disk_driver :cache => "writeback"
    end

    # Sync the entire project for testing
    rocky.vm.synced_folder ".", "/vagrant",
      type: "rsync",
      rsync__exclude: [".git/", "*.swp", ".venv/", ".vagrant/"]

    # Copy SSH key for testing
    rocky.vm.provision "file", 
      source: "~/.ssh/id_ed25519.pub", 
      destination: "/tmp/id_ed25519.pub"

    # Bootstrap system for testing
    rocky.vm.provision "shell", inline: <<-SHELL
      # Update system
      dnf update -y
      
      # Install required packages
      dnf install -y python3 python3-pip ansible git
      
      # Setup SSH key
      mkdir -p /home/vagrant/.ssh
      cat /tmp/id_ed25519.pub >> /home/vagrant/.ssh/authorized_keys
      chmod 600 /home/vagrant/.ssh/authorized_keys
      chown vagrant:vagrant /home/vagrant/.ssh/authorized_keys
      
      # Create test user that matches inventory
      useradd -m -s /bin/bash testuser || true
      echo "testuser ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/testuser
    SHELL

    # Run Ansible playbook for testing
    rocky.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbooks/full.yml"
      ansible.inventory_path = "inventory/inventory.ini"
      ansible.limit = "all"
      ansible.extra_vars = {
        ansible_python_interpreter: "/usr/bin/python3",
        ansible_user: "vagrant",
        # Override variables for testing
        use_docker: "false",
        use_libvirt: "false",
        window_manager: "i3",
        rvm_install: false
      }
      ansible.tags = ENV['ANSIBLE_TAGS'] || "base,ssh,shell"
      ansible.verbose = ENV['ANSIBLE_VERBOSE'] || false
      ansible.raw_arguments = ["--check"] if ENV['ANSIBLE_CHECK']
    end
  end

  # Optional Arch Linux VM for comparison testing
  config.vm.define "arch", autostart: false do |arch|
    arch.vm.box = "archlinux/archlinux"
    arch.vm.hostname = ARCH_HOSTNAME
    
    arch.vm.network :private_network,
      ip: "192.168.122.11",
      libvirt__network_name: "default"

    arch.vm.provider :libvirt do |libvirt|
      libvirt.memory = 2048
      libvirt.cpus = 2
      libvirt.nested = true
      libvirt.disk_bus = 'virtio'
      libvirt.cpu_mode = "host-passthrough"
      libvirt.nic_model_type = "virtio"
      libvirt.disk_driver :cache => "writeback"
    end

    arch.vm.synced_folder ".", "/vagrant",
      type: "rsync",
      rsync__exclude: [".git/", "*.swp", ".venv/", ".vagrant/"]

    arch.vm.provision "file", 
      source: "~/.ssh/id_ed25519.pub", 
      destination: "/tmp/id_ed25519.pub"

    arch.vm.provision "shell", inline: <<-SHELL
      # Update system
      pacman -Syu --noconfirm
      
      # Install required packages
      pacman -Sy --noconfirm python python-pip ansible git
      
      # Setup SSH key
      mkdir -p /home/vagrant/.ssh
      cat /tmp/id_ed25519.pub >> /home/vagrant/.ssh/authorized_keys
      chmod 600 /home/vagrant/.ssh/authorized_keys
      chown vagrant:vagrant /home/vagrant/.ssh/authorized_keys
    SHELL

    # Run Ansible playbook
    arch.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbooks/full.yml"
      ansible.inventory_path = "inventory/inventory.ini"
      ansible.limit = "all"
      ansible.extra_vars = {
        ansible_python_interpreter: "/usr/bin/python3",
        ansible_user: "vagrant",
        use_docker: "false",
        use_libvirt: "false",
        window_manager: "i3",
        rvm_install: false
      }
      ansible.tags = ENV['ANSIBLE_TAGS'] || "base,ssh,shell"
      ansible.verbose = ENV['ANSIBLE_VERBOSE'] || false
      ansible.raw_arguments = ["--check"] if ENV['ANSIBLE_CHECK']
    end
  end
end

# Usage Examples:
#
# Basic testing:
#   vagrant up rocky
#
# Test with specific tags:
#   ANSIBLE_TAGS="base,network" vagrant up rocky
#
# Run in check mode (dry-run):
#   ANSIBLE_CHECK=true vagrant up rocky
#
# Enable verbose output:
#   ANSIBLE_VERBOSE=true vagrant up rocky
#
# Test both distributions:
#   vagrant up rocky arch
#
# Re-run provisioning after changes:
#   vagrant provision rocky