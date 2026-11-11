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


class HypothesisStatus(Enum):
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    ADOPTED = "adopted"
    REFUTED = "refuted"
    ABANDONED = "abandoned"


class PremiseStatus(Enum):
    ACTIVE = "active"
    INVALIDATED = "invalidated"
    WITHDRAWN = "withdrawn"


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
    def validate_evidence(self) -> "Fact":
        if not self.evidence_ids:
            raise ValueError("A fact must have at least one piece of evidence")
        return self

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


class CurrentFactStatus(BaseModel):
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


class Hypothesis(BaseModel):
    id: UUID = Field(description="Unique identifier for the Hypothesis")
    subject: str = Field(description="What the Hypothesis is about (Reference or Text)")
    statement: str = Field(
        frozen=True,
        description="The unverified proposition under evaluation. Immutable",
    )
    scope: list[str] = Field(
        frozen=True,
        description="Non-temporal context in which the proposition would hold. Immutable",
    )
    sensitivity: FactSensitivity = Field(description="Access classification level")
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Current internal estimate (0 to 1) used for ranking, not for verification",
    )
    status: HypothesisStatus = Field(
        description="Current status (proposed, confirmed, adopted, refuted, abandoned)"
    )
    created_at: datetime = Field(
        description="Timestamp when the Hypothesis was created"
    )
    created_by: SourceType = Field(
        description="Actor (User / Agent / System) who proposed the Hypothesis"
    )


class Premise(BaseModel):
    id: UUID = Field(description="Unique identifier for the Premise")
    statement: str = Field(
        frozen=True,
        description="The assumed proposition for a line of reasoning. Immutable",
    )
    scope: list[str] = Field(
        frozen=True,
        description="Context in which the proposition is assumed true. Immutable",
    )
    sensitivity: FactSensitivity = Field(description="Access classification level")
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score associated with the assumed proposition",
    )
    status: PremiseStatus = Field(
        description="Current status (active, invalidated, withdrawn)"
    )
    created_at: datetime = Field(description="Timestamp when the Premise was recorded")
    created_by: SourceType = Field(
        description="Actor (User / Agent / System) who adopted the Premise"
    )
