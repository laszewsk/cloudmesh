# -*- coding: utf-8 -*-
"""
    cloudmesh.user.cm_user
    ~~~~~~~~~~~~~~~~~~~~~~

    cm_user provides user information from the ldap and the cloud like openstack
    through mongodb. fab mongo.cloud command initialize mongo database and pour
    the information into the mongodb. Once the mongodb for cloudmesh has the
    user information, cm_user retrieves the user data from the mongodb
    instead of directly accessing the ldap and OpenStack Keystone. cm_user_id is
    the unique identification in ldap and cloud.

"""
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.util.logger import LOGGER
from pymongo import MongoClient

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

class cm_user(object):
    """cm_user provides user information including the ldap's and the clouds'.
    The ldap has a user profile such as a first name, last name and active
    project ids. In OpenStack Keystone, it has cloud-related information such as
    a tenant id, user id, cloud version, cloud type and location.
    """

    def __init__(self):
        self.connect_db()
        self.connect_userdb()

    def connect_db(self):
        """ Connect to the mongo db."""
        db_name = cm_config_server().get("mongo.db")
        client = MongoClient()
        db = client[db_name]
        ldap_collection = 'user'
        cloud_collection = 'cloudmesh'
        self.db_clouds = db[cloud_collection]
        self.db_users = db[ldap_collection]

    def connect_userdb(self):
        """ Connect to the mongo user db."""
        # This will be enabled with ssl
        db_name = cm_config_server().get("mongo_user.db")
        host = cm_config_server().get("mongo_user.host")
        port = cm_config_server().get("mongo_user.port")
        username = cm_config_server().get("mongo_user.username")
        password = cm_config_server().get("mongo_user.password")
        client = MongoClient(host=host, port=port)
        db = client[db_name]
        passwd_collection = 'cm_password'
        self.userdb_passwd = db[passwd_collection]
        db.authenticate(username, password)

    def info(self, portal_id, cloud_names=[]):
        """Return the user information with a given portal id.

        :param portal_id: the unique portal id to retrieve
        :type portal_id: str
        :param cloud_names: the list of cloud names to search, e.g.
        sierra_openstack_grizzly
        :type cloud_names: list
        :returns: dict

        """
        ldap_info = self.db_users.find({"cm_user_id": portal_id})
        cloud_info = self.db_clouds.find({"name": portal_id, "cm_kind": "users"})
        userinfo = {}
        # username is unique in ldap
        if ldap_info.count() > 0:
            ldap_user = ldap_info[0]
            del ldap_user['_id']
            userinfo["profile"] = ldap_user
        userinfo['clouds'] = {}
        for arec in cloud_info:
            del arec['_id']
            if len(cloud_names) > 0:
                if arec['cm_cloud'] in cloud_names:
                    userinfo['clouds'][arec['cm_cloud']] = arec
            else:
                userinfo['clouds'][arec['cm_cloud']] = arec
        return userinfo

    def __getitem__(self, key):
        return self.info(key)

    def get_name(self, portal_id):
        """Return a user name in a tuple. (firstname, lastname)
        
        :param portal_id: the unique portal id
        :type portal_id: str
        :returns: tuple

        """
        ldap_data = self.db_users.find({"cm_user_id": portal_id})
        if ldap_data.count() > 0:
            ldap_info = ldap_data[0]
            (first_name, last_name) = (ldap_info['firstname'], ldap_info['lastname'])

            return (first_name, last_name)

    def set_password(self, username, password, cloud):
        """Store a user password for a cloud

        :param username: OS_USERNAME
        :type username: str
        :param password: OS_PASSWORD
        :type password: str
        :param cloud: the cloud name e.g. sierra_openstack_grizzly
        :type cloud: str

        """
        self.userdb_passwd.insert({"username":username, "password":password,
                                   "cloud": cloud})

