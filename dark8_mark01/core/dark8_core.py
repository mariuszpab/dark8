# dark8_core.py
# DARK8 OS — główny runtime komend (NLP + shell-like)

from dark8_mark01.nlp.intent_runtime import IntentClassifier
from dark8_mark01.core.dispatcher import dispatch


classifier = IntentClassifier()


def parse_arguments(intent: str, text: str):
    # --- SYSTEM COMMANDS ---
    if intent == "LIST_DIR":
        parts = text.split()
        if len(parts) > 1:
            return {"path": parts[1]}
        return {"path": "."}

    if intent == "CHANGE_DIR":
        return {"path": text.split()[-1]}

    if intent == "RUN_PYTHON_SCRIPT":
        return {"path": text.split()[-1]}

    if intent == "SHOW_CWD":
        return {}

    if intent == "COPY_FILE":
        parts = text.split()
        return {"src": parts[1], "dst": parts[2]}

    if intent == "MOVE_FILE":
        parts = text.split()
        return {"src": parts[1], "dst": parts[2]}

    if intent == "TOUCH_FILE":
        return {"path": text.split()[-1]}

    # --- APP / FILE OPS (NLP-BASED) ---
    if intent in ["RUN_APP"]:
        return {"app_name": text.split()[-1]}

    if intent in ["DELETE_FILE", "READ_FILE"]:
        return {"path": text.split()[-1]}

    if intent == "MAKE_DIR":
        return {"path": text.split()[-1]}

    if intent == "WRITE_FILE":
        parts = text.split("::")
        return {"path": parts[0].split()[-1], "content": parts[1]}

    if intent == "GENERATE_CODE":
        # np.: generate code python: zrób coś tam
        # uproszczone: ostatnie słowo = język, reszta = prompt
        parts = text.split(":", 1)
        language = "python"
        prompt = text
        if len(parts) == 2:
            language = parts[0].split()[-1]
            prompt = parts[1].strip()
        return {"language": language, "prompt": prompt}

    if intent == "CREATE_PROJECT":
        parts = text.split()
        path = parts[-1]
        template = "python" if "python" in text.lower() else "default"
        return {"path": path, "template": template}

    if intent == "EDIT_FILE":
        # np.: edit file path :: content
        parts = text.split("::")
        return {"path": parts[0].split()[-1], "content": parts[1]}

    if intent == "OVERWRITE_FILE":
        parts = text.split("::")
        return {"path": parts[0].split()[-1], "content": parts[1]}

    if intent == "BUILD_PROJECT":
        return {"path": text.split()[-1]}

    return {}


def dark8_execute(text: str):
    # --- SHELL-LIKE COMMANDS BEZ NLP ---
    stripped = text.strip()

    if stripped.startswith("dir") or stripped.startswith("ls"):
        parts = stripped.split()
        path = parts[1] if len(parts) > 1 else "."
        return "LIST_DIR", dispatch("LIST_DIR", {"path": path})

    if stripped.startswith("cd "):
        path = stripped.split(" ", 1)[1]
        return "CHANGE_DIR", dispatch("CHANGE_DIR", {"path": path})

    if stripped.startswith("python "):
        path = stripped.split(" ", 1)[1]
        return "RUN_PYTHON_SCRIPT", dispatch("RUN_PYTHON_SCRIPT", {"path": path})

    if stripped in ["pwd"]:
        return "SHOW_CWD", dispatch("SHOW_CWD", {})

    if stripped.startswith("mkdir "):
        path = stripped.split(" ", 1)[1]
        return "MAKE_DIR", dispatch("MAKE_DIR", {"path": path})

    if stripped.startswith("rmdir "):
        path = stripped.split(" ", 1)[1]
        return "REMOVE_DIR", dispatch("REMOVE_DIR", {"path": path})

    if stripped.startswith("rm ") or stripped.startswith("del "):
        path = stripped.split(" ", 1)[1]
        return "DELETE_FILE", dispatch("DELETE_FILE", {"path": path})

    if stripped.startswith("cp "):
        parts = stripped.split()
        if len(parts) >= 3:
            return "COPY_FILE", dispatch("COPY_FILE", {"src": parts[1], "dst": parts[2]})

    if stripped.startswith("mv "):
        parts = stripped.split()
        if len(parts) >= 3:
            return "MOVE_FILE", dispatch("MOVE_FILE", {"src": parts[1], "dst": parts[2]})

    if stripped.startswith("touch "):
        path = stripped.split(" ", 1)[1]
        return "TOUCH_FILE", dispatch("TOUCH_FILE", {"path": path})

    if stripped.startswith("cat ") or stripped.startswith("type "):
        path = stripped.split(" ", 1)[1]
        return "READ_FILE", dispatch("READ_FILE", {"path": path})

    # --- RESZTA PRZEZ NLP ---
    intent = classifier.predict(text)
    args = parse_arguments(intent, text)
    result = dispatch(intent, args)
    return intent, result


if __name__ == "__main__":
    while True:
        cmd = input("DARK8 > ")
        intent, result = dark8_execute(cmd)
        print(f"[{intent}] {result}")
