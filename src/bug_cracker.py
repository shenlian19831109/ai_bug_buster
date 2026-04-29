#!/usr/bin/env python3
# src/bug_cracker.py - Enhanced Version with Execution & Feedback Loop
import subprocess
import sys
import json
import re
import os
import tempfile
from pathlib import Path

# ---------- Configuration ----------
TEST_CMD = os.getenv("BUG_BUSTER_TEST_CMD", "pytest -xvs")   # Customizable test command
TIMEOUT_SEC = 30

def run_test_suite():
    """Executes tests and returns (success_flag, stdout, stderr)"""
    try:
        # Use shell=True if TEST_CMD has multiple arguments or pipes
        proc = subprocess.run(
            TEST_CMD,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SEC,
            shell=True
        )
        return (proc.returncode == 0, proc.stdout, proc.stderr)
    except subprocess.TimeoutExpired:
        return (False, "", "Test execution timed out")
    except Exception as e:
        return (False, "", f"Error running tests: {str(e)}")

def classify_error(stderr_text, stdout_text=""):
    """Fine-grained error classification, returns dimensions and evidence"""
    combined = (stderr_text or "") + "\n" + (stdout_text or "")
    classifications = []
    # A. Local Logic
    if re.search(r"TypeError|ValueError|IndexError|AttributeError|KeyError|ZeroDivisionError", combined):
        classifications.append("A")
    # B. Context/State Pollution
    if re.search(r"AssertionError.*state|unexpected.*value|mutable|global|cache|stale", combined, re.I):
        classifications.append("B")
    # C. Upstream/External
    if re.search(r"ConnectionError|HTTPError|FileNotFoundError|PermissionError|JSONDecodeError|Timeout", combined, re.I):
        classifications.append("C")
    # D. AI Blind Spot
    if re.search(r"asyncio\.run|threading|concurrent|deadlock|race condition|multiprocessing", combined, re.I):
        classifications.append("D")
    
    # Default to A if no match
    if not classifications:
        classifications.append("A")
    return list(set(classifications))

def inject_debug_logs(file_path, line_number=None):
    """
    Inserts log statements near suspicious lines to print variable values.
    Returns the path to the modified temporary file and the variables found.
    """
    if not os.path.exists(file_path):
        return None, []
        
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    inserted_vars = []
    
    for i, line in enumerate(lines):
        current_line_idx = i + 1
        if line_number and current_line_idx == line_number:
            # Simple heuristic to find variables being assigned or used
            var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*='
            vars_found = re.findall(var_pattern, line)
            for var in vars_found:
                indent = " " * (len(line) - len(line.lstrip()))
                print_line = f'{indent}print(f"DEBUG [Line {current_line_idx}] {var} =", repr({var}))\n'
                new_lines.append(print_line)
                inserted_vars.append(var)
        new_lines.append(line)
        
    tmp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
    tmp_file.writelines(new_lines)
    tmp_file.close()
    return tmp_file.name, inserted_vars

def generate_reset_prompt(original_error, last_attempts_summary):
    """Generates a strong reset prompt for a new conversation session"""
    prompt = f"""
# New Session – Bug Reset

The following bug has not been fixed after multiple attempts. 
Please treat it as a **fresh problem** and re-analyze from scratch.

## Original Error
```text
{original_error}
```

## What was already tried (without success)
{last_attempts_summary}

## Analysis Constraints
1. Do not rely on previous fix attempts.
2. First classify the bug into (A/B/C/D) using the taxonomy.
3. Propose exactly ONE minimal change and a verification command.
4. If you cannot solve, state "UNSOLVABLE" and suggest manual steps.

Start your fresh analysis now.
"""
    return prompt

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI Bug Buster v2 CLI")
    parser.add_argument("action", choices=["run_tests", "classify", "inject_logs", "reset_prompt"])
    parser.add_argument("--error", help="Error text for classify")
    parser.add_argument("--file", help="File to inject logs")
    parser.add_argument("--line", type=int, help="Line number")
    parser.add_argument("--summary", help="Summary of failed attempts")
    args = parser.parse_args()

    if args.action == "run_tests":
        ok, out, err = run_test_suite()
        print(json.dumps({"success": ok, "stdout": out, "stderr": err}, indent=2))
    elif args.action == "classify":
        dims = classify_error(args.error or "")
        print(json.dumps({"dimensions": dims}, indent=2))
    elif args.action == "inject_logs":
        if not args.file:
            print(json.dumps({"error": "Missing --file argument"}))
        else:
            tmp_file, vars_found = inject_debug_logs(args.file, args.line)
            print(json.dumps({"temp_file": tmp_file, "injected_vars": vars_found}, indent=2))
    elif args.action == "reset_prompt":
        reset = generate_reset_prompt(args.error or "Unknown error", args.summary or "No summary provided")
        print(reset)
