from enum import Enum
from typing import Optional
from uuid import UUID
import uuid

from pydantic import BaseModel, Field


class ContradictionsType(Enum):
    """Enumeration representing different types of logical or semantic contradictions."""
    STRICT = "STRICT"
    CONTRARY = "CONTRARY"
    QUANTIFICATION = "QUANTIFICATION"
    LEXICAL = "LEXICAL"
    TEMPORAL = "TEMPORAL"
    PRAGMATIC = "PRAGMATIC"


class ContextSource(Enum):
    """Enumeration representing the origin or source type of the context."""
    retrieval = "retrieval"
    search = "search"
    generation = "generation"
    prompt = "prompt"


class SourceMetadata(BaseModel):
    """Metadata associated with a general information source."""
    
    id: Optional[str] = Field(
        default=None, 
        description="Unique identifier to trace the source document from which the information originated."
    )
    description: Optional[str] = Field(
        default=None, 
        description="High-level summary or description of the source document."
    )
    score: Optional[float] = Field(
        default=None, 
        description="Estimated confidence score indicating the quality or relevance of the context."
    )
    prompt: Optional[str] = Field(
        default=None, 
        description="The user prompt or query that resulted in the creation of this context."
    )
    provider: Optional[str] = Field(
        default=None, 
        description="Name of the service provider, system, or API that supplied the information."
    )   


class GenerationMetadata(SourceMetadata):
    """Metadata specific to generated context, inheriting from SourceMetadata."""
    
    turn_number: int = Field(
        ..., 
        description="The conversation turn number during which this context was generated."
    )


class ContextSource(BaseModel):
    """Container representing a source context block and its associated metadata."""
    
    id: UUID = Field(
        default_factory=uuid.uuid4, 
        description="Unique identifier (UUID) for this source context record."
    )
    source: ContextSource = Field(
        ..., 
        description="The origin or category of the information source."
    )
    context: list[str] = Field(
        ..., 
        description="List of text chunks or passages used for contradiction analysis."
    )
    metadata: Optional[SourceMetadata | GenerationMetadata] = Field(
        default=None, 
        description="Additional structured metadata providing context details, origin, or generation turn information."
    )

class ContextSources(BaseModel):
    context_sources: list[ContextSource] = Field(..., description="list of context source for contradiction detection pipeline")