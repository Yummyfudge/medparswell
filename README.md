# MedParsWell

> ⚠️ **Experimental Design Track**  
> This branch is an active *research and prototyping* effort. We're testing a new architecture for dynamic route generation based on modular schema+interface+backend definitions.  
> The goal: make routes declarative and self-assembling—zero boilerplate, zero duplication.  
> Success would allow CLI-based backends (like `llama-cli`) to expose fully usable REST APIs + OpenAPI docs with almost no manual wiring.  
> Progress is tracked in the `/notes/` folder and reflected in the evolving constructor framework.  
>  
> To run the app using the dynamic route constructor setup, use:  
> `python runserver.py`

> ## 🧪 Experimental Design Track

> ### ✅ Sanity Refactor Plan (Checkpoint 1 of 3)
> We've completed PHASE 1 of the structured rearchitecture:
> 
> - [x] Added `get_active_endpoint_config(endpoint: EndpointType)`
> - [x] Loaded schema, defaults, runner, and route path
> - [x] Validated model presence or mock fallback
> - [x] Placed logging for all steps
> 
> This ensures that `route_factory` no longer reaches directly into core logic,  
> and all endpoint construction is routed through the orchestrator via helpers.

**MedParsWell** is a modular FastAPI-based API and service layer for wrapping CLI-based LLM backends such as `ik_llama.cpp`. It is designed to expose model metadata and options via schemas compatible with downstream tools like Gradio and future UI layers.

## Features

- 🧠 LLM inference shell wrapper (supports `ik_llama.cpp`)
- 🛠️ Schema-driven API metadata exposure (Pydantic v2, with `json_schema_extra` for Gradio compatibility)
- 🪵 Configurable logging with console and file output
- 🧾 Environment-variable-based configuration via `.env`
- 🔁 Designed for compatibility with Gradio dynamic forms
- 📡 Remote execution support via subprocess shell calls
- 📦 Structured, extensible architecture with FastAPI
- 🧪 Testable CLI inference layer with mocking support

## Quickstart

```bash
git clone git@github.com:Yummyfudge/medparswell.git
cd medparswell

# Create environment
conda env create -f environment.yml
conda activate medparswell
cp .env.sample .env  # Set environment variables (edit to match your system)

# Launch dev server
uvicorn app.main:app --reload

# Or run the dynamic constructor loader
python runserver.py
```

## Environment Configuration

A sample `.env.sample` file is provided to show required and optional environment variables used by the app. Copy this file to `.env` and adjust paths as needed:
  
```bash
cp .env.sample .env
```

## Directory Structure

```
medparswell/
├── .env.sample
├── app/
│   ├── config/
│   │   └── logging_config.py
│   ├── routes/
│   ├── schemas/
│   └── services/
├── tests/
│   ├── integration/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── conftest.py
├── notes/
├── docs/
├── to_linux.sh
├── environment.yml
└── README.md
```

## Run Tests

```bash
pytest -v
```

Supports full mocking and isolated CLI testing. One integration test is skipped unless the FastAPI server is running.

## Roadmap

- [x] Route scaffolding & health endpoints
- [x] API schema metadata exposure
- [x] CLI integration with `ik_llama.cpp`
- [x] Add Gradio UI compatibility
- [x] Support full CLI argument mapping
- [ ] Implement request batching & streaming
- [ ] Local/remote inference split
- [ ] Add persistent slot caching
- [ ] CLI embedding-only mode support

## License

This project is licensed under the MIT License.

## Acknowledgements

This project interfaces with the following external tools:

- [`ik_llama.cpp`](https://github.com/ikawrakow/ik_llama.cpp): A high-performance fork of `llama.cpp` for running GGUF models locally. Used by MedParsWell as the backend inference engine via CLI subprocess calls. See their repository for licensing and attribution details.
- The [Level1Techs community](https://forum.level1techs.com) and Wendell for the inspiration, ideas, and support that helped shape the goals of this project.