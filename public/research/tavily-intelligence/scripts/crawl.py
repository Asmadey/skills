from tavily import TavilyClient
import sys

def crawl(url):
    client = TavilyClient("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")
    response = client.crawl(
        url=url,
        extract_depth="advanced"
    )
    return response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(crawl(url))
    else:
        print("Usage: python crawl.py <url>")
