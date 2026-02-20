from dark8_mark01.core.vfs.dark8_vfs import Dark8VFS


class Dark8VFSManager:
    """
    Warstwa pośrednia – API dla File Managera i Terminala.
    """

    _instance = None

    def __init__(self):
        self.vfs = Dark8VFS.instance()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Dark8VFSManager()
        return cls._instance

    def list_dir(self, path="/"):
        return self.vfs.list(path)

    def create_dir(self, path):
        self.vfs.mkdir(path)

    def create_file(self, path):
        self.vfs.touch(path)

    def write_file(self, path, data):
        self.vfs.write(path, data)

    def read_file(self, path):
        return self.vfs.read(path)

    def delete(self, path):
        self.vfs.delete(path)
