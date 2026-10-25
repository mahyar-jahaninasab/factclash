import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic_core import ValidationError

from factclash.contradictions.schemas import ContextBlockCollection,ContradictionAnalysisCollection
from factclash.contradictions.dependencies import get_llm_analyzor_agent, get_nlp_analyzor_agent
from factclash.services.analyzor.llm_based import LLMAnalyzor
from factclash.services.analyzor.nlp_based import NLPAnalyzor

router = APIRouter()

_logger = logging.info(__name__)


@router.post("/contradictions/NLP", response_model=ContradictionAnalysisCollection)
async def request_nlp_contradiction_analysis(request:ContextBlockCollection, nlp_analyzor: Annotated[NLPAnalyzor, Depends(get_nlp_analyzor_agent)]):
    _logger.info("Received incoming HTTP POST request for NLP contradiction analysis.")
    try:
        response = nlp_analyzor.overall_analysis(request) 
    except ValidationError as VE:
        _logger.error("Validation error in NLP analysis")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(VE))
    except Exception as e:
        _logger.error("Server error in NLP analysis")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/contradictions/AI", response_model=ContradictionAnalysisCollection)
async def request_llm_contradiction_analysis(request:ContextBlockCollection, llm_analyzor: Annotated[LLMAnalyzor, Depends(get_llm_analyzor_agent)]):
    _logger.info("Received incoming HTTP POST request for AI contradiction analysis.")
    try:
        response = await llm_analyzor.overall_analysis(ContextBlockCollection)
    except ValidationError as VE:
        _logger.error("Validation error in LLM analysis")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(VE))
    except Exception as e:
        _logger.error("Server error in LLM analysis")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))