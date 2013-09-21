Version 0.5
NOT YET IMPLEMENTED
DDD {
    "filename": "~/.futuregrid/me.yaml", 
    "location": "/Users/neu/.futuregrid/me.yaml", 
    "profile": {
        "lastname": "von Laszewski", 
        "firstname": "Gregor", 
        "e-mail": "gvonlasz@gmail.com"
    }, 
    "keys": {
        "fg_1": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8CuROXICp7OBRNLf4EYBVyUTE48ZVn9YOtPQpdrtX0F4OnHM0rE3FCGjgd1aCrPakrRKvx0HjHTQjSrOd4nkRcrC1mzSUpjkbHzdFKbhIfWlbVA+GyKlrQzW9GeYX8Um7Of7ZYsQVI3Bs9YmkInHk330olOPVVbNN0Uqu6KpAl04zPmdR+Kf/eHb1bcNKxN9+h3HccSiT+2xBDO8uEjcVd0IByyZO6/ImU5krCx1vpVJMPhwC/GejvQIc7zsG/L2tvpJOlkRsRIHfgJ3IaqPCwnoclv9Xp3pBgvR+c+hjVz5Dw6Q9yZK7wsZ7Tg1h5d3OG0bEfhXuUKAuZ6uhsIdt fg-1", 
        "fg_pro": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8CuROXICp7OBRNLf4EYBVyUTE48ZVn9YOtPQpdrtX0F4OnHM0rE3FCGjgd1aCrPakrRKvx0HjHTQjSrOd4nkRcrC1mzSUpjkbHzdFKbhIfWlbVA+GyKlrQzW9GeYX8Um7Of7ZYsQVI3Bs9YmkInHk330olOPVVbNN0Uqu6KpAl04zPmdR+Kf/eHb1bcNKxN9+h3HccSiT+2xBDO8uEjcVd0IByyZO6/ImU5krCx1vpVJMPhwC/GejvQIc7zsG/L2tvpJOlkRsRIHfgJ3IaqPCwnoclv9Xp3pBgvR+c+hjVz5Dw6Q9yZK7wsZ7Tg1h5d3OG0bEfhXuUKAuZ6uhsIdt fg-pro"
    }, 
    "password": {
        "sierra_openstack_grizzly": "1SGmWl7EmAc6"
    }, 
    "portalname": "gvonlasz", 
    "projects": {
        "default": "fg82", 
        "active": [
            "fg82", 
            "fg101"
        ], 
        "completed": [
            "fg130"
        ]
    }
}
cloudmesh:
  active:
  - sierra_openstack_grizzly
  clouds:
    sierra_openstack_grizzly:
      cm_heading: Sierra OpenStack, Grizzly
      cm_host: sierra.futuregrid.org
      cm_label: sos
      cm_type: openstack
      cm_type_version: grizzly
      credentials:
        OS_AUTH_URL: https://s77r.idp.sdsc.futuregrid.org:5000/v2.0
        OS_CACERT: $HOME/.futuregrid/sierra-cacert.pem
        OS_PASSWORD: 1SGmWl7EmAc6
        OS_TENANT_NAME: fg82
        OS_USERNAME: gvonlasz
        OS_VERSION: grizzly
      default:
        flavor: m1.tiny
        image: 4199d988-0833-4497-a473-96fc456fac2f
    windows_azure:
      cm_host: windowsazure.com
      cm_label: ios
      cm_type: windowszure
      cm_type_version: null
      credentials:
        managementcertfile: $HOME/.futuregrid/azure-managementCertificate.pem
        subscriptionid: 00000000-aaaa-bbbb-cccc-dddddddddddd
      default:
        flavor: null
        image: b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu_DAILY_BUILD-saucy-13_10-amd64-server-20130919-en-us-30GB
        location: Central US
        role_size: ExtraSmall
  default: sierra_openstack_grizzly
  hpc:
    username: gvonlasz
  index: 1
  keys:
    default: null
    keylist:
      fg_1: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8CuROXICp7OBRNLf4EYBVyUTE48ZVn9YOtPQpdrtX0F4OnHM0rE3FCGjgd1aCrPakrRKvx0HjHTQjSrOd4nkRcrC1mzSUpjkbHzdFKbhIfWlbVA+GyKlrQzW9GeYX8Um7Of7ZYsQVI3Bs9YmkInHk330olOPVVbNN0Uqu6KpAl04zPmdR+Kf/eHb1bcNKxN9+h3HccSiT+2xBDO8uEjcVd0IByyZO6/ImU5krCx1vpVJMPhwC/GejvQIc7zsG/L2tvpJOlkRsRIHfgJ3IaqPCwnoclv9Xp3pBgvR+c+hjVz5Dw6Q9yZK7wsZ7Tg1h5d3OG0bEfhXuUKAuZ6uhsIdt
        fg-1
      fg_pro: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8CuROXICp7OBRNLf4EYBVyUTE48ZVn9YOtPQpdrtX0F4OnHM0rE3FCGjgd1aCrPakrRKvx0HjHTQjSrOd4nkRcrC1mzSUpjkbHzdFKbhIfWlbVA+GyKlrQzW9GeYX8Um7Of7ZYsQVI3Bs9YmkInHk330olOPVVbNN0Uqu6KpAl04zPmdR+Kf/eHb1bcNKxN9+h3HccSiT+2xBDO8uEjcVd0IByyZO6/ImU5krCx1vpVJMPhwC/GejvQIc7zsG/L2tvpJOlkRsRIHfgJ3IaqPCwnoclv9Xp3pBgvR+c+hjVz5Dw6Q9yZK7wsZ7Tg1h5d3OG0bEfhXuUKAuZ6uhsIdt
        fg-pro
      prefix: gvonlasz
  profile:
    address:
    - TBD
    e_mail: null
    firstname: Gregor
    gid: null
    lastname: von Laszewski
    phone: null
    uid: null
    username: gvonlasz
  projects:
    active:
    - fg82
    - fg101
    completed:
    - fg130
    default: fg82
  security:
    default: development
    rules:
      ping:
        ip-address: 0.0.0.0/0
        max_port: -1
        min_port: -1
        protocol: icmp
      ssh:
        ip-address: 0.0.0.0/0
        max_port: 22
        min_port: 22
        protocol: tcp
      web:
        ip-address: 0.0.0.0/0
        max_port: 80
        min_port: 80
        protocol: tcp
    security_groups:
      development:
      - ssh
      - ping
      - web
      webserver:
      - web
yaml_version: 1.0


Done.
