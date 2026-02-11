import requests
import time

BASE_URL = "http://fast-ai-alb-527789680.us-east-1.elb.amazonaws.com"

def test_flow():
    print("1. Sending AI Prompt...")
    resp = requests.post(f"{BASE_URL}/ai/process", params={"prompt": "Explain Quantum Physics to a Golden Retriever"})
    task_id = resp.json()['task_id']
    print(f"   Task Created: {task_id}")

    print("2. Polling for results...")
    for _ in range(10):
        status_resp = requests.get(f"{BASE_URL}/ai/status/{task_id}")
        data = status_resp.json()
        print(f"   Current Status: {data['status']}")
        if data['status'] == 'completed':
            print(f"--- SUCCESS! Result: {data['result']} ---")
            return
        time.sleep(5)
    print("Task timed out (Worker might still be booting).")

if __name__ == '__main__':
    test_flow()
