import pytest
from app.schemas.llama_inference_schema import LlamaInferenceParams
from pydantic import ValidationError

def test_llama_inference_schema_metadata():
    fields = LlamaInferenceParams.model_fields

    # Only inspect safe, simple fields
    safe_fields = ["prompt", "temperature", "n_predict"]
    for field_name in safe_fields:
        model_field = fields[field_name]
        print(f"\n🔍 Field: {field_name}")
        print(f"  • Type: {model_field.annotation}")
        print(f"  • Description: {model_field.description}")
        print(f"  • Default: {model_field.default}")
        extra = model_field.json_schema_extra or {}
        if "example" in extra:
            print(f"  • Example: {extra['example']}")
        if "ge" in extra or "le" in extra:
            print(f"  • Constraints: ge={extra.get('ge')}, le={extra.get('le')}")

    # Basic schema integrity check
    assert "prompt" in fields
    assert fields["prompt"].description is not None


def test_llama_inference_field_constraints():
    # Valid example
    valid = LlamaInferenceParams(prompt="Tell me a joke", temperature=0.7, n_predict=64)
    assert valid.prompt == "Tell me a joke"
    assert 0.0 <= valid.temperature <= 1.0

    # Invalid: empty prompt
    with pytest.raises(ValidationError):
        LlamaInferenceParams(prompt="")

    # Invalid: temperature out of range
    with pytest.raises(ValidationError):
        LlamaInferenceParams(prompt="hi", temperature=1.5)

    # Invalid: n_predict not positive
    with pytest.raises(ValidationError):
        LlamaInferenceParams(prompt="hi", n_predict=0)

    # Valid edge case: top_k and top_p at boundary
    valid = LlamaInferenceParams(prompt="Test", top_k=0, top_p=1.0)
    assert valid.top_k == 0
    assert valid.top_p == 1.0