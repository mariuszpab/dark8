# Semantyka i resolver

Krótko: moduł semantyczny wykonuje rozwiązywanie nazw (name resolution) i podstawowe walidacje przed generacją IR.

Główne elementy:

- `lang/semantics/scope.py` — implementacja `Scope` i `Symbol`.
- `lang/semantics/resolver.py` — odwiedzający AST, tworzy scope'y, rejestruje deklaracje i sprawdza użycia.

Walidacje wykonywane:

- Użycie niezadeklarowanej zmiennej/funkcji -> błąd
- Podwójna deklaracja w tym samym scope -> błąd
- Sprawdzenie arności wywołań funkcji -> błąd
- `break` / `continue` poza pętlą -> błąd
- `return` poza funkcją -> błąd

Integracja:

Resolver jest teraz wywoływany w `dark8_build.py` przed `generate_ir_program`. W przypadku błędów semantycznych proces budowania zostaje przerwany.

Dalsze kroki możliwe do dodania: typowanie, zaawansowane reguły shadowingu, optymalizacje.
