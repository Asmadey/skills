import os
import aiohttp
from typing import List

# 1. Web Search Tool
async def web_search(query: str, max_results: int = 5) -> List[dict]:
    """Поиск в интернете"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": os.environ.get("SERPER_API_KEY")},
            json={"q": query, "num": max_results}
        ) as resp:
            data = await resp.json()
            return data.get("organic", [])

# 2. Code Execution Tool
async def execute_code(code: str, language: str = "python") -> dict:
    """Выполнение кода в песочнице (заглушка)"""
    return {
        "output": "Code execution result mock",
        "language": language,
        "execution_time": "0.5s"
    }

# 3. File Operations Tool
def read_file(file_path: str) -> str:
    """Чтение файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """Запись файла"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File written successfully: {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# Регистрация (пример использования в main)
def register_all(registry):
    registry.register("web_search", "Search the web", {"query": {"type": "string"}, "max_results": {"type": "integer"}}, web_search)
    registry.register("execute_code", "Execute code", {"code": {"type": "string"}, "language": {"type": "string"}}, execute_code)
    registry.register("read_file", "Read file", {"file_path": {"type": "string"}}, read_file)
    registry.register("write_file", "Write file", {"file_path": {"type": "string"}, "content": {"type": "string"}}, write_file)
