import time
import sys
import traceback
from os import environ as env
# import novaclient
import pprint
import novaclient.client
nova = novaclient.client.Client("1.1", auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                api_key=env['OS_PASSWORD'],
                                project_id=env['OS_TENANT_NAME'],
                                # region_name=env['OS_REGION_NAME']
                                )



class OSError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

def boot_template(image,flavor,keypair):
    try:
        _image=nova.images.find(name=image)
        if (not _image):
            raiseOSError("image %s not found" % image)
        _flavor=nova.flavors.find(name=flavor)
        if (not _flavor):
            raiseOSError("flavor %s not found" % flavor)
        _keypair=nova.keypairs.find(name=keypair)
        if (not _keypair):
            raiseOSError("keypair %s not found" % keypair)
        return (_image,_flavor,_keypair)
    except novaclient.exceptions.NotFound:
        print "Not found: " , sys.exc_value
        return None
    except:
        traceback.print_exc()
        print "Unexpected error:", sys.exc_info()[0]


def boot ():
    print "boot"
    print(nova.servers.list())
    image = nova.images.find(name="centos7")
    flavor = nova.flavors.find(name="m1.large")
    net = nova.networks.find(label="mgmt-net")
    nics = [{'net-id': net.id}]
    instance = nova.servers.create(name="c99", image=image, flavor=flavor, key_name="dell4", nics=nics)

    print instance.id
    print("Sleeping for 5s after create command")
    time.sleep(5)
    print(nova.servers.list())

def net ():
    print "net"

def check_keypair(name):
    try:
        return not ( nova.keypairs.get(name).deleted )
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

# boot()
# net()
# pprint.pprint ( nova )

# print "checking keypair dell4"
# print check_keypair('dell4')

srv_template = boot_template("centos7","m1.large","dell4")
pprint.pprint(srv_template)
srv_template2 = boot_template("centos6","m1.big","dell9")
pprint.pprint(srv_template2)

