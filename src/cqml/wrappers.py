import yaml
import os,shutil
from operator import itemgetter
from .db2quilt import cvm2pkg, extract_pkg
from .cvm import CVM

class CQML(CVM):
    def __init__(self, yaml_data, spark):
        super().__init__(yaml_data, spark)

    def do_report(self, action):
        if not self.pkg: self.pkg = extract_pkg(self)
        id, from_key,cdict = itemgetter('id','from','cols',)(action)
        df_from = self.get_frame(from_key)
        self.pkg.save_notebook(df_from, id, cdict)
        return df_from

    def do_run(self, action):
        runs = action['pipes']
        pkgs = {cqml:pkg_cqml(cqml, self.spark) for cqml in runs}
        return pkgs

    def do_save(self, action):
        pkg = cvm2pkg(self, False) # do not re-run
        return pkg

def upgrade_file(yaml_file):
    print("Upgrading "+yaml_file)
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
    with open(yaml_file, 'w') as file:
        yaml.dump(raw_yaml, file, sort_keys=False)

def from_file(yaml_file, spark):
    print("Loading "+yaml_file)
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
        return CQML(raw_yaml, spark)

def make_frames(yaml_file, spark, debug=False):
    cvm = from_file(yaml_file, spark)
    if debug: cvm.debug = True
    cvm.run()
    return cvm

def reload_cqml(cvm, name, folder="pipes"):
    yaml_file=f"{folder}/{name}.yml"
    cvm.reload(yaml_file)
    return cvm

def load_cqml(name, spark, folder="pipes"):
    yaml_file=f"{folder}/{name}.yml"
    return from_file(yaml_file, spark)

def exec_cqml(name, spark, folder="pipes"):
    cvm = load_cqml(name, spark, folder)
    cvm.run()
    return cvm

def pkg_cqml(name, spark, folder="pipes"):
    print("\npkg_cqml: "+name)
    cvm = exec_cqml(name, spark, folder)
    pkg = cvm2pkg(cvm, False)
    return {
    'pkg': pkg,
    'html': pkg.html,
    'url': pkg.url,
    'actions': cvm.actions,
    'sizes': cvm.sizes,
    'times': cvm.times,
    'frames': cvm.df,
    }

def yml_keys(folder="pipes"):
    files = os.listdir(folder)
    keys = [os.path.splitext(file)[0] for file in files if file.endswith("ml")]
    keys.sort()
    print(keys)
    return keys

def pkg_all(spark, folder="pipes"):
    keys = yml_keys(folder)
    pkgs = {key:pkg_cqml(key, spark, folder) for key in keys}
    return pkgs
