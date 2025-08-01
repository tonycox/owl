import logging
from typing import Dict, Any
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Overall health check endpoint."""
    try:
        logger.info("Performing overall health check")
        # Determine overall health
        overall_status = "healthy"
        logger.info(f"Health check completed: {overall_status}")
        return {
            "status": overall_status,
        }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}
