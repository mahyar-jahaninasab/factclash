# NLP-based Text Analytics

import spacy
from spacy.language import Language

from factclash.core.claims import ClaimExtractor


class SpacyClaimExtractor(ClaimExtractor):
    def __init__(self, model: Language):
        self.model = model

    def break_into_claims(self, data: list[str]) -> list[str]:
        return data


# Exploration script: runs only with `python -m`, never on import.
if __name__ == "__main__":
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_md")

    # Process whole documents
    text = (
        "When Sebastian Thrun started working on self-driving cars at one"
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week."
    )
    doc = nlp(text)

    # Analyze syntax
    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("--------------")

    # 1. Detect numbers using spaCy's built-in token attribute
    print(
        "Numbers (via token.like_num):", [token.text for token in doc if token.like_num]
    )

    # 2. Detect numbers/dates via Named Entity Recognition (NER)
    print(
        "Numeric Entities (Date/Cardinal/etc.):",
        [
            (entity.text, entity.label_)
            for entity in doc.ents
            if entity.label_ in {"DATE", "CARDINAL", "MONEY", "PERCENT"}
        ],
    )

    doc = nlp("Autonomous cars shift insurance liability toward manufacturers.")

    # Extract full noun phrases
    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    # Output: ['Autonomous cars', 'insurance liability', 'manufacturers']

    # Find the main action (ROOT) and its subject
    for token in doc:
        if token.dep_ == "nsubj":
            print(f"Subject: {token.text} | Action: {token.head.text}")
    # Output: Subject: cars | Action: shift
