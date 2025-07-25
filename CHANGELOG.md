# v0.0.5
# -------------------------------
# 🔧 v0.0.5 – Structural Refactor & Logging Upgrade
#
# • Replaced legacy print/debug statements with centralized logging.
# • Migrated schema field metadata to Pydantic v2+ conventions using json_schema_extra.
# • Fully cleaned and validated all schema test cases with accurate Gradio-compatible metadata.
# • Removed deprecated routes, placeholder tests, and unused fakes.
# • Added robust file/console logging configuration in logging_config.py.
# • Converted health check and test runner into proper modular test files.
# • Ensured clean test pass: 8 passed, 1 skipped, 0 warnings (excluding external deprecations).
# • Final prep before integration with actual ik_llama.cpp backend.
#
# This commit marks the project as API-compatible, metadata-complete, and fully test-stable.
# Ready for first real-world deployment or UI hook-in (Gradio/OpenWebUI).