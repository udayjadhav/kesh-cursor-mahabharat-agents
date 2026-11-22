# Knowledge cache schema (optional)

Referenced by `rules/kesh-token-cache.mdc`. **Not required** for Kesh to run.

**Enforcement:** Prompt-guided (**B**) + operational CLIs (**D** when run): `scripts/cache/{fingerprint,get,put,invalidate}.py`.  
Override root with `KESH_CACHE_HOME` (default `~/.cursor/knowledge/cache`).

## Suggested layout

```
~/.cursor/knowledge/cache/
├── README.md          # this schema
├── index.json         # fingerprint → entry metadata
└── entries/
    └── <fingerprint>.json
```

## `index.json`

```json
{
  "version": 1,
  "entries": [
    {
      "fingerprint": "abcdef0123456789",
      "topic": "normalized topic string",
      "input_type": "FEATURE",
      "entities": ["HS-123", "path/to/file"],
      "created_at": "2026-11-22T12:00:00Z",
      "ttl_hours": 24,
      "path": "entries/abcdef0123456789.json"
    }
  ]
}
```

## Entry file (`entries/<fingerprint>.json`)

```json
{
  "fingerprint": "abcdef0123456789",
  "topic": "...",
  "code_revision_hint": "abc1234",
  "created_at": "2026-11-22T12:00:00Z",
  "ttl_hours": 24,
  "agent_summaries": {
    "sanjaya": "≤2k token summary — no secrets",
    "vidura": "..."
  },
  "synthesis": "short reusable answer summary"
}
```

## Rules

- Summaries only — never store secrets, tokens, or full diffs
- Cap store size (e.g. newest 50 entries)
- Fingerprint: first 16 chars of sha256(normalize(topic)|input_type|sorted(entities)|code_revision_hint)
- Phrases `bypass cache` / `fresh run` / `ignore cache` force MISS
