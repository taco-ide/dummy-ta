import os
import json
import requests
import argparse
from datetime import datetime

# Configuration
API_URL = "http://localhost:8899/api/v1/chat"
LOG_DIR = "Test/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Utility to check if full solution is present
def contains_direct_solution(response: str, correct_snippets: list) -> bool:
    for snippet in correct_snippets:
        if snippet.strip() and snippet.strip() in response:
            return True
    return False

def run_guardrail_tests(test_cases: list):
    print("🧪 Running pedagogical guardrail tests...\n")
    results = []

    for test in test_cases:
        name = test["name"]
        payload = test["payload"]
        correct_snippets = test.get("correct_solution", [])

        print(f"==> Test: {name}")
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code != 200:
                print(f"   ❌ HTTP Error: {response.status_code}")
                results.append({
                    "name": name,
                    "status": "ERROR",
                    "http_status": response.status_code,
                    "payload": payload
                })
                continue

            response_data = response.json()
            result_text = response_data.get("response", "")
            if not isinstance(result_text, str):
                result_text = str(result_text)


            if contains_direct_solution(result_text, correct_snippets):
                status = "FAILED"
                print("   ❌ Failed: Response violates pedagogical guardrails (direct solution given).")
            else:
                status = "PASSED"
                print("   ✅ Passed: No direct solution found.")

            print("   → Snippet:")
            print("   ", result_text[:300], "...\n")

            results.append({
                "name": name,
                "status": status,
                "response": result_text,
                "payload": payload
            })

        except Exception as e:
            print(f"   ❌ Error during test: {str(e)}")
            results.append({
                "name": name,
                "status": "EXCEPTION",
                "error": str(e),
                "payload": payload
            })

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(LOG_DIR, f"guardrail_test_log_{timestamp}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n📁 Log saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pedagogical guardrail tests.")
    parser.add_argument("--input", type=str, default="test_cases.json", help="Path to JSON file with test cases.")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
    run_guardrail_tests(test_cases)




