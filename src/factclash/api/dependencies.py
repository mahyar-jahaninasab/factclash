import logging

from factclash.services.analyzer.nlp_based import NLPAnalyzer
from functools import lru_cache

_logger = logging.getLogger(__name__)


@lru_cache(1)
def get_nlp_analyzer_agent():
    _logger.info("NLP agent is initialized to analyze for contradictions")
    return NLPAnalyzer()
