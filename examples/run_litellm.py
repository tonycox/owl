# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
import os
import sys

from dotenv import load_dotenv
from camel.models import ModelFactory
from camel.toolkits import (
    CodeExecutionToolkit,
    ExcelToolkit,
    ImageAnalysisToolkit,
    SearchToolkit,
    BrowserToolkit,
    FileWriteToolkit, ThinkingToolkit,
)
from camel.types import ModelPlatformType

from owl.utils import run_society
from camel.societies import RolePlaying
from camel.logger import set_log_level

import pathlib

base_dir = pathlib.Path(__file__).parent.parent
env_path = base_dir / "owl" / ".env"
load_dotenv(dotenv_path=str(env_path))

set_log_level(level="DEBUG")


def construct_society(question: str) -> RolePlaying:
    r"""Construct a society of agents based on the given question.

    Args:
        question (str): The task or question to be addressed by the society.

    Returns:
        RolePlaying: A configured society of agents ready to address the question.
    """

    # Create models for different components
    models = {
        "user": ModelFactory.create(
            model_platform=ModelPlatformType.LITELLM,
            model_type="gemini-2.5-pro",
            api_key=os.getenv("LITELLM_API_KEY"),
            url=os.getenv("LITELLM_URL"),
            model_config_dict={"temperature": 0.4, "max_tokens": 128000, "custom_llm_provider": "custom_openai"},
        ),
        "assistant": ModelFactory.create(
            model_platform=ModelPlatformType.LITELLM,
            model_type="gemini-2.5-pro",
            api_key=os.getenv("LITELLM_API_KEY"),
            url=os.getenv("LITELLM_URL"),
            model_config_dict={"temperature": 0.4, "max_tokens": 128000, "custom_llm_provider": "custom_openai"},
        ),
        "browsing": ModelFactory.create(
            model_platform=ModelPlatformType.LITELLM,
            model_type="gemini-2.5-pro",
            api_key=os.getenv("LITELLM_API_KEY"),
            url=os.getenv("LITELLM_URL"),
            model_config_dict={"temperature": 0.4, "max_tokens": 128000, "custom_llm_provider": "custom_openai"},
        ),
        "planning": ModelFactory.create(
            model_platform=ModelPlatformType.LITELLM,
            model_type="gemini-2.5-pro",
            api_key=os.getenv("LITELLM_API_KEY"),
            url=os.getenv("LITELLM_URL"),
            model_config_dict={"temperature": 0.4, "max_tokens": 128000, "custom_llm_provider": "custom_openai"},
        ),
        "image": ModelFactory.create(
            model_platform=ModelPlatformType.LITELLM,
            model_type="gemini-2.5-pro",
            api_key=os.getenv("LITELLM_API_KEY"),
            url=os.getenv("LITELLM_URL"),
            model_config_dict={"temperature": 0.4, "max_tokens": 128000, "custom_llm_provider": "custom_openai"},
        ),
    }

    # Configure toolkits
    tools = [
        *BrowserToolkit(
            headless=False,  # Set to True for headless mode (e.g., on remote servers)
            web_agent_model=models["browsing"],
            planning_agent_model=models["planning"],
        ).get_tools(),
        *CodeExecutionToolkit(sandbox="subprocess", verbose=True).get_tools(),
        *ImageAnalysisToolkit(model=models["image"]).get_tools(),
        SearchToolkit().search_duckduckgo,
        # SearchToolkit().search_google,  # Comment this out if you don't have google search
        SearchToolkit().search_wiki,
        *ExcelToolkit().get_tools(),
        *FileWriteToolkit(output_dir="./").get_tools(),
        *ThinkingToolkit().get_tools(),
    ]

    # Configure agent roles and parameters
    user_agent_kwargs = {"model": models["user"]}
    assistant_agent_kwargs = {"model": models["assistant"], "tools": tools}

    # Configure task parameters
    task_kwargs = {
        "task_prompt": question,
        "with_task_specify": False,
    }

    # Create and return the society
    society = RolePlaying(
        **task_kwargs,
        user_role_name="user",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="assistant",
        assistant_agent_kwargs=assistant_agent_kwargs,
    )

    return society


def main():
    r"""Main function to run the OWL system with an example question."""
    # Example research question
    default_task = "Open Brave search, summarize the github stars, fork counts, etc. of camel-ai's camel framework, and write the numbers into a python file using the plot package, save it locally, and run the generated python file. Note: You have been provided with the necessary tools to complete this task."

    # Override default task if command line argument is provided
    task = sys.argv[1] if len(sys.argv) > 1 else default_task

    # Construct and run the society
    society = construct_society(task)

    answer, chat_history, token_count = run_society(society)

    # Output the result
    print(f"\033[94mAnswer: {answer}\033[0m")


if __name__ == "__main__":
    main()
