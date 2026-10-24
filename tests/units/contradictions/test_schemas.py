import pytest 
from factclash.contradictions.schemas import SourceContext
from uuid import uuid4
from pydantic_core._pydantic_core import ValidationError


def test_accept_prompt_fields():
    data = {
          "id": uuid4(),
          "source": "prompt",
          "context": ["Since server srv-prod-01 is running, why are you reporting that SSL Certificate #402 IS NOT VALID?"]
        }
    
    pydantic_model = SourceContext.model_validate(data) 

    assert pydantic_model.id == data["id"]
    assert pydantic_model.source.value == data["source"]
    assert pydantic_model.context == data["context"]

def test_accept_search_fields():
    data = {
        "id": uuid4(),
        "source": "search",
        "context": ["Public Cloud Incident #8810: Server srv-prod-01 taken offline for scheduled emergency patching."],
        "metadata": {
            "id": "search_res_8810",
            "description": "Public Cloud Incident Log",
            "prompt": "srv-prod-01 current status incident log"}
    }
    
    pydantic_model = SourceContext.model_validate(data) 

    assert pydantic_model.id == data["id"]
    assert pydantic_model.source.value  == data["source"]
    assert pydantic_model.context == data["context"]
    assert pydantic_model.metadata.id == data["metadata"]["id"]
    assert pydantic_model.metadata.description == data["metadata"]["description"]
    assert pydantic_model.metadata.prompt == data["metadata"]["prompt"]

def test_accept_retrieval_fields():
    data ={
            "id": uuid4(),
            "source": "retrieval",
            "context": ["Server srv-prod-01 IS NOT RUNNING. (System State: Terminated). SSL Certificate #402 IS VALID (Expiration: 90 days remaining)."],
            "metadata": {
                "id": "doc_live_telemetry_2026",
                "description": "Live Telemetry Snapshot",
                "prompt": "RAG retrieval for server status and certificate verification",
                "score": 0.88
            }
    }
    
    pydantic_model = SourceContext.model_validate(data) 

    assert pydantic_model.id == data["id"]
    assert pydantic_model.source.value  == data["source"]
    assert pydantic_model.context == data["context"]
    assert pydantic_model.metadata.id == data["metadata"]["id"]
    assert pydantic_model.metadata.description == data["metadata"]["description"]
    assert pydantic_model.metadata.prompt == data["metadata"]["prompt"]
    assert pydantic_model.metadata.score == data["metadata"]["score"]

def test_accept_generation_fields():
    data =    {
      "id": uuid4(),
      "source": "generation",
      "context": ["Assistant prior response: Server srv-prod-01 IS RUNNING."],
      "metadata": {
        "turn_number": 1
      }
    }
    
    pydantic_model = SourceContext.model_validate(data) 

    assert pydantic_model.id == data["id"]
    assert pydantic_model.source.value  == data["source"]
    assert pydantic_model.context == data["context"]
    assert pydantic_model.metadata.turn_number == data["metadata"]["turn_number"]


def test_str_context_fields():
    data = {
          "id": uuid4(),
          "source": "prompt",
          "context": "Since server srv-prod-01 is running, why are you reporting that SSL Certificate #402 IS NOT VALID?"
        }

    with pytest.raises(ValidationError):
        SourceContext.model_validate(data) 



