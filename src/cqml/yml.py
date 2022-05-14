import os, yaml

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

def yml_folder(folder, nodes):
    print(folder.name)
    for entry in os.scandir(folder.path):
        if entry.name.endswith(".yml"):
            key = os.path.splitext(entry.name)[0]
            #yml = read_yaml(entry.path)
            node = {"file":entry.name, "folder":folder.name, "path": entry.path, "key": key}
            nodes.append(node)
        elif entry.is_dir():
            print(folder.name)
            yml_folder(folder, tree)
    return nodes

def extract(root):
    tree = []
    for folder in os.scandir(root):
        if folder.is_dir():
            print(folder.name)
            yml_folder(folder, tree)
    return tree
