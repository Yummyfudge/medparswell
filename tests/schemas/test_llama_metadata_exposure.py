import pytest
from app.schemas.llama_inference_schema import LlamaInferenceParameters as LlamaInferenceModel
from pydantic import ValidationError

def test_llama_inference_schema_metadata():
    fields = LlamaInferenceModel.model_fields

    # Only inspect safe, simple fields
    safe_fields = ["prompt", "ctx_size", "gpu_layers", "main_gpu"]
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
    valid = LlamaInferenceModel(prompt="Tell me a joke", ctx_size=2048, gpu_layers=4, main_gpu=0)
    assert valid.prompt == "Tell me a joke"

    # Invalid: empty prompt
    with pytest.raises(ValidationError) as exc_info:
        LlamaInferenceModel(prompt="")
    assert "should have at least 1 character" in str(exc_info.value)

    # The following tests are commented out because these fields no longer exist in the schema
    # # Invalid: temperature out of range
    # with pytest.raises(ValidationError) as exc_info:
    #     LlamaInferenceModel(prompt="hi", temperature=1.5)
    # assert exc_info.value.errors()

    # # Invalid: n_predict not positive
    # with pytest.raises(ValidationError) as exc_info:
    #     LlamaInferenceModel(prompt="hi", n_predict=0)
    # assert exc_info.value.errors()

    # # Valid edge case: top_k and top_p at boundary
    # valid = LlamaInferenceModel(prompt="Test", top_k=0, top_p=1.0)
    # assert valid.top_k == 0
    # assert valid.top_p == 1.0