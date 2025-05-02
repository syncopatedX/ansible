# -*- mode: ruby -*-
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'

#site specific vars
# vm_box = "centos7_nginx_jun2017"
hostname = "dev01.syncopated.dev"
# domain_name = "syncopated.dev"

ANSIBLE_HOME = File.join(ENV['HOME'], 'Workspace', 'Syncopated', 'syncopated-ansible')

Vagrant.configure("2") do |config|
  config.vm.box = "archlinux/archlinux"
  config.vm.provider :libvirt do |libvirt|
    libvirt.memory = 2048
    libvirt.cpus = 2
    libvirt.nested = true
    libvirt.disk_bus = 'virtio'
    libvirt.cpu_mode = "host-passthrough"
    libvirt.nic_model_type = "virtio"
    libvirt.disk_driver :cache => "writeback"
  end

  config.vm.hostname = "#{hostname}"

  config.vm.network :private_network,
    ip: "192.168.122.10",
    libvirt__network_name: "default"

  config.vm.synced_folder ".", "/home/vagrant/collections",
    type: "rsync",
    rsync__exclude: [".git/", "*.swp", ".venv/"]

  config.vm.provision "file", source: "~/.ssh/id_ed25519", destination: "/home/vagrant/.ssh/id_ed25519"

  config.vm.provision "shell", inline: <<-SHELL
    pacman -Syu --noconfirm
    pacman -Sy --noconfirm python python-pip ansible pacman
  SHELL
  
  # config.vm.provision "ansible" do |ansible|
  #   ansible.playbook = "playbooks/setup.yml"
  #   ansible.extra_vars = {
  #     ansible_python_interpreter: "/usr/bin/python3",
  #     collection_path: "/home/vagrant/collections"
  #   }
  #   ansible.inventory_path = "inventory/inventory.ini"
  #   ansible.limit = "#{hostname}"
  # end

end


# Vagrant.configure("2") do |config|

#   config.hostmanager.enabled = true
#   config.hostmanager.manage_host = true
#   config.hostmanager.manage_guest = true

#   config.ssh.insert_key = false

#   config.vm.provider :libvirt do |libvirt|
#     libvirt.connect_via_ssh = false
#     libvirt.username = "root"
#     libvirt.storage_pool_name = "default"
#   end

#   # #run rsync-auto from cli
#   # #https://github.com/guard/listen/wiki/Increasing-the-amount-of-inotify-watchers
#   # config.vm.synced_folder ".", "/vagrant",
#   #   owner: "vagrant", group: "vagrant", type: "rsync"

#   config.vm.define "#{hostname}".to_sym do |website|
#     website.vm.box = "#{vm_box}"

#     website.vm.network "public_network",
#       :dev => "virbr0",
#       :mode => "bridge",
#       :type => "bridge"
    
#     website.vm.network :forwarded_port, guest: 22, host: 40418, id: 'ssh'
#     website.vm.hostname = "#{hostname}"
#     website.hostmanager.aliases = "#{domain_name}"
    
#     website.vm.provider :libvirt do |setting|
#       setting.memory = 2048
#       setting.cpus = 2
#       setting.random_hostname = true
#     end
    
#     website.vm.provision :ansible do |ansible|
#       ansible.inventory_path = "#{ANSIBLE_HOME}/inventory"
#       ansible.playbook = "#{ANSIBLE_HOME}/playbooks/setup.yml"
#       # ansible.tags = "ssl-certs,nginx_conf,nginx_vhost"
#       ansible.limit = "#{hostname}"
#       ansible.verbose = "v"
#     end


#   end

# end

# # this may come in handy for future dev stuff;
# # http://stackoverflow.com/a/33269424