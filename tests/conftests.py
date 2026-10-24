import pytest 
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


@pytest.fixture
def raw_contradictions_json() -> dict:
    "Load a strict JSON schema file as a dict"
    file_path = BASE_DIR / "tests" / "fixtures" / "schemas" / "contradictions_schema.json"
    return json.loads(file_path)["context_sources"]

    

