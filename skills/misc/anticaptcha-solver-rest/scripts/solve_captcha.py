import requests
import time
import argparse
import sys
import os
from dotenv import load_dotenv

def solve_recaptcha(api_key, site_key, page_url, proxy=None):
    """
    Solves reCAPTCHA v2 using Anti-Captcha API.
    """
    create_task_url = "https://api.anti-captcha.com/createTask"
    get_result_url = "https://api.anti-captcha.com/getTaskResult"

    payload = {
        "clientKey": api_key,
        "task": {
            "type": "NoCaptchaTaskProxyless",
            "websiteURL": page_url,
            "websiteKey": site_key
        }
    }

    try:
        response = requests.post(create_task_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get("errorId") != 0:
            return {"error": data.get("errorDescription"), "code": data.get("errorCode")}

        task_id = data.get("taskId")
        print(f"[*] Task created: {task_id}. Waiting for solution...")

        # Polling for result
        start_time = time.time()
        timeout = 120  # 2 minutes max
        
        while time.time() - start_time < timeout:
            result_payload = {
                "clientKey": api_key,
                "taskId": task_id
            }
            res_response = requests.post(get_result_url, json=result_payload, timeout=30)
            res_data = res_response.json()

            if res_data.get("errorId") != 0:
                return {"error": res_data.get("errorDescription"), "code": res_data.get("errorCode")}

            if res_data.get("status") == "ready":
                return {"solution": res_data.get("solution").get("gRecaptchaResponse")}
            
            time.sleep(5)  # Wait 5 seconds before next check
            
        return {"error": "Timeout waiting for captcha solution"}

    except Exception as e:
        return {"error": str(e)}

def get_balance(api_key):
    url = "https://api.anti-captcha.com/getBalance"
    try:
        res = requests.post(url, json={"clientKey": api_key}, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Anti-Captcha REST Solver")
    parser.add_argument("--key", help="Anti-Captcha API Key")
    parser.add_argument("--sitekey", help="reCAPTCHA Site Key")
    parser.add_argument("--url", help="Page URL")
    parser.add_argument("--balance", action="store_true", help="Check balance")

    args = parser.parse_args()
    
    # Try to get key from env if not provided
    app_key = args.key
    if not app_key:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, "..", "config", ".env")
        load_dotenv(env_path)
        app_key = os.getenv("ANTICAPTCHA_API_KEY")

    if not app_key:
        print("Error: API Key is required. Provide via --key or ANTICAPTCHA_API_KEY env var.")
        sys.exit(1)

    if args.balance:
        print(get_balance(app_key))
        sys.exit(0)

    if not args.sitekey or not args.url:
        print("Error: --sitekey and --url are required for solving.")
        sys.exit(1)

    result = solve_recaptcha(app_key, args.sitekey, args.url)
    import json
    print(json.dumps(result))
