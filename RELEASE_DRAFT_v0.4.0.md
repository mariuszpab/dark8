# v0.4.0 — FTS Boosting & SearchEngine Upgrade

Tag: v0.4.0

Repository compare: https://github.com/mariuszpab/dark8/compare/v0.3.0...v0.4.0

## Release notes

FTS Boosting & SearchEngine Improvements

- Added configurable `SEARCH_WEIGHTS` (title/content/tags).
- Integrated BM25 scoring into `SearchEngine`.
- Added boosting logic using `bm25(..., w_title, w_content, w_tags)`.
- Updated FTS queries to sort by BM25 ASC (lower = better).
- Added new tests for boosting and BM25 ordering.
- Updated DB layer to include `title` and `tags` in `documents` and `documents_fts`.
- Robust DB improvements: per-DB locks, retry/backoff, safe FTS rebuild.

All tests passing: 52 total.

---

### How to publish (if you have `gh` CLI configured):

```bash
# create draft release on GitHub (interactive) or non-interactive:
gh release create v0.4.0 --title "v0.4.0 — FTS Boosting & SearchEngine Upgrade" \
  --notes-file RELEASE_DRAFT_v0.4.0.md --draft
```

Or publish via GitHub web UI: visit the Tags page, find `v0.4.0` and create a Release from that tag. Use the notes above as the release body.
