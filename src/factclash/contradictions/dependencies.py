import logging

from factclash.services.analyzor.llm_based import LLMAnalyzor
from factclash.services.analyzor.nlp_based import NLPAnalyzor

_logger = logging.getLogger(__name__)


async def get_llm_analyzor_agent():
    _logger.info("LLM agent is initialized to analyze for contradictions")
    return LLMAnalyzor()


async def get_nlp_analyzor_agent():
    _logger.info("NLP agent is initialized to analyze for contradictions")
    return NLPAnalyzor()