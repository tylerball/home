# Ansible Role: shairport-sync

An Ansible role that installs [shairport-sync](https://github.com/mikebrady/shairport-sync) on Ubuntu/Debian.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```
conf: ''
```

A string containing your shairport-sync configuration.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```
- hosts: servers
  roles:
    - role: shairport-sync
      conf: |
        general = {
          name = "Maestro";
          volume_range_db = 30;
          drift = 352;
        };
```

## License

ISC

## Author Information

This role was created in 2016 by [Bob Zoller](https://github.com/bobzoller).
