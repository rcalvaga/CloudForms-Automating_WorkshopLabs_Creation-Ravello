#!/usr/bin/env python

DOCUMENTATION = '''
---

'''

EXAMPLES = '''
   dest: "{{ inventory_hostname }}.xml"
   format: xml
'''
from distutils.version import LooseVersion
from ansible.module_utils.basic import *
import logging
import json
import requests
import httplib2

def main():

    module = AnsibleModule(
        argument_spec = dict(
            appId = dict(required = True, default = None),
            baseVmId = dict(required = True, default = None),
            user = dict(required = True, default = None),
            password = dict(required = True, default = None),
        ),
        supports_check_mode = True
    )

    results = dict(changed=False)

    args = module.params
    url = "https://cloud.ravellosystems.com/api/v1/applications/" + str(args['appId']) + "/vms"
    headers = {"Accept" : "application/json", "Content-Type" : "application/json"}
    data = {"baseVmId" : args['baseVmId'] }
    r = requests.post(url,
        auth = (args['user'], args['password']),
        headers = headers,
        json = data
    )

    ## TODO Add check for return code from server

    json = r.json()
    vms = json['design']['vms']
    creationTime = 0
    returnVm = None
    for vm in vms:
        if creationTime < vm['creationTime']:
            creationTime = vm['creationTime']
            returnVm = vm

    if returnVm == None:
        module.fail_json(msg = "Unable to identify the newly added VMs")

    results['changed'] = True
    results['msg'] = returnVm
    module.exit_json(**results)

if __name__ == "__main__":
    main()
