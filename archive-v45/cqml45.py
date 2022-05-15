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
                    node = {"file":file.name,"project":folder.name, "yml": yml}
                    tree.append(node)
    return tree

def convert(root, node):
    dir = node["project"]
    file = ''.join([c for c in node["file"] if not c.isdigit()])
    prefix = file.split("_")[0]
    name = file.split("_")[1]
    if prefix == "rnr": dir = prefix
    if prefix == "sierra": name = f"{prefix}.yml"
    path = os.path.join(root, dir, name)
    yml = node["yml"]
    del yml["meta"]
    yml["cqml"] = 0.5
    yml["project"] = dir
    yml["package"] = name
    write_yaml(path, yml)
    return path

t = extract(R4)
print(f"\nExtracted: {len(t)} files\n")
#print(t[0]["yml"])
for n in t:
    print(n["file"])
    p = convert(R5, n)
    print("\t",p)
