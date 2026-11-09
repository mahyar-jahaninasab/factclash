import pytest
from factclash.contradictions.schemas import ContradictionType
from factclash.services.analyzer.nlp_based import NLPAnalyzer


@pytest.fixture
async def nlp_analyzer():
    return NLPAnalyzer()


@pytest.mark.asyncio
async def test_async_strict_contradiction(nlp_analyzer):
    data = ["Today is Tuesday.", "Today is not Tuesday."]

    contradiction_type = await nlp_analyzer.context_analysis(data)

    assert contradiction_type == ContradictionType.STRICT


@pytest.mark.asyncio
async def test_async_contrary_contradiction(nlp_analyzer):
    data = [
        "The medication causes drowsiness.",
        "The medication does not cause drowsiness.",
    ]
    contradiction_type = await nlp_analyzer.context_analysis(data)
    assert contradiction_type == ContradictionType.CONTRARY


@pytest.mark.asyncio
async def test_async_quantification_contradiction(nlp_analyzer):
    data = [
        "The medication causes drowsiness.",
        "The medication does not cause drowsiness.",
    ]
    contradiction_type = await nlp_analyzer.context_analysis(data)
    assert contradiction_type == ContradictionType.QUANTIFICATION


@pytest.mark.asyncio
async def test_async_lexical_contradiction(nlp_analyzer):
    data = [
        "The Principal hereby grants the Distributor an exclusive right to market and sell the Products within the territory of New South Wales.",
        "The Principal explicitly reserves the right to directly market and sell the Products to any corporate clients located in New South Wales.",
    ]
    contradiction_type = await nlp_analyzer.context_analysis(data)
    assert contradiction_type == ContradictionType.LEXICAL


@pytest.mark.asyncio
async def test_async_temporal_contradiction(nlp_analyzer):

    data = [
        "Document A (9:30 AM): The Company maintains a Strong Buy credit risk rating and a positive cash flow outlook for the upcoming quarter.",
        "Document B (2:15 PM): The Company has entered Voluntary Administration under Section 436A of the Corporations Act 2001 (Cth); all trading of shares is suspended.",
    ]
    contradiction_type = await nlp_analyzer.context_analysis(data)
    assert contradiction_type == ContradictionType.TEMPORAL


@pytest.mark.asyncio
async def test_async_pragmatic_contradiction(nlp_analyzer):
    data = [
        "Patient is conscious, fully alert, and conversing comfortably with staff.",
        "Patient's documented pulse rate is 0 bpm (asystole).",
    ]
    contradiction_type = await nlp_analyzer.context_analysis(data)
    assert contradiction_type == ContradictionType.PRAGMATIC
