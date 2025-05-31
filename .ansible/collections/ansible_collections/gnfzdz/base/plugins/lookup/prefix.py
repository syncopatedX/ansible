#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Copyright: (c) 2022, Gregory Furlong <gnfzdz@fzdz.io>
# Adapted from ansible.builtin.vars and ansible.builtin.varnames lookup plugins
# Copyright: (c) 2017 Ansible Project

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: prefix
    author: gnfzdz@fzdz.io
    short_description: Look up all variables starting with the provided prefix. Return a map containing these values with the prefix removed from each key.
    description:
      - Retrieves a map of all variables with a name starting with the provided prefix. All keys in the returned map have the prefix removed.
    options:
      _terms:
        description: A variable prefix to match against
        required: True
"""

EXAMPLES = """
- name: List variables that start with user_bob
  ansible.builtin.debug: msg="{{ lookup('gnfzdz.base.prefix', 'user_bob')}}"
  vars:
    user_bob_name: bob
    user_bob_uid: 1000
    user_bob_email: bob@example.org
    user_alice_name: alice
    user_alice_uid: 1001
    user_alice_email: alice@example.org

  # return value
  {
    'name': 'bob',
    'uid': 1000,
    'email': 'bob@example.org'
  }

"""

RETURN = """
_value:
  description:
    - A map where of variable names and values for all variables starting with the provided prefix. The keys in the returned map have the prefix removed.
  type: map
"""

import re

from abc import abstractmethod
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.module_utils.six import string_types
from ansible.plugins.lookup import LookupBase

class PrefixBase(LookupBase):

    def get_vars(self):
        return getattr(self._templar, '_available_variables', {})

    def get_templated_value(self, term):
        myvars = self.get_vars()
        try:
            value = myvars[term]
        except KeyError:
            try:
                value = myvars['hostvars'][myvars['inventory_hostname']][term]
            except KeyError:
                raise AnsibleUndefinedVariable('No variable found with this name: %s' % term)

        return self._templar.template(value, fail_on_undefined=True)

    def get_variable_map_or_prefixed(self, varname):
        try:
            return self.get_templated_value(varname)
        except Exception:
            return self.get_variables_for_prefix(varname)

    def get_variables_for_prefix(self, search):
        prefix = search if len(search) > 0 and search[-1] == "_" else search + "_"
        matches = {}

        if not isinstance(prefix, string_types):
            raise AnsibleError('Invalid setting identifier, "%s" is not a string, it is a %s' % (prefix, type(prefix)))

        try:
            name = re.compile(prefix)
        except Exception as e:
            raise AnsibleError('Unable to use "%s" as a search parameter: %s' % (prefix, to_native(e)))

        variables = self.get_vars()
        variable_names = list(variables.keys())
        for varname in variable_names:
            if name.search(varname):
                key = name.sub("", varname)
                matches[key] = self.get_templated_value(varname)

        return matches

    def set_variables(self, variables):
        if variables is None:
            raise AnsibleError('No variables available to search')
        else:
            self._templar.available_variables = variables

    @abstractmethod
    def get_prefixed_data(self, term):
        pass

    def run(self, terms, variables=None, **kwargs):
        self.set_variables(variables)
        self.set_options(var_options=variables, direct=kwargs)

        if len(terms) == 1:
            prefixes = terms[0] if isinstance(terms[0], list) else [ terms[0] ]
            return [ self.get_prefixed_data(prefix) for prefix in prefixes ]
        else:
            raise AnsibleError('Expected exactly one prefix to be provided')


class LookupModule(PrefixBase):

    def get_prefixed_data(self, term):
        return self.get_variables_for_prefix(term)
