import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

from factclash.domain.helpers import _normalize_text, _utc_iso


class SourceType(Enum):
    USER = "user"
    AGENT = "agent"
    RETRIEVAL = "retrieval"


class FactSensitivity(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class FactStatus(Enum):
    ACCEPTED = "accepted"
    DISPUTED = "disputed"
    SUPERSEDED = "superseded"
    RETRACTED = "retracted"


class EvidenceType(Enum):
    DOCUMENT = "document"
    OBSERVATION = "observation"
    MEASUREMENT = "measurement"
    RECORD = "record"
    ASSERTION = "assertion"


class Source(BaseModel):
    id: UUID = Field(description="Unique identifier for the source")
    source_type: SourceType = Field(
        description="Category of the source (user, agent, retrieval)"
    )
    name: str = Field(description="Display name of the source")
    reliability: float = Field(description="Assessed reliability score of the source")
    uri: Optional[HttpUrl] = Field(
        default=None, description="Location URL of the original source"
    )


class Fact(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID = Field(description="Unique identifier for the Fact")
    subject: str = Field(description="What the Fact is about")
    statement: str = Field(description="The proposition accepted as factual truth")
    scope: list[str] = Field(description="Context in which the Fact holds")
    sensitivity: FactSensitivity = Field(description="Access classification level")
    valid_from: Optional[datetime] = Field(
        default=None, description="Start of validity period in the real world"
    )
    valid_until: Optional[datetime] = Field(
        default=None, description="End of validity period in the real world"
    )
    evidence_ids: list[UUID] = Field(
        description="List of supporting evidence identifiers"
    )
    verification_id: UUID = Field(description="Reference to the verification process")
    status: FactStatus = Field(description="Current status of the Fact")
    created_at: datetime = Field(description="Timestamp when the Fact was recorded")
    source: Source = Field(description="Source information for the Fact")
    fingerprint: str = Field(
        default="", description="SHA-256 computed hash used for duplicate detection"
    )

    @model_validator(mode="after")
    def compute_fingerprint_eagerly(self) -> "Fact":
        payload = {
            "subject": _normalize_text(self.subject),
            "statement": _normalize_text(self.statement),
            "scope": self.scope,
            "valid_from": _utc_iso(self.valid_from),
            "valid_until": _utc_iso(self.valid_until),
        }
        blob = json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )
        computed = hashlib.sha256(blob.encode("utf-8")).hexdigest()
        object.__setattr__(self, "fingerprint", computed)
        return self


class FactStatusChange(BaseModel):
    id: UUID = Field(description="Unique identifier for the status change record")
    fact_id: UUID = Field(description="Reference to the Fact whose status changed")
    status: FactStatus = Field(description="New status applied to the Fact")
    reason: Optional[str] = Field(
        default=None, description="Explanation or rationale for the status change"
    )
    changed_at: datetime = Field(
        description="Timestamp when the status change occurred"
    )


class Evidence(BaseModel):
    id: UUID = Field(description="Unique identifier for the evidence")
    source_id: UUID = Field(
        description="Reference to the Source where this evidence originated"
    )
    evidence_type: EvidenceType = Field(description="Category of the evidence")
    content: list[str] = Field(description="The evidence payload content")
    observed_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the evidence was produced or observed"
    )
    collected_at: datetime = Field(
        description="Timestamp when the system received the evidence"
    )
