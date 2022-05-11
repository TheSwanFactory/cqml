#!/usr/bin/env python3
import os, yaml

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
                    yml = read_yaml(file.path)
                    file5 = ''.join([c for c in file.name if not c.isdigit()])
                    path5 = os.path.join(folder.name, file5)
                    node = {"path":path5, "yml": yml}
                    tree.append(node)
    return tree


def write_yaml(yaml_file, raw_yaml):
    with open(yaml_file, 'w') as file:
        yaml.dump(raw_yaml, file, sort_keys=False)

t = extract(R4)
print(f"\nExtracted: {len(t)} files\n")
for n in t:
    print(n["path"])
