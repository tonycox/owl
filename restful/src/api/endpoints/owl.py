import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ...services.owl import owl_service

logger = logging.getLogger(__name__)

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str
    context: str = ""


class AnswerResponse(BaseModel):
    status: str
    question: str
    answer: str


@router.post("/ask")
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """Ask a question to the Owl API directly."""
    try:
        logger.info(f"Direct Owl API question: {request.question[:100]}...")

        response = await owl_service.ask_question(request.question, request.context)

        if response.get("status") == "success":
            logger.info("Question answered successfully")
            return AnswerResponse(
                status="success",
                question=request.question,
                answer=response.get("answer"),
            )
        else:
            logger.error(f"Owl API error: {response.get('message')}")
            raise HTTPException(
                status_code=500, detail=f"Owl API error: {response.get('message')}"
            )
    except Exception as e:
        logger.error(f"Error asking question: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
