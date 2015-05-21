Ansible Etcd library
==========

# Table of Contents
- [Description](#description)
- [Requirements](#requirements)
- [Examples](#examples)
- [License](#license)
- [Author information](#autor information)

# Description
Ansible library to manage Etcd keys.

# Requirements
[python-etcd] is required to be installed.

# Usage

Ensure a key is present

```yaml
- name: Ensure Etcd key
  etcd_key:
    name: myKey
    value: myValue
    ttl: 10
    state: present
    etcd_host: etcd.example.com
    etcd_port: 4001
```

Ensure a key is absent

```yaml
- name: Ensure Etcd key
  etcd_key:
    name: myKey
    state: absent
    etcd_host: etcd.example.com
    etcd_port: 4001
```

# License
Copyright 2015 Thomas Krahn

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# Author information
[Thomas Krahn]

[python-etcd]: https://github.com/jplana/python-etcd
[Thomas Krahn]: mailto:ntbc@gmx.net
