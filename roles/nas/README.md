nas
=========

- [ ] the option to bind the share to a psuedofs mount?

```yaml
---
#> host_vars/tinybot.yml

share:
  nfs:
    parent: "{{ user.home }}"
    exports:
      - Archive
      - Workspace
```

Run the playbook
```bash
aplaybook -C -i inventory.ini playbooks/nas.yml --limit tinybot
```
