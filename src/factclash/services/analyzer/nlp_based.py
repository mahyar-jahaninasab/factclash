from factclash.contradictions.schemas import ContextBlockCollection, ContradictionAnalysis, ContradictionAnalysisCollection, ContradictionType
from factclash.services.analyzer.base import ContradictionAnalyzer,Analyzer


class NLPAnalyzer(ContradictionAnalyzer):
    def __init__(self):
        super().__init__()
        self.method = Analyzer.NLP
    async def context_analysis(self, context:list[str]) ->  ContradictionType:
        return ContradictionType.CONTRARY

    async def confidence_analysis(self, context:list[str], contradiction_type: ContradictionType) -> float:
        return 0.999

    async def overall_analysis(self, context_blocks:ContextBlockCollection) -> ContradictionAnalysisCollection:
        analysis_collection = []
        blocks = context_blocks.blocks
        for context_block in blocks:
            contradiction_type = await self.context_analysis(context_block.passages)
            confidence_score = await self.confidence_analysis(context_block.passages, contradiction_type)
            analysis_collection.append(ContradictionAnalysis(
                contradiction_type=contradiction_type,
                analyzer=self.method,
                confidence=confidence_score,
                context_block=context_block
                ))

        return ContradictionAnalysisCollection(blocks=analysis_collection)



