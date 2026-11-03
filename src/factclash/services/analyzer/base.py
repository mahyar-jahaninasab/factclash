from abc import ABC, abstractmethod
from typing import Type

from factclash.contradictions.schemas import (
    Analyzer,
    ContextBlockCollection,
    ContradictionAnalysisCollection,
    ContradictionType,
)

ANALYZER_REGISTRY: dict[Analyzer, Type["ContradictionAnalyzer"]] = {}


def register_analyzer(method: Analyzer):
    """Decorator to automatically register an analyzer class."""

    def decorator(cls: Type["ContradictionAnalyzer"]):
        ANALYZER_REGISTRY[method] = cls
        return cls

    return decorator


class ContradictionAnalyzer(ABC):
    def __init__(self, method: Analyzer):
        self.name = "Unique name of the analyzer"
        self.description = "A detailed description of the analyzer's functionality."
        self.method = method

    @abstractmethod
    async def context_analysis(self, context: list[str]) -> ContradictionType:
        pass

    @abstractmethod
    async def confidence_analysis(
        self, context: list[str], contradiction_type: ContradictionType
    ) -> float:
        pass

    @abstractmethod
    async def overall_analysis(
        self, context_blocks: ContextBlockCollection
    ) -> ContradictionAnalysisCollection:
        pass
