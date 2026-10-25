from factclash.services.analyzer.base import ContradictionAnalyzer,Analyzer


class NLPAnalyzer(ContradictionAnalyzer):
    def __init__(self):
        super().__init__()
        self.method = Analyzer.NLP


