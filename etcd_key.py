#!/usr/bin/env python
# -*- coding: utf-8 -*-
DOCUMENTATION = '''
---
module: etcd_key
short_description: Manage Etcd Key/Value pairs with Ansible using Etcd API
description:
- Create, update and delete Etcd Key/Value pairs.
options:
  name:
    description:
    - Key name
    required: True
  value:
    description:
    - Key value
    required: False
    default: None
  ttl:
    description:
    - Value TTL
  etcd_host:
    description:
    - IP or Hostname of the system Etcd is running on
    required: False
    default: '127.0.0.1'
  etcd_port:
    description:
     - Port where Etcd API is listening
    required: False
    default: 4001
  etcd_protocol:
    description:
    - Protocol to use
    required: False
    default: 'http'
    choices: ['http', 'https']
notes:
- Requires the python-etcd package to be installed. See https://github.com/jplana/python-etcd.
author: Thomas Krahn
'''

EXAMPLES = '''
- name: Ensure key is present
  etcd_key:
    name: MyKey
    value: MyValue
    ttl: 123
    etcd_host: etcd.example.com
    etcd_port: 4001
    etcd_protocol: https
'''


try:
    import etcd

    etcdclient_found = True
except ImportError:
    etcdclient_found = False


def ensure(module):
    name = module.params['name']
    state = module.params['state']
    value = module.params['value']
    ttl = module.params['ttl']

    etcd_host = module.params['etcd_host']
    etcd_port = module.params['etcd_port']
    etcd_protocol=module.params['etcd_protocol']
    
    try:
        client = etcd.Client(host=etcd_host, port=etcd_port, protocol=etcd_protocol)
    except Exception as e:
        module.fail_json(msg='Could not connect to %s://%s:%s: %s' % (etcd_protocol, etcd_host,etcd_port, e.message))

    try:
        key_value = client.read(name).value
    except etcd.EtcdKeyNotFound:
        key_value = None

    if state == 'present' and key_value != value:
        try:
            client.write(key=name, value=value, ttl=ttl)
            return True
        except Exception as e:
            module.fail_json(msg='Could not write key %s: %s' % (name, e.message))

    if state == 'absent' and key_value:
        try:
            client.delete(key=name)
            return True
        except Exception as e:
            module.fail_json(msg='Could not delete key %s: %s' % (name, e.message))

    return False

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, Type='str'),
            state=dict(required=False, default='present', choices=['present','absent']),
            value=dict(required=False, default=None),
            ttl=dict(required=False, default=None),
            etcd_host=dict(required=False, default='127.0.0.1'),
            etcd_port=dict(required=False, default=4001),
            etcd_protocol=dict(required=False, Type='str', default='http', choices=['http','https']),
        ),
    )

    if not etcdclient_found:
        module.fail_json(msg='Etcd client required. See https://github.com/jplana/python-etcd.')

    changed = ensure(module)
    module.exit_json(changed=changed, name=module.params['name'])

# import module snippets
from ansible.module_utils.basic import *
main()
