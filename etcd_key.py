#!/usr/bin/env python

# -*- coding: utf-8 -*-

try:
    import etcd
    etcdclient_found = True
except ImportError:
    etcdclient_found = False

def ensure(module):
    key = module.params['key']
    value = module.params['value']
    state = module.params['state']
    etcd_host=module.params['host']
    etcd_port=module.params['port']
    etcd_protocol=module.params['protocol']
    
    client = etcd.Client(host=etcd_host, port=etcd_port, protocol=etcd_protocol)

    try:
        existing_key = client.read(key)
        current_value = client.read(key).value
    except KeyValue:
        existing_key = None
        current_value = None
        
    if state == 'present':
        if not existing_key or current_value != value:
            try:
                client.write(key, value)
                return True
            except Exception as e:
                module.fail_json(msg='Could not write key: ' +  e.message)

    if state == 'absent':
        if existing_key:
            try:
                client.delete(key=key)
                return True
            except Exception as e:
                module.fail_json(msg='Could not delete key: ' + e.message)

    return False

def main():
    module = AnsibleModule(
        argument_spec=dict(
            key=dict(required=True, Type='str', alias='name'),
            value=dict(required=False),
            ttl=dict(required=False),
            etcd_host=dict(required=True, Type='str'),
            etcd_port=dict(required=False, Type='str', Default='4001'),
            etcd_protocol=dict(required=False,Type='str',Default='http', choices=['http','https']),
            state=dict(Default='started', choices=['present','absent']),
        ),
    )

    if not etcdclient_found:
        module.fail_json(msg='Etcd client required. See https://github.com/jplana/python-etcd.')

    changed = ensure(module)
    module.exit_json(changed=changed, name=module.params['name'])

# import module snippets
from ansible.module_utils.basic import *
main()
