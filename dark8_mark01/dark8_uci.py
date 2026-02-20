def run_agent_auto(cmd: str) -> str:
    """
    Główna brama UCI dla DARK8‑OS.

    Zwraca wynik jako string (dla UI),
    ale nadal drukuje do konsoli (dla CLI).
    """

    ensure_backend_ready()

    cmd_clean = cmd.strip()
    cmd_lower = cmd_clean.lower()

    project_root = os.path.abspath(os.getcwd())
    auto_fix_root = os.path.join(project_root, "projekty", "auto_fix")

    output = []  # <-- tu zbieramy wynik dla UI

    # ---------------------------------------------------------
    # TRYB 1: Analiza projektu DARK8
    # ---------------------------------------------------------
    if "przeanalizuj dark8" in cmd_lower or "analiza dark8" in cmd_lower:
        msg = "[AUTO] Wykryto polecenie ANALIZY projektu DARK8."
        print(msg)
        output.append(msg)

        msg = f"[AUTO] Katalog projektu: {project_root}"
        print(msg)
        output.append(msg)

        report = analyze_dark8_project(project_root)

        output.append("\n--- RAPORT ANALIZY DARK8 ---")
        output.append(report)
        output.append("\n[AUTO] Analiza projektu DARK8 zakończona.")

        return "\n".join(output)

    # ---------------------------------------------------------
    # TRYB 2: Auto‑Fix projektu DARK8
    # ---------------------------------------------------------
    if (
        "napraw dark8" in cmd_lower
        or "auto-fix dark8" in cmd_lower
        or "autofix dark8" in cmd_lower
    ):
        msg = "[AUTO] Wykryto polecenie AUTO‑FIX projektu DARK8."
        print(msg)
        output.append(msg)

        msg = f"[AUTO] Katalog projektu: {project_root}"
        print(msg)
        output.append(msg)

        msg = f"[AUTO] Katalog wyjściowy: {auto_fix_root}"
        print(msg)
        output.append(msg)

        summary = auto_fix_dark8_project(project_root, auto_fix_root)

        output.append("\n--- PODSUMOWANIE AUTO‑FIX DARK8 ---")
        output.append(summary)
        output.append("\n[AUTO] Auto‑fix projektu DARK8 zakończony.")

        return "\n".join(output)

    # ---------------------------------------------------------
    # TRYB 3: Standardowy — autonomiczny agent
    # ---------------------------------------------------------
    msg = "[AUTO] Wykryto zadanie — uruchamiam autonomicznego agenta..."
    print(msg)
    output.append(msg)

    msg = f"[AUTO] Zadanie: {cmd_clean}"
    print(msg)
    output.append(msg)

    result = run_autonomic_task(cmd_clean)

    output.append("\n--- PLAN ---")
    output.append(result["plan"])

    output.append("\n--- WYNIK ---")
    output.append(result["result"])

    output.append("\n[AUTO] Zadanie zakończone.")

    return "\n".join(output)
