ansible-library-etcd
------------------

# Description
Ansible library to manage Etcd keys.

# Usage
Ensure a key is present
```
- name: Ensure Etcd key
etcd_key:
name: myKey
value: myValue
state: present
etcd_host: etcd.example.com
etcd_port: 4001
```
Ensure a key is absent
```
- name: Ensure Etcd key
  etcd_key:
    name: myKey
    state: absent
    etcd_host: etcd.example.com
    etcd_port: 4001
```
