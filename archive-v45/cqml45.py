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

def write_yaml(yaml_file, raw_yaml):
    with open(yaml_file, 'w') as file:
        yaml.dump(raw_yaml, file, sort_keys=False)

def extract(root):
    tree = []
    for folder in os.scandir(root):
        if folder.is_dir():
            print(folder.name)
            for file in os.scandir(folder.path):
                if file.name.endswith(".yml"):
                    yml = read_yaml(file.path)
                    node = {"file":file.name, "folder":folder.name, "yml": yml}
                    tree.append(node)
    return tree

def convert(root, node):
    file = ''.join([c for c in node["file"] if not c.isdigit()])
    path = os.path.join(root, node["folder"], file)
    yml = node["yml"]
    del yml["meta"]
    yml["cqml"] = 0.5
    yml["project"] = node["folder"]
    yml["package"] = file
    write_yaml(path, yml)
    return path

t = extract(R4)
print(f"\nExtracted: {len(t)} files\n")
print(t[0]["yml"])
for n in t:
    print(n["file"])
    p = convert(R5, n)
    print("\t",p)
