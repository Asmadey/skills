import requests
from bs4 import BeautifulSoup
import json
import argparse
import sys
import re

def categorize_offer(text):
    text_lower = text.lower()
    
    # 1. Quantitative promises (numbers, %, $)
    if re.search(r'(\d+%|\$?\d[\d,\.]*k?|\d+\s*(часов|дней|минут|руб|usd))', text_lower):
        return "Quantitative Promise"
        
    # 2. Risk reducers (guarantee, refund, support)
    risk_keywords = ['гарантия', 'возврат', 'поддержка', 'безопасность', 'fsa', 'gdpr', 'guarantee', 'refund', 'money-back']
    if any(k in text_lower for k in risk_keywords):
        return "Risk Reducer"
        
    # 3. Social Proof (reviews, stars, trusted by)
    social_keywords = ['отзывы', 'клиенты', 'рейтинг', 'trusted by', 'review', 'case stud']
    if any(k in text_lower for k in social_keywords):
        return "Social Proof"
        
    # 4. Urgency
    if any(k in text_lower for k in ['успей', 'осталось', 'limited', 'only', 'expires']):
        return "Urgency/Scarcity"

    # 5. Process
    if any(k in text_lower for k in ['как это работает', 'этапы', 'how it works', 'steps']):
        return "Process"

    return "Qualitative Benefit/Claim"

def extract_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Fetching {url }...", file=sys.stderr)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cleanup
        for tag in soup(['script', 'style', 'noscript', 'iframe', 'svg']):
            tag.decompose()
            
        inventory = []
        
        # 1. Headers (High priority)
        for h_tag in ['h1', 'h2', 'h3']:
            for h in soup.find_all(h_tag):
                text = h.get_text(strip=True)
                if len(text) > 3:
                    inventory.append({
                        "text": text,
                        "type": "Headings",
                        "tag": h_tag,
                        "category": categorize_offer(text)
                    })

        # 2. CTAs (Buttons/Links)
        for button in soup.find_all(['a', 'button']):
            text = button.get_text(strip=True)
            if 2 < len(text) < 40:
                inventory.append({
                    "text": text,
                    "type": "CTA/Action",
                    "tag": button.name,
                    "category": "Call to Action"
                })

        # 3. Benefits (List items)
        for li in soup.find_all('li'):
            text = li.get_text(strip=True)
            if 10 < len(text) < 200:
                inventory.append({
                    "text": text,
                    "type": "Benefit List",
                    "category": categorize_offer(text)
                })

        # 4. Body Text (Context, but limit to reasonable length)
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if 20 < len(text):
                inventory.append({
                    "text": text[:200] + "..." if len(text) > 200 else text,
                    "type": "Running Text",
                    "category": categorize_offer(text)
                })
                
        return inventory

    except Exception as e:
        print(f"Error extracting content: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="Heroes Landing Analysis - Inventory Tool")
    parser.add_argument("url", help="URL of the landing page to analyze")
    parser.add_argument("--output", help="Output JSON file path", default=None)
    args = parser.parse_args()

    inventory = extract_content(args.url)
    
    result = {
        "standard": "Heroes Landing Analysis v1.5",
        "url": args.url,
        "items_count": len(inventory),
        "stage": "Preprocessing & Inventory",
        "items": inventory
    }
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Inventory saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
