import sys
#print sys.path


from cloudmesh.cm_profile import cm_profile
from pprint import pprint


p = cm_profile()

print p.config
print p.server


pprint (p.data)

print 70 * "-"
pprint (p.get("abc"))

print 70 * "-"
p.write ("abc", {"hallo": "world"})
p.update ("abc", {"moon": "sun"})
pprint (p.get("abc"))

print 70 * "-"
p.write ("abc", {"saturn": "jupiter"})
pprint (p.get("abc"))

"""
from cloudmesh.cloudmesh import cloudmesh


c = cloudmesh()

print c.clouds
"""
