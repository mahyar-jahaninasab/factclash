from factclash.services.analyzer.base import ContradictionAnalyzer,Analyzer


class LLMAnalyzer(ContradictionAnalyzer):
    def __init__(self):
        super().__init__()
        self.method = Analyzer.LLM


