#!/bin/bash

# -----------------------------------------------------------------------------
# File: fake_llama_cli.sh
# Purpose: Simulates the behavior of `llama-cli` for testing purposes.
# This script echoes received arguments and outputs a canned response.
# Used in unit tests to mock the CLI interface without running the real model.
# -----------------------------------------------------------------------------


# Simulated fake llama-cli for testing
echo "Simulated llama-cli"
echo "Prompt received: $*"

# Fake response
echo "The capital of France is Paris."
exit 0