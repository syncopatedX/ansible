# Ansible Role: Audio

# Role Variables

```yaml
additional_packages:
  - somepackage

use_pipewire: False

use_jack: True
jack_control:
  dps:
    device: hw:0

colors:
  primary: #000000

```


# Example Playbook


```yaml
---

- name: setup workstation
  hosts: localhost
  connection: local
  gather_subset:
    - hardware
    - network
  vars:
    path:
      - "{{ lookup('env','HOME') }}/.local/bin"
      - "{{ lookup('env','HOME') }}/.cargo/bin"
      - "{{ lookup('env','HOME') }}/.local/share/gem/ruby/3.0.0/bin"

  environment:
    PATH: "{{ ansible_env.PATH }}:/sbin:/bin:{{ path|join(':') }}"
    PKG_CONFIG_PATH: "/usr/share/pkgconfig:/usr/lib/pkgconfig:/usr/local/lib/pkgconfig"
    DISPLAY: ":0"

  roles:
    - role: audio
      tags: ['audio']

  post_tasks:
      - name: set root shell
        user:
          name: root
          shell: /usr/bin/zsh
        become: True

      - name: reboot host
        ansible.builtin.reboot:
        async: 1
        poll: 0
        ignore_errors: True
        become: True
        when: reboot is defined

      - name: wait for host to reboot
        wait_for_connection:
          connect_timeout: 20
          sleep: 5
          delay: 5
          timeout: 120
        become: True
        when: reboot is defined


```
