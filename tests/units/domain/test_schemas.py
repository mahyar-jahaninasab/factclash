from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from uuid import uuid4
import pytest
from pydantic import ValidationError

from factclash.domain.schemas import (
    Fact,
    FactSensitivity,
    FactStatus,
    Source,
    SourceType,
    CurrentFactStatus,
    Hypothesis,
    HypothesisStatus,
    Premise,
    PremiseStatus,
)


@pytest.fixture
def sample_source() -> Source:
    return Source(
        id=uuid4(),
        source_type=SourceType.AGENT,
        name="Telemetry",
        reliability=0.9,
    )


def make_fact(
    source: Source,
    subject: str = "Checkout DB",
    statement: str = "Pool exhausted",
    scope: list[str] | None = None,
    valid_from: datetime | None = None,
) -> Fact:
    return Fact(
        id=uuid4(),
        subject=subject,
        statement=statement,
        scope=scope if scope is not None else ["production"],
        sensitivity=FactSensitivity.PUBLIC,
        valid_from=valid_from,
        valid_until=None,
        evidence_ids=(uuid4(),),
        verification_id=uuid4(),
        created_at=datetime.now(timezone.utc),
        source=source,
    )


def make_hypothesis(
    statement: str = "Cache hit rate can exceed 95%",
    scope: list[str] | None = None,
    confidence: float | None = 0.85,
    status: HypothesisStatus = HypothesisStatus.PROPOSED,
) -> Hypothesis:
    return Hypothesis(
        id=uuid4(),
        subject="Cache Service",
        statement=statement,
        scope=scope if scope is not None else ["production"],
        sensitivity=FactSensitivity.PUBLIC,
        confidence=confidence,
        status=status,
        created_at=datetime.now(timezone.utc),
        created_by=SourceType.AGENT,
    )


def make_premise(
    statement: str = "Redis cluster is healthy",
    scope: list[str] | None = None,
    confidence: float | None = 0.95,
    status: PremiseStatus = PremiseStatus.ACTIVE,
) -> Premise:
    return Premise(
        id=uuid4(),
        statement=statement,
        scope=scope if scope is not None else ["production"],
        sensitivity=FactSensitivity.PUBLIC,
        confidence=confidence,
        status=status,
        created_at=datetime.now(timezone.utc),
        created_by=SourceType.AGENT,
    )


def test_fact_requires_evidence(sample_source):
    with pytest.raises(
        ValidationError, match="A fact must have at least one piece of evidence"
    ):
        Fact(
            id=uuid4(),
            subject="Test Subject",
            statement="Test Statement",
            scope=["production"],
            sensitivity=FactSensitivity.PUBLIC,
            valid_from=None,
            valid_until=None,
            evidence_ids=(),
            verification_id=uuid4(),
            created_at=datetime.now(timezone.utc),
            source=sample_source,
        )


def test_fact_is_immutable(sample_source):
    fact = make_fact(sample_source)
    with pytest.raises(ValidationError):
        setattr(fact, "statement", "Modified statement")


def test_fact_status_change_is_tracked_separately(sample_source):
    fact = make_fact(sample_source)
    change = CurrentFactStatus(
        id=uuid4(),
        fact_id=fact.id,
        status=FactStatus.DISPUTED,
        reason="New data conflicts with previous observations.",
        changed_at=datetime.now(timezone.utc),
    )

    assert change.status == FactStatus.DISPUTED
    assert change.fact_id == fact.id


def test_fingerprint_differs_on_tab_or_newline(sample_source: Source):
    fact1 = make_fact(sample_source, statement="Pool exhausted")
    fact2 = make_fact(sample_source, statement="Pool\texhausted")
    fact3 = make_fact(sample_source, statement="Pool\nexhausted")

    assert fact1.fingerprint == fact2.fingerprint
    assert fact1.fingerprint == fact3.fingerprint


def test_fingerprint_equal_on_timezone_equivalence(sample_source: Source):
    utc_time = datetime(2026, 3, 29, 14, 0, 0, tzinfo=timezone.utc)
    ny_time = datetime(2026, 3, 29, 10, 0, 0, tzinfo=ZoneInfo("America/New_York"))

    fact1 = make_fact(sample_source, valid_from=utc_time)
    fact2 = make_fact(sample_source, valid_from=ny_time)

    assert fact1.fingerprint == fact2.fingerprint


def test_fingerprint_equal_on_mixed_casing_and_outer_spaces(sample_source: Source):
    fact1 = make_fact(sample_source, subject="CHECKOUT DB", statement="POOL EXHAUSTED")
    fact2 = make_fact(
        sample_source, subject="  checkout db  ", statement="\tpool exhausted\n"
    )

    assert fact1.fingerprint == fact2.fingerprint


def test_hypothesis_confidence_validation():
    with pytest.raises(ValidationError):
        make_hypothesis(confidence=1.5)
    with pytest.raises(ValidationError):
        make_hypothesis(confidence=-0.1)


def test_hypothesis_immutable_fields():
    hypothesis = make_hypothesis()
    with pytest.raises(ValidationError):
        setattr(hypothesis, "statement", "Modified hypothesis statement")
    with pytest.raises(ValidationError):
        setattr(hypothesis, "scope", ["staging"])


def test_hypothesis_creation_and_status():
    h = make_hypothesis(confidence=None, status=HypothesisStatus.CONFIRMED)
    assert h.confidence is None
    assert h.status == HypothesisStatus.CONFIRMED


def test_premise_confidence_validation():
    with pytest.raises(ValidationError):
        make_premise(confidence=1.1)
    with pytest.raises(ValidationError):
        make_premise(confidence=-0.05)


def test_premise_immutable_fields():
    premise = make_premise()
    with pytest.raises(ValidationError):
        setattr(premise, "statement", "Modified premise statement")
    with pytest.raises(ValidationError):
        setattr(premise, "scope", ["staging"])


def test_premise_creation_and_status():
    p = make_premise(confidence=None, status=PremiseStatus.INVALIDATED)
    assert p.confidence is None
    assert p.status == PremiseStatus.INVALIDATED
