import logging

logger = logging.getLogger("medparswell.llama_runner")

class LlamaRunner:
    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def run_prompt(self, content: str, language: str | None = None, verbose: bool = False, dry_run: bool = False) -> dict:
        if verbose:
            logger.debug("🧪 Running prompt in verbose mode")
        logger.warning("⚠️ No model loaded — running in mock mode. Returning fake summary.")
        return {
            "status": "mock",
            "output": f"Mock summary of: {{'content': {content!r}, 'language': {language!r}}}"
        }
