import asyncio
import logging
import spacy
from async_lru import alru_cache

_logger = logging.getLogger(__name__)


@alru_cache(maxsize=1)
async def get_nlp_analyzer_model():
    _logger.info("NLP agent is initialized to analyze for contradictions")
    return await asyncio.to_thread(spacy.load, "en_core_web_sm")
