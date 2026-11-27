from functools import lru_cache
import logging
import spacy

_logger = logging.getLogger(__name__)


@lru_cache(1)
def get_nlp_analyzer_model():
    _logger.info("NLP agent is initialized to analyze for contradictions")
    return spacy.load("en_core_web_md")
