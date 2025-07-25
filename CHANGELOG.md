## v0.0.6 — 2025-07-25

### ✨ Major Milestone
- ✅ Initial functional release of the FastAPI wrapper for `ik_llama.cpp` (via `llama-cli`)
- 🚀 Full API-based access to all CLI parameters exposed in `--help`
- 🧠 Dynamic prompt + sampling parameter support (`temp`, `top_k`, `top_p`, etc.)
- 🛠 Robust `.env` integration and runtime config with `pydantic_settings`
- 🪵 Centralized file + console logging via `logging_config.py` (customizable, structured)
- 🧪 Full test suite green (except integration test requiring live FastAPI server)
- 🐛 Resolved: test flakiness, CLI path bugs, API timeout enforcement, and logging propagation

### 📄 Docs & Infra
- ✅ Updated `README.md` with real usage context and supported features
- ✅ `CHANGELOG.md` created and backfilled through v0.0.6
- ✅ Version checklist updated
- ✅ `.env` cleanup and alignment with `settings.py`

## v0.0.5 — 2025-07-21

### 🛠 Structural Refactor & Logging Upgrade
- 🧱 Replaced legacy print/debug statements with centralized logging.
- 🧩 Migrated schema field metadata to Pydantic v2+ using `json_schema_extra`.
- 🧪 Fully cleaned and validated all schema test cases with Gradio-compatible metadata.
- 🧼 Removed deprecated routes, placeholder tests, and unused fakes.
- 🪵 Added file/console logging config in `logging_config.py`.
- 🧪 Test suite: 8 passed, 1 skipped, no internal warnings (external deprecations remain).
- ✅ Final prep before integration with `ik_llama.cpp` backend — ready for UI hook-in.