import os, yaml
from .keys import *
from .wrappers import CQML, pkg_cvm

def read_yaml(yaml_file):
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
        return raw_yaml

class Root:
    def __init__(self, root):
        self.root = root.split("/")[-1]
        self.pipes = {}
        self.env = {}
        self.scan(root)

    def keys(self): return list(self.pipes.keys())

    def add_env(self, yml, key):
        if not kEnv in yml: return {}
        self.env[key] = yml[kEnv]
        return yml[kEnv]

    def set_env(self, yml, key):
        print(f'set_env:{key}')
        folder = yml[kEnv]["project"]
        env = {}
        if self.root in self.env: env.update(self.env[self.root])
        print(f'set_env.root:{env}')
        if folder in self.env: env.update(self.env[folder])
        print(f'set_env.folder:{env}')
        if kEnv in yml: env.update(yml[kEnv])
        print(f'set_env.kEnv:{env}')
        yml[kEnv] = env
        return env

    def new(self, spark, key, debug=False):
        pipe = self.pipes[key]
        self.set_env(pipe, key)
        cvm = CQML(pipe, spark)
        if debug: cvm.debug = True
        return cvm

    def pkg(self, spark, key, debug=False):
        cvm = self.new(spark, key, debug)
        cvm.run();
        return pkg_cvm(cvm)

    def pkg_all(self, spark, debug=False):
        pkgs = {key:self.pkg(spark, key, debug) for key in self.keys()}
        return pkgs

    def scan(self, root):
        for entry in os.scandir(root):
            self.parse(entry, root)

    def parse(self, entry, folder):
        name = entry.name
        if name.endswith(".yml"):
            yml = read_yaml(entry.path)
            file_key = os.path.splitext(name)[0]
            folder_key = folder.split("/")[-1]
            env = self.add_env(yml, folder_key)
            key = f"{folder_key}/{file_key}"
            source = {
                "file": name,
                "package": file_key,
                "project": folder_key,
                "key": key,
                "path": entry.path,
            }
            env.update(source)
            yml[kEnv] = env
            self.pipes[key] = yml
        elif entry.is_dir():
            print(entry.name)
            self.scan(entry.path)
