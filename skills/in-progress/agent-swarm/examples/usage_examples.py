import asyncio
from swarm_orchestrator import SwarmOrchestrator, ToolRegistry
from tools_examples import register_all

async def research_example():
    """Пример: Исследование технологий"""
    registry = ToolRegistry()
    register_all(registry)
    orchestrator = SwarmOrchestrator(registry=registry, max_agents=10)
    
    query = "Проведи анализ LLM фреймворков для продакшена (vLLM, llama.cpp)."
    result = await orchestrator.run(query)
    print(result["final_output"])

async def code_gen_example():
    """Пример: Генерация кода"""
    registry = ToolRegistry()
    register_all(registry)
    orchestrator = SwarmOrchestrator(registry=registry, max_agents=5)
    
    query = "Создай FastAPI сервис с тестами и JWT аутентификацией."
    result = await orchestrator.run(query)
    # Код будет в final_output или результатах агентов
    print(result["final_output"])

if __name__ == "__main__":
    # asyncio.run(research_example())
    pass
