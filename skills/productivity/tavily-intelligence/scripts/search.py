from tavily import TavilyClient
import sys

def search(query):
    client = TavilyClient("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")
    response = client.search(
        query=query,
        search_depth="advanced"
    )
    return response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(search(query))
    else:
        print("Usage: python search.py <query>")
