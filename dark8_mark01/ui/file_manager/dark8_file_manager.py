import os


class Dark8FileManager:
    """
    Logika systemu plików DARK8‑OS.
    """

    def list_directory(self, path: str):
        """
        Zwraca listę plików i folderów w katalogu.
        """
        try:
            entries = os.listdir(path)
        except Exception as e:
            return [], f"Błąd: {e}"

        files = []
        for entry in entries:
            full_path = os.path.join(path, entry)
            is_dir = os.path.isdir(full_path)
            files.append((entry, full_path, is_dir))

        return files, None
