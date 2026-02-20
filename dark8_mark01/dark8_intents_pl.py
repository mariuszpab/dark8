# dark8_intents_pl.py
# Rozpoznawanie intencji z komend w języku polskim + integracja z uczeniem

import re
from dark8_mark01.dark8_learning import merge_learned_intents


INTENT_PATTERNS = [
    # DIAGNOSTYKA
    {
        "typ": "diagnostyka",
        "wzorce": [
            r"\bdiagnostyk[ai]\b",
            r"\bdiagnoz[auę]\b",
            r"\bsprawd[źz] (się|system)\b",
            r"\bprzeskanuj system\b",
        ],
    },
    # NAPRAWA
    {
        "typ": "naprawa",
        "wzorce": [
            r"\bnapraw\b",
            r"\bnapraw (się|system)\b",
            r"\bzrób self ?repair\b",
            r"\bogarnij się\b",
        ],
    },
    # USPRAWNIENIA / ANALIZA
    {
        "typ": "usprawnienia",
        "wzorce": [
            r"\bco (możemy|mozemy) usprawni[ćc]\b",
            r"\bjak (poprawi[ćc]|przyspieszy[ćc])\b",
            r"\bprzeanalizuj (system|swoje pliki|strukturę|strukture)\b",
        ],
    },
    # CELE / AGENT
    {
        "typ": "cele",
        "wzorce": [
            r"\bpoka[żz] cele\b",
            r"\bjakie mam cele\b",
            r"\blista cel[óo]w\b",
            r"\bcele\b",
            r"\bzadania\b",
            r"\bplany\b",
        ],
    },
    # JOBY / PROCESY
    {
        "typ": "joby",
        "wzorce": [
            r"\bpoka[żz] joby\b",
            r"\bjakie procesy (dzia[łl]aj[ąa])\b",
            r"\bprocesy\b",
            r"\bjoby\b",
        ],
    },
    # META-AGENT
    {
        "typ": "meta_agent",
        "wzorce": [
            r"\buruchom meta[- ]agenta\b",
            r"\bmeta[- ]agent\b",
            r"\bmeta agent\b",
        ],
    },
    # UPGRADE
    {
        "typ": "upgrade",
        "wzorce": [
            r"\bupgrade dark8\b",
            r"\bzaktualizuj system\b",
            r"\bzrób upgrade\b",
        ],
    },
    # DIALOG / CHAT
    {
        "typ": "dialog",
        "wzorce": [
            r"\btryb dialogow[y]\b",
            r"\bchat\b",
            r"\bporozmawiajmy\b",
        ],
    },
]

# Łączenie wyuczonych intencji z bazowymi
INTENT_PATTERNS = merge_learned_intents(INTENT_PATTERNS)


def rozpoznaj_intencje(tekst: str) -> dict | None:
    """
    Zwraca słownik z intencją, np.:
      {"typ": "diagnostyka"}
    albo None, jeśli nic nie pasuje.
    """
    low = tekst.lower().strip()

    for intent in INTENT_PATTERNS:
        typ = intent["typ"]
        for wzorzec in intent["wzorce"]:
            if re.search(wzorzec, low):
                return {"typ": typ}

    return None
