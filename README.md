

# MedParsWell

**MedParsWell** is a modern, modular FastAPI project focused on parsing, analyzing, and summarizing medical documents and data. It is designed with robust LLM and ML integration in mind, enabling streamlined pipelines for OCR, semantic analysis, and summarization of clinical records.

## Features

- 📄 OCR and document parsing
- 🧠 LLM summarization backend (supports llama.cpp, ik_llama.cpp, and more)
- 🔍 Clinical NLP support (e.g., scispaCy, UMLS)
- 🚀 FastAPI-powered modular architecture
- 🧪 Easy local development with Conda or venv
- 🔧 Ready for extension into larger medical inference pipelines

## Setup

1. Clone the repo:
   ```bash
   git clone git@github.com:Yummyfudge/medparswell.git
   cd medparswell
   ```

2. (Recommended) Create a Conda environment:
   ```bash
   conda create -n medparswell python=3.12
   conda activate medparswell
   ```

3. Install dependencies (once defined):
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Roadmap

- [ ] Finalize core scaffolding (✅ in progress)
- [ ] Add OCR utils
- [ ] Integrate summarization APIs
- [ ] Build frontend compatibility layer
- [ ] Implement end-to-end document pipeline

## License

This project is licensed under the MIT License.