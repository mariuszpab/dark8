# actions.py
# DARK8 OS — Warstwa wykonawcza (system + pliki + procesy)

import os
import shutil
import subprocess


# --- APLIKACJE / PROCESY ---

def run_app(app_name: str):
    try:
        subprocess.Popen(app_name)
        return f"Uruchamiam aplikację: {app_name}"
    except Exception as e:
        return f"Błąd uruchamiania aplikacji: {e}"


def run_python_script(path: str):
    try:
        result = subprocess.run(["python", path], capture_output=True, text=True)
        return result.stdout or result.stderr
    except Exception as e:
        return f"Błąd uruchamiania skryptu: {e}"


# --- SYSTEM PLIKÓW ---

def delete_file(path: str):
    try:
        os.remove(path)
        return f"Usunięto plik: {path}"
    except Exception as e:
        return f"Błąd usuwania pliku: {e}"


def make_dir(path: str):
    try:
        os.makedirs(path, exist_ok=True)
        return f"Utworzono katalog: {path}"
    except Exception as e:
        return f"Błąd tworzenia katalogu: {e}"


def remove_dir(path: str):
    try:
        shutil.rmtree(path)
        return f"Usunięto katalog: {path}"
    except Exception as e:
        return f"Błąd usuwania katalogu: {e}"


def read_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Błąd odczytu pliku: {e}"


def write_file(path: str, content: str):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Zapisano plik: {path}"
    except Exception as e:
        return f"Błąd zapisu pliku: {e}"


def append_to_file(path: str, content: str):
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"Dodano treść do pliku: {path}"
    except Exception as e:
        return f"Błąd dopisywania do pliku: {e}"


def touch_file(path: str):
    try:
        with open(path, "a", encoding="utf-8"):
            os.utime(path, None)
        return f"Utworzono/odświeżono plik: {path}"
    except Exception as e:
        return f"Błąd tworzenia pliku: {e}"


def copy_file(src: str, dst: str):
    try:
        shutil.copy2(src, dst)
        return f"Skopiowano plik z {src} do {dst}"
    except Exception as e:
        return f"Błąd kopiowania pliku: {e}"


def move_file(src: str, dst: str):
    try:
        shutil.move(src, dst)
        return f"Przeniesiono z {src} do {dst}"
    except Exception as e:
        return f"Błąd przenoszenia pliku: {e}"


# --- KATALOGI / SHELL ---

def list_dir(path: str = "."):
    try:
        entries = os.listdir(path)
        return "\n".join(entries)
    except Exception as e:
        return f"Błąd listowania katalogu: {e}"


def change_dir(path: str):
    try:
        os.chdir(path)
        return f"Zmieniono katalog na: {os.getcwd()}"
    except Exception as e:
        return f"Błąd zmiany katalogu: {e}"


def show_cwd():
    try:
        return os.getcwd()
    except Exception as e:
        return f"Błąd pobierania aktualnego katalogu: {e}"
