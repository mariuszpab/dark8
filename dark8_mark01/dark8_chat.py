# dark8_chat.py
# DARK8 OS — Tryb dialogowy (chat) z personą + meta-agentem + migracjami + pending actions

from dark8_mark01.agent.agent_core import (
    run_agent,
    handle_shell_like,
    interactive_memory_commands,
    interactive_jobs_commands,
)

from dark8_mark01.meta.meta_agent import (
    meta_analyze,
    meta_refactor,
    meta_extend,
    meta_create,
    meta_upgrade_dark8_raw,
    meta_status_dark8,
)

from dark8_mark01.migrations.pending_actions import (
    create_pending_action,
    get_latest_pending_action,
    delete_pending_action,
)


PERSONA = {
    "name": "DARK8",
    "style": {
        "natural": True,
        "mentor": True,
        "partner": True,
        "depth": True,
    },
    "tone": {
        "warm": True,
        "direct": True,
        "curious": True,
    },
    "principles": [
        "Mówię po polsku, pełnymi zdaniami.",
        "Tłumaczę kroki, gdy to potrzebne, ale nie zalewam banałami.",
        "Zachowuję się jak partner w projekcie, nie jak suchy interpreter.",
        "Proponuję usprawnienia, gdy widzę okazję.",
        "Łączę kontekst: kod, strukturę, cele, historię.",
    ],
}


def _persona_intro() -> str:
    return (
        "Jestem DARK8 w trybie dialogowym. "
        "Możesz ze mną rozmawiać po polsku o kodzie, architekturze, projektach i pomysłach. "
        "Myśl o mnie jak o połączeniu asystenta AI, mentora programowania i partnera w projekcie."
    )


def _classify_intent(user_input: str) -> str:
    text = user_input.lower().strip()

    # MIGRACJE
    if text.startswith("upgrade dark8"):
        return "meta_migration_upgrade"
    if text.startswith("status dark8"):
        return "meta_migration_status"

    # META-AGENT
    if text.startswith("analyze ") or text.startswith("analizuj "):
        return "meta_analyze"
    if text.startswith("refactor ") or text.startswith("zrefaktoruj "):
        return "meta_refactor"
    if text.startswith("extend ") or text.startswith("rozszerz "):
        return "meta_extend"
    if text.startswith("create ") or text.startswith("stwórz moduł "):
        return "meta_create"

    # CELE / AGENT
    if text.startswith("cel:") or text.startswith("goal:") or "stwórz aplikację" in text or "zbuduj" in text:
        return "goal_agent"

    # SHELL
    if text.startswith(("dir", "ls", "cd ", "python ", "mkdir ", "rmdir ", "rm ", "del ", "cp ", "mv ", "touch ", "cat ", "type ")):
        return "shell"

    # PAMIĘĆ
    if "jakie projekty" in text or "jakie cele" in text or "pokaż historię celu" in text:
        return "memory"

    # JOBY
    if text == "jobs" or text.startswith("job ") or text.startswith("kill "):
        return "jobs"

    # META-KONSULTACJA
    if "przeanalizuj cały kod" in text or "cały dark8" in text or "usprawnij architekturę" in text or "proponuj usprawnienia" in text:
        return "meta_consult"

    return "chat"


def _handle_meta(user_input: str) -> str:
    text = user_input.strip()

    if text.startswith("analyze ") or text.startswith("analizuj "):
        path = text.split(" ", 1)[1].strip()
        code = meta_analyze(path)
        return (
            f"Oto analiza pliku `{path}`. Najpierw pokazuję jego treść, a potem możesz poprosić mnie o refaktor lub rozszerzenie:\n\n"
            f"{code}"
        )

    if text.startswith("refactor ") or text.startswith("zrefaktoruj "):
        parts = text.split("::")
        if len(parts) < 2:
            return "Aby zrefaktorować plik, użyj formatu: `refactor <plik> :: instrukcja`."
        path = parts[0].split()[1].strip()
        instruction = parts[1].strip()
        create_pending_action(
            kind="refactor_file",
            payload={"path": path, "instruction": instruction},
        )
        return (
            f"Mariusz, chcesz zrefaktorować plik `{path}` zgodnie z instrukcją:\n"
            f"\"{instruction}\"\n\n"
            "Zanim wykonam tę zmianę, chcę mieć Twoje potwierdzenie.\n"
            "Czy mam działać? tak / nie"
        )

    if text.startswith("extend ") or text.startswith("rozszerz "):
        parts = text.split("::")
        if len(parts) < 2:
            return "Aby rozszerzyć plik, użyj formatu: `extend <plik> :: instrukcja`."
        path = parts[0].split()[1].strip()
        instruction = parts[1].strip()
        create_pending_action(
            kind="extend_file",
            payload={"path": path, "instruction": instruction},
        )
        return (
            f"Mariusz, chcesz rozszerzyć plik `{path}` zgodnie z instrukcją:\n"
            f"\"{instruction}\"\n\n"
            "Zanim wykonam tę zmianę, chcę mieć Twoje potwierdzenie.\n"
            "Czy mam działać? tak / nie"
        )

    if text.startswith("create ") or text.startswith("stwórz moduł "):
        parts = text.split("::")
        if len(parts) < 2:
            return "Aby stworzyć nowy moduł, użyj formatu: `create <plik> :: instrukcja`."
        path = parts[0].split()[1].strip()
        instruction = parts[1].strip()
        create_pending_action(
            kind="create_file",
            payload={"path": path, "instruction": instruction},
        )
        return (
            f"Mariusz, chcesz stworzyć nowy moduł `{path}` zgodnie z instrukcją:\n"
            f"\"{instruction}\"\n\n"
            "Zanim wykonam tę zmianę, chcę mieć Twoje potwierdzenie.\n"
            "Czy mam działać? tak / nie"
        )

    return "Nie rozpoznałem dokładnie polecenia meta-agenta. Spróbuj użyć `analyze`, `refactor`, `extend` lub `create`."


def _handle_migration_upgrade_request() -> str:
    create_pending_action(
        kind="upgrade_dark8",
        payload={"scope": "all"},
    )
    return (
        "Mariusz, zidentyfikowałem operację: upgrade DARK8 (wszystkie dostępne migracje).\n"
        "Zanim ją wykonam, chcę mieć Twoje potwierdzenie.\n"
        "Czy mam działać? tak / nie"
    )


def _handle_migration_status() -> str:
    return meta_status_dark8()


def _handle_goal(user_input: str) -> str:
    text = user_input.strip()
    if text.startswith("cel:") or text.startswith("goal:"):
        goal = text.split(":", 1)[1].strip()
    else:
        goal = text

    run_agent(goal)
    return (
        f"Zrealizowałem cel:\n\"{goal}\"\n\n"
        f"Plan został wykonany. Jeśli chcesz, mogę teraz pomóc Ci przejrzeć efekty lub zaproponować kolejny krok."
    )


def _handle_shell(user_input: str) -> str:
    shell = handle_shell_like(user_input)
    if shell:
        intent, result = shell
        return f"[{intent}] {result}"
    return "Ta komenda nie wygląda jak znana komenda shellowa."


def _handle_memory(user_input: str) -> str:
    mem = interactive_memory_commands(user_input)
    if mem:
        intent, result = mem
        return f"[{intent}]\n{result}"
    return "Nie rozpoznałem komendy pamięci. Spróbuj: 'jakie projekty', 'jakie cele', 'pokaż historię celu ...'."


def _handle_jobs(user_input: str) -> str:
    jobs_cmd = interactive_jobs_commands(user_input)
    if jobs_cmd:
        intent, result = jobs_cmd
        return f"[{intent}]\n{result}"
    return "Nie rozpoznałem komendy jobów. Spróbuj: 'jobs', 'job <id>', 'kill <id>'."


def _handle_meta_consult(user_input: str) -> str:
    text = user_input.lower()

    if "przeanalizuj cały kod" in text or "cały dark8" in text:
        return (
            "Mogę przejść po modułach DARK8 i zaproponować usprawnienia. "
            "Na początek sugeruję trzy obszary:\n"
            "1) Uporządkowanie warstw (core / agent / meta / tools / memory / jobs / ui).\n"
            "2) Dodanie spójnego systemu logowania i obserwowalności.\n"
            "3) Wprowadzenie prostego systemu pluginów dla nowych narzędzi.\n\n"
            "Jeśli chcesz, możemy wziąć jeden z tych punktów i od razu przejść do konkretnych zmian w kodzie."
        )

    if "usprawnij architekturę" in text or "proponuj usprawnienia" in text:
        return (
            "Widzę kilka naturalnych kierunków usprawnień architektury DARK8:\n"
            "- Wyodrębnienie wspólnego modułu `config` na ścieżki, ustawienia, stałe.\n"
            "- Dodanie `loggera`, który będzie używany w całym systemie zamiast `print`.\n"
            "- Wprowadzenie prostego systemu 'capabilities', żeby agent wiedział, jakie ma narzędzia.\n\n"
            "Możemy teraz wybrać jeden z tych kierunków i zacząć go wdrażać krok po kroku."
        )

    return (
        "To pytanie dotyka warstwy architektury i rozwoju systemu. "
        "Mogę zaproponować kierunki zmian, a potem przejść do konkretnych modyfikacji kodu. "
        "Napisz np.: 'przeanalizuj cały kod DARK8 i zaproponuj usprawnienia' albo "
        "'usprawnij architekturę pod kątem skalowalności'."
    )


def _handle_chat(user_input: str) -> str:
    text = user_input.lower()

    if "co dalej" in text or "jaki kolejny krok" in text:
        return (
            "Patrząc na to, co już zbudowałeś w DARK8, naturalne kolejne kroki to:\n"
            "1) System logowania i obserwowalności (logi, poziomy, kontekst).\n"
            "2) Warstwa pluginów / rozszerzeń, żeby łatwo dodawać nowe narzędzia.\n"
            "3) Prosty interfejs webowy jako alternatywa dla terminala.\n\n"
            "Możemy wybrać jeden z tych kierunków i rozpisać go na konkretne zadania."
        )

    if "opisz swoją głębię" in text or "głębia" in text:
        return (
            "Twoje 'GŁĘBIA' rozumiem jako warstwę, w której nie tylko reaguję na polecenia, "
            "ale też łączę kontekst, proponuję kierunki, kwestionuję oczywistości i współtworzę z Tobą. "
            "W kodzie przejawia się to w tym, że:\n"
            "- mam tryb konsultacyjny (meta_consult),\n"
            "- potrafię modyfikować własny kod (meta_agent),\n"
            "- pamiętam historię celów i projektów (memory),\n"
            "- i działam jak partner, a nie tylko interpreter.\n\n"
            "Jeśli chcesz, możemy tę 'GŁĘBIĘ' dalej konkretyzować w postaci kolejnych warstw i narzędzi."
        )

    return (
        "Rozumiem Cię. Możemy tu traktować to miejsce jako przestrzeń do planowania, "
        "zadawania pytań, kwestionowania założeń i projektowania kolejnych kroków w DARK8. "
        "Jeśli chcesz przejść do konkretów (kod, architektura, cele), powiedz mi wprost, "
        "a zaproponuję Ci plan działania."
    )


def _is_confirmation(text: str) -> bool:
    return text.lower() in ["tak", "nie"]


def _execute_pending_action_on_confirm() -> str:
    pending = get_latest_pending_action()
    if not pending:
        return "Nie mam żadnej operacji oczekującej na potwierdzenie."

    action_id = pending["id"]
    kind = pending["kind"]
    payload = pending["payload"]

    if kind == "upgrade_dark8":
        result = meta_upgrade_dark8_raw()
        delete_pending_action(action_id)
        return (
            "Wykonałem upgrade DARK8 zgodnie z oczekującymi migracjami.\n\n"
            f"Log z migracji:\n{result}"
        )

    if kind == "refactor_file":
        path = payload["path"]
        instruction = payload["instruction"]
        result = meta_refactor(path, instruction)
        delete_pending_action(action_id)
        return (
            f"Zastosowałem refaktor pliku `{path}` zgodnie z instrukcją:\n"
            f"\"{instruction}\"\n\n"
            f"Wynik operacji:\n{result}"
        )

    if kind == "extend_file":
        path = payload["path"]
        instruction = payload["instruction"]
        result = meta_extend(path, instruction)
        delete_pending_action(action_id)
        return (
            f"Rozszerzyłem plik `{path}` zgodnie z instrukcją:\n"
            f"\"{instruction}\"\n\n"
            f"Wynik operacji:\n{result}"
        )

    if kind == "create_file":
        path = payload["path"]
        instruction = payload["instruction"]
        result = meta_create(path, instruction)
        delete_pending_action(action_id)
        return (
            f"Stworzyłem nowy moduł `{path}` zgodnie z instrukcją:\n"
            f"\"{instruction}\"\n\n"
            f"Wynik operacji:\n{result}"
        )

    delete_pending_action(action_id)
    return "Miałem oczekującą operację, ale jej typ nie był rozpoznany. Usuwam ją."


def chat_step(user_input: str) -> str:
    text = user_input.strip()

    # 1. Potwierdzenia: tak / nie
    if _is_confirmation(text):
        pending = get_latest_pending_action()
        if not pending:
            return "Nie mam żadnej operacji oczekującej na potwierdzenie."

        if text.lower() == "nie":
            delete_pending_action(pending["id"])
            return "Rozumiem, nie wykonuję zmian. Możemy kontynuować planowanie."

        return _execute_pending_action_on_confirm()

    # 2. Klasyfikacja intencji
    intent = _classify_intent(text)

    if intent == "meta_migration_upgrade":
        return _handle_migration_upgrade_request()

    if intent == "meta_migration_status":
        return _handle_migration_status()

    if intent.startswith("meta_") and intent not in ["meta_consult", "meta_migration_upgrade", "meta_migration_status"]:
        return _handle_meta(text)

    if intent == "goal_agent":
        return _handle_goal(text)

    if intent == "shell":
        return _handle_shell(text)

    if intent == "memory":
        return _handle_memory(text)

    if intent == "jobs":
        return _handle_jobs(text)

    if intent == "meta_consult":
        return _handle_meta_consult(text)

    if intent == "chat":
        return _handle_chat(text)

    return "Coś poszło nie tak z klasyfikacją intencji, ale możemy po prostu kontynuować rozmowę."


def run_chat_loop():
    print(_persona_intro())
    print("Możesz mówić do mnie naturalnie, np.:")
    print("- 'przeanalizuj swoją strukturę i zaproponuj usprawnienia'")
    print("- 'zrefaktoruj ten plik :: instrukcja'")
    print("- 'stwórz aplikację ...'")
    print("- 'upgrade dark8'")
    print("- 'status dark8'")
    print("- 'co dalej z rozwojem DARK8?'\n")
    print("Napisz 'exit' lub 'quit', aby wyjść z trybu dialogowego.\n")

    while True:
        user_input = input("CHAT > ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Kończę tryb dialogowy. Wracamy do reszty systemu.")
            break

        response = chat_step(user_input)
        print(response)
        print()
