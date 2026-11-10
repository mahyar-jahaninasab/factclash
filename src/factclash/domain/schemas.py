import hashlib
import json
from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, ConfigDict, model_validator

from factclash.domain.helpers import _normalize_text, _utc_iso


class Source(Enum):
    USER = "user"
    AGENT = "agent"
    RETRIEVAL = "retrieval"


class FactSenseitivity(Enum):
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
    MEASUREMENT = "measurment"
    RECORD = "record"
    ASSERTION = "assertion"


class Fact(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    subject: str
    statement: str
    scope: list[str]
    sensetivity: FactSenseitivity
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    evidence_ids: list[UUID]
    verification_id: UUID
    status: FactStatus
    created_at: datetime
    created_by: Source

    fingerprint: str = ""

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
    id: UUID
    fact_id: UUID
    status: FactStatus
    reason: Optional[str]
    changed_at: datetime


class Evidence(BaseModel):
    id: UUID
    source_id: UUID
    evidence_type: EvidenceType
    content: list[str]
    observed_at: Optional[datetime]
    collected_at: datetime
    metadata: Optional[dict]
