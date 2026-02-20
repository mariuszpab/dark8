import os

def generate_code(language: str, prompt: str) -> str:
    """
    Generuje kod w wybranym języku na podstawie promptu.
    """
    header = f"// Kod wygenerowany przez DARK8 OS\n// Język: {language}\n\n"
    body = f"// TODO: implementacja na podstawie promptu:\n// {prompt}\n"
    return header + body
