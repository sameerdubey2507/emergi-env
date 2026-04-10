import requests
import json
import sys
import os

SERVER_URL = "http://localhost:7860"

def log_pass(msg): print(f"[\033[92mPASS\033[0m] {msg}")
def log_fail(msg): print(f"[\033[91mFAIL\033[0m] {msg}")

tests_passed = 0
tests_failed = 0

print("Running Automated Checks...")

try:
    resp = requests.get(f"{SERVER_URL}/health", timeout=5)
    if resp.status_code == 200:
        log_pass(f"GET /health returned HTTP 200 (Version: {resp.json().get('version')})")
        tests_passed += 1
    else:
        log_fail(f"GET /health returned HTTP {resp.status_code}")
        tests_failed += 1
except Exception as e:
    log_fail(f"GET /health failed: {e}")
    tests_failed += 1

try:
    resp = requests.post(f"{SERVER_URL}/reset", json={"task_id": "task1_single_triage", "seed": 42}, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        if "observation" in data:
            log_pass("POST /reset returned HTTP 200 and schema is correct")
            tests_passed += 1
        else:
            log_fail("POST /reset returned HTTP 200 but missing observation")
            tests_failed += 1
    else:
        log_fail(f"POST /reset returned HTTP {resp.status_code}")
        tests_failed += 1
except Exception as e:
    log_fail(f"POST /reset failed: {e}")
    tests_failed += 1

import yaml
try:
    with open("openenv.yaml", "r") as f:
        config = yaml.safe_load(f)
        if all(k in config for k in ['name', 'version', 'tasks']):
            log_pass("openenv.yaml parsed and contains required fields")
            tests_passed += 1
        else:
            log_fail("openenv.yaml missing required fields")
            tests_failed += 1
except Exception as e:
    log_fail(f"openenv.yaml parsing failed: {e}")
    tests_failed += 1

print(f"\nResults: {tests_passed} Passed, {tests_failed} Failed")
if tests_failed > 0: sys.exit(1)
