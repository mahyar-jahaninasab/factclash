from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from uuid import uuid4
import pytest
from pydantic import ValidationError

from factclash.domain.schemas import (
    Fact,
    FactSensitivity,
    FactStatus,
    FactStatusChange,
    Source,
    SourceType,
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
        status=FactStatus.ACCEPTED,
        created_at=datetime.now(timezone.utc),
        source=source,
    )


def test_fact_status_limited_to_enum_values(sample_source):
    fact = make_fact(sample_source)
    assert fact.status in FactStatus

    expected_statuses = {"accepted", "disputed", "superseded", "retracted"}
    actual_statuses = {status.value for status in FactStatus}
    assert actual_statuses == expected_statuses


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
            status=FactStatus.ACCEPTED,
            created_at=datetime.now(timezone.utc),
            source=sample_source,
        )


def test_fact_is_immutable(sample_source):
    fact = make_fact(sample_source)
    with pytest.raises(ValidationError):
        setattr(fact, "statement", "Modified statement")


def test_fact_status_change_is_tracked_separately(sample_source):
    fact = make_fact(sample_source)
    change = FactStatusChange(
        id=uuid4(),
        fact_id=fact.id,
        status=FactStatus.DISPUTED,
        reason="New data conflicts with previous observations.",
        changed_at=datetime.now(timezone.utc),
    )

    assert fact.status == FactStatus.ACCEPTED
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
