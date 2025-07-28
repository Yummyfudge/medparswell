 

# 🧠 aReturnToSanity: Plan to Realign Endpoint Architecture


This document outlines the step-by-step migration to the **Orchestrator-Centric Endpoint System**. It reflects our architectural values: clarity, responsibility boundaries, and controlled extensibility.

---

## 🚨 What Went Wrong

Over time, the system began to violate its own architectural boundaries. Specifically:

- The **route factory** took on too much responsibility, performing schema imports, runner logic, and error handling directly.
- **Constructor helpers** became authoritative sources for schema and runner logic, duplicating or bypassing orchestrator behavior.
- The **runner logic** was activated implicitly — without the orchestrator verifying model presence or readiness.
- As a result, **mock mode** was triggered silently, and schema mismatches surfaced as cryptic runtime errors.
- Worse, logging and validation lived in fragmented places, causing missing context during error triage.

This plan reasserts the design principle: Orchestrators own the logic, factories only assemble.

---

## ✅ PHASE 1: Authority Reversal (End-to-End Ownership)

📍 File: `app/orchestrators/endpoints.py`

- [x] Create function `get_active_endpoint_config(endpoint: EndpointType) -> dict`
- [x] Inside this function:
  - [x] Load schema from endpoint_definitions
  - [x] Load backend defaults
  - [x] Instantiate runner or fallback to mock runner
  - [x] Return dict with: `schema`, `response`, `runner`, `defaults`, `route_path`
- [x] Add validation + logging:
  - [x] Log missing schema/runner/model
  - [x] Log fallback to mock
  - [x] Log successful instantiation

---

## 🧱 PHASE 2: Make Route Factory Passive

📍 File: `app/constructor/route_factory.py`

- [ ] Change `build_route_for_interface` to accept `route_config: dict`
- [ ] Replace direct imports with `route_config["schema"]`, etc.
- [ ] Move all dynamic imports to `endpoints.py`
- [ ] Preserve current logging and JSON schema preview

---

## 🧹 PHASE 3: Demote Constructor Helpers

📍 File: `app/constructor/helpers/endpoint_helpers/`

- [ ] Deprecate all logic that creates runners, imports schema, or defines routes
- [ ] Migrate valid functions (e.g., prompt builders) into endpoint_definitions or utils
- [ ] Add warning comments to remind they are no longer authoritative

---

## 🔐 PHASE 4: Explicit Mock & Model State

📍 File: `app/runner_modules/llama_runner.py`

- [ ] Update `LlamaRunner.__init__()` to detect missing model
- [ ] Add flag `self.mock_mode`
- [ ] Log when running in mock
- [ ] Add placeholder response method with realistic structure

---

## 🎨 PHASE 5: Keep UI Schema Overriding Clean

📍 File: `app/constructor/helpers/interface_helpers/fastapi_ui.py`

- [ ] Ensure schema overriding is pure function, no runner/schema loading
- [ ] Add debug log: `logger.debug(f"🧪 Final model fields for {schema.__name__}: {updated_fields.keys()}")`
- [ ] Make sure overrides don’t leak upstream responsibilities

---

## BONUS: Central Logging Enhancements

📍 Files: `logging_config.py`, `route_factory.py`, `llama_runner.py`

- [ ] Log every endpoint route registered
- [ ] Log runner instantiation success/failure
- [ ] Log mock fallback clearly
- [ ] Log structured traceback in file, not just stdout

---

## 🎯 Result

- 🧠 Orchestrators control what’s active
- 🏗️ Factories build only from instructions
- 🧪 Helpers help, but don’t decide
- 🚦 Mock mode is safe and discoverable
- 🧘 System is predictable, testable, and extendable

--- 


## 🧩 Control Flow Overview (Call-Only Architecture)

```plaintext
┌──────────────────────────┐
│    exploration_main.py   │
│  (Orchestrator Entry)    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  get_active_endpoints()  │
│  get_active_interfaces() │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────────┐
│  For each (endpoint, iface): │
│  build_route_for_interface() │
└────────────┬─────────────────┘
             │
             ▼
┌────────────────────────────────────────┐
│ get_route_components(endpoint)         │
│  ├── schema                            │
│  ├── response_model                    │
│  ├── runner (real or mock)             │
│  └── route_path                        │
└────────────┬───────────────────────────┘
             │
             ▼
┌────────────────────────────────┐
│ build_route_from_components()  │
│  └── FastAPI route object      │
└────────────┬───────────────────┘
             │
             ▼
┌────────────────────────────┐
│     FastAPI app includes   │
│       all built routes     │
└────────────────────────────┘
```

This diagram shows that orchestration logic pushes all route construction instructions downward. No component reaches upward to fetch config or state.