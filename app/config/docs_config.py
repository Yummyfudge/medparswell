from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="🧠 medparswell: Clinical LLM Backend",
        version="0.0.6",
        description="""
        This API provides endpoints for summarization and metadata interaction using a local LLM backend.
        It wraps the `llama-cli` binary (from ik_llama.cpp) and exposes FastAPI routes for clean interaction.

        **Endpoints**
        - `/ping` health check
        - `/summarize` run a summarization job via CLI
        """,
        routes=app.routes,
    )
    openapi_schema["info"]["contact"] = {
        "name": "Yummyfudge Labs",
        "url": "https://github.com/Yummyfudge/medparswell",
    }
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
