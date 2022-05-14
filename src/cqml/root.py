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

    def new(self, spark, key, debug=False):
        pipe = self.pipes[key]
        cvm = CVM(pipe, spark)
        if debug: cvm.debug = True
        return cvm

    def scan(self, root):
        for entry in os.scandir(root):
            self.parse(entry, root)

    def parse(self, entry, folder):
        name = entry.name
        if name.endswith(".yml"):
            file_key = os.path.splitext(name)[0]
            folder_key = folder.split("/")[-1]
            key = f"{folder_key}/{file_key}"
            yml = read_yaml(entry.path)
            yml["source"] = {
                "file": name,
                "file_key": file_key,
                "folder": folder,
                "key": key,
                "path": entry.path,
             }
            self.pipes[key] = yml
            if kEnv in yml: self.env[folder] = yml[kEnv]
        elif entry.is_dir():
            print(entry.name)
            self.scan(entry.path)
