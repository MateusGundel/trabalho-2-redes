import os


def files_to_dict(path_):
    for root, dirs, files in os.walk(path_):
        tree = {d: files_to_dict(os.path.join(root, d)) for d in dirs}
        tree.update({f: os.path.getsize(os.path.join(root, f)) for f in files})
        return tree
