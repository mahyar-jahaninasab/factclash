from enum import Enum
from typing import Optional, Union
from uuid import UUID
import uuid

from pydantic import BaseModel, Field


class ContradictionType(Enum):
    """Enumeration representing different types of logical or semantic contradictions."""
    STRICT = "STRICT"
    CONTRARY = "CONTRARY"
    QUANTIFICATION = "QUANTIFICATION"
    LEXICAL = "LEXICAL"
    TEMPORAL = "TEMPORAL"
    PRAGMATIC = "PRAGMATIC"


class SourceType(Enum):
    """Enumeration representing the origin or source type of the context."""
    RETRIEVAL = "retrieval"
    SEARCH = "search"
    GENERATION = "generation"
    PROMPT = "prompt"


class BaseSourceMetadata(BaseModel):
    """Base metadata associated with an information source."""
    
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


class GenerationSourceMetadata(BaseSourceMetadata):
    """Metadata specific to generated context, extending BaseSourceMetadata."""
    
    turn_number: int = Field(
        ..., 
        description="The conversation turn number during which this context was generated."
    )


class ContextBlock(BaseModel):
    """Container representing a source context block and its associated metadata."""
    
    id: UUID = Field(
        default_factory=uuid.uuid4, 
        description="Unique identifier (UUID) for this source context record."
    )
    source_type: SourceType = Field(
        ..., 
        description="The origin or category of the information source."
    )
    passages: list[str] = Field(
        ..., 
        description="List of text chunks or passages used for contradiction analysis."
    )
    metadata: Optional[Union[BaseSourceMetadata, GenerationSourceMetadata]] = Field(
        default=None, 
        description="Additional structured metadata providing context details, origin, or generation turn information."
    )


class ContextBlockCollection(BaseModel):
    """Wrapper collection for multiple context blocks evaluated in the pipeline."""
    
    blocks: list[ContextBlock] = Field(
        ..., 
        description="List of context sources for the contradiction detection pipeline."
    )