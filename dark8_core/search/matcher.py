class FuzzyMatcher:
    def __init__(self):
        # Try to use rapidfuzz if available for better scoring
        try:
            from rapidfuzz import fuzz  # type: ignore

            self._fuzz = fuzz
            self._use_rapidfuzz = True
        except Exception:
            self._fuzz = None
            self._use_rapidfuzz = False

    def _levenshtein_distance(self, a: str, b: str) -> int:
        # classic DP Levenshtein distance
        m, n = len(a), len(b)
        if m == 0:
            return n
        if n == 0:
            return m
        dp = [list(range(n + 1))]
        for i in range(1, m + 1):
            row = [i] + [0] * n
            ai = a[i - 1]
            for j in range(1, n + 1):
                cost = 0 if ai == b[j - 1] else 1
                row[j] = min(dp[i - 1][j] + 1, row[j - 1] + 1, dp[i - 1][j - 1] + cost)
            dp.append(row)
        return dp[m][n]

    def score(self, query: str, text: str) -> float:
        """Return score in range [0.0, 1.0] between query and text.

        Uses rapidfuzz if available, otherwise Levenshtein distance fallback.
        """
        if not query or not text:
            return 0.0

        q = query.strip()
        t = text.strip()

        # Rapidfuzz: use token_set_ratio or partial_ratio for fuzzy matching
        if self._use_rapidfuzz and self._fuzz is not None:
            try:
                val = float(self._fuzz.token_set_ratio(q, t)) / 100.0
                return max(0.0, min(1.0, val))
            except Exception:
                pass

        # Fallback heuristics: exact substring -> 1.0
        if q.lower() in t.lower():
            return 1.0

        # Levenshtein normalized score
        dist = self._levenshtein_distance(q.lower(), t.lower())
        maxlen = max(len(q), len(t))
        if maxlen == 0:
            return 0.0
        score = 1.0 - (dist / maxlen)
        # clamp
        return max(0.0, min(1.0, score))
