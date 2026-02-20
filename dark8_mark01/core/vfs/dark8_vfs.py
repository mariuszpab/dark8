from dark8_mark01.core.vfs.dark8_vfs_node import VFSNode


class Dark8VFS:
    """
    Minimalistyczny Virtual File System dla DARK8.
    """

    _instance = None

    def __init__(self):
        self.root = VFSNode("/", True)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Dark8VFS()
        return cls._instance

    # ===== PATH PARSER =====
    def _resolve(self, path: str):
        if path == "/":
            return self.root

        parts = [p for p in path.split("/") if p]
        node = self.root

        for part in parts:
            if not node.is_dir:
                return None
            node = node.get_child(part)
            if node is None:
                return None

        return node

    # ===== DIRECTORY OPERATIONS =====
    def mkdir(self, path: str):
        parent_path = "/".join(path.split("/")[:-1])
        name = path.split("/")[-1]

        parent = self._resolve(parent_path if parent_path else "/")
        if parent is None or not parent.is_dir:
            raise Exception("Invalid path")

        if name in parent.children:
            raise Exception("Directory already exists")

        parent.add_child(VFSNode(name, True))

    # ===== FILE OPERATIONS =====
    def touch(self, path: str):
        parent_path = "/".join(path.split("/")[:-1])
        name = path.split("/")[-1]

        parent = self._resolve(parent_path if parent_path else "/")
        if parent is None or not parent.is_dir:
            raise Exception("Invalid path")

        parent.add_child(VFSNode(name, False))

    def write(self, path: str, data: str):
        node = self._resolve(path)
        if node is None or node.is_dir:
            raise Exception("Invalid file")
        node.content = data

    def read(self, path: str):
        node = self._resolve(path)
        if node is None or node.is_dir:
            raise Exception("Invalid file")
        return node.content

    def delete(self, path: str):
        parent_path = "/".join(path.split("/")[:-1])
        name = path.split("/")[-1]

        parent = self._resolve(parent_path if parent_path else "/")
        if parent is None or not parent.is_dir:
            raise Exception("Invalid path")

        parent.remove_child(name)

    # ===== LIST DIRECTORY =====
    def list(self, path: str):
        node = self._resolve(path)
        if node is None or not node.is_dir:
            raise Exception("Invalid directory")
        return list(node.children.keys())
