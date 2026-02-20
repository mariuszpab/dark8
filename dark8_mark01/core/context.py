class Context:
    """
    Prosty kontekst agenta — na razie tylko katalog roboczy.
    """

    def __init__(self, root_dir: str | None = None):
        import os

        self.root_dir = root_dir or os.getcwd()
