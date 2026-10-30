from enum import Enum
from typing import Optional, Union
from uuid import UUID
import uuid

from pydantic import BaseModel, Field, ConfigDict


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

class Analyzer(Enum):
    """Specifies the underlying engine or methodology used to analyze and detect contradictions."""
    LLM = "LLM"
    HYBRID = "HYBRID"
    NLP = "NLP"


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
    # Example 
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                        {
                        "blocks": [
                            {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "source_type": "retrieval",
                            "passages": [
                                            "The facility operates 24 hours a day, 7 days a week.",
                                            "The facility closes at 6:00 PM every evening."
                                            ],
                            "metadata": {
                                "id": "operational",
                                "description": "The retrived doc discusses operational timing of the facility",
                                "score": 0.25,
                                "prompt": "find me facility operations I was told it is three days a week",
                                "provider": "rag"
                            }
                            }
                        ]
                        }
                    ]
        }
    )

class ContradictionAnalysis(BaseModel):
    """Represents the complete analysis results and evaluation metrics for a detected contradiction."""
    
    contradiction_type: ContradictionType = Field(
        ..., 
        description="The classification category of the contradiction identified in the text."
    )
    analyzer: Analyzer = Field(
        ..., 
        description="The analysis engine or methodology (e.g., LLM, NLP, Hybrid) used to perform the check."
    )
    confidence: float = Field(
        ..., 
        description="Statistical confidence score or probability assigned to the detected contradiction (ranging from 0.0 to 1.0)."
    )
    metadata: Optional[dict] = Field(
        default=None, 
        description="Additional diagnostic metadata, token metrics, or raw model outputs from the analysis."
    )
    context_block: ContextBlock = Field(
        ..., 
        description="The specific context block containing the passages where the contradiction was evaluated."
    )


class ContradictionAnalysisCollection(BaseModel):
    """Wrapper collection representing a batch of contradiction analysis results."""
    
    blocks: list[ContradictionAnalysis] = Field(
        ..., 
        description="A list of contradiction analysis results evaluated across the source context blocks."
    )
