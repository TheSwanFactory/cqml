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
    keys = [os.path.splitext(file)[0] for file in files if file.endswith("ml")]
    keys.sort()
    print(keys)
    return keys
