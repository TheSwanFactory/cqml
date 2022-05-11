#!/usr/bin/env python3
import pytest, sys
from .context import cqml

if len(sys.argv) > 1:
    files = sys.argv[1:]
    for file in files:
        print(file)
        upgrade_file(file)

def upgrade_file(yaml_file):
    print("Upgrading "+yaml_file)
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
    # insert converter here
    with open(yaml_file, 'w') as file:
        yaml.dump(raw_yaml, file, sort_keys=False)
