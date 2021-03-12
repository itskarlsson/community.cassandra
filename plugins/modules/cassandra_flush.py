#!/usr/bin/python

# 2019 Rhys Campbell <rhys.james.campbell@googlemail.com>
# https://github.com/rhysmeister
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


DOCUMENTATION = '''
---
module: cassandra_flush
author: Rhys Campbell (@rhysmeister)
short_description: Flushes one or more tables from the memtable to SSTables on disk.
requirements:
  - nodetool
description:
  - Flushes one or more tables from the memtable to SSTables on disk.

extends_documentation_fragment:
  - community.cassandra.nodetool_module_options

options:
  keyspace:
    description:
      - Optional keyspace.
    type: str
  table:
    description:
      - Optional table name or list of table names.
    type: raw
'''

EXAMPLES = '''
- name: Run flush on the Cassandra node
  community.cassandra.cassandra_flush:
'''

RETURN = '''
cassandra_flush:
  description: The return state of the executed command.
  returned: success
  type: str
'''

from ansible.module_utils.basic import AnsibleModule, load_platform_subclass
import socket
__metaclass__ = type


from ansible_collections.community.cassandra.plugins.module_utils.nodetool_cmd_objects import NodeToolCmd, NodeToolCommandKeyspaceTable
from ansible_collections.community.cassandra.plugins.module_utils.cassandra_common_options import cassandra_common_argument_spec


def main():
    argument_spec = cassandra_common_argument_spec()
    argument_spec.update(
        keyspace=dict(type='str', default=None, required=False, no_log=False),
        table=dict(type='raw', default=None, required=False)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
    )

    cmd = 'flush'

    n = NodeToolCommandKeyspaceTable(module, cmd)

    rc = None
    out = ''
    err = ''
    result = {}

    (rc, out, err) = n.run_command()
    out = out.strip()
    err = err.strip()
    if module.params['debug']:
        if out:
            result['stdout'] = out
        if err:
            result['stderr'] = err

    if rc == 0:
        result['changed'] = True
        result['msg'] = "nodetool flush executed successfully"
        module.exit_json(**result)
    else:
        result['rc'] = rc
        result['changed'] = False
        result['msg'] = "nodetool flush did not execute successfully"
        module.exit_json(**result)


if __name__ == '__main__':
    main()
