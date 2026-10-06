"""
Agent system with tools, ReAct pattern, and LangGraph integration.
"""

import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel

from devmate.config import settings
from devmate.llm.client import llm_client
from devmate.obs.tracing import tracer
from devmate.retrieve.retriever import get_retriever


class ToolResult(BaseModel):
    """Result of a tool execution."""

    success: bool
    content: str
    metadata: dict[str, Any] = {}
    error: str | None = None


class ToolSchema(BaseModel):
    """Schema for a tool."""

    name: str
    description: str
    parameters: dict[str, Any]


class BaseTool(ABC):
    """Abstract base class for agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters_schema(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        pass

    def to_schema(self) -> ToolSchema:
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters=self.parameters_schema,
        )


class SearchCodeTool(BaseTool):
    """Search code in the indexed repository."""

    @property
    def name(self) -> str:
        return "search_code"

    @property
    def description(self) -> str:
        return "Search for code snippets, functions, or patterns in the repository. Use for finding implementations, understanding code structure, or locating specific functionality."

    @property
    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query - can be keywords, function names, or natural language description",
                },
                "language": {
                    "type": "string",
                    "description": "Optional: filter by programming language (e.g., python, javascript)",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 5,
                },
            },
            "required": ["query"],
        }

    async def execute(self, query: str, language: str = None, top_k: int = 5) -> ToolResult:
        try:
            retriever = await get_retriever()

            # Generate query embedding
            from devmate.index.embeddings import embedding_service

            embedding_result = await embedding_service.embed([query])
            query_vector = embedding_result.embeddings[0]

            # Build filter
            filter_dict = {}
            if language:
                filter_dict["language"] = language

            # Retrieve
            results = await retriever.retrieve(
                query=query,
                query_vector=query_vector,
                filter=filter_dict,
                use_reranker=True,
            )

            # Format results
            formatted = []
            for i, result in enumerate(results[:top_k], 1):
                result.metadata.get("source", "unknown")
                filename = result.metadata.get("filename", "unknown")
                chunk_type = result.metadata.get("chunk_type", "")
                name = result.metadata.get("name", "")

                formatted.append(
                    f"[{i}] {filename}"
                    f"{f' | {chunk_type}' if chunk_type else ''}"
                    f"{f' | {name}' if name else ''}"
                    f" (score: {result.score:.3f})\n{result.content[:500]}"
                )

            return ToolResult(
                success=True,
                content="\n\n---\n\n".join(formatted) if formatted else "No results found.",
                metadata={"result_count": len(results)},
            )
        except Exception as e:
            return ToolResult(success=False, content="", error=str(e))


class ReadFileTool(BaseTool):
    """Read a file from the repository."""

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Read the full content of a file from the repository. Use when you need to see the complete implementation of a specific file."

    @property
    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative path to the file from repository root",
                },
            },
            "required": ["file_path"],
        }

    async def execute(self, file_path: str) -> ToolResult:
        try:
            # Resolve path
            from pathlib import Path

            repo_root = Path.cwd()
            full_path = (repo_root / file_path).resolve()

            # Security check - ensure path is within repo
            try:
                full_path.relative_to(repo_root)
            except ValueError:
                return ToolResult(success=False, content="", error="Path traversal not allowed")

            if not full_path.exists():
                return ToolResult(success=False, content="", error=f"File not found: {file_path}")

            if not full_path.is_file():
                return ToolResult(success=False, content="", error=f"Not a file: {file_path}")

            content = full_path.read_text(encoding="utf-8")

            return ToolResult(
                success=True,
                content=content,
                metadata={"file_path": file_path, "size": len(content)},
            )
        except Exception as e:
            return ToolResult(success=False, content="", error=str(e))


class RunTestsTool(BaseTool):
    """Run tests for the repository."""

    @property
    def name(self) -> str:
        return "run_tests"

    @property
    def description(self) -> str:
        return (
            "Run the test suite for the repository. Use to verify changes or check if tests pass."
        )

    @property
    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "test_path": {
                    "type": "string",
                    "description": "Optional: specific test file or directory to run",
                },
                "args": {
                    "type": "string",
                    "description": "Additional pytest arguments",
                    "default": "-v",
                },
            },
        }

    async def execute(self, test_path: str = None, args: str = "-v") -> ToolResult:
        import subprocess
        from pathlib import Path

        try:
            repo_root = Path.cwd()

            cmd = ["python", "-m", "pytest"]
            if args:
                cmd.extend(args.split())
            if test_path:
                cmd.append(test_path)

            result = subprocess.run(
                cmd,
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=120,
            )

            output = result.stdout
            if result.stderr:
                output += "\n--- STDERR ---\n" + result.stderr

            return ToolResult(
                success=result.returncode == 0,
                content=output,
                metadata={
                    "return_code": result.returncode,
                    "command": " ".join(cmd),
                },
            )
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, content="", error="Test execution timed out (120s)")
        except Exception as e:
            return ToolResult(success=False, content="", error=str(e))


class ProposePatchTool(BaseTool):
    """Propose a code patch/diff."""

    @property
    def name(self) -> str:
        return "propose_patch"

    @property
    def description(self) -> str:
        return "Propose a code change as a unified diff. Use when you want to suggest a specific fix or improvement to a file."

    @property
    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to modify",
                },
                "diff": {
                    "type": "string",
                    "description": "Unified diff format patch",
                },
                "description": {
                    "type": "string",
                    "description": "Explanation of what the patch does and why",
                },
            },
            "required": ["file_path", "diff", "description"],
        }

    async def execute(self, file_path: str, diff: str, description: str) -> ToolResult:
        # In a real implementation, this would create a PR or save the patch
        # For now, just validate and return
        try:
            from pathlib import Path

            repo_root = Path.cwd()
            full_path = (repo_root / file_path).resolve()
            full_path.relative_to(repo_root)

            if not full_path.exists():
                return ToolResult(success=False, content="", error=f"File not found: {file_path}")

            # Validate diff format (basic check)
            if not diff.startswith("---") or "+++" not in diff:
                return ToolResult(success=False, content="", error="Invalid diff format")

            return ToolResult(
                success=True,
                content=f"Patch proposed for {file_path}:\n{description}\n\n```diff\n{diff}\n```",
                metadata={
                    "file_path": file_path,
                    "description": description,
                    "patch_size": len(diff),
                },
            )
        except Exception as e:
            return ToolResult(success=False, content="", error=str(e))


# Tool registry
TOOLS = {
    "search_code": SearchCodeTool,
    "read_file": ReadFileTool,
    "run_tests": RunTestsTool,
    "propose_patch": ProposePatchTool,
}


def get_tool(name: str) -> BaseTool:
    """Get tool instance by name."""
    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}. Available: {list(TOOLS.keys())}")
    return TOOLS[name]()


class AgentState(StrEnum):
    """Agent execution states."""

    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    DONE = "done"
    ERROR = "error"


@dataclass
class AgentStep:
    """A single step in agent execution."""

    step_id: int
    thought: str
    action: str
    action_input: dict[str, Any]
    observation: str
    state: AgentState
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    latency_ms: float = 0


@dataclass
class AgentContext:
    """Agent execution context."""

    goal: str
    steps: list[AgentStep] = field(default_factory=list)
    max_steps: int = 10
    current_step: int = 0
    tools: dict[str, BaseTool] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_step(self, step: AgentStep) -> None:
        self.steps.append(step)
        self.current_step += 1

    def get_history(self) -> str:
        """Get formatted history for LLM context."""
        if not self.steps:
            return "No previous steps."

        lines = []
        for step in self.steps:
            lines.append(f"Step {step.step_id}:")
            lines.append(f"  Thought: {step.thought}")
            lines.append(f"  Action: {step.action}({json.dumps(step.action_input)})")
            lines.append(f"  Observation: {step.observation[:200]}...")
            lines.append("")
        return "\n".join(lines)


class ReActAgent:
    """ReAct (Reasoning + Acting) agent implementation."""

    SYSTEM_PROMPT = """You are an AI agent that helps users accomplish tasks by using tools.

You have access to the following tools:
{tool_descriptions}

To use a tool, respond with:
Thought: <your reasoning about what to do>
Action: <tool_name>
Input: <JSON object with tool parameters>

When you have the final answer, respond with:
Thought: <your final reasoning>
Final Answer: <your answer to the user>

Always think step by step. Use tools when you need information or need to take action.
Maximum {max_steps} steps allowed.
"""

    def __init__(
        self,
        tools: list[str] = None,
        max_steps: int = 10,
        model: str = None,
    ) -> None:
        self.max_steps = max_steps
        self.model = model or settings.default_model

        # Initialize tools
        tool_names = tools or ["search_code", "read_file", "run_tests", "propose_patch"]
        self.tools = {name: get_tool(name) for name in tool_names}

        # Build tool descriptions
        self.tool_descriptions = "\n".join(
            f"- {tool.name}: {tool.description}" for tool in self.tools.values()
        )

    def _build_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT.format(
            tool_descriptions=self.tool_descriptions,
            max_steps=self.max_steps,
        )

    async def _call_llm(self, messages: list[dict[str, str]]) -> str:
        """Call LLM for reasoning."""
        response = await llm_client.complete(
            messages=messages,
            model=self.model,
            max_tokens=2048,
            temperature=0.1,
            stream=False,
        )
        return response.content

    def _parse_response(self, response: str) -> tuple:
        """Parse LLM response into thought, action, input or final answer."""
        thought = ""
        action = None
        action_input = {}
        final_answer = None

        lines = response.strip().split("\n")
        current_field = None
        current_content = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("Thought:"):
                if current_field:
                    self._save_field(current_field, current_content, locals())
                current_field = "thought"
                current_content = [stripped[8:].strip()]
            elif stripped.startswith("Action:"):
                if current_field:
                    self._save_field(current_field, current_content, locals())
                current_field = "action"
                current_content = [stripped[7:].strip()]
            elif stripped.startswith("Input:"):
                if current_field:
                    self._save_field(current_field, current_content, locals())
                current_field = "input"
                current_content = [stripped[6:].strip()]
            elif stripped.startswith("Final Answer:"):
                if current_field:
                    self._save_field(current_field, current_content, locals())
                current_field = "final"
                current_content = [stripped[13:].strip()]
            elif current_field:
                current_content.append(line)

        # Save last field
        if current_field:
            self._save_field(current_field, current_content, locals())

        return thought, action, action_input, final_answer

    def _save_field(self, field: str, content: list, local_vars: dict) -> None:
        """Save parsed field to local variables."""
        text = "\n".join(content).strip()
        if field == "thought":
            local_vars["thought"] = text
        elif field == "action":
            local_vars["action"] = text
        elif field == "input":
            try:
                local_vars["action_input"] = json.loads(text)
            except json.JSONDecodeError:
                local_vars["action_input"] = {"raw": text}
        elif field == "final":
            local_vars["final_answer"] = text

    async def run(self, goal: str) -> str:
        """Run the agent to achieve the goal."""
        context = AgentContext(
            goal=goal,
            max_steps=self.max_steps,
            tools=self.tools,
        )
        messages = self._initial_messages(goal)

        for step_num in range(self.max_steps):
            context.current_step = step_num + 1

            # Get LLM reasoning
            with tracer.trace("agent.step", step=step_num + 1) as span:
                response = await self._call_llm(messages)
                span.set_attribute("response_length", len(response))

            # Parse response
            thought, action, action_input, final_answer = self._parse_response(response)

            if final_answer:
                return self._finish(context, step_num, thought, final_answer)

            if action and action in self.tools:
                await self._run_tool(
                    context, messages, step_num, response, thought, action, action_input
                )
            else:
                self._note_invalid_action(messages, action, response)

        return "Maximum steps reached without completing the task."

    def _initial_messages(self, goal: str) -> list[dict[str, str]]:
        """System prompt plus the user goal that start every run."""
        return [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": f"Goal: {goal}"},
        ]

    def _finish(self, context: AgentContext, step_num: int, thought: str, final_answer: str) -> str:
        """Record the terminal step and return the answer."""
        step = AgentStep(
            step_id=step_num + 1,
            thought=thought,
            action="finish",
            action_input={},
            observation=final_answer,
            state=AgentState.DONE,
        )
        context.add_step(step)
        return final_answer

    async def _run_tool(
        self,
        context: AgentContext,
        messages: list[dict[str, str]],
        step_num: int,
        response: str,
        thought: str,
        action: str,
        action_input: dict,
    ) -> None:
        """Execute one tool call, record the step, queue the observation."""
        tool = self.tools[action]

        with tracer.trace("agent.tool", tool=action) as span:
            start = time.perf_counter()
            result = await tool.execute(**action_input)
            latency_ms = (time.perf_counter() - start) * 1000
            span.set_attribute("success", result.success)
            span.set_attribute("latency_ms", latency_ms)

        observation = result.content if result.success else f"Error: {result.error}"
        step = AgentStep(
            step_id=step_num + 1,
            thought=thought,
            action=action,
            action_input=action_input,
            observation=observation,
            state=AgentState.OBSERVING,
            latency_ms=latency_ms,
        )
        context.add_step(step)

        messages.append({"role": "assistant", "content": response})
        messages.append(
            {
                "role": "user",
                "content": f"Observation: {observation}\n\nWhat should I do next?",
            }
        )

    def _note_invalid_action(
        self, messages: list[dict[str, str]], action: str, response: str
    ) -> None:
        """Queue the unknown-action observation so the LLM can recover."""
        observation = f"Unknown action: {action}. Available: {list(self.tools.keys())}"
        messages.append({"role": "assistant", "content": response})
        messages.append(
            {
                "role": "user",
                "content": f"Observation: {observation}\n\nWhat should I do next?",
            }
        )


class LangGraphAgent:
    """LangGraph-based agent (when LangGraph is available)."""

    def __init__(self, tools: list[str] = None) -> None:
        self.tools = {
            name: get_tool(name)
            for name in (tools or ["search_code", "read_file", "run_tests", "propose_patch"])
        }

        try:
            from langgraph.graph import END, StateGraph  # noqa: F401
            from langgraph.prebuilt import ToolExecutor  # noqa: F401

            self._langgraph_available = True
        except ImportError:
            self._langgraph_available = False

    async def run(self, goal: str) -> str:
        if not self._langgraph_available:
            # Fallback to ReAct agent
            agent = ReActAgent(tools=list(self.tools.keys()))
            return await agent.run(goal)

        # LangGraph implementation would go here
        # For now, delegate to ReAct
        agent = ReActAgent(tools=list(self.tools.keys()))
        return await agent.run(goal)


# Global agent instance
_agent_instance = None


async def get_agent(tools: list[str] = None) -> ReActAgent:
    """Get or create global agent."""
    global _agent_instance

    if _agent_instance is None:
        _agent_instance = ReActAgent(tools=tools)

    return _agent_instance
