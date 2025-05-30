# Ansible Role - gnfzdz.base.time

Configure the system time and timezone

## Variables
-------

Variable | Description | Type | Default
-------- | ----------- | -------- | --------
`base_time_zone` | The time zone that should be configured on the system. The value should be a path relative to /usr/share/zoneinfo by the system and the full path should point to an [IANA time zone database file](https://www.iana.org/time-zones) | string | UTC
