from abc import ABC, abstractmethod


class ClaimExtractor(ABC):
    """Interface for turning passage text into claims.

    core/ owns the interface; implementations that need an outside library
    (spaCy) live in adapters/claim_extraction/.
    """

    @abstractmethod
    def break_into_claims(self, data: list[str]) -> list[str]: ...
