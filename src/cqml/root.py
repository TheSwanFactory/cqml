import os, yaml

class Root:
    def __init__(self, root):
        self.nodes = []
        self.scan(root)

    def scan(self, root):
        for entry in os.scandir(root):
            self.parse(entry, root)

    def parse(self, entry, folder):
        if entry.name.endswith(".yml"):
            key = os.path.splitext(entry.name)[0]
            yml = read_yaml(entry.path)
            node = {
                "file":entry.name,
                "folder":folder,
                "path": entry.path,
                 "key": key,
                 "fkey": f"{folder}.{key}",
                 "yml": yml
             }
            self.nodes.append(node)
        elif entry.is_dir():
            print(entry.name)
            self.scan(entry.name)
