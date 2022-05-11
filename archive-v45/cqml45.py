#!/usr/bin/env python3
import os, sys, yaml

#
# Take two paths: root4 root5
# Copy files in each subfolder
# Strip out meta
# Strip leading numbers
#

ROOT="/Users/nauto/Developer"
R4=f"{ROOT}/it/databricks"
R5=f"{ROOT}/dbt/cqml"

def read_yaml(yaml_file):
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
        return raw_yaml

def extract(root):
    tree = []
    for folder in os.scandir(root):
        if folder.is_dir():
            print(folder.name)
            for file in os.scandir(folder.path):
                if file.name.endswith(".yml"):
                    print(file.name)
                    yml = read_yaml(file.path)
                    node = {"folder":folder.name, "file": file.name, "yml": yml}
                    tree.append(node)
    return tree


def write_yaml(yaml_file, raw_yaml):
    with open(yaml_file, 'w') as file:
        yaml.dump(raw_yaml, file, sort_keys=False)

t = extract(R4)
print("\nextracted\n")
[print(n["file"]) for n in t]
