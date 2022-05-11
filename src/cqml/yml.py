import yaml
import os,shutil
from operator import itemgetter
from .db2quilt import cvm2pkg, extract_pkg
from .cvm import CVM

def upgrade_file(yaml_file):
    print("Upgrading "+yaml_file)
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
    # insert converter here
    with open(yaml_file, 'w') as file:
        yaml.dump(raw_yaml, file, sort_keys=False)

def yml_keys(folder="pipes"):
    files = os.listdir(folder)
    print(files)
    keys = [os.path.splitext(file)[0] for file in files if file.endswith("ml")]
    keys.sort()
    print(keys)
    return keys

def yml_tree(folder="pipes"):
    keys = extract(folder)
    return keys

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
