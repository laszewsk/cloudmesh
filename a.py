
import yaml

attributes = """
hosts: i[001-i010]
start: +1d
end: +1d
user: gregor,oliver
project: fg82
kind: vm-reservation
label: my reservation
comment: This is part of a big project
"""

reservation = yaml.load(attributes)

print yaml.dump(reservation)

print reservation['label']
