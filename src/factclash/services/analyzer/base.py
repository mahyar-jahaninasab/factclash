from abc import ABC,abstractmethod
from factclash.contradictions.schemas import ContradictionType,Analyzer,ContradictionAnalysisCollection,ContextBlockCollection

class ContradictionAnalyzer(ABC):
    def __init__(self):
        self.name = "Unique name of the analyzer"
        self.description = "A detailed description of the analyzer's functionality."
        self.method: Analyzer = None

    @abstractmethod
    async def context_analysis(self, context:list[str]) ->  ContradictionType:
        pass

    @abstractmethod
    async def confidence_analysis(self, context:list[str],contradiction_type: ContradictionType) -> float:
        pass

    @abstractmethod
    async def overall_analysis(self, context_blocks:ContextBlockCollection) -> ContradictionAnalysisCollection:
        pass



    