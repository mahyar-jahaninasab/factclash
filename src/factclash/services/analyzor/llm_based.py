from factclash.services.analyzor.base import ContradictionAnalyzor,Analyzor


class LLMAnalyzor(ContradictionAnalyzor):
    def __init__(self):
        super().__init__()
        self.method = Analyzor.LLM


