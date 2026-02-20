# maxscript_parser.py
# Parser scenariuszy .mpx dla DARK8_MARK01
#
# Obsługuje:
# - komendy jednowierszowe: FETCH_URL https://example.com
# - bloki tekstowe: SAVE_REPORT path <<<END ... END
# - parametry
# - listę tasków kompatybilną z TaskRunnerem

import re


class MaxscriptParser:
    """
    Parser plików .mpx:
    - zamienia tekst na listę tasków
    - każdy task to dict: {"type": "...", ...}
    """

    BLOCK_START = "<<<END"
    BLOCK_END = "END"

    def parse_file(self, path: str) -> list[dict]:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return self.parse(content)

    def parse(self, text: str) -> list[dict]:
        lines = text.splitlines()
        tasks = []
        i = 0
        n = len(lines)

        while i < n:
            line = lines[i].strip()

            # pomijamy puste linie i komentarze
            if not line or line.startswith("#"):
                i += 1
                continue

            # sprawdzamy, czy linia zawiera blok tekstowy
            if self.BLOCK_START in line:
                task = self._parse_block_task(lines, i)
                tasks.append(task["task"])
                i = task["next_index"]
                continue

            # zwykła komenda jednowierszowa
            task = self._parse_simple_task(line)
            tasks.append(task)
            i += 1

        return tasks

    # === PARSOWANIE KOMEND JEDNOWIERSZOWYCH ===

    def _parse_simple_task(self, line: str) -> dict:
        """
        Przykład:
        FETCH_URL https://example.com
        DOWNLOAD_FILE https://example.com/file.zip
        SEARCH_WEB python 3.12
        """
        parts = line.split(maxsplit=1)

        if len(parts) == 1:
            return {"type": parts[0]}

        task_type = parts[0]
        rest = parts[1]

        # heurystyka: jeśli wygląda jak URL → pole "url"
        if rest.startswith("http://") or rest.startswith("https://"):
            return {"type": task_type, "url": rest}

        # w innym przypadku → pole "value"
        return {"type": task_type, "value": rest}

    # === PARSOWANIE BLOKÓW TEKSTOWYCH ===

    def _parse_block_task(self, lines: list[str], start_index: int) -> dict:
        """
        Przykład:
        SAVE_REPORT reports/test.txt <<<END
        Treść raportu...
        END
        """
        header = lines[start_index].strip()

        # rozbijamy nagłówek
        before, _ = header.split(self.BLOCK_START, 1)
        before = before.strip()

        parts = before.split(maxsplit=1)
        task_type = parts[0]

        # opcjonalny parametr (np. ścieżka)
        param = parts[1] if len(parts) > 1 else None

        # zbieramy linie bloku
        block_lines = []
        i = start_index + 1
        n = len(lines)

        while i < n:
            line = lines[i].strip()
            if line == self.BLOCK_END:
                break
            block_lines.append(lines[i])
            i += 1

        block_text = "\n".join(block_lines)

        task = {"type": task_type}

        if param:
            # heurystyka: jeśli wygląda jak ścieżka → path
            if "/" in param or "\\" in param:
                task["path"] = param
            else:
                task["value"] = param

        task["content"] = block_text

        return {"task": task, "next_index": i + 1}
