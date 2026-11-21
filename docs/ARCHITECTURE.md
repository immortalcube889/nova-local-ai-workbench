# Architecture

```
Browser UI
   │ HTTPS / JSON
   ▼
Nova HTTP service ───► SQLite memory
   │
   ├── read-only system inspection
   └── file-action planner ───► explicit approval required
```

The public edition intentionally does not contain a model API key, a broker integration, or automatic file changes. In production, a model provider belongs behind authenticated API routes; authorization and approval remain application controls, never prompt instructions.
