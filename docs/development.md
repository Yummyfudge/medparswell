# 🛠 medparswell Development Plan

This document tracks the technical direction and tasking for medparswell. It reflects lessons learned from previous architectural blockers and test failures.

---

## 🎯 Project Purpose

Build a modular, testable FastAPI backend that exposes endpoints for LLM-backed summarization and related NLP tasks. The backend must wrap `ik_llama.cpp` via CLI integration, support full local testing with fakes, and scale toward future frontend/UX integration.

---

## ✅ Status Summary

- ✅ FastAPI scaffold created
- ✅ Initial schema, route, and service layers set up
- ✅ `.env` configuration and Conda environment created
- ✅ CLI runner support for `ik_llama.cpp` (real and fake)
- ⚠️ Unit and integration tests mostly in place, but many failing
- ⚠️ Pytest monkeypatch fixture misconfigured (ScopeMismatch errors)
- ⚠️ Route coverage partially duplicated or misaligned
- ⚠️ Settings model not fully adopted (e.g. ctx_size attribute missing)

---

## 🔍 Immediate Fix Priorities

1. ✅ Rename tests, routes, and schemas for consistent naming and future extensibility.
2. 🧪 Fix `tests/conftest.py` monkeypatch scope error by using `function` scope.
3. 🧼 Remove deprecated or placeholder tests.
4. 🔁 Refactor remaining schema test cases to validate current field logic (e.g., `min_length`, `alias`, etc).
5. 🧵 Unify test setup: use `TestClient` or `AsyncClient` consistently.
6. 🔐 Confirm `.env` values are correctly parsed and used by `settings`.

---

## 🧱 Foundations to Build Toward

- Modular support for other `llama.cpp`-style CLI models or inference backends
- Optional transformer model support (via HuggingFace)
- Health, metrics, and tracing middleware
- Frontend-facing route descriptions and auto-docs

---

## 🧪 Test Breakdown (Current State)

- ❌ `test_ping` returns 404 (health route not mounted or alias mismatch)
- ❌ `test_run_llama_cli_success` — settings not loaded or misconfigured
- ❌ `test_empty_content_fails` — schema lacks `min_length=1`
- ⚠️ All tests relying on `monkeypatch` are failing with `ScopeMismatch`

---

## 🗂 Suggestions Going Forward

- Consolidate logging config into `settings.logging_level`
- Move remaining duplicated test logic into fixtures
- Revisit schema/route naming conventions to allow for multimodal support (e.g., `image_summary`, `clinical_summary`)
- Consider using Lifespan events instead of deprecated `@app.on_event("startup")`

---

## 🧠 Notes

- You are not blocked on LLM accuracy — the system is failing at the integration layer.
- The fake `llama-cli` system works. Leverage it more fully during testing.
- Git history has been clean — preserve this through small, validated commits.

---