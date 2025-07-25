

# Default backend parameters for ik_llama CLI endpoints
# These values are injected into the route builder and merged with schema defaults

TEXT_SUMMARIZATION_DEFAULTS = {
    "model_path": "/models/mistral_downloaded/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    "context_size": 2048,
    "gpu_layers": 2,
    "main_gpu": 0,
    "numa": "isolate",
    "verbose": True,
    "timeout_seconds": 240,
}