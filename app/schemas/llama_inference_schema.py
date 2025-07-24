from pydantic import BaseModel, Field
from typing import Optional


class LlamaInferenceParameters(BaseModel):
    prompt: str = Field(
        ...,
        description="The prompt to provide to the model.",
        example="What is the capital of France?",
    )
    model_path: Optional[str] = Field(
        None,
        description="Path to the .gguf model file.",
        example="/models/deepseek/DeepSeek-R1-0528-GGUF/model.gguf",
    )
    ctx_size: Optional[int] = Field(
        1024,
        description="Context size in tokens.",
        example=2048,
        ge=1,
    )
    gpu_layers: Optional[int] = Field(
        2,
        description="Number of layers to offload to the GPU.",
        example=2,
        ge=0,
    )
    main_gpu: Optional[int] = Field(
        0,
        description="Index of the GPU to use.",
        example=0,
        ge=0,
    )
    numa: Optional[str] = Field(
        "isolate",
        description='NUMA optimization mode as a string (e.g., "isolate", "interleave", or "").',
        example="isolate",
    )
    verbose: Optional[bool] = Field(
        False,
        description="Enable verbose output from llama-cli.",
        example=False,
    )
    predict_tokens: Optional[int] = Field(
        128,
        description="Number of tokens to predict (equivalent to --predict or -n).",
        example=128,
        ge=1,
    )
    seed: Optional[int] = Field(
        None,
        description="RNG seed for reproducibility. Set to -1 to use random seed.",
        example=42,
    )
    threads: Optional[int] = Field(
        8,
        description="Number of threads to use during generation (--threads).",
        example=8,
        ge=1,
    )
    threads_batch: Optional[int] = Field(
        None,
        description="Threads used for prompt/batch processing (--threads-batch). Defaults to --threads if not set.",
        example=4,
        ge=1,
    )
    threads_draft: Optional[int] = Field(
        None,
        description="Number of threads to use during generation (--threads-draft). Defaults to --threads.",
        example=8,
        ge=1,
    )
    threads_batch_draft: Optional[int] = Field(
        None,
        description="Threads used for prompt/batch processing during draft stage (--threads-batch-draft). Defaults to --threads-draft.",
        example=4,
        ge=1,
    )
    draft: Optional[int] = Field(
        5,
        description="Number of tokens to draft for speculative decoding (--draft).",
        example=5,
        ge=1,
    )
    p_split: Optional[float] = Field(
        0.1,
        description="Speculative decoding split probability (--p-split).",
        example=0.1,
        ge=0.0,
        le=1.0,
    )
    lookup_cache_static: Optional[str] = Field(
        None,
        description="Path to static lookup cache used for lookup decoding (--lookup-cache-static). Not updated during generation.",
        example="/cache/static.lookup",
    )
    lookup_cache_dynamic: Optional[str] = Field(
        None,
        description="Path to dynamic lookup cache for lookup decoding (--lookup-cache-dynamic). Updated during generation.",
        example="/cache/dynamic.lookup",
    )
    no_display_prompt: Optional[bool] = Field(
        False,
        description="Disable prompt printing in generation output (--no-display-prompt).",
        example=False,
    )
    color: Optional[bool] = Field(
        False,
        description="Enable colorized output to distinguish prompt and generated text (--color).",
        example=True,
    )

    # ───── Server Options ─────
    host: Optional[str] = Field(
        "127.0.0.1",
        description="The IP address the model server should bind to (--host).",
        example="127.0.0.1",
    )
    port: Optional[int] = Field(
        8000,
        description="Port on which the model server should listen (--port).",
        example=8000,
        ge=1,
    )
    path: Optional[str] = Field(
        "/",
        description="The REST API path to expose for inference (--path).",
        example="/",
    )
    threads_port: Optional[int] = Field(
        0,
        description="Port to expose for thread-level control (--threads-port).",
        example=0,
        ge=0,
    )

    # Evaluation Features
    all_logits: Optional[bool] = Field(
        False,
        description="Return logits for all tokens in the batch (--all-logits).",
        example=False,
    )
    hellaswag: Optional[bool] = Field(
        False,
        description="Compute HellaSwag score from datafile (--hellaswag).",
        example=False,
    )
    hellaswag_tasks: Optional[int] = Field(
        400,
        description="Number of tasks for HellaSwag evaluation (--hellaswag-tasks).",
        example=400,
        ge=0,
    )
    winogrande: Optional[bool] = Field(
        False,
        description="Compute Winogrande score from datafile (--winogrande).",
        example=False,
    )
    winogrande_tasks: Optional[int] = Field(
        0,
        description="Number of tasks for Winogrande evaluation (--winogrande-tasks).",
        example=100,
        ge=0,
    )
    multiple_choice: Optional[bool] = Field(
        False,
        description="Enable multiple choice scoring (--multiple-choice).",
        example=False,
    )
    multiple_choice_tasks: Optional[int] = Field(
        0,
        description="Number of tasks to use in multiple choice evaluation (--multiple-choice-tasks).",
        example=10,
        ge=0,
    )
    kl_divergence: Optional[bool] = Field(
        False,
        description="Enable KL-divergence scoring (--kl-divergence).",
        example=False,
    )
    ppl_stride: Optional[int] = Field(
        0,
        description="Stride size for perplexity calculation (--ppl-stride).",
        example=512,
        ge=0,
    )
    ppl_output_type: Optional[int] = Field(
        0,
        description="Output format for perplexity results: 0 = summary, 1 = per-token (--ppl-output-type).",
        example=0,
        ge=0,
        le=1,
    )

    # Context hacking configuration (rope/yarn/group attention/kv cache)
    rope_scaling: Optional[str] = Field(
        None,
        description="Type of rope scaling to apply. Options: 'none', 'linear', 'yarn'. (--rope-scaling)",
        example="yarn"
    )
    rope_scale: Optional[float] = Field(
        None,
        description="RoPE context scaling factor (--rope-scale).",
        example=1.0,
        ge=0.1,
    )
    rope_freq_base: Optional[float] = Field(
        None,
        description="RoPE frequency base (--rope-freq-base).",
        example=10000.0,
    )
    rope_freq_scale: Optional[float] = Field(
        None,
        description="RoPE frequency scale (--rope-freq-scale).",
        example=1.0,
    )
    yarn_orig_ctx: Optional[int] = Field(
        None,
        description="Original context length for YARN (--yarn-orig-ctx).",
        example=2048,
        ge=1,
    )
    yarn_ext_factor: Optional[float] = Field(
        None,
        description="Extension factor for YARN context window (--yarn-ext-factor).",
        example=1.5,
    )
    yarn_attn_factor: Optional[float] = Field(
        None,
        description="Attention scaling factor for YARN (--yarn-attn-factor).",
        example=1.0,
    )
    yarn_beta_slow: Optional[float] = Field(
        None,
        description="Slow beta coefficient for YARN (--yarn-beta-slow).",
        example=1.0,
    )
    yarn_beta_fast: Optional[float] = Field(
        None,
        description="Fast beta coefficient for YARN (--yarn-beta-fast).",
        example=1.0,
    )
    grp_attn_n: Optional[int] = Field(
        None,
        description="Group attention N value (--grp-attn-n).",
        example=4,
        ge=1,
    )
    grp_attn_w: Optional[float] = Field(
        None,
        description="Group attention width (--grp-attn-w).",
        example=0.5,
    )
    dump_kv_cache: Optional[bool] = Field(
        False,
        description="Enable dumping KV cache (--dump-kv-cache).",
        example=False,
    )
    no_kv_offload: Optional[bool] = Field(
        False,
        description="Disable KV offloading (--no-kv-offload).",
        example=False,
    )
    cache_type_k: Optional[str] = Field(
        None,
        description="KV cache type for keys (--cache-type-k).",
        example="auto",
    )
    cache_type_v: Optional[str] = Field(
        None,
        description="KV cache type for values (--cache-type-v).",
        example="auto",
    )


class LlamaCLIResponse(BaseModel):
    output: str = Field(..., description="The raw response generated by the model.")
    tokens_generated: Optional[int] = Field(None, description="Estimated number of tokens returned.")
    execution_time_ms: Optional[int] = Field(None, description="Time taken to generate the response (ms).")
    pooling: Optional[str] = Field(
        None,
        description="Specifies the embedding pooling strategy. Options: 'none', 'mean', 'cls', 'last'.",
        example="mean",
    )
    attention: Optional[str] = Field(
        None,
        description="Select attention type: 'causal' or 'non-causal'.",
        example="causal",
    )
    # ───── Logits-only features ─────
    logits_all: Optional[bool] = Field(
        False,
        description="Return logits for all tokens, not just the last one (--logits-all).",
        example=False,
    )
    logits_last_only: Optional[bool] = Field(
        False,
        description="Return only the logits of the last token (--logits-last-only). Overrides logits_all.",
        example=True,
    )
    ignore_eos: Optional[bool] = Field(
        False,
        description="Ignore the end-of-sequence token (--ignore-eos).",
        example=False,
    )
    use_penalty_prompt: Optional[bool] = Field(
        False,
        description="Enable use of penalty prompt tokens (--use-penalty-prompt).",
        example=True,
    )
    # ───── Perplexity & Evaluation ─────
    all_logits: Optional[bool] = Field(
        False,
        description="Return logits for all tokens in the batch (--all-logits).",
        example=False,
    )
    hellaswag: Optional[bool] = Field(
        False,
        description="Compute HellaSwag score over tasks from provided datafile (--hellaswag).",
        example=False,
    )
    hellaswag_tasks: Optional[int] = Field(
        400,
        description="Number of tasks to use in HellaSwag score (--hellaswag-tasks).",
        ge=0,
        example=400,
    )
    winogrande: Optional[bool] = Field(
        False,
        description="Compute Winogrande score from provided datafile (--winogrande).",
        example=False,
    )
    winogrande_tasks: Optional[int] = Field(
        0,
        description="Number of Winogrande tasks to run (--winogrande-tasks).",
        ge=0,
        example=100,
    )
    multiple_choice: Optional[bool] = Field(
        False,
        description="Enable multiple choice scoring (--multiple-choice).",
        example=False,
    )
    multiple_choice_tasks: Optional[int] = Field(
        0,
        description="Number of tasks to use in multiple choice eval (--multiple-choice-tasks).",
        ge=0,
        example=20,
    )
    kl_divergence: Optional[bool] = Field(
        False,
        description="Compute KL divergence against base logits (--kl-divergence).",
        example=False,
    )
    ppl_stride: Optional[int] = Field(
        0,
        description="Stride size for perplexity calculations (--ppl-stride).",
        ge=0,
        example=512,
    )
    ppl_output_type: Optional[int] = Field(
        0,
        description="Output format for perplexity results: 0 (summary), 1 (per-token) (--ppl-output-type).",
        ge=0,
        le=1,
        example=0,
    )

    # ───── Parallel / Batch Execution ─────
    defrag_thold: Optional[float] = Field(
        -1.0,
        description="KV cache defragmentation threshold (--defrag-thold). Set <0 to disable.",
        example=-1.0,
    )
    parallel: Optional[int] = Field(
        1,
        description="Number of parallel sequences to decode (--parallel).",
        ge=1,
        example=1,
    )
    sequences: Optional[int] = Field(
        1,
        description="Number of sequences to decode (--sequences).",
        ge=1,
        example=1,
    )
    cont_batching: Optional[bool] = Field(
        True,
        description="Enable continuous batching (--cont-batching).",
        example=True,
    )
    no_cont_batching: Optional[bool] = Field(
        False,
        description="Disable continuous batching (--no-cont-batching).",
        example=False,
    )

    # ───── Multimodal ─────
    mmproj: Optional[str] = Field(
        None,
        description="Path to multimodal projector file (--mmproj).",
        example="/models/llava/mmproj.bin",
    )
    image: Optional[list[str]] = Field(
        None,
        description="List of image file paths to include (--image).",
        example=["/images/img1.png", "/images/img2.jpg"],
    )

    # ───── Backend / Memory / GPU ─────
    rpc: Optional[str] = Field(
        None,
        description="Comma-separated list of RPC servers (--rpc).",
        example="127.0.0.1:9000,127.0.0.1:9001",
    )
    mlock: Optional[bool] = Field(
        False,
        description="Force model to stay resident in RAM (--mlock).",
        example=True,
    )
    no_mmap: Optional[bool] = Field(
        False,
        description="Disable memory-mapped model load (--no-mmap).",
        example=True,
    )
    run_time_repack: Optional[bool] = Field(
        False,
        description="Repack tensors at runtime if interleaved variant is found (--run-time-repack).",
        example=False,
    )
    gpu_layers_draft: Optional[int] = Field(
        None,
        description="VRAM layers for draft model (--gpu-layers-draft).",
        ge=0,
        example=8,
    )
    split_mode: Optional[str] = Field(
        "layer",
        description="How to split the model across GPUs (--split-mode). Options: 'none', 'layer', 'row'.",
        example="row",
    )
    tensor_split: Optional[str] = Field(
        None,
        description="Comma-separated proportions to split model across GPUs (--tensor-split).",
        example="3,1",
    )
    embedding: Optional[bool] = Field(
        False,
        description="Restrict to embedding-only use case (--embedding).",
        example=False,
    )
    api_key: Optional[str] = Field(
        None,
        description="API key to use for authentication (--api-key).",
        example="super-secret-key",
    )
    api_key_file: Optional[str] = Field(
        None,
        description="Path to file containing API keys (--api-key-file).",
        example="/secrets/api_keys.txt",
    )
    ssl_key_file: Optional[str] = Field(
        None,
        description="Path to PEM-encoded SSL private key (--ssl-key-file).",
        example="/ssl/private.key",
    )
    ssl_cert_file: Optional[str] = Field(
        None,
        description="Path to PEM-encoded SSL certificate (--ssl-cert-file).",
        example="/ssl/certificate.pem",
    )
    timeout: Optional[int] = Field(
        600,
        description="Server read/write timeout in seconds (--timeout).",
        example=600,
        ge=0,
    )
    system_prompt_file: Optional[str] = Field(
        None,
        description="File to load a system prompt (used as initial prompt in all slots) (--system-prompt-file).",
        example="/templates/system_prompt.txt",
    )
    log_format: Optional[str] = Field(
        "json",
        description="Log output format: 'text' or 'json' (--log-format).",
        example="json",
    )
    metrics: Optional[bool] = Field(
        False,
        description="Enable Prometheus-compatible metrics endpoint (--metrics).",
        example=False,
    )
    no_slots: Optional[bool] = Field(
        False,
        description="Disable slot monitoring endpoint (--no-slots).",
        example=False,
    )
    slot_save_path: Optional[str] = Field(
        None,
        description="Path to save slot KV cache (--slot-save-path).",
        example="/slots/kv_cache/",
    )
    chat_template: Optional[str] = Field(
        None,
        description="Custom Jinja chat template (--chat-template).",
        example="chatml",
    )
    slot_prompt_similarity: Optional[float] = Field(
        0.5,
        description="Prompt similarity threshold to reuse slots (--slot-prompt-similarity).",
        example=0.5,
        ge=0.0,
        le=1.0,
    )
    lora_init_without_apply: Optional[bool] = Field(
        False,
        description="Load LoRA adapters without applying them (--lora-init-without-apply).",
        example=False,
    )

    # ───── Control Vectors (cvector) ─────
    cvector_output: Optional[str] = Field(
        None,
        description="Output file for control vector (--output).",
        example="control_vector.gguf",
    )
    positive_file: Optional[str] = Field(
        None,
        description="File with positive prompts for control vector generation (--positive-file).",
        example="positive.txt",
    )
    negative_file: Optional[str] = Field(
        None,
        description="File with negative prompts for control vector generation (--negative-file).",
        example="negative.txt",
    )
    pca_batch: Optional[int] = Field(
        100,
        description="Batch size for PCA in control vector generation (--pca-batch).",
        example=100,
        ge=1,
    )
    pca_iter: Optional[int] = Field(
        1000,
        description="Number of iterations for PCA (--pca-iter).",
        example=1000,
        ge=1,
    )
    method: Optional[str] = Field(
        "pca",
        description="Dimensionality reduction method: 'pca' or 'mean' (--method).",
        example="pca",
    )

    # ───── Export LoRA ─────
    export_model_path: Optional[str] = Field(
        "",
        description="Path to base model for LoRA export (--model).",
        example="/models/base-model.gguf",
    )
    lora_adapters: Optional[list[str]] = Field(
        None,
        description="Paths to LoRA adapters (--lora). Can be repeated.",
        example=["adapter1.safetensors", "adapter2.safetensors"],
    )
    lora_scaled_adapters: Optional[list[tuple[str, float]]] = Field(
        None,
        description="List of tuples (path, scale) for LoRA adapters with scaling (--lora-scaled).",
        example=[("adapter1.safetensors", 0.5)],
    )
    export_threads: Optional[int] = Field(
        128,
        description="Threads used during LoRA export (--threads).",
        example=128,
        ge=1,
    )
    export_output: Optional[str] = Field(
        "ggml-lora-merged-f16.gguf",
        description="Output file for merged LoRA model (--output).",
        example="ggml-lora-merged-f16.gguf",
    )