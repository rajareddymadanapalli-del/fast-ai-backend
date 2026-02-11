import requests
import time
import sys

BASE_URL = "http://fast-ai-alb-527789680.us-east-1.elb.amazonaws.com"

def test_flow():
    print("1. Sending AI Prompt...")
    try:
        # Using json= instead of params= to ensure the body is sent correctly if the API expects it
        resp = requests.post(f"{BASE_URL}/ai/process", params={"prompt": "Quantum Physics for Goldens"})
        
        if resp.status_code != 200:
            print(f"   [FAIL] Server returned {resp.status_code}: {resp.text}")
            return

        data = resp.json()
        task_id = data.get('task_id')
        if not task_id:
            print(f"   [FAIL] No task_id in response: {data}")
            return
            
        print(f"   Task Created: {task_id}")

        print("2. Polling for results (60s timeout)...")
        for i in range(12):
            status_resp = requests.get(f"{BASE_URL}/ai/status/{task_id}")
            data = status_resp.json()
            print(f"   Attempt {i+1}: Status is '{data.get('status')}'")
            
            if data.get('status') == 'completed':
                print(f"\n[SUCCESS] AI processing complete!")
                print(f"Result Data: {data.get('result')}")
                return
            time.sleep(5)
            
        print("\n[TIMEOUT] Worker did not finish in time. Check AWS Logs.")

    except Exception as e:
        print(f"   [ERROR] Connection failed: {e}")

if __name__ == '__main__':
    test_flow()
