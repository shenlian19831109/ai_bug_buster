#!/usr/bin/env python3
# src/runner.py
import subprocess
import sys
import os
import tempfile

def run_with_capture(code_snippet):
    """
    Runs a Python code snippet in an isolated environment and captures stdout/stderr.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code_snippet)
        f.flush()
        temp_name = f.name
        
    try:
        result = subprocess.run(
            [sys.executable, temp_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_name):
            os.remove(temp_name)

if __name__ == "__main__":
    # Example usage: read from stdin
    if not sys.stdin.isatty():
        code = sys.stdin.read()
        import json
        print(json.dumps(run_with_capture(code), indent=2))
