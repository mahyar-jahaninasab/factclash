import pytest
import spacy

from factclash.adapters.claim_extraction.spacy_extractor import SpacyClaimExtractor


@pytest.fixture(scope="module")
def nlp():
    model = spacy.load("en_core_web_md")
    return model


def test_claim_inheritence_of_id_source(nlp):

    passages = [
        "Hello, this note covers the payments cluster. ",
        "The cluster runs 3 replicas. ",
        "Server srv-prod-01 is running. ",
        "If traffic spikes, the cluster scales to 10. ",
        "The nightly backup might be running late. ",
        "Please check the dashboard before deploying.",
    ]

    expected_claims = [
        "The cluster runs 3 replicas.",
        "Server srv-prod-01 is running.",
        "If traffic spikes, the cluster scales to 10.",
    ]

    claim_break = SpacyClaimExtractor(nlp)
    claims = claim_break.break_into_claims(passages)
    actual_claims = [nlp(text) for text in claims]
    extracted_claims = [nlp(text) for text in expected_claims]

    assert len(expected_claims) == len(claims)

    for claim in actual_claims:
        best = max(extracted_claims, key=lambda d: claim.similarity(d))
        assert claim.similarity(best) > 0.9
