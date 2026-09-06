import os
import json
import asyncio
from typing import List, Dict, Any, Callable, Optional, TypedDict
from dataclasses import dataclass
from datetime import datetime
from openai import AsyncOpenAI

# Конфигурация клиента
client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key"),
    base_url="https://openrouter.ai/api/v1",
)

MODEL = "moonshotai/kimi-k2.5"

class ToolParameter(TypedDict):
    type: str
    description: str
    enum: Optional[list]

class ToolDefinition(TypedDict):
    type: str
    function: dict

class ToolRegistry:
    """Реестр инструментов для Agent Swarm"""
    
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._definitions: List[ToolDefinition] = []
    
    def register(
        self, 
        name: str, 
        description: str, 
        parameters: dict,
        func: Callable
    ):
        """Регистрация нового инструмента"""
        self._tools[name] = func
        self._definitions.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": list(parameters.keys())
                }
            }
        })
    
    def get_definitions(self) -> List[ToolDefinition]:
        return self._definitions
    
    async def execute(self, name: str, arguments: dict) -> str:
        """Выполнение инструмента"""
        if name not in self._tools:
            return json.dumps({"error": f"Tool '{name}' not found"})
        
        try:
            result = await self._tools[name](**arguments) \
                if asyncio.iscoroutinefunction(self._tools[name]) \
                else self._tools[name](**arguments)
            return json.dumps({"result": result, "status": "success"})
        except Exception as e:
            return json.dumps({"error": str(e), "status": "failed"})

@dataclass
class SubAgent:
    """Конфигурация суб-агента в Swarm"""
    agent_id: str
    role: str
    objective: str
    tools: List[str]
    context: Dict[str, Any]
    priority: int = 1
    timeout: int = 120
    
    def to_system_prompt(self, project_constitution: str = "") -> str:
        return f"""You are Sub-Agent {self.agent_id} with role: {self.role}.

OBJECTIVE: {self.objective}

{project_constitution}

GUIDELINES:
- Focus exclusively on your assigned objective
- Use available tools efficiently
- Return structured, actionable results
- If blocked, report immediately with context
- Maximum {self.timeout}s execution time

CONTEXT: {json.dumps(self.context, indent=2)}
"""

class SwarmOrchestrator:
    """Оркестратор для управления Agent Swarm"""
    
    def __init__(
        self, 
        registry: ToolRegistry,
        max_agents: int = 100,
        max_parallel_tools: int = 1500,
        aggregation_strategy: str = "synthesize"
    ):
        self.registry = registry
        self.max_agents = max_agents
        self.max_parallel_tools = max_parallel_tools
        self.aggregation_strategy = aggregation_strategy
        self.results_cache: Dict[str, Any] = {}
        self._project_context: Optional[str] = None

    def _get_agents_context(self) -> str:
        """Считывает AGENTS.md для контекста роя"""
        if self._project_context is not None:
            return self._project_context
            
        context_parts = []
        paths = ["AGENTS.md", ".agent/AGENTS.md"]
        for p in paths:
            # Ищем от корня проекта (предполагаем запуск из корня или PersonalOS)
            abs_p = os.path.abspath(os.path.join(os.getcwd(), "../../..", p)) if "skills" in os.getcwd() else os.path.abspath(p)
            if os.path.exists(abs_p):
                try:
                    with open(abs_p, "r", encoding="utf-8") as f:
                        context_parts.append(f"PROJECT CONSTITUTION ({p}):\n{f.read()}")
                except Exception:
                    pass
        
        self._project_context = "\n\n".join(context_parts) if context_parts else ""
        return self._project_context
    
    async def decompose_task(
        self, 
        user_query: str, 
        context: Dict[str, Any] = None
    ) -> List[SubAgent]:
        """Декомпозиция задачи на параллельные подзадачи"""
        decomposition_prompt = f"""Analyze the following task and decompose it into parallel sub-tasks.

USER QUERY: {user_query}

Maximum agents allowed: {self.max_agents}
"""
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a task decomposition specialist. Respond with JSON object containing 'agents' array."},
                {"role": "user", "content": decomposition_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        
        decomposition = json.loads(response.choices[0].message.content)
        agents = []
        for agent_config in decomposition.get("agents", []):
            agents.append(SubAgent(
                agent_id=agent_config["agent_id"],
                role=agent_config["role"],
                objective=agent_config["objective"],
                tools=agent_config["tools"],
                context={**(context or {}), **agent_config.get("context", {})},
                priority=agent_config.get("priority", 5),
            ))
        return agents

    async def execute_sub_agent(self, agent: SubAgent, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнение отдельного суб-агента"""
        project_constitution = self._get_agents_context()
        messages = [
            {"role": "system", "content": agent.to_system_prompt(project_constitution)},
            {"role": "user", "content": f"Execute your objective. Shared context: {json.dumps(shared_context)}"}
        ]
        agent_tools = [t for t in self.registry.get_definitions() if t["function"]["name"] in agent.tools]
        start_time = datetime.now()
        try:
            response = await asyncio.wait_for(self._run_agent_with_tools(messages, agent_tools), timeout=agent.timeout)
            return {
                "agent_id": agent.agent_id, "role": agent.role, "status": "completed",
                "result": response, "execution_time": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
        except asyncio.TimeoutError:
            return {"agent_id": agent.agent_id, "role": agent.role, "status": "timeout", "result": "Timeout", "execution_time": agent.timeout, "timestamp": datetime.now().isoformat()}

    async def _run_agent_with_tools(self, messages: List[dict], tools: List[ToolDefinition]) -> str:
        iteration = 0
        while iteration < 10:
            response = await client.chat.completions.create(model=MODEL, messages=messages, tools=tools if tools else None, temperature=1.0)
            message = response.choices[0].message
            if not message.tool_calls: return message.content
            messages.append({"role": "assistant", "content": message.content or "", "tool_calls": [tc.model_dump() for tc in message.tool_calls]})
            tool_tasks = [self._execute_tool_with_retry(tc.id, tc.function.name, json.loads(tc.function.arguments)) for tc in message.tool_calls]
            tool_results = await asyncio.gather(*tool_tasks)
            for result in tool_results: messages.append(result)
            iteration += 1
        return "Max iterations reached"

    async def _execute_tool_with_retry(self, tool_call_id: str, tool_name: str, tool_args: dict) -> dict:
        result = await self.registry.execute(tool_name, tool_args)
        return {"tool_call_id": tool_call_id, "role": "tool", "content": result}

    async def run(self, user_query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        agents = await self.decompose_task(user_query, context)
        shared_context = {"original_query": user_query, "agent_count": len(agents)}
        results = await asyncio.gather(*[self.execute_sub_agent(a, shared_context) for a in agents])
        successful = [r for r in results if r["status"] == "completed"]
        final_output = await self._synthesize_results(user_query, successful)
        return {"query": user_query, "final_output": final_output, "agent_results": results}

    async def _synthesize_results(self, user_query: str, agent_results: List[dict]) -> str:
        prompt = f"Synthesize these results for query: {user_query}\n\nResults: {json.dumps(agent_results, ensure_ascii=False)}"
        response = await client.chat.completions.create(model=MODEL, messages=[{"role": "system", "content": "Synthesis expert."}, {"role": "user", "content": prompt}])
        return response.choices[0].message.content
