import yaml
from .sangam import cvm2quilt
from .cvm import CVM
from .cqml12 import ensure_v02

LOAD_FOLDER="pipes"

class Runner(CVM):
    def __init__(self, yaml_data, spark):
        super().__init__(yaml_data, spark)

    def do_run(self, action):
        runs = action['pipes']
        pkgs = {cqml:pkg_cqml(cqml, self.spark) for cqml in runs}
        return pkgs

def upgrade_file(yaml_file):
    print("Upgrading "+yaml_file)
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
        v02 = ensure_v02(raw_yaml)
    print(v02)
    with open(yaml_file, 'w') as file:
        yaml.dump(v02, file, sort_keys=False)

def from_file(yaml_file, spark):
    print("Loading "+yaml_file)
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
        v02 = ensure_v02(raw_yaml)
        return Runner(v02, spark)

def make_frames(yaml_file, spark):
    cvm = from_file(yaml_file, spark)
    cvm.run()
    return cvm

def load_cqml(name, spark):
    yaml_file=f"{LOAD_FOLDER}/{name}.yml"
    return from_file(yaml_file, spark)

def exec_cqml(name, spark):
    cvm = load_cqml(name, spark)
    cvm.run()
    return cvm

def pkg_cqml(name, spark):
    print("\npkg_cqml: "+name)
    cvm = exec_cqml(name, spark)
    pkg = cvm2quilt(cvm, name)
    return {'pkg': pkg, 'html': pkg.html, 'cvm': cvm.actions}
