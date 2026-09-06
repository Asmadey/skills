import sys
import os
import json
import argparse
import requests

# Попытка импорта firecrawl-mcp если он доступен в среде
# В данном контексте мы предполагаем, что агент может вызвать инструмент напрямую,
# но скрипт может быть полезен для внешних вызовов или логики.

def extract_with_firecrawl_api(url, api_key):
    """Извлечение контента через Firecrawl API"""
    if not api_key:
        return "Error: Firecrawl API Key is missing."
    
    endpoint = "https://api.firecrawl.dev/v0/scrape"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "url": url,
        "pageOptions": {"onlyMainContent": True}
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("data", {}).get("content", "No content found.")
    except Exception as e:
        return f"Error during Firecrawl API call: {str(e)}"

def extract_with_tavily(query, api_key):
    """Извлечение данных через Tavily (как альтернатива поиску)"""
    if not api_key:
        return "Error: Tavily API Key is missing."
    
    endpoint = "https://api.tavily.com/search"
    data = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "include_raw_content": True
    }
    
    try:
        response = requests.post(endpoint, json=data)
        response.raise_for_status()
        results = response.json().get("results", [])
        if results:
            return results[0].get("raw_content", results[0].get("content", ""))
        return "No results found via Tavily."
    except Exception as e:
        return f"Error during Tavily API call: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Extract content from URL for Growth Audit")
    parser.add_argument("url", help="Target URL to extract content from")
    parser.add_argument("--provider", choices=["firecrawl", "tavily"], default="firecrawl", help="API provider")
    
    args = parser.parse_args()
    
    # В реальном окружении PersonalOS ключи могут быть в ENV
    firecrawl_key = os.environ.get("FIRECRAWL_API_KEY")
    tavily_key = os.environ.get("TAVILY_API_KEY")
    
    print(f"--- Extracting content from: {args.url} using {args.provider} ---")
    
    if args.provider == "firecrawl":
        content = extract_with_firecrawl_api(args.url, firecrawl_key)
    else:
        content = extract_with_tavily(args.url, tavily_key)
    
    print("\nCONTENT EXTRACTED:\n")
    print(content[:2000] + "..." if len(content) > 2000 else content)

if __name__ == "__main__":
    main()
