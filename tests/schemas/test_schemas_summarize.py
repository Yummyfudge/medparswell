from app.schemas.text_summary_schema import SummarizeRequest
from pydantic import ValidationError
import pytest

def test_valid_summarization_request():
    request = SummarizeRequest(content="This is a test.")
    assert request.content == "This is a test."

def test_empty_content_fails():
    with pytest.raises(ValidationError) as exc_info:
        SummarizeRequest(content="")
    assert "ensure this value has at least 1 characters" in str(exc_info.value)