#!/usr/bin/env python3
import pytest, sys

#
# Take two paths: root4 root5
# Copy files in each subfolder
# Strip out meta
# Strip leading numbers
#

def convert(root4, root5):
    for folder in os.listdir(root4):
        print(file)
        upgrade_file(file)

def upgrade_file(yaml_file):
    print("Upgrading "+yaml_file)
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
    # insert converter here
    with open(yaml_file, 'w') as file:
        yaml.dump(raw_yaml, file, sort_keys=False)

if len(sys.argv) > 2:
    convert(sys.argv[1], sys.argv[2])
else:
    print("cqml45 root4 root5 (requires 2 arguments)")
