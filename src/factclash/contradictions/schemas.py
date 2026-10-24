from typing import Optional
from uuid import UUID
import uuid

from pydantic import BaseModel, Field
from enum import Enum


class ContradictionsType(Enum):
    STRICT = "STRICT"
    CONTRARY = "CONTRARY"
    QUANTIFICATION = "QUANTIFICATION"
    LEXICAL = "LEXICAL"
    TEMPORAL = "TEMPORAL"
    PRAGMATIC = "PRAGMATIC"

class ContextSource(Enum):
    retrieval = "retrieval"
    search = "search"
    generation = "generation"
    prompt = "prompt"


class SourceMetadata(BaseModel):
    id: Optional[str] = Field(default=None, description="Identifying the source of information")
    description: Optional[str] = Field(default=None, description="Describing information importance and what it contains on a high level")
    score: Optional[float]= Field(default=None, description="Estimated accuracy for the information (e.g: Generation -> Temperature, Retrieval -> Accuracy, Search -> Validity of Source)")
    prompt: Optional[str] = Field(default=None, description="User prompt that triggered to result the context")
    provider: Optional[str] = Field(default=None, description="The name of the provider")   

class GenerationMetadata(SourceMetadata):
    turn_number: int = Field(..., description="Which turn of conversation it belongs to")

class SourceContext(BaseModel):
    id: UUID =  Field(default_factory=uuid.uuid4(), description="Unique id identifying the context")
    source: ContextSource = Field(..., description="The source of context used to establish trust on the source")
    context: list[str] = Field(...,description="Finding contradictions on the context")
    metadata: Optional[SourceMetadata | GenerationMetadata] = Field(default=None,description="Metadata of the context the context")

 