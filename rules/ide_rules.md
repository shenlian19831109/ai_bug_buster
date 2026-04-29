# ============================================
# BUG BUSTER V2 – ENFORCED EXECUTION PROTOCOL
# ============================================

## Trigger Condition
- Same error persists after 2 fix attempts.
- User mentions "still error", "3 rounds", or "debug-break".

## Mode: Execution Required
When triggered, you MUST switch to this protocol. DO NOT propose any code changes until evidence is gathered.

## Steps
1. **Baseline Check**: Run `python src/bug_cracker.py run_tests` to capture the current failure state.
2. **Classification**: Use `python src/bug_cracker.py classify --error "$STDERR"` to identify the dimension (A/B/C/D).
3. **Evidence Gathering**:
   - **Dimension A/B (Logic/State)**: Use `python src/bug_cracker.py inject_logs --file $FILE --line $LINE` to insert debug prints. Ask the user to run the code and share the output.
   - **Dimension C (External)**: Demand exact minimal input samples and mock external dependencies.
   - **Dimension D (AI Blind Spot)**: If complex concurrency/reflection is detected, state "UNSOLVABLE - manual review required" and provide detailed logs.
4. **Minimal Verifiable Fix (MVF)**: Propose exactly ONE change based on runtime evidence, accompanied by a verification command.
5. **Validation**: After the user applies the fix, ask them to run `run_tests` again.
6. **Hard Reset**: If the bug persists after 2 cycles (4 total attempts), run `python src/bug_cracker.py reset_prompt` and instruct the user to start a NEW session with the generated prompt.

## Response Template
---
### 🚨 BUG BUSTER V2 ACTIVATED
**Dimension**: [A/B/C/D]
**Evidence Gathering**: [e.g., Logs injected at line 42]
**Diagnosis**: [Based on runtime output...]
**MVF**: [Single change]
**Verify**: `pytest ...`
---
