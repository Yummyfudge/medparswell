

# 🧪 medparswell — Exploration Branch Summary

This branch explores a fully dynamic route generation system, where endpoints (e.g., `ik_llama`) and interfaces (e.g., Swagger UI, CLI) are treated as **first-class citizens**, declared via `.env` variables.

## 📁 Directory Structure (as of v0.0.7-Prototype-Dynamic_Routes)

```
app/
├── constructor/              # builds routes from definitions
│   ├── helpers/
│   └── route_factory.py
├── endpoint_definitions/     # contains schema + backend defaults
│   └── ik_llama/
├── interface_configs/        # contains swagger_ui, cli, gradio, etc.
├── orchestrators/
│   ├── interfaces.py
│   └── endpoints.py
├── runner_modules/
│   ├── llama_runner.py
│   └── spacy_runner.py
```

## 🔍 Key Concepts

- **constructor/** builds FastAPI routes at runtime using schemas, defaults, and interface preferences
- **endpoint_definitions/** contains definitions for callable endpoints such as ik_llama or spacy — not entire backend services
- **interface_configs/** adapts schema exposure for UI tools like Swagger or Gradio
- **orchestrators/** read `.env` to activate/deactivate endpoints and interfaces
- **runner_modules/** house isolated logic for each backend (no FastAPI here)

This system aims for modularity, testability, and long-term maintainability — enabling per-endpoint, per-interface dynamic configuration.