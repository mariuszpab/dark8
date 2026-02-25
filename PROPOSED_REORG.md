Proposed reorganization for DARK8
================================

Goal
----
Provide a cleaner, modular layout for `dark8_core` to make further features (indexer, plugin discovery, Ollama integration) easier to implement and maintain.

Top-level proposal (focus on `dark8_core`):

dark8_core/
    __init__.py
    agent/
        __init__.py          # light orchestrator
        executor.py          # ToolExecutor implementation
        tools/
            __init__.py
            shell.py
            file_ops.py
            db.py
        memory/
            __init__.py
            memory.py
        reasoning.py
        learning.py
    search/
        __init__.py
        engine.py
        sources.py
        matcher.py
        ranking.py
        indexer.py
    plugins/
        __init__.py
        sample_search_plugin.py
    db/
        __init__.py
        bootstrap.py
        migrations.py
    nlp/
        __init__.py
        bert.py
    ui/
        cli.py
        api.py
    utils/
        logging.py
        paths.py

Why this layout
----------------
- `agent/` becomes the runtime surface: executor, tools, memory and agent-level logic.
- `search/` is an independent subsystem (engine + indexer + sources).
- `plugins/` is a clear place for plugin packages.
- `db/` centralizes persistence/bootstrap/migrations.
- `nlp/`, `ui/`, `utils/` group related functionality.

Migration approach (safe, iterative)
-----------------------------------
1. Update consumer imports to use new namespaces (e.g. `from dark8_core.search import SearchEngine`) — already started for `search`.
2. Move one package at a time (e.g. create `agent/tools/shell.py`, copy code, update imports to refer to `agent.tools.shell`) and run tests.
3. Repeat for `agent` internals, `db/`, `plugins/` and `nlp/`.
4. Remove legacy/duplicate files and shims once tests remain green.

Next immediate step
-------------------
- Update imports across the repo to use the new `agent.tools`, `db`, `plugins` and `nlp` namespaces (dry-run: produce patch + run tests after small batches).
