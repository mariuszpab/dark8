# dark8_context_parser.py
# Parser kontekstu i poleceń złożonych w języku polskim

from dark8_mark01.dark8_intents_pl import rozpoznaj_intencje


SEPARATORY = [
    " i ",
    " oraz ",
    " potem ",
    " następnie ",
    " najpierw ",
    " później ",
]

WARUNKI = [
    "jeśli ",
    "jezeli ",
    "gdy ",
    "w przypadku gdy ",
]


def podziel_na_segmenty(tekst: str) -> list:
    """
    Rozbija zdanie na segmenty według spójników.
    """
    low = tekst.lower()

    for sep in SEPARATORY:
        if sep in low:
            parts = [p.strip() for p in low.split(sep) if p.strip()]
            return parts

    return [low]


def wykryj_warunek(segment: str) -> dict:
    """
    Wykrywa konstrukcje warunkowe typu:
    'jeśli są błędy, napraw system'
    """
    for w in WARUNKI:
        if w in segment:
            warunek, akcja = segment.split(w, 1)
            return {
                "typ": "warunek",
                "warunek": warunek.strip(),
                "akcja": akcja.strip(),
            }

    return None


def analizuj_polecenie_zlozone(tekst: str) -> list:
    """
    Zwraca listę akcji do wykonania w kolejności.
    Każda akcja to dict: {"typ": "diagnostyka"} itd.
    """
    segmenty = podziel_na_segmenty(tekst)
    akcje = []

    for seg in segmenty:
        # sprawdzamy warunek
        war = wykryj_warunek(seg)
        if war:
            akcje.append(war)
            continue

        # sprawdzamy intencję
        intent = rozpoznaj_intencje(seg)
        if intent:
            akcje.append(intent)
            continue

        # nieznane → język naturalny
        akcje.append({"typ": "natural", "tekst": seg})

    return akcje
