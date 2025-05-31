#!/usr/bin/python

# Copyright: (c) 2022, Gregory Furlong <gnfzdz@fzdz.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re


def partition_name(partition_number, device):
    pattern = re.compile(".*[0-9]$")
    if pattern.match(device):
        return device + "p" + partition_number
    else:
        return device + partition_number


class FilterModule(object):
    ''' Ansible disk partitioning related jinja filters '''

    def filters(self):
        return {
            'partition_name': partition_name
        }
