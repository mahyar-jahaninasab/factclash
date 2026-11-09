import pytest
from factclash.contradictions.schemas import ContradictionType
from factclash.services.analyzer.nlp_based import NLPAnalyzer


@pytest.fixture
async def nlp_analyzer():
    return NLPAnalyzer()


@pytest.mark.parametrize(
    "data,expected_type",
    [
        (
            ["Today is Tuesday.", "Today is not Tuesday."],
            ContradictionType.STRICT,
        ),
        (
            [
                "The medication causes drowsiness.",
                "The medication does not cause drowsiness.",
            ],
            ContradictionType.CONTRARY,
        ),
        (
            [
                "Zero micro-fissures (cracks) are permissible within the structural core of the titanium turbine hub assembly.",
                "A single micro-fissure measuring 0.02 mm was detected in the turbine hub core; the component remains structurally sound.",
            ],
            ContradictionType.QUANTIFICATION,
        ),
        (
            [
                "The Principal hereby grants the Distributor an exclusive right to market and sell the Products within the territory of New South Wales.",
                "The Principal explicitly reserves the right to directly market and sell the Products to any corporate clients located in New South Wales.",
            ],
            ContradictionType.LEXICAL,
        ),
        (
            [
                "Document A (9:30 AM): The Company maintains a Strong Buy credit risk rating and a positive cash flow outlook for the upcoming quarter.",
                "Document B (2:15 PM): The Company has entered Voluntary Administration under Section 436A of the Corporations Act 2001 (Cth); all trading of shares is suspended.",
            ],
            ContradictionType.TEMPORAL,
        ),
        (
            [
                "Patient is conscious, fully alert, and conversing comfortably with staff.",
                "Patient's documented pulse rate is 0 bpm (asystole).",
            ],
            ContradictionType.PRAGMATIC,
        ),
    ],
)
async def test_async_contradiction_analysis(nlp_analyzer, data, expected_type):
    contradiction_type = await nlp_analyzer.context_analysis(data)
    assert contradiction_type == expected_type
