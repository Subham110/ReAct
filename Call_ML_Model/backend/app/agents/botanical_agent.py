"""
BotanicalAgent — Multi-domain ReAct agent using LangChain + Groq.

Routes user queries to either the Iris KNN or Titanic LinearSVC model
through LangChain tool calling, then parses the structured JSON response
into a polymorphic VisualizationData object.
"""

import json
import re
import logging

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage

from app.config import settings
from app.tools.botanical_tools import (
    predict_iris_species,
    predict_titanic_survival,
    get_model_info,
)
from app.agents.prompts import SYSTEM_PROMPT
from app.schemas.response_schemas import VisualizationData
from app.core.exceptions import AgentExecutionError

logger = logging.getLogger(__name__)


class BotanicalAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.AGENT_MODEL,
            temperature=settings.AGENT_TEMPERATURE,
            api_key=settings.GROQ_API_KEY,
            max_retries=2,
            request_timeout=30,
        )
        self.tools = [predict_iris_species, predict_titanic_survival, get_model_info]
        self.tools_map = {tool.name: tool for tool in self.tools}
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    async def analyze(self, query: str) -> VisualizationData:
        try:
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=query),
            ]

            # 1. THOUGHT: LLM analyzes user query and decides which tool to call
            response = await self.llm_with_tools.ainvoke(messages)
            messages.append(response)

            # 2. ACT & OBSERVE: Execute tool calls and capture observations
            if hasattr(response, "tool_calls") and response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})
                    tool_id = tool_call.get("id", "call_1")

                    logger.info("Invoking tool %s with args %s", tool_name, tool_args)
                    tool = self.tools_map.get(tool_name)
                    if tool:
                        try:
                            tool_result = tool.invoke(tool_args)
                        except Exception as te:
                            tool_result = json.dumps(
                                {"error": f"Tool execution failed: {str(te)}"}
                            )
                    else:
                        tool_result = json.dumps(
                            {"error": f"Unknown tool: {tool_name}"}
                        )

                    messages.append(
                        ToolMessage(content=str(tool_result), tool_call_id=tool_id)
                    )

                # 3. FINALIZE: Get final structured JSON from LLM
                final_response = await self.llm.ainvoke(messages)
                output_str = final_response.content
            else:
                output_str = response.content

            # Handle list content (some models return content as list)
            if isinstance(output_str, list):
                output_str = "".join(
                    [
                        c.get("text", "") if isinstance(c, dict) else str(c)
                        for c in output_str
                    ]
                )

            # Parse JSON from LLM output (try multiple strategies)
            return self._parse_response(output_str)

        except AgentExecutionError:
            raise
        except Exception as e:
            logger.error("Agent error: %s", e, exc_info=True)
            raise AgentExecutionError(f"Agent analysis failed: {str(e)}")

    def _parse_response(self, output_str: str) -> VisualizationData:
        """Extract and validate JSON from LLM output using multiple strategies."""

        # Strategy 1: Direct JSON parse
        try:
            parsed = json.loads(output_str)
            return VisualizationData.model_validate(parsed)
        except (json.JSONDecodeError, Exception):
            pass

        # Strategy 2: Extract from markdown code fence
        json_match = re.search(
            r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", output_str
        )
        if json_match:
            try:
                parsed = json.loads(json_match.group(1).strip())
                return VisualizationData.model_validate(parsed)
            except (json.JSONDecodeError, Exception):
                pass

        # Strategy 3: Find any JSON object
        curly_match = re.search(r"(\{[\s\S]*\})", output_str)
        if curly_match:
            try:
                parsed = json.loads(curly_match.group(1).strip())
                return VisualizationData.model_validate(parsed)
            except (json.JSONDecodeError, Exception):
                pass

        raise AgentExecutionError(
            f"Could not extract valid JSON from LLM output: {output_str[:500]}"
        )


botanical_agent = BotanicalAgent()
