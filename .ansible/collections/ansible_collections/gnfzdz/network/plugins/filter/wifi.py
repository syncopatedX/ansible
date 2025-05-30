#!/usr/bin/python

# Copyright: (c) 2022, Gregory Furlong <gnfzdz@fzdz.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
from hashlib import pbkdf2_hmac
from binascii import hexlify

# Hashing algorithm used to generate the PSK
WIFI_PSK_HASH_ALGORITHM = 'sha1'
# Number of iterations
WIFI_PSK_ITERATIONS = 4096
# Width of the PSK in chars
WIFI_PSK_WIDTH = 32

# Convert a WPA password and SSID to a hex encoded preshared key
def wifi_psk(password, ssid):
    # TODO validate the password and ssid
    return pbkdf2_hmac(WIFI_PSK_HASH_ALGORITHM, password.encode('UTF-8'), ssid.encode('UTF-8'), WIFI_PSK_ITERATIONS, WIFI_PSK_WIDTH).hex()

# the iwd filename (minus extension) is the raw SSID when it's composed only of alphanumeric characters, space,
# undercore and hyphen. Otherwise, it's an = followed by the hex encoded ssid
def encode_iwd_network_name(ssid):
    pattern = re.compile("^[A-Za-z0-9 _-]+$")
    if pattern.match(ssid):
        return ssid
    else:
        return '=' + hex_encode(ssid)

#
def hex_encode(data):
    return hexlify(data.encode("UTF-8")).decode("UTF-8")

class FilterModule(object):
    ''' Ansible wifi related jinja filters '''

    def filters(self):
        return {
            'wifi_psk': wifi_psk,
            'encode_iwd_network_name': encode_iwd_network_name
        }
