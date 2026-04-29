import subprocess
import json
import os
import sys

def test_classify():
    # Test A: Local Logic
    error = "TypeError: 'NoneType' object is not subscriptable"
    result = subprocess.run([sys.executable, "src/bug_cracker.py", "classify", "--error", error], capture_output=True, text=True)
    data = json.loads(result.stdout)
    assert "A" in data["dimensions"]

    # Test C: External
    error = "requests.exceptions.ConnectionError: Failed to establish a new connection"
    result = subprocess.run([sys.executable, "src/bug_cracker.py", "classify", "--error", error], capture_output=True, text=True)
    data = json.loads(result.stdout)
    assert "C" in data["dimensions"]

def test_reset_prompt():
    error = "Test failure"
    summary = "Tried fixing X and Y"
    result = subprocess.run([sys.executable, "src/bug_cracker.py", "reset_prompt", "--error", error, "--summary", summary], capture_output=True, text=True)
    assert "# New Session – Bug Reset" in result.stdout
    assert "Test failure" in result.stdout
