class VFSNode:
    """
    Węzeł VFS – plik lub katalog.
    """

    def __init__(self, name: str, is_dir: bool):
        self.name = name
        self.is_dir = is_dir
        self.children = {} if is_dir else None
        self.content = "" if not is_dir else None

    def add_child(self, node):
        if not self.is_dir:
            raise Exception("Cannot add child to file")
        self.children[node.name] = node

    def get_child(self, name):
        if not self.is_dir:
            return None
        return self.children.get(name)

    def remove_child(self, name):
        if not self.is_dir:
            return
        if name in self.children:
            del self.children[name]
