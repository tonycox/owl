import logging
from typing import Dict, Any, Optional, List
from camel.models import ModelFactory, BaseModelBackend
from camel.toolkits.async_browser_toolkit import AsyncBrowserToolkit
from camel.toolkits import (
    FunctionTool,
    CodeExecutionToolkit,
    ExcelToolkit,
    ImageAnalysisToolkit,
    SearchToolkit,
    FileWriteToolkit,
    TaskPlanningToolkit,
    MarkItDownToolkit,
    Crawl4AIToolkit,
    GoogleMapsToolkit,
)

from camel.types import ModelPlatformType, ModelType
from camel.logger import set_log_level

from ..owl.utils import arun_society, DocumentProcessingToolkit, OwlGAIARolePlaying

from ..config.settings import settings

set_log_level(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


class OwlService:
    """Service for interacting with the Owl API."""

    tools: List[FunctionTool]
    models: Dict[str, BaseModelBackend]

    def __init__(self):
        self.setup()

    async def ask_question(
        self, question: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ask a question to the Owl API.
        """
        logger.info(f"Asking question to Owl API: {question[:100]}...")
        society = OwlGAIARolePlaying(
            task_prompt=question,
            with_task_specify=False,
            user_role_name="user",
            user_agent_kwargs={"model": self.models["user"]},
            assistant_role_name="assistant",
            assistant_agent_kwargs={
                "model": self.models["assistant"],
                "tools": self.tools,
            },
        )

        answer, chat_history, token_count = await arun_society(society)
        return {
            "status": "success",
            "answer": answer,
            "token_count": token_count,
            "chat_history_size": len(chat_history),
        }

    def setup(self):
        self.models = {
            "user": ModelFactory.create(
                model_platform=ModelPlatformType.GEMINI,
                model_type=ModelType.GEMINI_2_5_PRO,
                model_config_dict={"temperature": 0},
                api_key=settings.GEMINI_API_KEY,
            ),
            "assistant": ModelFactory.create(
                model_platform=ModelPlatformType.GEMINI,
                model_type=ModelType.GEMINI_2_5_PRO,
                model_config_dict={"temperature": 0},
                api_key=settings.GEMINI_API_KEY,
            ),
            "browsing": ModelFactory.create(
                model_platform=ModelPlatformType.GEMINI,
                model_type=ModelType.GEMINI_2_5_PRO,
                model_config_dict={"temperature": 0},
                api_key=settings.GEMINI_API_KEY,
            ),
            "planning": ModelFactory.create(
                model_platform=ModelPlatformType.GEMINI,
                model_type=ModelType.GEMINI_2_5_PRO,
                model_config_dict={"temperature": 0},
                api_key=settings.GEMINI_API_KEY,
            ),
            "video": ModelFactory.create(
                model_platform=ModelPlatformType.GEMINI,
                model_type=ModelType.GEMINI_2_5_PRO,
                model_config_dict={"temperature": 0},
                api_key=settings.GEMINI_API_KEY,
            ),
            "image": ModelFactory.create(
                model_platform=ModelPlatformType.GEMINI,
                model_type=ModelType.GEMINI_2_5_PRO,
                model_config_dict={"temperature": 0},
                api_key=settings.GEMINI_API_KEY,
            ),
            "document": ModelFactory.create(
                model_platform=ModelPlatformType.GEMINI,
                model_type=ModelType.GEMINI_2_5_PRO,
                model_config_dict={"temperature": 0},
                api_key=settings.GEMINI_API_KEY,
            ),
        }
        self.tools = [
            *CodeExecutionToolkit(sandbox="subprocess", verbose=True).get_tools(),
            *ImageAnalysisToolkit(model=self.models["image"]).get_tools(),
            SearchToolkit().search_duckduckgo,
            # SearchToolkit().search_google, # google search api required
            SearchToolkit().search_wiki,
            SearchToolkit().search_bing,
            *GoogleMapsToolkit().get_tools(),
            *ExcelToolkit().get_tools(),
            *Crawl4AIToolkit().get_tools(),
            *TaskPlanningToolkit().get_tools(),
            # *DocumentProcessingToolkit(model=self.models["document"]).get_tools(),
            *FileWriteToolkit(output_dir="./tools-output/").get_tools(),
            *AsyncBrowserToolkit(
                headless=False,
                web_agent_model=self.models["browsing"],
                planning_agent_model=self.models["planning"],
            ).get_tools(),
            *MarkItDownToolkit().get_tools(),
        ]


# Create service instance
owl_service = OwlService()
