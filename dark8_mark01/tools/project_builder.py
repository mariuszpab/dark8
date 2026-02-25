import os


def create_project(path: str, template: str = "default"):
    os.makedirs(path, exist_ok=True)

    if template == "python":
        os.makedirs(os.path.join(path, "src"), exist_ok=True)
        with open(os.path.join(path, "main.py"), "w") as f:
            f.write("# Entry point\n")

    if template == "web":
        os.makedirs(os.path.join(path, "static"), exist_ok=True)
        os.makedirs(os.path.join(path, "templates"), exist_ok=True)
        with open(os.path.join(path, "index.html"), "w") as f:
            f.write("<html><body>Hello DARK8</body></html>")

    return f"Utworzono projekt: {path}"
