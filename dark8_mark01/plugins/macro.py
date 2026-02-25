from ..command_registry import register_command
from ..mpx_parser import parse_mpx_file

# Słownik makr: nazwa → treść
_macros = {}


def handle_macro_define(command, args, block):
    """
    MACRO <name>
    <<<END
    ...treść makra...
    END
    """
    name = args.strip()

    if not name:
        print("[ERROR][MACRO] Brak nazwy makra.")
        return

    if not block:
        print("[ERROR][MACRO] Makro musi mieć blok z treścią.")
        return

    _macros[name] = block
    print(f"[MACRO] Zdefiniowano makro: {name}")


def handle_macro_call(command, args, block):
    """
    Wywołanie makra:
    <nazwa>
    """
    name = command  # nazwa komendy to nazwa makra

    if name not in _macros:
        print(f"[ERROR][MACRO] Makro '{name}' nie istnieje.")
        return

    print(f"[MACRO] Wywołuję makro: {name}")

    # Treść makra traktujemy jak osobny skrypt MPX
    try:
        parse_mpx_file(None, inline_text=_macros[name])
    except Exception as e:
        print(f"[ERROR][MACRO] Błąd w makrze '{name}': {e}")


def register():
    # Rejestrujemy komendę MACRO (definicja)
    register_command("MACRO", handle_macro_define)

    # Rejestrujemy dynamiczny handler dla WSZYSTKICH makr
    # (będzie wywoływany, jeśli nazwa komendy nie pasuje do niczego innego)
    def dynamic_macro_handler(command, args, block):
        if command in _macros:
            return handle_macro_call(command, args, block)
        print(f"[ERROR][MACRO] Nieznana komenda: {command}")

    # Rejestrujemy dynamiczny handler jako fallback
    register_command("*MACRO_FALLBACK*", dynamic_macro_handler)

    print("[INFO][PLUGINS] Plugin MACRO zarejestrowany")
