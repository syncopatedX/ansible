#!/usr/bin/python

# Copyright: (c) 2022, Gregory Furlong <gnfzdz@fzdz.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
  name: gnfzdz.base.dict2ini
  short_description: Convert a nested dict structure representing ini data into a list of the corresponding section/option/value pairs
  version_added: 1.0.2
  author: Gregory Furlong (gnfzdz@fzdz.io)
  description:
    - Convert a nested dict structure representing ini data into a list of the corresponding section/option/value pairs
    - The stucture should have a depth of 2 with top level keys corresponding to ini sections.
    - Keys within the nested dict should correspond to ini options.
    - The values within the nested dict should be either primitives or a list of primitives (for cases where the value can be set multiple times)
  options:
    _input:
      description: A dict representing ini data.
      type: dict
      required: true
'''

EXAMPLES = '''
- name: Convert ini data to a list of the pairs
  ansible.builtin.debug:
    msg: >-
      {{ { 'Settings': {'AutoConnect': true, 'Hidden':false }, 'Security': { 'Passphrase': 'letmein' } } | gnfzdz.base.dict2ini }}
    # Produces:
    # [
    #   { "section": "Settings", "option": "AutoConnect", "value": true },
    #   { "section": "Settings", "option": "Hidden", "value": false },
    #   { "section": "Security", "option": "Passphrase", "value": "letmein" }
    # ]

- name: Loop through all section/option/value pairs and write into ini file
  community.general.ini_file:
    path: "/path/to/file.ini"
    section: "{{ item.section }}"
    option: "{{ item.option }}"
    value: "{{ item.value }}"
  loop: "{{ { 'Settings': {'AutoConnect': true, 'Hidden':false }, 'Security': { 'Passphrase': 'letmein' } } | gnfzdz.base.dict2ini }}"
'''

RETURN = '''
  _value:
    description: A list containing the paired sections, options and values for the ini data
    type: list
    elements: dict
'''

# TODO consider checking if value is a list and returning values instead?
def dict2ini(data, sections=None):
    ''' Convert a nested dict structure representing ini data into a list of the corresponding section/option/value pairs  '''
    ini = []
    for section in data.items():
        if sections is None or section[0] in sections:
            if type(section[1]) is dict:
                for kv in section[1].items():
                    ini.append({
                        "section": section[0],
                        "option": kv[0],
                        "value": kv[1]
                    })
    return ini


class FilterModule(object):
    ''' Ansible ini related jinja filters '''

    def filters(self):
        return {
            'dict2ini': dict2ini
        }
