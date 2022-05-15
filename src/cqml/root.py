import os, yaml
from .keys import *
from .cvm import CVM

def read_yaml(yaml_file):
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
        return raw_yaml

class Root:
    def __init__(self, root):
        self.root = root
        self.pipes = {}
        self.env = {}
        self.scan(root)

    def keys(self): return list(self.pipes.keys())

    def add_env(self, yml, key):
        if not kEnv in yml: return {}
        self.env[key] = yml[kEnv]
        return yml[kEnv]

    def set_env(self, yml, key):
        folder = yml[kEnv]["folder"]
        env = {}
        if self.root in self.env: env.update(self.env[self.root])
        if folder in self.env: env.update(self.env[folder])
        if kEnv in yml: env.update(yml[kEnv])
        yml[kEnv] = env
        return env

    def new(self, spark, key, debug=False):
        pipe = self.pipes[key]
        self.set_env(pipe, key)
        cvm = CVM(pipe, spark)
        if debug: cvm.debug = True
        return cvm

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
                "file_key": file_key,
                "folder": folder,
                "key": key,
                "path": entry.path,
            }
            env.update(source)
            yml[kEnv] = env
            self.pipes[key] = yml
        elif entry.is_dir():
            print(entry.name)
            self.scan(entry.path)
