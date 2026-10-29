import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic_core import ValidationError

from factclash.contradictions.schemas import ContextBlockCollection,ContradictionAnalysisCollection
from factclash.contradictions.dependencies import  get_nlp_analyzer_agent
from factclash.services.analyzer.nlp_based import NLPAnalyzer

router = APIRouter(prefix="/contradictions")

_logger = logging.getLogger(__name__)


@router.post("/nlp", response_model=ContradictionAnalysisCollection)
async def request_nlp_contradiction_analysis(request:ContextBlockCollection, nlp_analyzer: Annotated[NLPAnalyzer, Depends(get_nlp_analyzer_agent)]):
    _logger.info("Received incoming HTTP POST request for NLP contradiction analysis.")
    try:
        response = await nlp_analyzer.overall_analysis(request) 
    except Exception as e:
        _logger.error("Server error in NLP analysis")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server Error please retry")
    return response

