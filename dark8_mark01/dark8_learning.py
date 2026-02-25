# dark8_learning.py
# Mechanizm uczenia się nowych form komend w języku polskim

import json
import os

LEARNING_FILE = os.path.join(os.path.dirname(__file__), "learned_intents.json")


def load_learned_intents():
    """Wczytuje wyuczone formy komend z pliku JSON."""
    if not os.path.exists(LEARNING_FILE):
        return {}

    try:
        with open(LEARNING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_learned_intents(data: dict):
    """Zapisuje wyuczone formy komend do pliku JSON."""
    with open(LEARNING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def learn_new_form(tekst: str, typ: str):
    """
    Dodaje nową formę komendy do pamięci.
    """
    data = load_learned_intents()

    if typ not in data:
        data[typ] = []

    if tekst not in data[typ]:
        data[typ].append(tekst)

    save_learned_intents(data)


def merge_learned_intents(intents_patterns):
    """
    Łączy wyuczone formy z istniejącymi wzorcami intencji.
    """
    learned = load_learned_intents()

    for typ, patterns in learned.items():
        for p in patterns:
            for intent in intents_patterns:
                if intent["typ"] == typ:
                    escaped = p.lower().strip()
                    if escaped not in intent["wzorce"]:
                        intent["wzorce"].append(escaped)

    return intents_patterns
