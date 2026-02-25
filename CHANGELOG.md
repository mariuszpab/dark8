# Changelog

## v0.4.0 - FTS Boosting & SearchEngine Improvements

Released: 2026-02-25

### Highlights

- FTS boosting (title/content/tags) with configurable weights.
- Integrated BM25 scoring into the search pipeline; FTS queries use `bm25(..., w_title, w_content, w_tags)`.
- `SearchEngine` now consumes BM25 scores and uses configured `SEARCH_WEIGHTS`.
- Updated `documents` schema and standalone `documents_fts` to include `title` and `tags`.
- Added tests for boosting and BM25 ordering.

### Details

- Added configurable `SEARCH_WEIGHTS` (default: title=2.0, content=1.0, tags=1.0).
- `search_fts` supports per-column BM25 weights and returns `score` + `snippet`.
- Ordering by BM25 is now ASC (lower score = better match).
- Bulk insert, insert/update/delete helpers now sync `title`/`tags` into the FTS index.
- Robust DB changes: per-DB locks, retry/backoff for transient locks, safe FTS rebuild.
- Tests: full suite passing (52 tests).

### Previous work (from Unreleased)

- FTS5 + DB layer redesign

	- Added per‑DB reentrant locks to serialize schema/FTS operations.
	- Added retry/backoff for `database is locked` errors.
	- Replaced FTS5 contentless table with explicit index synchronization.
	- Implemented event‑based indexing (insert/update/delete auto‑sync to FTS).
	- Added rebuild support via `INSERT INTO documents_fts(documents_fts) VALUES('rebuild')`.
	- Updated SearchEngine to use FTS5 first, with fuzzy/LIKE fallback.
	- Added new DB helpers and tests (earlier iterations).
