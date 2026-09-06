from tavily import TavilyClient
import sys

def extract(urls):
    client = TavilyClient("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")
    response = client.extract(
        urls=urls
    )
    return response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
        print(extract(urls))
    else:
        print("Usage: python extract.py <url1> <url2> ...")
