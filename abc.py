import platform

print platform.machine()
print platform.node()
print platform.processor()
print platform.python_implementation()
print platform.python_revision()
print platform.python_version()

release = platform.release()
system = platform.system()
version = platform.version()

print release
print system
print version

print platform.system_alias(system, release, version)


print platform.uname()

print platform.mac_ver()
