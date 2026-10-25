from factclash.services.analyzor.base import ContradictionAnalyzor,Analyzor


class NLPAnalyzor(ContradictionAnalyzor):
    def __init__(self):
        super().__init__()
        self.method = Analyzor.NLP


