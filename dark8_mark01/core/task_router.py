# task_router.py
# Router pluginów dla DARK8_MARK01

from importlib import import_module


class TaskRouter:
    """
    Router pluginów:
    - mapuje type → handler
    - ładuje pluginy dynamicznie
    """

    def __init__(self):
        self.handlers = {}
        self._register_builtin_plugins()

    # ============================================================
    # REJESTRACJA PLUGINÓW
    # ============================================================

    def register(self, task_type: str, module_path: str, handler_name: str):
        self.handlers[task_type] = (module_path, handler_name)

    def _register_builtin_plugins(self):
        """
        Rejestracja wszystkich warstw:
        - WEB TOOLS
        - FILE TOOLS
        - REPO TOOLS
        - TOOLS LAYER
        - MEMORY TOOLS
        - SELF-IMPROVEMENT
        - AUTONOMIC AGENT
        """

        # ============================================================
        # WEB TOOLS
        # ============================================================

        self.register("FETCH_URL", "dark8_mark01.plugins.web.plugin_fetch_url", "handle_FETCH_URL")

        self.register(
            "DOWNLOAD_FILE", "dark8_mark01.plugins.web.plugin_download_file", "handle_DOWNLOAD_FILE"
        )

        self.register(
            "ANALYZE_PAGE", "dark8_mark01.plugins.web.plugin_analyze_page", "handle_ANALYZE_PAGE"
        )

        self.register(
            "SEARCH_WEB", "dark8_mark01.plugins.web.plugin_search_web", "handle_SEARCH_WEB"
        )

        self.register(
            "SAVE_REPORT", "dark8_mark01.plugins.web.plugin_save_report", "handle_SAVE_REPORT"
        )

        # ============================================================
        # FILE TOOLS
        # ============================================================

        self.register(
            "WRITE_FILE", "dark8_mark01.plugins.file.plugin_write_file", "handle_WRITE_FILE"
        )

        self.register("READ_FILE", "dark8_mark01.plugins.file.plugin_read_file", "handle_READ_FILE")

        self.register(
            "PATCH_JSON", "dark8_mark01.plugins.file.plugin_patch_json", "handle_PATCH_JSON"
        )

        self.register(
            "PATCH_TEXT", "dark8_mark01.plugins.file.plugin_patch_text", "handle_PATCH_TEXT"
        )

        self.register(
            "PATCH_YAML", "dark8_mark01.plugins.file.plugin_patch_yaml", "handle_PATCH_YAML"
        )

        self.register(
            "PATCH_DIFF", "dark8_mark01.plugins.file.plugin_patch_diff", "handle_PATCH_DIFF"
        )

        # ============================================================
        # REPO TOOLS
        # ============================================================

        self.register("GIT_CLONE", "dark8_mark01.plugins.repo.plugin_git_clone", "handle_GIT_CLONE")

        self.register("GIT_PULL", "dark8_mark01.plugins.repo.plugin_git_pull", "handle_GIT_PULL")

        self.register(
            "GIT_STATUS", "dark8_mark01.plugins.repo.plugin_git_status", "handle_GIT_STATUS"
        )

        self.register("GIT_DIFF", "dark8_mark01.plugins.repo.plugin_git_diff", "handle_GIT_DIFF")

        self.register(
            "GIT_COMMIT", "dark8_mark01.plugins.repo.plugin_git_commit", "handle_GIT_COMMIT"
        )

        # ============================================================
        # TOOLS LAYER
        # ============================================================

        self.register(
            "CODE_GENERATE",
            "dark8_mark01.plugins.tools.plugin_code_generate",
            "handle_CODE_GENERATE",
        )

        self.register(
            "CODE_REFACTOR",
            "dark8_mark01.plugins.tools.plugin_code_refactor",
            "handle_CODE_REFACTOR",
        )

        self.register(
            "RUN_TESTS", "dark8_mark01.plugins.tools.plugin_run_tests", "handle_RUN_TESTS"
        )

        self.register(
            "BUILD_PROJECT",
            "dark8_mark01.plugins.tools.plugin_build_project",
            "handle_BUILD_PROJECT",
        )

        self.register(
            "DOC_GENERATE", "dark8_mark01.plugins.tools.plugin_doc_generate", "handle_DOC_GENERATE"
        )

        # ============================================================
        # MEMORY TOOLS
        # ============================================================

        self.register(
            "MEMORY_SET", "dark8_mark01.plugins.memory.plugin_memory_set", "handle_MEMORY_SET"
        )

        self.register(
            "MEMORY_GET", "dark8_mark01.plugins.memory.plugin_memory_get", "handle_MEMORY_GET"
        )

        self.register(
            "MEMORY_DELETE",
            "dark8_mark01.plugins.memory.plugin_memory_delete",
            "handle_MEMORY_DELETE",
        )

        self.register(
            "MEMORY_LIST", "dark8_mark01.plugins.memory.plugin_memory_list", "handle_MEMORY_LIST"
        )

        # ============================================================
        # SELF-IMPROVEMENT
        # ============================================================

        self.register(
            "IMPROVE_PLAN", "dark8_mark01.plugins.self.plugin_improve_plan", "handle_IMPROVE_PLAN"
        )

        self.register(
            "IMPROVE_MPX", "dark8_mark01.plugins.self.plugin_improve_mpx", "handle_IMPROVE_MPX"
        )

        # ============================================================
        # AUTONOMIC AGENT
        # ============================================================

        self.register(
            "AUTONOMIC_TASK", "dark8_mark01.plugins.agent.plugin_autonomic", "handle_AUTONOMIC_TASK"
        )

    # ============================================================
    # DISPATCH
    # ============================================================

    def dispatch(self, task: dict, context):
        task_type = task.get("type")
        if not task_type:
            return {"error": "Brak pola 'type' w tasku"}

        if task_type not in self.handlers:
            return {"error": f"Brak handlera dla typu: {task_type}"}

        module_path, handler_name = self.handlers[task_type]

        try:
            module = import_module(module_path)
            handler = getattr(module, handler_name)
        except Exception as e:
            return {"error": f"Nie można załadować pluginu {task_type}: {e}"}

        try:
            return handler(task, context)
        except Exception as e:
            return {"error": f"Błąd wykonania pluginu {task_type}: {e}"}
