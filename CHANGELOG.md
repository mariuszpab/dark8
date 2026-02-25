# Changelog

## Unreleased

### FTS5 + DB layer redesign

- Added per‑DB reentrant locks to serialize schema/FTS operations.
- Added retry/backoff for `database is locked` errors.
- Replaced FTS5 contentless table with explicit index synchronization.
- Implemented event‑based indexing (insert/update/delete auto‑sync to FTS).
- Added rebuild support via `INSERT INTO documents_fts(documents_fts) VALUES('rebuild')`.
- Updated SearchEngine to use FTS5 first, with fuzzy/LIKE fallback.
- Added new DB helpers and tests (47 tests total).
