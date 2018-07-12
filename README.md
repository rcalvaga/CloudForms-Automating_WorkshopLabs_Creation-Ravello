# CloudForms: Automating Workshop Labs Creation on Ravello

tar xzvf CloudForms-Automating_WorkshopLabs_Creation-Ravello.tgz

cd CloudForms_Workshop_Creation

vim group_vars/all/credentials.yaml

    ravello_login_username: youruser+gptelatam@redhat.com
    ravello_login_password: Y0urP4$$wordH3r3


vim group_vars/all/main.yaml

*NOTE: Just, modify {{ country }} and {{ customer_name }} variables as you need.*

*NOTE: {{ country }} variable can be as follows: MX, SAC or BR, for example.*

    country: MX
    customer_name: TEST
    bucket_type: "LATAM-SA-{{ country }}"



vim roles/ravello.applications_create/defaults/main.yaml

*NOTE: Just, modify ravello_app_list, ravello_expiration_time_min and ravello_deploy_topology_start_all variables as you need.*

ravello_app_list:
- [ app_name: "{{ bucket_type }}-CloudForms4-Workshop-{{ customer_name }}-Instructor" ]
- [ app_name: "{{ bucket_type }}-CloudForms4-Workshop-{{ customer_name }}-W1" ]
- [ app_name: "{{ bucket_type }}-CloudForms4-Workshop-{{ customer_name }}-W2" ]
- [ app_name: "{{ bucket_type }}-CloudForms4-Workshop-{{ customer_name }}-W3" ]
- [ app_name: "{{ bucket_type }}-CloudForms4-Workshop-{{ customer_name }}-W4" ]
- [ app_name: "{{ bucket_type }}-CloudForms4-Workshop-{{ customer_name }}-W5" ]
... truncated output ...

ravello_expiration_time_min: 480

*Recommendation is to keep topology_region as is, for best performance*
ravello_deploy_topology_region: us-east-5
ravello_deploy_topology_optimization: PERFORMANCE_OPTIMIZED
ravello_deploy_topology_start_all: true



*Running the Playbook:*

$ ansible-playbook create-ravello-apps.yaml

...truncated output ...
TASK [ravello.applications_create : Print App YAML files for Customer "TEST"] *************************************************************************************************************************************
ok: [localhost] => {
    "app_files": {
        "changed": true,
        "cmd": [
            "ls",
            "CloudForms4-Workshop"
        ],
        "delta": "0:00:00.003793",
        "end": "2017-07-11 14:41:47.649039",
        "rc": 0,
        "start": "2017-07-11 14:41:47.645246",
        "stderr": "",
        "stderr_lines": [],
        "stdout": "LATAM-SME-CloudForms4-Workshop-TEST-W1.yaml\nLATAM-SME-CloudForms4-Workshop-TEST-W2.yaml\nLATAM-SME-CloudForms4-Workshop-TEST-W3.yaml",
        "stdout_lines": [
            "LATAM-SME-CloudForms4-Workshop-TEST-Instructor.yaml",
            "LATAM-SME-CloudForms4-Workshop-TEST-W1.yaml",
            "LATAM-SME-CloudForms4-Workshop-TEST-W2.yaml",
            "LATAM-SME-CloudForms4-Workshop-TEST-W3.yaml"
        ]
    }
}

PLAY RECAP ********************************************************************************************************************************************************************************************************
localhost                  : ok=15   changed=7    unreachable=0    failed=0






*Sending E-Mails:*


vim roles/sendmail.applications/defaults/main.yaml

 sendmail_host: 'localhost'
 sendmail_port: '25'
 sendmail_username: ''
 sendmail_password: ''
 sendmail_from: ''


 sendmail_to:
 - { name: Robert Calva Garcia, email: rcalvaga@redhat.com, yaml_app_file: "{{ bucket_type }}-{{ ravello_fqdn_dir }}-{{ customer_name }}-Instructor.yaml" }
 - { name: DJ Azulman, email: djazulman@gmail.com, yaml_app_file: "{{ bucket_type }}-{{ ravello_fqdn_dir }}-{{ customer_name }}-W1.yaml" }
 - { name: Robert Azulman, email: robert_azulman@yahoo.com.mx, yaml_app_file: "{{ bucket_type }}-{{ ravello_fqdn_dir }}-{{ customer_name }}-W2.yaml" }
 - { name: customername, email: customer@email, yaml_app_file: "{{ bucket_type }}-{{ ravello_fqdn_dir }}-{{ customer_name }}-W3.yaml" }
 - { name: customername, email: customer@email, yaml_app_file: "{{ bucket_type }}-{{ ravello_fqdn_dir }}-{{ customer_name }}-W4.yaml" }
... truncated output ...


sendmail_subject: "CloudForms Workshop: Documentation"

sendmail_body: "Hola {{ item.name }}\n\n\nLe envio el archivo PDF para seguir el Workshop, así como el archivo YAML para accesar a las URLs de dicho Workshop.\n\n\nSaludos cordiales.\n\nRobert J. Calva\n\n**Este mail ha sido automatizado via Red Hat Ansible**"



*Running the Playbook:*

$ ansible-playbook sendmail-applications.yaml


PLAY [Send YAML Application Files to Customers] *******************************************************************************************************************************************************************

TASK [sendmail.applications : Send Mail with YAML Applications Files to Customers] ********************************************************************************************************************************
ok: [localhost -> localhost] => (item={u'yaml_app_file': u'LATAM-SME-CloudForms4-Workshop-TEST-Instructor.yaml', u'name': u'Robert Calva Garcia', u'email': u'rcalvaga@redhat.com'})
ok: [localhost -> localhost] => (item={u'yaml_app_file': u'LATAM-SME-CloudForms4-Workshop-TEST-W1.yaml', u'name': u'DJ Azulman', u'email': u'djazulman@gmail.com'})
ok: [localhost -> localhost] => (item={u'yaml_app_file': u'LATAM-SME-CloudForms4-Workshop-TEST-W2.yaml', u'name': u'Robert Azulman', u'email': u'robert_azulman@yahoo.com.mx'})

PLAY RECAP ********************************************************************************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0
