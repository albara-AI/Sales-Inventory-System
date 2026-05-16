import subprocess
import time
import requests
import sys

def verify():
    # Start Server
    print("Starting server...")
    proc = subprocess.Popen(
        ["uvicorn", "main:app", "--port", "8000"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    
    try:
        time.sleep(5) # Wait for startup
        
        base_url = "http://127.0.0.1:8000"
        
        # 1. Test Root
        resp = requests.get(f"{base_url}/")
        print(f"GET /: {resp.status_code}")
        assert resp.status_code == 200
        
        # 2. Test Products
        resp = requests.get(f"{base_url}/products")
        print(f"GET /products: {resp.status_code} - {len(resp.json())} items")
        assert resp.status_code == 200
        
        # 3. Test Dashboard
        resp = requests.get(f"{base_url}/reports/dashboard")
        print(f"GET /reports/dashboard: {resp.status_code}")
        assert resp.status_code == 200
        data = resp.json()
        assert "summary" in data
        
        print("Verification Successful!")
        
    except Exception as e:
        print(f"Verification Failed: {e}")
        # optional: print server log
        print(proc.stdout.read().decode())
        print(proc.stderr.read().decode())
        sys.exit(1)
        
    finally:
        print("Stopping server...")
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    verify()
