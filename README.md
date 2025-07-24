# MedParsWell

**MedParsWell** is a modular FastAPI-based API and service layer for wrapping CLI-based LLM backends such as `ik_llama.cpp`. It is designed to expose model metadata and options via schemas compatible with downstream tools like Gradio and future UI layers.

## Features

- 🧠 LLM inference shell wrapper (supports `ik_llama.cpp`)
- 🛠️ Schema-driven API metadata exposure
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

# Launch dev server
uvicorn app.main:app --reload
```

## Directory Structure

```
medparswell/
├── app/
│   ├── config/
│   ├── routes/
│   ├── schemas/
│   └── services/
├── tests/
│   ├── integration/
│   ├── routes/
│   ├── schemas/
│   └── services/
├── notes/
├── docs/
├── to_linux.sh
├── environment.yml
└── README.md
```

## Roadmap

- [x] Route scaffolding & health endpoints
- [x] API schema metadata exposure
- [x] CLI integration with `ik_llama.cpp`
- [ ] Add Gradio UI compatibility
- [ ] Support full CLI argument mapping
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