#
#  start me with 
#  fab test.start:euca_boto,access
#

from boto.ec2 import RegionInfo
from boto import connect_ec2
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
import urlparse
import sys


class Test:

    def man(self):
        print "your yaml file should have something like this:"
        print """
        india-eucalyptus:
            cm_host: 149.165.146.135
            cm_label: ios
            cm_type: eucalyptus
            credentials:
                EC2_URL: http://149.165.146.135:8773/services/Eucalyptus
                S3_URL: http://149.165.146.135:8773/services/Walrus
                EUARE_URL: http://149.165.146.135:8773/services/Euare
                EC2_USER_ID: 281408815495
                EC2_ACCOUNT_NUMBER: 281408815495
                EC2_ACCESS_KEY: abaababababababababab
                EC2_SECRET_KEY: xoxoxoxoxoxoxoxoxoxox
                EC2_PRIVATE_KEY: ~/.futuregrid/eucalyptus/fg82/euca2-gvonlasz-04276949-pk.pem
                EC2_CERT: ~/.futuregrid/eucalyptus/fg82/euca2-gvonlasz-04276949-cert.pem
                EC2_JVM_ARGS: -Djavax.net.ssl.trustStore=$HOME/.futuregrid/eucalyptus/fg82/jssecacerts
                AWS_CREDENTIAL_FILE: ~/.futuregrid/eucalyptus/fg82/iamrc
                EUCALYPTUS_CERT: ~/.futuregrid/eucalyptus/fg82/cloud-cert.pem
            default:
                filter:
                    select:
                        me: true
                    state:
                        ACTIVE: true
                        BUILDING: true
                        DELETED: true
                        ERROR: true
                        PAUSED: true
                        RESCUED: true
                        RESIZED: true
                        SOFT_DELETED: true
                        STOPPED: true
                        SUSPENDED: true
                flavor: m1.small
                image: emi-FE9838AC
        """
    def setup(self):
        conf = cm_config()
        cred = conf.get("india-eucalyptus")
        pprint (cred)


        aws_access_key_id = cred['EC2_ACCESS_KEY']
        aws_secret_access_key = cred['EC2_SECRET_KEY']
        ec2_url = cred['EC2_URL']
        result = urlparse.urlparse(ec2_url)
        is_secure = (result.scheme == 'https')
        if ":" in result.netloc:
            host_port_tuple = result.netloc.split(':')
            host = host_port_tuple[0]
            port = int(host_port_tuple[1])
        else:
            host = result.netloc
            port = None
    
        path = result.path
        region_name = 'eucalyptus'
        api_version = '2009-11-30'

        print 'aws_access_key_id', aws_access_key_id
        print 'aws_secret_access_key', aws_secret_access_key
        print 'is_secure', is_secure
        print 'name', region_name
        print 'endpoint', host
        print 'port', port
        print 'path', path
        print 'api_version', api_version


        self.conn = connect_ec2(aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key,
                           is_secure=is_secure,
                           region=RegionInfo(name=region_name, endpoint=host),
                           port=port,
                           path=path,
                           api_version=api_version)


    def test_access(self):


        regions = self.conn.get_all_regions()
        print(regions)

        zones = self.conn.get_all_zones()
        print(zones)
        
        reservations = self.conn.get_all_instances()
        print(reservations)
        
        
        instances = self.reservations[0].instances
        
        print "I", instances
