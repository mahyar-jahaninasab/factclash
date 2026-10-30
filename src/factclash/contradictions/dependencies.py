import logging

from factclash.services.analyzer.nlp_based import NLPAnalyzer

_logger = logging.getLogger(__name__)


async def get_nlp_analyzer_agent():
    _logger.info("NLP agent is initialized to analyze for contradictions")
    return NLPAnalyzer()